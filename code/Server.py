from tabnanny import check
from data_handling import Router
from flask import Flask, Blueprint, render_template, url_for, request
import sqlite3
import stripe

app = Flask(__name__)

con = sqlite3.connect('Accounts.db')

app.config['STRIPE_PUBLIC_KEY'] = 'enter key'
app.config['STRIPE_SECRET_KEY'] = 'enter key'

product_id = 'enter id'
stripe.api_key = 'enter key'

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/purchase", methods=['GET', 'POST'])
def purchase():

    if request.method == "POST":
        print(request.form.getlist('myCheckbox'))
        return 'Done'
    Accounts=[1, 4, 5, 7, 2]
    session = stripe.checkout.Session.create(
        line_items=[
            {
                # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                'price': product_id,
                'quantity': len(Accounts),
            },
        ],
        mode='payment',
        success_url= url_for('results', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url= url_for('results', _external=True),
        automatic_tax={'enabled': True},
    )

    return render_template(
        "purchase.html",
        checkout_session_id=session['id'],
        checkout_public_key=app.config['STRIPE_PUBLIC_KEY']
    )

@app.route("/results")
def results():
    return render_template("base.html")
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)
