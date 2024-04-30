DOSTEPNE_KOMENDY = ['saldo', 'sprzedaz', 'zakup', 'konto', 'lista',
                    'magazyn', 'przeglad', 'koniec']


class Magazyn:
    def __init__(self, konto, magazyn, lista_operacji, nazwa_pliku):
        self.konto = konto
        self.magazyn = magazyn
        self.lista_operacji = lista_operacji
        self.nazwa_pliku = nazwa_pliku

    def zapisz_do_pliku(self, nazwa_pliku):
        self.nazwa_pliku = nazwa_pliku
        with open(self.nazwa_pliku, 'w') as plik:
            plik.write(f'Stan konta: {self.konto}\n')
            plik.write('Stan magazynu wynosi:\n')
            pusty_magazyn = True
            for nazwa_produktu, ilosc in self.magazyn.items():
                if self.magazyn[nazwa_produktu]['sztuk'] > 0:
                    pusty_magazyn = False
                    plik.write(f'Produkt: {nazwa_produktu}, sztuk: {ilosc["sztuk"]}\n')
            if pusty_magazyn:
                plik.write('Magazyn jest pusty.\n')
            plik.write('Historia operacji:\n')
            for operacja in self.lista_operacji:
                plik.write(f'{operacja}\n')

    def odczytaj_z_pliku(self, nazwa_pliku):
        self.nazwa_pliku = nazwa_pliku

        try:
            with open(self.nazwa_pliku, 'r') as plik:
                linie = plik.readlines()
                self.konto = float(linie[0].split(': ')[1].strip())
                print(f'Stan konta wynosi: {self.konto}')
                if len(linie) > 1:
                    print('Stan magazynu wynosi:')
                    pusty_magazyn = True
                    for linia in linie[2:]:
                        if linia.startswith('Produkt'):
                            czesci = linia.split(',')
                            nazwa_produktu = czesci[0].split(': ')[1].strip()
                            ilosc_sztuk = int(czesci[1].split(': ')[1].strip())
                            self.magazyn[nazwa_produktu] = {'sztuk': ilosc_sztuk, 'cena': 0}
                            if ilosc_sztuk > 0:
                                pusty_magazyn = False
                                print(f'Produkt: {nazwa_produktu}, sztuk: {ilosc_sztuk}')
                    if pusty_magazyn:
                        print('Magazyn jest pusty.')
                else:
                    print('Magazyn jest pusty.')
                for linia in linie:
                    linia = linia.strip()
                    if (linia.startswith('Sprzedano') or
                            linia.startswith('Kupiono') or
                            linia.startswith('Zaktualizowano')):
                        self.lista_operacji.append(linia)
        except FileNotFoundError:
            print("Plik nie istnieje. Nie wczytano stanu.")


def wykonaj_saldo(magazyn):
    kwota = float(input('Podaj kwote do dodania [+] lub odjecia [-] z konta: '))
    if kwota > 0:
        magazyn.konto += kwota
        magazyn.lista_operacji.append(f'Zaktualizowano saldo. Do konta dodano {kwota}.')
    elif kwota < 0:
        magazyn.konto += kwota
        magazyn.lista_operacji.append(f'Zaktualizowano saldo. Od konta odjeto {-kwota}.')
    else:
        print('Kwota nie moze byc zerowa.')


def sprzedaj(magazyn):
    nazwa_produktu = input('Podaj nazwe produktu: ')
    if nazwa_produktu not in magazyn.magazyn:
        print('Produktu nie ma w magazynie.')
    else:
        liczba_sztuk = int(input('Podaj liczbe sztuk: '))
        if liczba_sztuk <= 0:
            print('Nieprawidlowa ilosc.')
        elif liczba_sztuk > magazyn.magazyn[nazwa_produktu]['sztuk']:
            print('Nie ma tylu sztuk w magazynie.')
        else:
            cena_produktu = float(input('Podaj cene produktu: '))
            if cena_produktu <= 0:
                print('Cena nie mozna byc ujemna ani zerowa.')
            else:
                magazyn.magazyn[nazwa_produktu]['sztuk'] -= liczba_sztuk
                magazyn.konto += cena_produktu * liczba_sztuk
                magazyn.lista_operacji.append(
                    f'Sprzedano produkt {nazwa_produktu}, '
                    f'sztuk {liczba_sztuk} po {cena_produktu}'
                )


def kup(magazyn):
    nazwa_produktu = input('Podaj nazwe produktu: ')
    liczba_sztuk = int(input('Podaj liczbe sztuk: '))
    if liczba_sztuk <= 0:
        print('Nieprawidlowa ilosc.')
    else:
        cena_produktu = float(input('Podaj cenę produktu: '))
        if cena_produktu > magazyn.konto or cena_produktu * liczba_sztuk > magazyn.konto:
            print('Nie masz wystarczajacych srodkow na koncie.')
        elif cena_produktu <= 0:
            print('Cena nie mozna byc ujemna ani zerowa.')
        else:
            kwota_zakupu = cena_produktu * liczba_sztuk
            if nazwa_produktu not in magazyn.magazyn:
                magazyn.magazyn[nazwa_produktu] = {'sztuk': 0, 'cena': cena_produktu}
            else:
                magazyn.magazyn[nazwa_produktu]['cena'] = cena_produktu
            magazyn.magazyn[nazwa_produktu]['sztuk'] += liczba_sztuk
            magazyn.konto -= kwota_zakupu
            cena_magazynowa = cena_produktu
            magazyn.lista_operacji.append(
                f'Kupiono produkt {nazwa_produktu}, '
                f'sztuk {liczba_sztuk} '
                f'po {cena_magazynowa}'
            )


