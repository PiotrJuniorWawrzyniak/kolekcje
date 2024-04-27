from constants_2 import COMMANDS
from models_2 import Warehouse


def main():
    warehouse = Warehouse(account=0, warehouse={}, actions_list=[], file_name='stan_magazynu.txt')
    file_name = 'stan_magazynu.txt'
    warehouse.read_from_file(file_name)

    while True:
        print(f'Dostepne komendy: {COMMANDS}')
        user_choice = input('Podaj komende: ')
        if user_choice == 'saldo':
            warehouse.account_balance()
        elif user_choice == 'sprzedaz':
            warehouse.sell_product()
        elif user_choice == 'zakup':
            warehouse.buy_product()
        elif user_choice == 'konto':
            warehouse.check_account()
        elif user_choice == 'lista':
            warehouse.list_warehouse()
        elif user_choice == 'magazyn':
            warehouse.check_warehouse()
        elif user_choice == 'przeglad':
            warehouse.show_overview()
        elif user_choice == 'koniec':
            warehouse.save_to_file(file_name)
            break
        else:
            print('Nie ma takiej komendy.')


if __name__ == '__main__':
    main()
