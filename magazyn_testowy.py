DOSTEPNE_KOMENDY = ['saldo', 'sprzedaz', 'zakup', 'konto', 'lista',
                    'magazyn', 'przeglad', 'koniec']

konto = 0
magazyn = {}
liczba_sztuk_w_magazynie = 0
nazwa_produktu = None
cena_magazynowa = 0
lista_operacji = []

while True:
    print(f'Dostepne komendy: {DOSTEPNE_KOMENDY}')
    wybor_uzytkownika = input('Podaj komende: ')
    if wybor_uzytkownika == 'koniec':
        break

    elif wybor_uzytkownika == 'saldo':
        kwota = float(input('Podaj kwote do dodania lub odjecia z konta: '))
        konto += kwota
        lista_operacji.append(f'Zaktualizowano saldo o {kwota}')

    elif wybor_uzytkownika == 'sprzedaz':
        nazwa_produktu = input('Podaj nazwe produktu: ')
        if nazwa_produktu not in magazyn:
            print('Produktu nie ma w magazynie.')
            continue
        else:
            liczba_sztuk = int(input('Podaj liczbe sztuk: '))
            if liczba_sztuk <= 0:
                print('Nieprawidlowa ilosc.')
                continue
            elif liczba_sztuk > magazyn[nazwa_produktu]['sztuk']:
                print('Nie ma tylu sztuk w magazynie.')
                continue
            else:
                cena_produktu = float(input('Podaj cene produktu: '))
                if cena_produktu <= 0:
                    print('Cena nie mozna byc ujemna ani zerowa.')
                else:
                    magazyn[nazwa_produktu]['sztuk'] -= liczba_sztuk
                    konto += cena_produktu * liczba_sztuk
                    lista_operacji.append(
                        f'Sprzedano produkt {nazwa_produktu}, '
                        f'sztuk {liczba_sztuk} po {cena_produktu}'
                    )

    elif wybor_uzytkownika == 'zakup':
        nazwa_produktu = input('Podaj nazwe produktu: ')
        liczba_sztuk = int(input('Podaj liczbe sztuk: '))
        if liczba_sztuk <= 0:
            print('Nieprawidlowa ilosc.')
            continue
        cena_produktu = float(input('Podaj cenę produktu: '))
        if cena_produktu > konto or cena_produktu * liczba_sztuk > konto:
            print('Nie masz wystarczajacych srodkow na koncie.')
            continue
        elif cena_produktu <= 0:
            print('Cena nie mozna byc ujemna ani zerowa.')
            continue
        else:
            if nazwa_produktu not in magazyn:
                magazyn[nazwa_produktu] = {'sztuk': 0, 'cena': 0}
            magazyn[nazwa_produktu]['sztuk'] += liczba_sztuk
            liczba_sztuk_w_magazynie = magazyn[nazwa_produktu]['sztuk']
            magazyn[nazwa_produktu]['cena'] += cena_produktu
            konto -= cena_produktu * liczba_sztuk_w_magazynie
            cena_magazynowa = cena_produktu
            lista_operacji.append(
                f'Kupiono produkt {nazwa_produktu}, '
                f'sztuk {liczba_sztuk} '
                f'po {cena_magazynowa}'
            )

    elif wybor_uzytkownika == 'konto':
        print(f'Stan konta wynosi: {konto}')

    elif wybor_uzytkownika == 'lista':
        magazyn_pusty = True
        print('Stan magazynu wynosi:')
        for nazwa_produktu, ilosc in magazyn.items():
            liczba_sztuk_w_magazynie = ilosc['sztuk']
            if magazyn[nazwa_produktu]['sztuk'] > 0:
                magazyn_pusty = False
                print(f'Produkt {nazwa_produktu}, sztuk {liczba_sztuk_w_magazynie}')
        if magazyn_pusty:
            print('Magazyn jest pusty.')

    elif wybor_uzytkownika == 'magazyn':
        towar = input('Podaj nazwe towaru: ')
        for nazwa_produktu, ilosc in magazyn.items():
            liczba_sztuk_w_magazynie = ilosc['sztuk']
            if towar == nazwa_produktu:
                if magazyn[nazwa_produktu]['sztuk'] > 0:
                    print(f'Stan magazynu dla produktu {nazwa_produktu}: '
                          f'sztuk {liczba_sztuk_w_magazynie}')
                elif magazyn[nazwa_produktu]['sztuk'] == 0:
                    print('Produktu nie ma w magazynie.')
        if towar not in magazyn:
            print('Produktu nie ma w magazynie.')
            continue

    elif wybor_uzytkownika == 'przeglad':
        poczatek = int(input('Podaj zakres opeacji od: ')) - 1
        koniec = int(input('Podaj zakres operacji do: ')) - 1
        dlugosc_listy = len(lista_operacji)
        if poczatek in range(dlugosc_listy) and koniec in range(dlugosc_listy):
            print(f'Lista operacji: {lista_operacji[poczatek:koniec + 1]}')
        elif poczatek > dlugosc_listy or koniec > dlugosc_listy:
            print(f'Wartosc poza zakresem. Zakres wynosi 1 - {dlugosc_listy}')
            poczatek = int(input('Podaj zakres od: ')) - 1
            koniec = int(input('Podaj zakres do: ')) - 1
            print(f'Lista operacji: {lista_operacji[poczatek:koniec + 1]}')
        elif poczatek == -1 and koniec != -1:
            print(f'Lista operacji: {lista_operacji[0:koniec + 1]}')
        elif koniec == -1 and poczatek != -1:
            print(f'Lista operacji: {lista_operacji[poczatek:dlugosc_listy]}')
        elif poczatek == -1 and koniec == -1:
            print(f'Lista operacji: {lista_operacji[0:dlugosc_listy]}')

    else:
        print('Nie ma takiej komendy.')
