from flask import Flask, render_template, request, redirect, url_for
from warehouse_html_2 import Warehouse

app = Flask(__name__)

warehouse = Warehouse(account=0, warehouse={}, actions_list=[],
                      file_name_1='stan_magazynu.txt', file_name_2='historia_operacji.txt')

warehouse.read_from_file('stan_magazynu.txt', 'historia_operacji.txt')


@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = None
    if request.method == 'POST':
        action = request.form['action']
        try:
            if action == 'zakup':
                product_name = request.form['product_name']
                product_price = float(request.form['product_price'])
                pieces_number = int(request.form['pieces_number'])
                if product_price <= 0 or pieces_number <= 0:
                    raise ValueError("Podaj poprawne dane.")
                if product_price * pieces_number > warehouse.account:
                    raise ValueError("Brak wystarczających środków na koncie.")
                warehouse.buy_product(product_name, pieces_number, product_price)
            elif action == 'sprzedaz':
                product_name = request.form['product_name']
                product_price = float(request.form['product_price'])
                pieces_number = int(request.form['pieces_number'])
                if product_price <= 0 or pieces_number <= 0:
                    raise ValueError("Podaj poprawne dane.")
                warehouse.sell_product(product_name, pieces_number, product_price)
            elif action == 'saldo':
                amount = float(request.form['amount'])
                comment = request.form['comment']
                if amount == 0:
                    raise ValueError("Podaj poprawne dane.")
                warehouse.update_balance(amount, comment)
        except ValueError as e:
            error_message = str(e)
        return redirect(url_for('index'))
    return render_template('index.html',
                           magazyn=warehouse.warehouse,
                           saldo=warehouse.account,
                           error_message=error_message)


@app.route('/historia/')
def historia():
    line_from = request.args.get('line_from', default=0, type=int)
    line_to = request.args.get('line_to', default=len(warehouse.actions_list) - 1, type=int)
    actions = warehouse.actions_list[line_from:line_to + 1]
    return render_template('historia.html', historia=actions)


if __name__ == '__main__':
    app.run(debug=True)
