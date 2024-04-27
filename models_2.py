class Warehouse:
    def __init__(self, account, warehouse, actions_list, file_name):
        self.account = account
        self.warehouse = warehouse
        self.actions_list = actions_list
        self.file_name = file_name

    def account_balance(self):
        amount_money = float(input('Podaj kwote do dodania [+] lub odjecia [-] z konta: '))
        if amount_money > 0:
            self.account += amount_money
            self.actions_list.append(f'Zaktualizowano saldo. Do konta dodano {amount_money}.')
        elif amount_money < 0:
            self.account += amount_money
            self.actions_list.append(f'Zaktualizowano saldo. Od konta odjeto {-amount_money}.')
        else:
            print('Kwota nie moze byc zerowa.')

    def sell_product(self):
        product_name = input('Podaj nazwe produktu: ')
        if product_name not in self.warehouse:
            print('Produktu nie ma w magazynie.')
        else:
            pieces_number = int(input('Podaj liczbe sztuk: '))
            if pieces_number <= 0:
                print('Nieprawidlowa ilosc.')
            elif pieces_number > self.warehouse[product_name]['sztuk']:
                print('Nie ma tylu sztuk w magazynie.')
            else:
                product_price = float(input('Podaj cene produktu: '))
                if product_price <= 0:
                    print('Cena nie mozna byc ujemna ani zerowa.')
                else:
                    self.warehouse[product_name]['sztuk'] -= pieces_number
                    self.account += product_price * pieces_number
                    self.actions_list.append(
                        f'Sprzedano produkt {product_name}, '
                        f'sztuk {pieces_number} po {product_price}'
                    )

    def buy_product(self):
        product_name = input('Podaj nazwe produktu: ')
        pieces_number = int(input('Podaj liczbe sztuk: '))
        if pieces_number <= 0:
            print('Nieprawidlowa ilosc.')
        else:
            product_price = float(input('Podaj cenę produktu: '))
            if product_price > self.account or product_price * pieces_number > self.account:
                print('Nie masz wystarczajacych srodkow na koncie.')
            elif product_price <= 0:
                print('Cena nie mozna byc ujemna ani zerowa.')
            else:
                if product_name not in self.warehouse:
                    self.warehouse[product_name] = {'sztuk': 0, 'cena': 0}
                self.warehouse[product_name]['sztuk'] += pieces_number
                stock_pieces_number = self.warehouse[product_name]['sztuk']
                self.warehouse[product_name]['cena'] += product_price
                self.account -= product_price * stock_pieces_number
                warehouse_price = product_price
                self.actions_list.append(
                    f'Kupiono produkt {product_name}, '
                    f'sztuk {pieces_number} '
                    f'po {warehouse_price}'
                )

    def check_account(self):
        print(f'Stan konta wynosi: {self.account}')

    def list_warehouse(self):
        empty_warehouse = True
        print('Stan magazynu wynosi:')
        for product_name, quantity in self.warehouse.items():
            stock_pieces_number = quantity['sztuk']
            if self.warehouse[product_name]['sztuk'] > 0:
                empty_warehouse = False
                print(f'Produkt {product_name}, sztuk {stock_pieces_number}')
        if empty_warehouse:
            print('Magazyn jest pusty.')

    def check_warehouse(self):
        ware = input('Podaj nazwe towaru: ')
        for product_name, quantity in self.warehouse.items():
            stock_pieces_number = quantity['sztuk']
            if ware == product_name:
                if self.warehouse[product_name]['sztuk'] > 0:
                    print(f'Stan magazynu dla produktu {product_name}: '
                          f'sztuk {stock_pieces_number}')
                elif self.warehouse[product_name]['sztuk'] == 0:
                    print('Produktu nie ma w magazynie.')
        if ware not in self.warehouse:
            print('Produktu nie ma w magazynie.')

    def show_overview(self):
        beginning = int(input('Podaj zakres operacji od: ')) - 1
        finish = int(input('Podaj zakres operacji do: ')) - 1
        list_length = len(self.actions_list)
        if finish != -1 and beginning > finish:
            print('Bledny zakres.')
        elif beginning in range(list_length) and finish in range(list_length):
            print(f'Lista operacji: {self.actions_list[beginning:finish + 1]}')
        elif beginning >= list_length or finish >= list_length:
            print(f'Wartosc poza zakresem. Zakres wynosi 1 - {list_length}')
            beginning = int(input('Podaj zakres od: ')) - 1
            finish = int(input('Podaj zakres do: ')) - 1
            if beginning > finish:
                print('Bledny zakres.')
            elif beginning in range(list_length) and finish in range(list_length):
                print(f'Lista operacji: {self.actions_list[beginning:finish + 1]}')
            else:
                print('Bledny zakres.')
        elif beginning == -1 and finish != -1:
            print(f'Lista operacji: {self.actions_list[0:finish + 1]}')
        elif finish == -1 and beginning != -1:
            print(f'Lista operacji: {self.actions_list[beginning:list_length]}')
        elif beginning == -1 and finish == -1:
            print(f'Lista operacji: {self.actions_list[0:list_length]}')

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
