COMMANDS = ['saldo', 'sprzedaz', 'zakup', 'konto', 'lista',
            'magazyn', 'przeglad', 'koniec']


class Warehouse:
    def __init__(self, account, warehouse, actions_list, file_name):
        self.account = account
        self.warehouse = warehouse
        self.actions_list = actions_list
        self.file_name = file_name

    def save_to_file(self, file_name):
        self.file_name = file_name
        with open(self.file_name, 'w') as file:
            file.write(f'Stan konta: {self.account}\n')
            file.write('Stan magazynu wynosi:\n')
            empty_warehouse = True
            for product_name, quantity in self.warehouse.items():
                if self.warehouse[product_name]['sztuk'] > 0:
                    empty_warehouse = False
                    file.write(f'Produkt: {product_name}, sztuk: {quantity["sztuk"]}\n')
            if empty_warehouse:
                file.write('Magazyn jest pusty.\n')
            file.write('Historia operacji:\n')
            for action in self.actions_list:
                file.write(f'{action}\n')

    def read_from_file(self, file_name):
        self.file_name = file_name

        try:
            with open(self.file_name, 'r') as file:
                lines = file.readlines()
                self.account = float(lines[0].split(': ')[1].strip())
                print(f'Stan konta wynosi: {self.account}')
                if len(lines) > 1:
                    print('Stan magazynu wynosi:')
                    empty_warehouse = True
                    for line in lines[2:]:
                        if line.startswith('Produkt'):
                            parts = line.split(',')
                            product_name = parts[0].split(': ')[1].strip()
                            pieces_number = int(parts[1].split(': ')[1].strip())
                            self.warehouse[product_name] = {'sztuk': pieces_number, 'cena': 0}
                            if pieces_number > 0:
                                empty_warehouse = False
                                print(f'Produkt: {product_name}, sztuk: {pieces_number}')
                    if empty_warehouse:
                        print('Magazyn jest pusty.')
                else:
                    print('Magazyn jest pusty.')
                for line in lines:
                    line = line.strip()
                    if (line.startswith('Sprzedano') or
                            line.startswith('Kupiono') or
                            line.startswith('Zaktualizowano')):
                        self.actions_list.append(line)
        except FileNotFoundError:
            print("Plik nie istnieje. Nie wczytano stanu.")


def account_balance(warehouse):
    amount_money = float(input('Podaj kwote do dodania [+] lub odjecia [-] z konta: '))
    if amount_money > 0:
        warehouse.account += amount_money
        warehouse.actions_list.append(f'Zaktualizowano saldo. Do konta dodano {amount_money}.')
    elif amount_money < 0:
        warehouse.account += amount_money
        warehouse.actions_list.append(f'Zaktualizowano saldo. Od konta odjeto {-amount_money}.')
    else:
        print('Kwota nie moze byc zerowa.')


def sell_product(warehouse):
    product_name = input('Podaj nazwe produktu: ')
    if product_name not in warehouse.warehouse:
        print('Produktu nie ma w magazynie.')
    else:
        pieces_number = int(input('Podaj liczbe sztuk: '))
        if pieces_number <= 0:
            print('Nieprawidlowa ilosc.')
        elif pieces_number > warehouse.warehouse[product_name]['sztuk']:
            print('Nie ma tylu sztuk w magazynie.')
        else:
            product_price = float(input('Podaj cene produktu: '))
            if product_price <= 0:
                print('Cena nie mozna byc ujemna ani zerowa.')
            else:
                warehouse.warehouse[product_name]['sztuk'] -= pieces_number
                warehouse.account += product_price * pieces_number
                warehouse.actions_list.append(
                    f'Sprzedano produkt {product_name}, '
                    f'sztuk {pieces_number} po {product_price}'
                )


def buy_product(warehouse):
    product_name = input('Podaj nazwe produktu: ')
    pieces_number = int(input('Podaj liczbe sztuk: '))
    if pieces_number <= 0:
        print('Nieprawidlowa ilosc.')
    else:
        product_price = float(input('Podaj cenę produktu: '))
        if product_price > warehouse.account or product_price * pieces_number > warehouse.account:
            print('Nie masz wystarczajacych srodkow na koncie.')
        elif product_price <= 0:
            print('Cena nie mozna byc ujemna ani zerowa.')
        else:
            purchase_amount = product_price * pieces_number
            if product_name not in warehouse.warehouse:
                warehouse.warehouse[product_name] = {'sztuk': 0, 'cena': product_price}
            else:
                warehouse.warehouse[product_name]['cena'] = product_price
            warehouse.warehouse[product_name]['sztuk'] += pieces_number
            warehouse.account -= purchase_amount
            warehouse_price = product_price
            warehouse.actions_list.append(
                f'Kupiono produkt {product_name}, '
                f'sztuk {pieces_number} '
                f'po {warehouse_price}'
            )


