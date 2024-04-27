from constants import DOSTEPNE_KOMENDY
from models import Magazyn


def main():
    magazyn = Magazyn(konto=0, magazyn={}, lista_operacji=[], nazwa_pliku='stan_magazynu.txt')
    nazwa_pliku = 'stan_magazynu.txt'
    magazyn.odczytaj_z_pliku(nazwa_pliku)

    while True:
        print(f'Dostepne komendy: {DOSTEPNE_KOMENDY}')
        wybor_uzytkownika = input('Podaj komende: ')
        if wybor_uzytkownika == 'saldo':
            magazyn.wykonaj_saldo()
        elif wybor_uzytkownika == 'sprzedaz':
            magazyn.sprzedaj()
        elif wybor_uzytkownika == 'zakup':
            magazyn.kup()
        elif wybor_uzytkownika == 'konto':
            magazyn.sprawdz_konto()
        elif wybor_uzytkownika == 'lista':
            magazyn.wylistuj_magazyn()
        elif wybor_uzytkownika == 'magazyn':
            magazyn.sprawdz_magazyn()
        elif wybor_uzytkownika == 'przeglad':
            magazyn.pokaz_przeglad()
        elif wybor_uzytkownika == 'koniec':
            magazyn.zapisz_do_pliku(nazwa_pliku)
            break
        else:
            print('Nie ma takiej komendy.')


if __name__ == '__main__':
    main()
