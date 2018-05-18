import os
import json
import postcodes
import mysql.connector
from mysql.connector import errorcode
from flask import Flask, render_template, request


try:
    cnx = mysql.connector.connect(user='root', password='1234567890', host='127.0.0.1', database='finance')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something went wrong with your credentials")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("database does not exists")
    else:
        print(err)

app = Flask(__name__)


@app.route('/')
def home():
    user = {'name': 'angel', 'username': 'angelvargas'}
    posts = {}
    return render_template('home.html', title='.: Scurri -- Technical assignment :. Menu', user=user, posts=posts, g=None);


@app.route('/multiples')
def multiples():
    def multiples_three_five(below):
        yield (['ThreeFive' if n % 3 == 0 and n % 5 == 0 else 'Three' if n % 3 == 0 else
            'Five' if n % 5 == 0 else n for n in range(1, below + 1)])

    multiples_ = next(multiples_three_five(100))

    return render_template('multiples.html', title='Multiples', multiples=multiples_)


@app.route('/postal-codes', methods=['GET'])
def postal_codes():
    def format_codes():
        filename = os.path.join(os.path.dirname(__file__), 'storage/postal_codes.json')
        with open(filename, encoding='utf-8') as postal_codes:
            data = json.loads(postal_codes.read())
        return data
    return render_template('postal-codes.html', title='UK - Postal Codes', postalcodes=format_codes())


@app.route('/postal-codes', methods=['POST'])
def postal_codes_form():
    def process_form():
        formatted = ''
        valid_ps = False
        error_message = '';
        try:
            original_input = request.form['postal_code']
            formatted = ' '.join([str(part) for part in postcodes.parse_format(str(original_input))])
            valid_ps = True
        except ValueError as Exc:
            error_message = Exc

        return {'pristine': original_input, 'valid': valid_ps, 'formatted': formatted, 'error_message': error_message}
    return render_template('postal-codes.html', title='UK - Postal Codes', postal_codes={}, post_results=process_form())


@app.route('/postal-codes/<string:code_text>', methods=['GET'])
def get_postcode(code_text):
    search = postcodes.parse_format(code_text)

    search = ' '.join([str(part) for part in search])

    response = app.response_class(
        response=json.dumps({'success': {'foo': search}}),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run(debug=True)
