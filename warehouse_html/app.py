from flask import Flask, render_template, request
from warehouse_html_2 import warehouse

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', saldo=warehouse.account, magazyn=warehouse.warehouse)


@app.route('/historia/', defaults={'line_from': 0, 'line_to': None})
@app.route('/historia/<int:line_from>/<int:line_to>/')
def historia(line_from, line_to):
    if line_to is None:
        line_to = len(warehouse.actions_list)
    historia_fragment = warehouse.actions_list[line_from:line_to]
    return render_template('historia.html', historia=historia_fragment)


if __name__ == '__main__':
    app.run(debug=True)
