DOSTEPNE_KOMENDY = ['saldo', 'sprzedaz', 'zakup', 'konto', 'lista',
                    'magazyn', 'przeglad', 'koniec']

print('Dostepne komendy:', DOSTEPNE_KOMENDY)

konto = 0
magazyn = []
liczba_sztuk_w_magazynie = 0
towar = None
cena_produktu = 0
cena_magazynowa = 0
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
            liczba_sztuk = int(input('Podaj liczbe sztuk: '))
            if liczba_sztuk <= liczba_sztuk_w_magazynie:
                cena_produktu = float(input('Podaj cene produktu: '))
                if cena_produktu < 0:
                    print('Cena nie mozna byc ujemna.')
                else:
                    if nazwa_produktu in magazyn == 1:
                        magazyn.remove(nazwa_produktu)
                    elif nazwa_produktu in magazyn != 1:
                        magazyn.remove(nazwa_produktu)
                        magazyn.append(nazwa_produktu)
                    liczba_sztuk_w_magazynie -= liczba_sztuk
                    konto += cena_produktu * liczba_sztuk
                    lista_operacji.append(
                        f'Sprzedano produkt {nazwa_produktu}, '
                        f'sztuk {liczba_sztuk} po {cena_produktu}'
                    )
            else:
                print('Nie ma tylu sztuk w magazynie.')
        else:
            print('Produktu nie ma w magazynie.')
        wybor_uzytkownika = input('Podaj komende: ')
    elif wybor_uzytkownika == 'zakup':
        nazwa_produktu = input('Podaj nazwe produktu: ')
        liczba_sztuk = int(input('Podaj liczbe sztuk: '))
        cena_produktu = float(input('Podaj cenę produktu: '))
        if cena_produktu > konto:
            print('Nie masz wystarczajacych srodkow na koncie.')
        elif cena_produktu < 0:
            print('Cena nie mozna byc ujemna.')
        elif cena_produktu * liczba_sztuk > konto:
            print('Nie masz wystarczajacych srodkow na koncie.')
        else:
            magazyn.append(nazwa_produktu)
            liczba_sztuk_w_magazynie += liczba_sztuk
            konto -= cena_produktu * liczba_sztuk
            cena_magazynowa = cena_produktu
            lista_operacji.append(
                f'Kupiono produkt {nazwa_produktu}, '
                f'sztuk {liczba_sztuk} '
                f'po {cena_magazynowa}'
            )
        wybor_uzytkownika = input('Podaj komende: ')
    elif wybor_uzytkownika == 'konto':
        print(f'Stan konta wynosi: {konto}')
        wybor_uzytkownika = input('Podaj komende: ')
    elif wybor_uzytkownika == 'lista':
        if len(magazyn) == 0:
            print('Magazyn jest pusty.')
        else:
            print(
                f'Stan magazynu wynosi: produkt {towar}, '
                f'cena magazynowa {cena_magazynowa}, '
                f'sztuk {liczba_sztuk_w_magazynie}'
            )
        wybor_uzytkownika = input('Podaj komende: ')
    elif wybor_uzytkownika == 'magazyn':
        towar = input('Podaj nazwe towaru: ')
        print(f'Stan magazynu dla produktu {towar} wynosi: {liczba_sztuk_w_magazynie}')
        wybor_uzytkownika = input('Podaj komende: ')
    elif wybor_uzytkownika == 'przeglad':
        poczatek = int(input('Podaj zakres opeacji od: ')) - 1
        koniec = int(input('Podaj zakres operacji do: ')) - 1
        if poczatek in range(len(lista_operacji)) and koniec in range(len(lista_operacji)):
            print(f'Lista operacji: {lista_operacji[poczatek:koniec + 1]}')
        elif poczatek > len(lista_operacji) or koniec > len(lista_operacji):
            print(f'Wartosc poza zakresem. Zakres wynosi 1 - {len(lista_operacji)}')
            poczatek = int(input('Podaj zakres od: ')) - 1
            koniec = int(input('Podaj zakres do: ')) - 1
            print(f'Lista_operacji: {lista_operacji[poczatek:koniec + 1]}')
        elif poczatek == -1 and koniec != -1:
            print(f'Lista operacji: {lista_operacji[0:koniec + 1]}')
        elif koniec == -1 and poczatek != -1:
            print(f'Lista operacji: {lista_operacji[poczatek:len(lista_operacji)]}')
        elif poczatek == -1 and koniec == -1:
            print(f'Lista operacji: {lista_operacji[0:len(lista_operacji)]}')
        wybor_uzytkownika = input('Podaj komende: ')
