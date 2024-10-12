import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    # Fetch all transactions for the user
    transactions_db = db.execute(
        "SELECT symbol, SUM(shares) AS shares, price FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)

    # Fetch user's current cash balance
    cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = cash_db[0]["cash"]

    # Calculate total value of all stock holdings
    total_stock_value = 0
    for row in transactions_db:
        total_stock_value += row["shares"] * row["price"]

    # Calculate grand total (total stock value + cash)
    grand_total = total_stock_value + cash

    return render_template("index.html", database=transactions_db, cash=cash, total_value=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    else:
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        # Check if symbol is provided
        if not symbol:
            return apology("must provide symbol")

        # Look up the stock symbol
        stock = lookup(symbol.upper())

        # Check if the stock symbol is valid
        if stock is None:
            return apology("symbol does not exist")

        # Check if shares is a positive integer
        if shares <= 0:
            return apology("shares must be a positive integer")

        transaction_value = shares * stock["price"]

        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash_db[0]["cash"]

        if user_cash < transaction_value:
            return apology("Not Enough Money")

        uptd_cash = user_cash - transaction_value

        # Update user's cash balance
        db.execute("UPDATE users SET cash = ? WHERE id = ?", uptd_cash, user_id)

        # Record transaction in transactions table
        date = datetime.now()
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
                   user_id, symbol.upper(), shares, stock["price"], date)

        flash("Bought!")
        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]

    # Fetch transaction history from the database
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", user_id)

    # Render history.html template with transaction data
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    # POST request
    symbol = request.form.get("symbol")

    # Check if symbol is provided
    if not symbol:
        return apology("must provide symbol")

    # Look up the stock symbol
    stock = lookup(symbol.upper())

    # Check if the stock symbol is valid
    if stock == None:
        return apology("symbol does not exist")

    # Render quoted.html with the stock information
    return render_template("quoted.html", symbol=stock["symbol"], price=stock["price"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username")

        if not password:
            return apology("must provide password")

        if not confirmation:
            return apology("must confirm password")

        if password != confirmation:
            return apology("passwords must match")

        hash = generate_password_hash(password)

        try:
            # INSERT INTO table_name (column1, column2, column3, ...) VALUES (value1, value2, value3, ...);
            new_user = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except:
            return apology("username already exists")

        # Log in the newly registered user
        session["user_id"] = new_user

        # Redirect user to home page
        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        try:
            user_id = session["user_id"]
            symbols_user = db.execute(
                "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", user_id)
            symbols = [row["symbol"] for row in symbols_user]
            return render_template("sell.html", symbols=symbols)
        except Exception as e:
            return apology(f"An error occurred: {e}")

    else:
        try:
            symbol = request.form.get("symbol")
            shares = int(request.form.get("shares"))

            # Check if symbol is provided
            if not symbol:
                return apology("must provide symbol")

            # Look up the stock symbol
            stock = lookup(symbol.upper())

            # Check if the stock symbol is valid
            if stock is None:
                return apology("symbol does not exist")

            # Check if shares is a positive integer
            if shares <= 0:
                return apology("shares must be a positive integer")

            # Check if the user owns enough shares of the selected symbol
            user_id = session["user_id"]
            user_shares = db.execute(
                "SELECT SUM(shares) AS total_shares FROM transactions WHERE user_id = ? AND symbol = ?", user_id, symbol)
            if user_shares[0]["total_shares"] < shares:
                return apology("not enough shares to sell")

            # Calculate transaction value
            transaction_value = shares * stock["price"]

            # Update user's cash balance
            db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", transaction_value, user_id)

            # Record the transaction in the transactions table
            date = datetime.now()
            db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
                       user_id, symbol.upper(), -shares, stock["price"], date)

            flash("Sold!")
            return redirect("/")
        except Exception as e:
            return apology(f"An error occurred: {e}")


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Add additional cash to user's account"""
    if request.method == "POST":
        amount = request.form.get("amount")

        # Validate the amount
        if not amount or float(amount) <= 0:
            return apology("must provide a positive amount")

        # Update user's cash balance
        user_id = session["user_id"]
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", float(amount), user_id)

        flash("Cash added!")
        return redirect("/")

    else:
        return render_template("add_cash.html")
