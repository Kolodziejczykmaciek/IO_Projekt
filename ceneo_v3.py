import urllib.request
import time
import requests
import re

from bs4 import BeautifulSoup
import csv


plik = [[], [], []] # lista na wczystanie produktów z pliku csv [0] - produkt 1 [1] -produkt 2 itd.
prod1 = [[], [], [], [], [], [], []]  # lista na dane dla algorytmu [0] - id sprzedawcy, [1] - cena, [2] - koszt dostawy, [3] - reputacja (gwiazdki),[4] - ilosc opini, [5] - linki
prod2 = [[], [], [], [], [], [], []]
prod3 = [[], [], [], [], [], [], []]
prod = [[], [], [], [], [], []] # tymczasowa lista

log_Time = []
log_Time_of_getInfoFunc = []


def wczytaj():
    f = open('Book1.csv', 'r')
    reader = csv.reader(f)

    for line in reader:                         # odczyt linia po lini i wpisanie do listy plik[]
        phrase = line[1].split()
        for p in phrase:
            plik[int(line[0])].append(p)
        plik[int(line[0])].append(line[2])
        plik[int(line[0])].append(line[3])
        if int(line[0]) == 0:
            prod1[6].append(line[4])
        if int(line[0]) == 1:
            prod2[6].append(line[4])
        if int(line[0]) == 2:
            prod3[6].append(line[4])

def search(product):
    def first_search(*args):
        ###     PREAERING A SEARCHED URL
        dane = []  # przechwyt argumentow
        for element in args:
            dane.append(element)

        url = "https://www.ceneo.pl/;szukaj-"
        daneSize = len(dane)
        for val in range(daneSize - 2):  # budowa linku
            if val == 0:
                url += dane[val]
            else:
                url += "+" + dane[val]
        url += ";0191;m" + str(dane[-2]) + ";n" + str(dane[-1]) + ";0115-0.htm"  # gotowy reguest url
        print(url)  # do testu

        ###     CREATING A REQUEST WITH URL AND PARSING THE RESPONSE
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        shop_numb = []
        i = 0
        for el in soup.find_all('span', class_='shop-numb'):    # pętla zapisująca ilość ofert
            temp = el.get_text()
            if not temp:
                shop_numb.append('1')
            else:
                temp = temp.split()
                shop_numb.append(temp[1])
            i = i + 1

        match = soup.find_all('div',
                              class_='cat-prod-row js_category-list-item js_clickHashData js_man-track-event')  # tylko div z podaną klasą
        ID_numbers = re.findall('(?:data-pid=")(.*)(?:"\sid)', str(match))
        # ID_numbers containg searched numbers but they are replacing

        new_ID_numbers = []  # new list for not replacing products ID
        try:
            new_ID_numbers.append(ID_numbers[0])
        except IndexError:
            print("Cound not find anything!")  # in case no products were found
            return False

        for i in range(len(ID_numbers)):  # it fills the new_ID_numbers list with individual id products
            if i == len(ID_numbers) - 1:
                break
            if (ID_numbers[i] != ID_numbers[i + 1]):
                new_ID_numbers.append(ID_numbers[i + 1])

        return new_ID_numbers, shop_numb  # fuction returns a ID products list
    log_Time.append(time.perf_counter())
    PID, shop_numb = first_search(*product)
    log_Time.append(time.perf_counter())
    # print(PID)
    # print(shop_numb)
    selected_pid = 0
    temp = 0

    for x in range(0, len(PID)):            # szukamy pozycji z największa liczba ofert
        i = int(shop_numb[x])
        if i > temp:
            temp = i
            selected_pid = PID[x]

    print(selected_pid)

    def get_info(product_ID):

        url = "https://www.ceneo.pl/" + str(
            product_ID) + ";0284-0;02511.htm"  # only status 'dostępny' and sorded from the lowes price
        print(url)  # do testu
        log_Time_of_getInfoFunc.append(time.perf_counter())
        response = requests.get(url)
        log_Time_of_getInfoFunc.append(time.perf_counter()
                                       )
        soup = BeautifulSoup(response.text, 'html.parser')

        match = soup.find_all('tr', {'class': 'clickable-offer'})
        # print(match)
        pattern_shopid = r'(?:data-shop=")(.*)(?:"\sdata-shopurl=")'
        pattern_links = r'(?:data-click-url=")(.*)(?:"\sdata-gacategoryname=")'
        pattern_opinion = r'(?:">)(.*)(?:\sopini[iea]</span>)'
        pattern_mark = r'(?:class="screen-reader-text">Ocena\s)(.*)(?:\s/\s5</span>)'
        pattern_price = r'(?:data-price=")(.*)(?:"\sdata-productid=")'

        log_Time_of_getInfoFunc.append(time.perf_counter())
        price = re.findall(pattern_price, str(match))
        log_Time_of_getInfoFunc.append(time.perf_counter())

        log_Time_of_getInfoFunc.append(time.perf_counter())
        shop_id = re.findall(pattern_shopid, str(match))
        log_Time_of_getInfoFunc.append(time.perf_counter())

        log_Time_of_getInfoFunc.append(time.perf_counter())
        links = re.findall(pattern_links, str(match))
        log_Time_of_getInfoFunc.append(time.perf_counter())

        log_Time_of_getInfoFunc.append(time.perf_counter())
        mark = re.findall(pattern_mark, str(soup))
        log_Time_of_getInfoFunc.append(time.perf_counter())

        log_Time_of_getInfoFunc.append(time.perf_counter())
        opinion = re.findall(pattern_opinion, str(soup))
        log_Time_of_getInfoFunc.append(time.perf_counter())

        log_Time_of_getInfoFunc.append(time.perf_counter())
        ma = soup.find_all('div', {'class': 'js_deliveryInfo'})
        log_Time_of_getInfoFunc.append(time.perf_counter())

        price_d = []
        i = 0
        for element in ma:
            element = element.get_text()
            element = element.split()
            #print(element)
            if len(element) == 2:
                price_d.append(0)
            else:
                temp = element[3]
                temp = temp.split(',')
                p = int(temp[0]) - int(price[i])
                price_d.append(p)
            i = i + 1

        prod[0] = shop_id
        prod[1] = price
        prod[2] = price_d
        prod[3] = mark
        prod[4] = opinion
        prod[5] = links

    log_Time.append(time.perf_counter())
    get_info(selected_pid)      # wywolanie funkcji dla id z najwieksza liczba ofert
    log_Time.append(time.perf_counter())
    return prod[0], prod[1], prod[2], prod[3], prod[4], prod[5]