def check_account(warehouse):
    print(f'Stan konta wynosi: {warehouse.account}')


def list_warehouse(warehouse):
    empty_warehouse = True
    print('Stan magazynu wynosi:')
    for product_name, quantity in warehouse.warehouse.items():
        stock_pieces_number = quantity['sztuk']
        if warehouse.warehouse[product_name]['sztuk'] > 0:
            empty_warehouse = False
            print(f'Produkt {product_name}, sztuk {stock_pieces_number}')
    if empty_warehouse:
        print('Magazyn jest pusty.')


def check_warehouse(warehouse):
    ware = input('Podaj nazwe towaru: ')
    for product_name, quantity in warehouse.warehouse.items():
        stock_pieces_number = quantity['sztuk']
        if ware == product_name:
            if warehouse.warehouse[product_name]['sztuk'] > 0:
                print(f'Stan magazynu dla produktu {product_name}: '
                      f'sztuk {stock_pieces_number}')
            elif warehouse.warehouse[product_name]['sztuk'] == 0:
                print('Produktu nie ma w magazynie.')
    if ware not in warehouse.warehouse:
        print('Produktu nie ma w magazynie.')


def show_overview(warehouse):
    enter_beginning = input('Podaj zakres operacji od: ')
    if enter_beginning == '' or enter_beginning == '0':
        beginning = -1
    else:
        beginning = int(enter_beginning) - 1
    enter_finish = input('Podaj zakres operacji do: ')
    if enter_finish == '' or enter_finish == '0':
        finish = -1
    else:
        finish = int(enter_finish) - 1
    list_length = len(warehouse.actions_list)
    if finish != -1 and beginning > finish:
        print('Bledny zakres.')
    elif beginning in range(list_length) and finish in range(list_length):
        print(f'Lista operacji: {warehouse.actions_list[beginning:finish + 1]}')
    elif beginning >= list_length or finish >= list_length:
        print(f'Wartosc poza zakresem. Zakres wynosi 1 - {list_length}')
        enter_beginning = input('Podaj zakres operacji od: ')
        if enter_beginning == '' or enter_beginning == '0':
            beginning = -1
        else:
            beginning = int(enter_beginning) - 1
        enter_finish = input('Podaj zakres operacji do: ')
        if enter_finish == '' or enter_finish == '0':
            finish = -1
        else:
            finish = int(enter_finish) - 1
        if beginning > finish:
            print('Bledny zakres.')
        elif beginning in range(list_length) and finish in range(list_length):
            print(f'Lista operacji: {warehouse.actions_list[beginning:finish + 1]}')
        else:
            print('Bledny zakres.')
    elif beginning == -1 and finish != -1:
        print(f'Lista operacji: {warehouse.actions_list[0:finish + 1]}')
    elif finish == -1 and beginning != -1:
        print(f'Lista operacji: {warehouse.actions_list[beginning:list_length]}')
    elif beginning == -1 and finish == -1:
        print(f'Lista operacji: {warehouse.actions_list[0:list_length]}')


def main():
    warehouse = Warehouse(account=0, warehouse={}, actions_list=[], file_name='stan_magazynu.txt')
    warehouse.file_name = 'stan_magazynu.txt'
    warehouse.read_from_file(warehouse.file_name)

    while True:
        print(f'Dostepne komendy: {COMMANDS}')
        user_choice = input('Podaj komende: ')
        if user_choice == 'saldo':
            account_balance(warehouse)
        elif user_choice == 'sprzedaz':
            sell_product(warehouse)
        elif user_choice == 'zakup':
            buy_product(warehouse)
        elif user_choice == 'konto':
            check_account(warehouse)
        elif user_choice == 'lista':
            list_warehouse(warehouse)
        elif user_choice == 'magazyn':
            check_warehouse(warehouse)
        elif user_choice == 'przeglad':
            show_overview(warehouse)
        elif user_choice == 'koniec':
            warehouse.save_to_file(warehouse.file_name)
            break
        else:
            print('Nie ma takiej komendy.')


if __name__ == '__main__':
    main()
