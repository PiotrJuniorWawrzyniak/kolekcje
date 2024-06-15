COMMANDS = ['saldo', 'sprzedaz', 'zakup', 'konto', 'lista',
            'magazyn', 'przeglad', 'koniec']


class Warehouse:
    def __init__(self, account, warehouse, actions_list, file_name_1, file_name_2):
        self.account = account
        self.warehouse = warehouse
        self.actions_list = actions_list
        self.file_name_1 = file_name_1
        self.file_name_2 = file_name_2

    def save_to_file(self, file_name_1, file_name_2):
        self.file_name_1 = file_name_1
        self.file_name_2 = file_name_2
        with open(self.file_name_1, 'w') as file:
            file.write(f'Stan konta: {self.account}\n')
            file.write('Stan magazynu wynosi:\n')
            empty_warehouse = True
            for product_name, quantity in self.warehouse.items():
                if self.warehouse[product_name]['sztuk'] > 0:
                    empty_warehouse = False
                    file.write(f'Produkt: {product_name}, sztuk: {quantity["sztuk"]}\n')
            if empty_warehouse:
                file.write('Magazyn jest pusty.\n')
        with open(self.file_name_2, 'w') as file:
            file.write('Historia operacji:\n')
            for action in self.actions_list:
                file.write(f'{action}\n')

    def read_from_file(self, file_name_1, file_name_2):
        self.file_name_1 = file_name_1
        self.file_name_2 = file_name_2

        try:
            with open(self.file_name_1, 'r') as file:
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
            with open(self.file_name_2, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip()
                    if (line.startswith('Sprzedano') or
                            line.startswith('Kupiono') or
                            line.startswith('Zaktualizowano')):
                        self.actions_list.append(line)
        except FileNotFoundError:
            print("Plik nie istnieje. Nie wczytano stanu.")


class Manager:
    def __init__(self, warehouse):
        self.warehouse = warehouse
        self.commands = {}

    def assign(self, command_name):
        def decorator(func):
            self.commands[command_name] = func
            return func
        return decorator

    def execute(self, command_name):
        if command_name in self.commands:
            self.commands[command_name]()
        else:
            print('Nie ma takiej komendy.')


def account_balance(manager):
    @manager.assign('saldo')
    def balance():
        amount_money = float(input('Podaj kwote do dodania [+] lub odjecia [-] z konta: '))
        if amount_money > 0:
            manager.warehouse.account += amount_money
            manager.warehouse.actions_list.append(f'Zaktualizowano saldo. Do konta dodano {amount_money}.')
        elif amount_money < 0:
            manager.warehouse.account += amount_money
            manager.warehouse.actions_list.append(f'Zaktualizowano saldo. Od konta odjeto {-amount_money}.')
        else:
            print('Kwota nie moze byc zerowa.')


def sell_product(manager):
    @manager.assign('sprzedaz')
    def sell():
        product_name = input('Podaj nazwe produktu: ')
        if product_name not in manager.warehouse.warehouse or manager.warehouse.warehouse[product_name]['sztuk'] == 0:
            print('Produktu nie ma w magazynie.')
            return
        pieces_number = int(input('Podaj liczbe sztuk: '))
        if pieces_number <= 0:
            print('Nieprawidlowa ilosc.')
            return
        if pieces_number > manager.warehouse.warehouse[product_name]['sztuk']:
            print('Nie ma tylu sztuk w magazynie.')
            return
        product_price = float(input('Podaj cene produktu: '))
        if product_price <= 0:
            print('Cena nie mozna byc ujemna ani zerowa.')
            return
        manager.warehouse.warehouse[product_name]['sztuk'] -= pieces_number
        manager.warehouse.account += product_price * pieces_number
        manager.warehouse.actions_list.append(
            f'Sprzedano produkt {product_name}, '
            f'sztuk {pieces_number} po {product_price}'
        )


def buy_product(manager):
    @manager.assign('zakup')
    def buy():
        product_name = input('Podaj nazwe produktu: ')
        pieces_number = int(input('Podaj liczbe sztuk: '))
        if pieces_number <= 0:
            print('Nieprawidlowa ilosc.')
            return
        product_price = float(input('Podaj cenę produktu: '))
        if product_price <= 0:
            print('Cena nie mozna byc ujemna ani zerowa.')
            return
        if product_price > manager.warehouse.account or product_price * pieces_number > manager.warehouse.account:
            print('Nie masz wystarczajacych srodkow na koncie.')
            return
        purchase_amount = product_price * pieces_number
        if product_name not in manager.warehouse.warehouse:
            manager.warehouse.warehouse[product_name] = {'sztuk': 0, 'cena': product_price}
        else:
            manager.warehouse.warehouse[product_name]['cena'] = product_price
        manager.warehouse.warehouse[product_name]['sztuk'] += pieces_number
        manager.warehouse.account -= purchase_amount
        manager.warehouse_price = product_price
        manager.warehouse.actions_list.append(
            f'Kupiono produkt {product_name}, '
            f'sztuk {pieces_number} '
            f'po {manager.warehouse_price}'
        )


def check_account(manager):
    @manager.assign('konto')
    def check():
        print(f'Stan konta wynosi: {manager.warehouse.account}')


def list_warehouse(manager):
    @manager.assign('lista')
    def list_items():
        empty_warehouse = True
        print('Stan magazynu wynosi:')
        for product_name, quantity in manager.warehouse.warehouse.items():
            stock_pieces_number = quantity['sztuk']
            if manager.warehouse.warehouse[product_name]['sztuk'] > 0:
                empty_warehouse = False
                print(f'Produkt {product_name}, sztuk {stock_pieces_number}')
        if empty_warehouse:
            print('Magazyn jest pusty.')


def check_warehouse(manager):
    @manager.assign('magazyn')
    def check_items():
        ware = input('Podaj nazwe towaru: ')
        for product_name, quantity in manager.warehouse.warehouse.items():
            stock_pieces_number = quantity['sztuk']
            if ware == product_name:
                if manager.warehouse.warehouse[product_name]['sztuk'] > 0:
                    print(f'Stan magazynu dla produktu {product_name}: '
                          f'sztuk {stock_pieces_number}')
                elif manager.warehouse.warehouse[product_name]['sztuk'] == 0:
                    print('Produktu nie ma w magazynie.')
        if ware not in manager.warehouse.warehouse:
            print('Produktu nie ma w magazynie.')


def show_overview(manager):
    @manager.assign('przeglad')
    def overview():
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
        list_length = len(manager.warehouse.actions_list)
        if finish != -1 and beginning > finish:
            print('Bledny zakres.')
        elif beginning in range(list_length) and finish in range(list_length):
            print(f'Lista operacji: {manager.warehouse.actions_list[beginning:finish + 1]}')
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
                print(f'Lista operacji: {manager.warehouse.actions_list[beginning:finish + 1]}')
            else:
                print('Bledny zakres.')
        elif beginning == -1 and finish != -1:
            print(f'Lista operacji: {manager.warehouse.actions_list[0:finish + 1]}')
        elif finish == -1 and beginning != -1:
            print(f'Lista operacji: {manager.warehouse.actions_list[beginning:list_length]}')
        elif beginning == -1 and finish == -1:
            print(f'Lista operacji: {manager.warehouse.actions_list[0:list_length]}')


def main():
    warehouse = Warehouse(account=0,
                          warehouse={},
                          actions_list=[],
                          file_name_1='stan_magazynu.txt',
                          file_name_2='historia_operacji.txt')
    warehouse.file_name_1 = 'stan_magazynu.txt'
    warehouse.file_name_2 = 'historia_operacji.txt'
    warehouse.read_from_file(warehouse.file_name_1, warehouse.file_name_2)

    manager = Manager(warehouse)

    account_balance(manager)
    sell_product(manager)
    buy_product(manager)
    check_account(manager)
    list_warehouse(manager)
    check_warehouse(manager)
    show_overview(manager)

    while True:
        print(f'Dostepne komendy: {COMMANDS}')
        user_choice = input('Podaj komende: ')
        if user_choice == 'koniec':
            warehouse.save_to_file(warehouse.file_name_1, warehouse.file_name_2)
            break
        else:
            manager.execute(user_choice)


if __name__ == '__main__':
    main()