########################################################################################################
log_Time.append(time.perf_counter())
wczytaj()
log_Time.append(time.perf_counter())
for x in range(0, len(plik)):
    if plik[x]:
        if x == 0:
            prod1[0], prod1[1], prod1[2], prod1[3], prod1[4], prod1[5] = search(plik[x])

        if x == 1:
            prod2[0], prod2[1], prod2[2], prod2[3], prod2[4], prod2[5] = search(plik[x])
        if x == 2:
            prod3[0], prod3[1], prod3[2], prod3[3], prod3[4], prod3[5] = search(plik[x])

#Tworzenie trójwymiarowej listy zestaw[a][b][c], gdzie a to numer zestawu, b to id przedmiotu a c to oferta sklepu
d = 0
a = len(prod1[0])
b = len(prod2[0])
c = len(prod3[0])

if int(a) == 0:
    prod1 = [[0], [0], [0], [0], [0], [0], [0]]
    a = 1
if int(b) == 0:
    prod2 = [[0], [0], [0], [0], [0], [0], [0]]
    b = 1
if int(c) == 0:
    prod3 = [[0], [0], [0], [0], [0], [0], [0]]
    c = 1

zestaw = [[[0 for r in range(7)] for r in range(4)] for r in range(a*b*c)]
zestawkw = [[[0 for r in range(6)] for r in range(3)] for r in range(a*b*c)]
for i in range(a):
    for j in range(b):
        for k in range(c):

            zestaw[d][0] = [prod1[0][i], prod1[1][i], prod1[2][i], prod1[3][i], prod1[4][i], prod1[5][i], prod1[6][0]]
            zestaw[d][1] = [prod2[0][j], prod2[1][j], prod2[2][j], prod2[3][j], prod2[4][j], prod2[5][j], prod2[6][0]]
            zestaw[d][2] = [prod3[0][k], prod3[1][k], prod3[2][k], prod3[3][k], prod3[4][k], prod3[5][k], prod3[6][0]]

