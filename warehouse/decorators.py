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


def log_operation(func_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f'Wykonywanie operacji: {func_name}')
            result = func(*args, **kwargs)
            print(f'Zakończono operację: {func_name}')
            return result
        return wrapper
    return decorator


def validate_positive_number(func):
    def wrapper(self, *args, **kwargs):
        for arg in args:
            if isinstance(arg, (int, float)) and arg <= 0:
                raise ValueError(f'Argument {arg} musi być liczbą dodatnią.')
        return func(self, *args, **kwargs)
    return wrapper


class Manager:
    def __init__(self, warehouse):
        self.warehouse = warehouse
        self.commands = {}

    def assign(self, command_name, function):
        if command_name in COMMANDS:
            self.commands[command_name] = function

    def execute(self, command_name):
        if command_name in self.commands:
            self.commands[command_name]()
        else:
            print('Nie ma takiej komendy.')

    @log_operation('account_balance')
    def account_balance(self):
        amount_money = float(input('Podaj kwote do dodania [+] lub odjecia [-] z konta: '))
        if amount_money > 0:
            self.warehouse.account += amount_money
            self.warehouse.actions_list.append(f'Zaktualizowano saldo. Do konta dodano {amount_money}.')
        elif amount_money < 0:
            self.warehouse.account += amount_money
            self.warehouse.actions_list.append(f'Zaktualizowano saldo. Od konta odjeto {-amount_money}.')
        else:
            print('Kwota nie moze byc zerowa.')

    @log_operation('sell_product')
    @validate_positive_number
    def sell_product(self):
        product_name = input('Podaj nazwe produktu: ')
        if product_name not in self.warehouse.warehouse or self.warehouse.warehouse[product_name]['sztuk'] == 0:
            print('Produktu nie ma w magazynie.')
            return
        pieces_number = int(input('Podaj liczbe sztuk: '))
        if pieces_number <= 0:
            print('Nieprawidlowa ilosc.')
            return
        if pieces_number > self.warehouse.warehouse[product_name]['sztuk']:
            print('Nie ma tylu sztuk w magazynie.')
            return
        product_price = float(input('Podaj cene produktu: '))
        if product_price <= 0:
            print('Cena nie mozna byc ujemna ani zerowa.')
            return
        self.warehouse.warehouse[product_name]['sztuk'] -= pieces_number
        self.warehouse.account += product_price * pieces_number
        self.warehouse.actions_list.append(
            f'Sprzedano produkt {product_name}, '
            f'sztuk {pieces_number} po {product_price}'
        )

    @log_operation('buy_product')
    @validate_positive_number
    def buy_product(self):
        product_name = input('Podaj nazwe produktu: ')
        pieces_number = int(input('Podaj liczbe sztuk: '))
        if pieces_number <= 0:
            print('Nieprawidlowa ilosc.')
            return
        product_price = float(input('Podaj cenę produktu: '))
        if product_price <= 0:
            print('Cena nie mozna byc ujemna ani zerowa.')
            return
        if product_price > self.warehouse.account or product_price * pieces_number > self.warehouse.account:
            print('Nie masz wystarczajacych srodkow na koncie.')
            return
        purchase_amount = product_price * pieces_number
        if product_name not in self.warehouse.warehouse:
            self.warehouse.warehouse[product_name] = {'sztuk': 0, 'cena': product_price}
        else:
            self.warehouse.warehouse[product_name]['cena'] = product_price
        self.warehouse.warehouse[product_name]['sztuk'] += pieces_number
        self.warehouse.account -= purchase_amount
        self.warehouse_price = product_price
        self.warehouse.actions_list.append(
            f'Kupiono produkt {product_name}, '
            f'sztuk {pieces_number} '
            f'po {self.warehouse_price}'
        )

    @log_operation('check_account')
    def check_account(self):
        print(f'Stan konta wynosi: {self.warehouse.account}')

    @log_operation('list_warehouse')
    def list_warehouse(self):
        empty_warehouse = True
        print('Stan magazynu wynosi:')
        for product_name, quantity in self.warehouse.warehouse.items():
            stock_pieces_number = quantity['sztuk']
            if self.warehouse.warehouse[product_name]['sztuk'] > 0:
                empty_warehouse = False
                print(f'Produkt {product_name}, sztuk {stock_pieces_number}')
        if empty_warehouse:
            print('Magazyn jest pusty.')

    @log_operation('check_warehouse')
    def check_warehouse(self):
        ware = input('Podaj nazwe towaru: ')
        for product_name, quantity in self.warehouse.warehouse.items():
            stock_pieces_number = quantity['sztuk']
            if ware == product_name:
                if self.warehouse.warehouse[product_name]['sztuk'] > 0:
                    print(f'Stan magazynu dla produktu {product_name}: '
                          f'sztuk {stock_pieces_number}')
                elif self.warehouse.warehouse[product_name]['sztuk'] == 0:
                    print('Produktu nie ma w magazynie.')
        if ware not in self.warehouse.warehouse:
            print('Produktu nie ma w magazynie.')

    @log_operation('show_overview')
    def show_overview(self):
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
        list_length = len(self.warehouse.actions_list)
        if finish != -1 and beginning > finish:
            print('Bledny zakres.')
        elif beginning in range(list_length) and finish in range(list_length):
            print(f'Lista operacji: {self.warehouse.actions_list[beginning:finish + 1]}')
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
                print(f'Lista operacji: {self.warehouse.actions_list[beginning:finish + 1]}')
            else:
                print('Bledny zakres.')
        elif beginning == -1 and finish != -1:
            print(f'Lista operacji: {self.warehouse.actions_list[0:finish + 1]}')
        elif finish == -1 and beginning != -1:
            print(f'Lista operacji: {self.warehouse.actions_list[beginning:list_length]}')
        elif beginning == -1 and finish == -1:
            print(f'Lista operacji: {self.warehouse.actions_list[0:list_length]}')


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
    manager.assign('saldo', manager.account_balance)
    manager.assign('sprzedaz', manager.sell_product)
    manager.assign('zakup', manager.buy_product)
    manager.assign('konto', manager.check_account)
    manager.assign('lista', manager.list_warehouse)
    manager.assign('magazyn', manager.check_warehouse)
    manager.assign('przeglad', manager.show_overview)

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
