class Magazyn:
    def __init__(self, konto, magazyn, lista_operacji, nazwa_pliku):
        self.konto = konto
        self.magazyn = magazyn
        self.lista_operacji = lista_operacji
        self.nazwa_pliku = nazwa_pliku

    def wykonaj_saldo(self):
        kwota = float(input('Podaj kwote do dodania [+] lub odjecia [-] z konta: '))
        if kwota > 0:
            self.konto += kwota
            self.lista_operacji.append(f'Zaktualizowano saldo. Do konta dodano {kwota}.')
        elif kwota < 0:
            self.konto += kwota
            self.lista_operacji.append(f'Zaktualizowano saldo. Od konta odjeto {-kwota}.')
        else:
            print('Kwota nie moze byc zerowa.')

    def sprzedaj(self):
        nazwa_produktu = input('Podaj nazwe produktu: ')
        if nazwa_produktu not in self.magazyn:
            print('Produktu nie ma w magazynie.')
        else:
            liczba_sztuk = int(input('Podaj liczbe sztuk: '))
            if liczba_sztuk <= 0:
                print('Nieprawidlowa ilosc.')
            elif liczba_sztuk > self.magazyn[nazwa_produktu]['sztuk']:
                print('Nie ma tylu sztuk w magazynie.')
            else:
                cena_produktu = float(input('Podaj cene produktu: '))
                if cena_produktu <= 0:
                    print('Cena nie mozna byc ujemna ani zerowa.')
                else:
                    self.magazyn[nazwa_produktu]['sztuk'] -= liczba_sztuk
                    self.konto += cena_produktu * liczba_sztuk
                    self.lista_operacji.append(
                        f'Sprzedano produkt {nazwa_produktu}, '
                        f'sztuk {liczba_sztuk} po {cena_produktu}'
                    )

    def kup(self):
        nazwa_produktu = input('Podaj nazwe produktu: ')
        liczba_sztuk = int(input('Podaj liczbe sztuk: '))
        if liczba_sztuk <= 0:
            print('Nieprawidlowa ilosc.')
        else:
            cena_produktu = float(input('Podaj cenę produktu: '))
            if cena_produktu > self.konto or cena_produktu * liczba_sztuk > self.konto:
                print('Nie masz wystarczajacych srodkow na koncie.')
            elif cena_produktu <= 0:
                print('Cena nie mozna byc ujemna ani zerowa.')
            else:
                if nazwa_produktu not in self.magazyn:
                    self.magazyn[nazwa_produktu] = {'sztuk': 0, 'cena': 0}
                self.magazyn[nazwa_produktu]['sztuk'] += liczba_sztuk
                liczba_sztuk_w_magazynie = self.magazyn[nazwa_produktu]['sztuk']
                self.magazyn[nazwa_produktu]['cena'] += cena_produktu
                self.konto -= cena_produktu * liczba_sztuk_w_magazynie
                cena_magazynowa = cena_produktu
                self.lista_operacji.append(
                    f'Kupiono produkt {nazwa_produktu}, '
                    f'sztuk {liczba_sztuk} '
                    f'po {cena_magazynowa}'
                )

    def sprawdz_konto(self):
        print(f'Stan konta wynosi: {self.konto}')

    def wylistuj_magazyn(self):
        pusty_magazyn = True
        print('Stan magazynu wynosi:')
        for nazwa_produktu, ilosc in self.magazyn.items():
            liczba_sztuk_w_magazynie = ilosc['sztuk']
            if self.magazyn[nazwa_produktu]['sztuk'] > 0:
                pusty_magazyn = False
                print(f'Produkt {nazwa_produktu}, sztuk {liczba_sztuk_w_magazynie}')
        if pusty_magazyn:
            print('Magazyn jest pusty.')

    def sprawdz_magazyn(self):
        towar = input('Podaj nazwe towaru: ')
        for nazwa_produktu, ilosc in self.magazyn.items():
            liczba_sztuk_w_magazynie = ilosc['sztuk']
            if towar == nazwa_produktu:
                if self.magazyn[nazwa_produktu]['sztuk'] > 0:
                    print(f'Stan magazynu dla produktu {nazwa_produktu}: '
                          f'sztuk {liczba_sztuk_w_magazynie}')
                elif self.magazyn[nazwa_produktu]['sztuk'] == 0:
                    print('Produktu nie ma w magazynie.')
        if towar not in self.magazyn:
            print('Produktu nie ma w magazynie.')

    def pokaz_przeglad(self):
        poczatek = int(input('Podaj zakres opeacji od: ')) - 1
        koniec = int(input('Podaj zakres operacji do: ')) - 1
        dlugosc_listy = len(self.lista_operacji)
        if koniec != -1 and poczatek > koniec:
            print('Bledny zakres.')
        elif poczatek in range(dlugosc_listy) and koniec in range(dlugosc_listy):
            print(f'Lista operacji: {self.lista_operacji[poczatek:koniec + 1]}')
        elif poczatek >= dlugosc_listy or koniec >= dlugosc_listy:
            print(f'Wartosc poza zakresem. Zakres wynosi 1 - {dlugosc_listy}')
            poczatek = int(input('Podaj zakres od: ')) - 1
            koniec = int(input('Podaj zakres do: ')) - 1
            if poczatek > koniec:
                print('Bledny zakres.')
            elif poczatek in range(dlugosc_listy) and koniec in range(dlugosc_listy):
                print(f'Lista operacji: {self.lista_operacji[poczatek:koniec + 1]}')
            else:
                print('Bledny zakres.')
        elif poczatek == -1 and koniec != -1:
            print(f'Lista operacji: {self.lista_operacji[0:koniec + 1]}')
        elif koniec == -1 and poczatek != -1:
            print(f'Lista operacji: {self.lista_operacji[poczatek:dlugosc_listy]}')
        elif poczatek == -1 and koniec == -1:
            print(f'Lista operacji: {self.lista_operacji[0:dlugosc_listy]}')

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