#pomocnicza lista trójwymiarowa na potrzeby wyliczenia kosztów wysyłki
            zestawkw[d][0] = [prod1[0][i], prod1[1][i],  prod1[2][i], prod1[6][0]]
            zestawkw[d][1] = [prod2[0][j], prod2[1][j], prod2[2][j], prod2[6][0]]
            zestawkw[d][2] = [prod3[0][k], prod3[1][k], prod3[2][k], prod3[6][0]]

            for z in range(3):
                # pomnożenie ceny razy ilosć sztuk
                zestawkw[d][z][1] = int(zestawkw[d][z][1]) * int(zestawkw[d][z][3])
                # sprawdzenie, czy id sklepu się powtarza. jeżeli tak, wyzeruj niższy koszt przesyłki dla przedmiotu
                for y in range(z+1, 3):
                    if zestawkw[d][z][0] == zestawkw[d][y][0]:
                        if zestawkw[d][z][2] >= zestawkw[d][y][2]:
                            zestawkw[d][y][2] = 0
                        else:
                            zestawkw[d][z][2] = 0
            zestaw[d][3] = [int(zestawkw[d][0][1]) + int(zestawkw[d][1][1]) + int(zestawkw[d][2][1])
                            + int(zestawkw[d][0][2]) + int(zestawkw[d][1][2]) + int(zestawkw[d][2][2])
                            ]
            d=d+1


poz = 0
min = zestaw[0][3]
for x in range(1, a*b*c):
    if zestaw[x][3] < min:
        poz = x
        min = zestaw[x][3]

log_Time.append(time.perf_counter())

print(zestaw[poz])



def log():
    File_object = open(r"log.txt", "w")
    cheapest_product_list = zestaw[poz]

    data_to_write_to_file = []
    data_to_write_to_file.append('Wyszukanie ceny ze sparsowanego dokumentu: ' + str((log_Time_of_getInfoFunc[1] - log_Time_of_getInfoFunc[0])) + "\n")
    data_to_write_to_file.append("Wyszukane ID sklepu ze sparsowanego dokumentu: " + str((log_Time_of_getInfoFunc[3] - log_Time_of_getInfoFunc[2])) + "\n")
    data_to_write_to_file.append("Wyszukane linków ze sparsowanego dokumentu: " + str((log_Time_of_getInfoFunc[5] - log_Time_of_getInfoFunc[4])) + "\n")
    data_to_write_to_file.append("Wyszukane ocen ze sparsowanego dokumentu: " + str((log_Time_of_getInfoFunc[7] - log_Time_of_getInfoFunc[6])) + "\n")
    data_to_write_to_file.append("Wyszukane opinii ze sparsowanego dokumentu: " + str((log_Time_of_getInfoFunc[9] - log_Time_of_getInfoFunc[8])) + "\n")
    data_to_write_to_file.append("Wyszukanie ms ze sparsowanego dokumentu: " + str((log_Time_of_getInfoFunc[11] - log_Time_of_getInfoFunc[10])) + "\n")
    data_to_write_to_file.append("Czas zapytanie ceneo o szczegóły strone produktu i otrzymanie odp: " + str((log_Time_of_getInfoFunc[13] - log_Time_of_getInfoFunc[12])) + "\n")

    data_to_write_to_file.append("\n" + "Czas wykonanie funkcji first_search(): " + str(log_Time[1] - log_Time[0]) + "\n")
    data_to_write_to_file.append("Czas wykonanie funkcji getInfo(): " + str(log_Time[3] - log_Time[2]) + "\n")
    data_to_write_to_file.append("Czas wykonanie funkcji wczytaj(), która wczytuje dane wejsciowe z pliku csv: " + str(log_Time[5] - log_Time[4]) + "\n")
    data_to_write_to_file.append("\n" + "Czas wykonywania algorytmu znajdującego najlepszy zestaw: " + str(log_Time[6] - log_Time[5]) + "\n")

    for line in data_to_write_to_file:
        File_object.write(line)

    File_object.write("\n" + "Słowa użyte do wyszukania (dwie ostatnie liczby to cena min i max): " + str(plik[0]))
    File_object.write("\n" + "Słowa użyte do wyszukania (dwie ostatnie liczby to cena min i max): " + str(plik[1]))
    File_object.write("\n" + "Słowa użyte do wyszukania (dwie ostatnie liczby to cena min i max): " + str(plik[2]))

    File_object.write("\n" + "Linki do konkretnych znalezionych produktów w konkretnych sklepach:" + "\n")
    File_object.write("\n" + "https://www.ceneo.pl" + str(zestaw[poz][0][5]) + "\n")
    File_object.write("\n" + "https://www.ceneo.pl" + str(zestaw[poz][1][5]) + "\n")
    File_object.write("\n" + "https://www.ceneo.pl" + str(zestaw[poz][2][5]) + "\n")

    File_object.close()

log()