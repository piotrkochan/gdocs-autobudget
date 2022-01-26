import gspread
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from gspread.utils import rowcol_to_a1, ValueRenderOption
from collections import OrderedDict
import locale

locale.setlocale(locale.LC_ALL, '')
gc = gspread.service_account(filename='credentials.json')

# Open a sheet from a spreadsheet in one go
gs = gc.open("Budżet automat")
category_sheet = gs.worksheet('Wzorzec kategorii')

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/api/categories')
def get_incomes():
    return jsonify(category_map(category_sheet))


#
# # Update a range of cells using the top left corner address
# wks.update('A1', [[1, 2], [3, 4]])
#
# # Or update a single cell
# wks.update('B42', "it's down there somewhere, let me take another look.")
#
# # Format the header
# wks.format('A1:B1', {'textFormat': {'bold': True}})

month_to_sheet = {
    1: 'Styczeń',
    2: 'Luty',
    3: 'Marzec',
    4: 'Kwiecień',
    5: 'Maj',
    6: 'Czerwiec',
    7: 'Lipiec',
    8: 'Sierpień',
    9: 'Wrzesień',
    10: 'Październik',
    11: 'Listopad',
    12: 'Grudzień',
}


def category_map(sheet):
    in_group = 0
    curr = -1
    m = []
    for v in sheet.get('B35:B250'):
        if in_group == 0:
            if v and v[0] != ".":
                in_group = 1
                curr += 1
                m.append({
                    'group': v[0],
                    'categories': []
                })
        else:
            if not v:
                in_group = 0
            else:
                if v[0] != ".":
                    m[curr]['categories'].append(v[0])
    return m


def money(amount):
    return locale.currency(float(amount), symbol=False, grouping=False)


def __get_expense(sheet, row, col, value_render_option=ValueRenderOption.unformatted):
    val = sheet.get(rowcol_to_a1(row, col), value_render_option=value_render_option)
    if not val:
        return float(0)
    return val[0][0]


def get_expense(date, category):
    sheet = gs.worksheet(month_to_sheet[date.month])
    cat = sheet.find(category, in_column=2)
    day = sheet.find(str(date.day), in_row=1)
    return __get_expense(sheet, cat.row, day.col)


def add_expense(date, amount, category):
    sheet = gs.worksheet(month_to_sheet[date.month])
    cat = sheet.find(category, in_column=2)
    day = sheet.find(str(date.day), in_row=1)

    formula = __get_expense(sheet, cat.row, day.col, value_render_option=ValueRenderOption.formula)
    expr = formula

    if isinstance(formula, str):
        if formula[0] == "=":
            p = formula[1:].split('+')
            curr = tuple(map(money, p))
            expr = '=%s+%s' % ('+'.join(curr), money(amount))
    elif formula > 0:
        expr = '=%s+%s' % (money(formula), money(amount))
    else:
        expr = money(amount)

    sheet.update_cell(cat.row, day.col, expr)

print(category_map(category_sheet))

#
# d = datetime.datetime.strptime("05.01.2022", "%d.%m.%Y")
# add_expense(d, 1, "Paliwo do auta")
# print(get_expense(d, "Paliwo do auta"))

# w =
# build_category_map(w)
