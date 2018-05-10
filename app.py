from flask import render_template
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    user = {'name': 'angel', 'username': 'angelvargas'}
    posts = {}
    return render_template('home.html', title='.: Scurri -- Technical assignment :. Menu', user=user, posts=posts, g=None);


@app.route('/multiples')
def multiples():
    def divisibles(below, *divisors):
        return (n for n in range(below) if 0 in (n % d for d in divisors))

    print
    sum(divisibles(100, 3, 5))

    return render_template('multiples.html', title='Multiples')


@app.route('/postal-codes')
def postalCodes():
    return render_template('postal-codes.html', title='UK - Postal Codes')


if __name__ == '__main__':
    app.run()
