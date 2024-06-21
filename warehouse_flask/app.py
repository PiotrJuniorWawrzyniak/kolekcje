from flask import Flask, render_template, request, redirect, url_for
from warehouse_flask import Warehouse

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
                comment = request.form.get('comment', '')
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
    line_from = request.args.get('line_from', default=1, type=int)
    line_to = request.args.get('line_to', default=len(warehouse.actions_list), type=int)
    if line_from < 1 or line_to > len(warehouse.actions_list) or line_from > line_to:
        return f"Podano niepoprawny zakres. Zakres powinien być od 1 do {len(warehouse.actions_list)}.", 400
    actions = warehouse.actions_list[line_from - 1:line_to]
    return render_template('historia.html', historia=actions)


@app.route('/historia/<int:start>/<int:end>/')
def historia_range(start, end):
    if start < 1 or end > len(warehouse.actions_list) or start > end:
        return f"Podano niepoprawny zakres. Zakres powinien być od 1 do {len(warehouse.actions_list)}.", 400
    actions = warehouse.actions_list[start - 1:end]
    return render_template('historia.html', historia=actions)


if __name__ == '__main__':
    app.run(debug=True)
