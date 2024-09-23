from flask import Flask, render_template, request, redirect, flash
from models import db, URL
from validators import url as validate_url
import string
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form['url']

        if not validate_url(original_url):
            flash("Invalid URL. Please enter a valid URL.")
            return redirect('/')

        short_id = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        new_url = URL(original_url=original_url, short_id=short_id)

        db.session.add(new_url)
        db.session.commit()

        short_url = request.host_url + short_id
        return render_template('home.html', short_url=short_url)

    return render_template('home.html')

@app.route('/<short_id>')
def redirect_url(short_id):
    url = URL.query.filter_by(short_id=short_id).first_or_404()
    return redirect(url.original_url)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
