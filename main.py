from asyncio.windows_events import NULL
import pandas
import math

# Wczytanie danych
data = pandas.read_csv("data.csv", header=0)
# p(x) * log2(p(x))
def entropy(n, N):
    p = n / N
    if(p != 0):
        return -p * math.log(p, 2)
    else:
        return 0

# Zmienna liczy warianty odpowiedzi dla danej kolumny
def getTypes(name):
    column = data[name]
    variants = []
    types = 1
    variants.append(column[0])
    for i in range(1, len(column)):
        check = 0
        for j in range(0, len(variants)):
            if(column[i] == variants[j]):
                check = 1
                break
        if(check == 0):
            variants.append(column[i])
            types += 1
    return int(types)

# Zamienia wartości tekstowe na liczbowe
def transform(name):
    column = data[name]
    variants = []
    types = 1
    variants.append(column[0])
    for i in range(1, len(column)):
        check = 0
        for j in range(0, len(variants)):
            if (column[i] == variants[j]):
                check = 1
                break
        if (check == 0):
            types += 1
            variants.append(column[i])

    tColumn = []
    for i in range(0, len(column)):
        for j in range(0, len(variants)):
            if(column[i] == variants[j]):
                tColumn.append(j)

    return tColumn




def partEntropy(table):
    N1 = 0  # nigdzie
    N3 = 0  # w kraju
    N2 = 0  # za granicą

    # Entropia dla całego układu: I = 1.43253376700698
    destinity = data['destinity']
    for i in range (0, len (destinity)):
        if (destinity[i] == "nowhere"):
            N1 += 1
        if (destinity[i] == "country"):
            N2 += 1
        if (destinity[i] == "aboard"):
            N3 += 1
    ent = entropy (N1, 100) + entropy (N2, 100) + entropy (N3, 100)

    informationProfit = []
    for i in range(0, len(table) - 1):
        n = []
        nPart = []
        for j in range(0, types[i]):
            sum = 0
            nX = []
            nX.append(0)
            nX.append(0)
            nX.append(0)
            for k in range(0, len(table[0])):#liczę ilość wierszy
                if(table[i][k] == j):
                    sum += 1
                    for l in range(0, 3):
                        if(table[5][k] == l):
                            nX[l] += 1

            nPart.append(nX)
            n.append(sum)

        for j in range(0, len(n)):
            Ip = entropy(nPart[j][0], N1) + entropy(nPart[j][1], N2) + entropy(nPart[j][2], N3)
            Im = entropy(n[j] - nPart[j][1] - nPart[j][2], 100 - N1) + \
                 entropy(n[j] - nPart[j][0] - nPart[j][2], 100 - N2) + \
                 entropy(n[j] - nPart[j][0] - nPart[j][1], 100 - N3)

            E = (n[j]/100) * Ip + ((100 - n[j])/100) * Im
            infProfit = ent - E
            informationProfit.append(infProfit)
    return informationProfit


table = []
table.append(transform('budget'))
table.append(transform('transport'))
table.append(transform('period'))
table.append(transform('type'))
table.append(transform('abundance'))
table.append(transform('destinity'))

types = []
types.append(getTypes('budget'))
types.append(getTypes('transport'))
types.append(getTypes('period'))
types.append(getTypes('type'))
types.append(getTypes('abundance'))
types.append(getTypes('destinity'))

typesList =[]
for  i in types:
    t =[]
    for j in range(0,i):
        t.append(j)
    typesList.append(t)
    
print(typesList)


def getColumnAndTypeValue (index):
    counter =0
    for colId, i in enumerate(typesList):
        for j in i:
            if(counter == index):
                return [colId, j]
            counter+=1
    return NULL


def all_equal(iterator):
    return len(set(iterator)) <= 1

# partialEntropy = partEntropy(table)
# colNValue = getColumnAndTypeValue(partialEntropy.index(max(partialEntropy)))
# tableDF = pandas.DataFrame(table).transpose()
# m=tableDF[colNValue[0]]==colNValue[1]
# table1=tableDF[~m].to_numpy()
# table2=tableDF[m].to_numpy()
# print(table)
# print(" ")
# print(table1)
# print(" ")
# print(table2)

print(all_equal([1,1,1,1,1,1]))
print(all_equal([1,1,1,1,1,2]))
#ze względu na to że tworzymy drzewo binarne nie możey uzyc pętli bo w każdej kolejnej iteracji musimy zrobić podział dla 2 table . Z tego względu wchodzi w grę jedynie rekurencja
def countEntireEntropy (table):
    partialEntropy = partEntropy(table)
    if(all_equal(partialEntropy)):
        return table #jeśli wszystkie entropie sa równe zraca podzialona tabele => z warunkiem jest problem,zdaje sie że źle rozumiem finalny wynik (funkcja wywala ze względu na za dużą ilośc iteracji)
    colNValue = getColumnAndTypeValue(partialEntropy.index(max(partialEntropy)))
    tableDF = pandas.DataFrame(table).transpose()
    m=tableDF[colNValue[0]]==colNValue[1]
    table1 = countEntireEntropy(tableDF[~m].transpose().to_numpy())
    table2 = countEntireEntropy(tableDF[m].transpose().to_numpy())
    table = []
    table.append(table1)
    table.append(table2)
    return table # nie byłem w stanie sprawdzic czy funkcja podaje poprawny wynik

print(countEntireEntropy(table))