def sprawdz_konto(magazyn):
    print(f'Stan konta wynosi: {magazyn.konto}')


def wylistuj_magazyn(magazyn):
    pusty_magazyn = True
    print('Stan magazynu wynosi:')
    for nazwa_produktu, ilosc in magazyn.magazyn.items():
        liczba_sztuk_w_magazynie = ilosc['sztuk']
        if magazyn.magazyn[nazwa_produktu]['sztuk'] > 0:
            pusty_magazyn = False
            print(f'Produkt {nazwa_produktu}, sztuk {liczba_sztuk_w_magazynie}')
    if pusty_magazyn:
        print('Magazyn jest pusty.')


def sprawdz_magazyn(magazyn):
    towar = input('Podaj nazwe towaru: ')
    for nazwa_produktu, ilosc in magazyn.magazyn.items():
        liczba_sztuk_w_magazynie = ilosc['sztuk']
        if towar == nazwa_produktu:
            if magazyn.magazyn[nazwa_produktu]['sztuk'] > 0:
                print(f'Stan magazynu dla produktu {nazwa_produktu}: '
                      f'sztuk {liczba_sztuk_w_magazynie}')
            elif magazyn.magazyn[nazwa_produktu]['sztuk'] == 0:
                print('Produktu nie ma w magazynie.')
    if towar not in magazyn.magazyn:
        print('Produktu nie ma w magazynie.')


def pokaz_przeglad(magazyn):
    podaj_poczatek = input('Podaj zakres opeacji od: ')
    if podaj_poczatek == '' or podaj_poczatek == '0':
        poczatek = -1
    else:
        poczatek = int(podaj_poczatek) - 1
    podaj_koniec = input('Podaj zakres operacji do: ')
    if podaj_koniec == '' or podaj_koniec == '0':
        koniec = -1
    else:
        koniec = int(podaj_koniec) - 1
    dlugosc_listy = len(magazyn.lista_operacji)
    if koniec != -1 and poczatek > koniec:
        print('Bledny zakres.')
    elif poczatek in range(dlugosc_listy) and koniec in range(dlugosc_listy):
        print(f'Lista operacji: {magazyn.lista_operacji[poczatek:koniec + 1]}')
    elif poczatek >= dlugosc_listy or koniec >= dlugosc_listy:
        print(f'Wartosc poza zakresem. Zakres wynosi 1 - {dlugosc_listy}')
        podaj_poczatek = input('Podaj zakres od: ')
        if podaj_poczatek == '' or podaj_poczatek == '0':
            poczatek = -1
        else:
            poczatek = int(podaj_poczatek) - 1
        podaj_koniec = input('Podaj zakres do: ')
        if podaj_koniec == '' or podaj_koniec == '0':
            koniec = -1
        else:
            koniec = int(podaj_koniec) - 1
        if poczatek > koniec:
            print('Bledny zakres.')
        elif poczatek in range(dlugosc_listy) and koniec in range(dlugosc_listy):
            print(f'Lista operacji: {magazyn.lista_operacji[poczatek:koniec + 1]}')
        else:
            print('Bledny zakres.')
    elif poczatek == -1 and koniec != -1:
        print(f'Lista operacji: {magazyn.lista_operacji[0:koniec + 1]}')
    elif koniec == -1 and poczatek != -1:
        print(f'Lista operacji: {magazyn.lista_operacji[poczatek:dlugosc_listy]}')
    elif poczatek == -1 and koniec == -1:
        print(f'Lista operacji: {magazyn.lista_operacji[0:dlugosc_listy]}')


def main():
    magazyn = Magazyn(konto=0, magazyn={}, lista_operacji=[], nazwa_pliku='stan_magazynu.txt')
    magazyn.nazwa_pliku = 'stan_magazynu.txt'
    magazyn.odczytaj_z_pliku(magazyn.nazwa_pliku)

    while True:
        print(f'Dostepne komendy: {DOSTEPNE_KOMENDY}')
        wybor_uzytkownika = input('Podaj komende: ')
        if wybor_uzytkownika == 'saldo':
            wykonaj_saldo(magazyn)
        elif wybor_uzytkownika == 'sprzedaz':
            sprzedaj(magazyn)
        elif wybor_uzytkownika == 'zakup':
            kup(magazyn)
        elif wybor_uzytkownika == 'konto':
            sprawdz_konto(magazyn)
        elif wybor_uzytkownika == 'lista':
            wylistuj_magazyn(magazyn)
        elif wybor_uzytkownika == 'magazyn':
            sprawdz_magazyn(magazyn)
        elif wybor_uzytkownika == 'przeglad':
            pokaz_przeglad(magazyn)
        elif wybor_uzytkownika == 'koniec':
            magazyn.zapisz_do_pliku(magazyn.nazwa_pliku)
            break
        else:
            print('Nie ma takiej komendy.')


if __name__ == '__main__':
    main()
