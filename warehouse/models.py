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
