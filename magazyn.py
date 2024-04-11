DOSTEPNE_KOMENDY = ['saldo', 'sprzedaz', 'zakup', 'konto', 'lista',
                    'magazyn', 'przeglad', 'koniec']

konto = 0
magazyn = []
liczba_sztuk_w_magazynie = 0
towar = None
cena_produktu = 0
lista_operacji = []

wybor_uzytkownika = input('Podaj komende: ')

while wybor_uzytkownika != 'koniec':
    if wybor_uzytkownika not in DOSTEPNE_KOMENDY:
        print(f'{wybor_uzytkownika} nie jest dozwolone.')
        wybor_uzytkownika = input('Podaj komende: ')
    elif wybor_uzytkownika == 'saldo':
        kwota = float(input('Podaj kwote do dodania lub odjecia z konta: '))
        konto += kwota
        lista_operacji.append(f'Zaktualizowano saldo o {kwota}')
        wybor_uzytkownika = input('Podaj komende: ')
    elif wybor_uzytkownika == 'sprzedaz':
        nazwa_produktu = input('Podaj nazwe produktu: ')
        if nazwa_produktu in magazyn:
            magazyn.remove(nazwa_produktu)
        else:
            print('Produktu nie ma w magazynie.')
        liczba_sztuk = int(input('Podaj liczbe sztuk: '))
        if liczba_sztuk <= liczba_sztuk_w_magazynie:
            liczba_sztuk_w_magazynie -= liczba_sztuk
        else:
            print('Nie ma tylu sztuk w magazynie.')
        cena_produktu = float(input('Podaj cene produktu: '))
        if cena_produktu < 0:
            print('Cena nie mozna byc ujemna.')
        else:
            konto += cena_produktu * liczba_sztuk
        lista_operacji.append(f'Sprzedano produkt {nazwa_produktu}, sztuk {liczba_sztuk} po {cena_produktu}')
        wybor_uzytkownika = input('Podaj komende: ')
    elif wybor_uzytkownika == 'zakup':
        nazwa_produktu = input('Podaj nazwe produktu: ')
        magazyn.append(nazwa_produktu)
        cena_produktu = float(input('Podaj cenę produktu: '))
        liczba_sztuk = int(input('Podaj liczbe sztuk: '))
        liczba_sztuk_w_magazynie += liczba_sztuk
        if cena_produktu > konto:
            print('Nie masz wystarczajacych srodkow na koncie.')
        elif cena_produktu < 0:
            print('Cena nie mozna byc ujemna.')
        else:
            konto -= cena_produktu * liczba_sztuk
        lista_operacji.append(f'Kupiono produkt {nazwa_produktu}, sztuk {liczba_sztuk} po {cena_produktu}')
        wybor_uzytkownika = input('Podaj komende: ')
    elif wybor_uzytkownika == 'konto':
        print(f'Stan konta wynosi: {konto}')
        wybor_uzytkownika = input('Podaj komende: ')
    elif wybor_uzytkownika == 'lista':
        print(f'Stan magazynu wynosi: produkt {towar}, cena {cena_produktu}, sztuk {liczba_sztuk_w_magazynie}')
        wybor_uzytkownika = input('Podaj komende: ')
    elif wybor_uzytkownika == 'magazyn':
        towar = input('Podaj nazwe towaru: ')
        print(f'Stan magazynu dla produktu {towar} wynosi: {liczba_sztuk_w_magazynie}')
        wybor_uzytkownika = input('Podaj komende: ')
    elif wybor_uzytkownika == 'przeglad':
        poczatek = int(input('Podaj zakres opeacji od: ')) - 1
        koniec = int(input('Podaj zakres operacji do: ')) - 1
        print(f'Lista operacji: {lista_operacji[poczatek:koniec + 1]}')
        wybor_uzytkownika = input('Podaj komende: ')
        if poczatek == 0:
            poczatek = 1
        elif koniec == 0:
            koniec = len(lista_operacji) - 1
        elif poczatek != range(len(lista_operacji)) or koniec != range(len(lista_operacji)):
            print(f'Wartosc poza zakresem. Zakres wynosi 1 - {len(lista_operacji)}')
            poczatek = int(input('Podaj zakres od: ')) - 1
            koniec = int(input('Podaj zakres do: ')) - 1
            print(f'Lista_operacji: {lista_operacji[poczatek:koniec + 1]}')
        wybor_uzytkownika = input('Podaj komende: ')
