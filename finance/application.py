from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    #Will query the database for the user's cash
    rows = db.execute("SELECT cash FROM users WHERE id = :id" , id=session["user_id"])
    if not rows:
       return apology("missing user")
    cash = rows[0]["cash"]
    total = cash
    #Will query the database for the user's stocks
    stocks = db.execute("""SELECT symbol, SUM(shares) AS shares FROM transactions
        WHERE user_id = :user_id GROUP BY symbol HAVING SUM(shares) > 0""", user_id=session["user_id"])
    #Will go through Yahoo's database for the most up to date names and prices of stocks
    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["name"] = quote["name"]
        stock["price"] = quote["price"]
        total += stock["shares"] * quote["price"]
    # Will render the portfolio
    return render_template("index.html", cash=cash, stocks=stocks, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
         # Ensure valid form was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol")
        elif not request.form.get("shares"):
            return apology("shares not found")
        elif not request.form.get("shares").isdigit():
            return apology("must provide number of shares")
        shares = int(request.form.get("shares"))


        # Get stock quote
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("invalid symbol")

        cost = shares * quote["price"]

        #check user's available cash
        rows = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        if not rows:
            return apology("missing user")
        cash = rows[0]["cash"]

         #compares stock's price with user's cash to ensure that stock can be bought
        if cash < cost:
            return apology("stock price is greater than cash available")
        #records transaction into table
        db.execute("""INSERT INTO transactions (price, shares, symbol, user_id) VALUES(:price, :shares, :symbol, :user_id)""",
                        price=quote["price"], shares=shares, symbol=quote["symbol"], user_id=session["user_id"])
        #will deduct the cash
        db.execute("UPDATE users SET cash = cash - :cost WHERE id = :id",
                    cost=cost, id=session["user_id"])

        #Display portfolio
        flash("Bought")
        return redirect("/")

    # Get
    else:
       return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = :user_id", user_id=session["user_id"])
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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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
    """Log user out."""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        # Ensures symbol was submitted
        if not request.form.get("symbol"):
             return apology("please input symbol")
        #looks up symbol
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("symbol is invalid")
        #Display quote
        return render_template("quoted.html", quote=quote)
    #Get
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Missing username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Missing password")

        elif not request.form.get("confirmation"):
            return apology("Missing confimation password")

        # Ensure that password and confirmation password are equal
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password and comfirmation password do not match")

        #Ensure password security
        hashed_password = generate_password_hash(request.form.get("password"))

        # Insert users into database
        rows = db.execute("INSERT INTO users (username,hash) VALUES (:username, :hash)",
                          username=request.form.get("username"), hash=hashed_password)
        if not rows:
            return apology("username taken")

        # Remember which user has logged in
        session["user_id"] = rows
        # Redirect user to home page
        return redirect("/")
    if request.method == "GET":
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":
         # Ensure correct form is submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol")
        symbol = request.form.get("symbol").upper()
        if not request.form.get("shares"):
            return apology("missing shares")
        elif not request.form.get("shares").isdigit():
            return apology("invalid shares")
        shares = int(request.form.get("shares"))

        #Check how many shares user owes
        rows = db.execute("""SELECT SUM(shares) AS shares FROM transactions WHERE user_id = :user_id AND symbol = :symbol GROUP
            BY symbol""", user_id=session["user_id"], symbol=symbol)
        if len(rows) != 1:
            return apology("symbol not owned")
        if shares > rows[0]["shares"]:
            return apology("too many shares")
        # Get stock quote
        quote = lookup(request.form.get("symbol"))

        #records the transaction
        db.execute("""INSERT INTO transactions (user_id, shares, symbol, price) VALUES(:user_id, :shares, :symbol,
            :price)""", user_id=session["user_id"], symbol=quote["symbol"], shares=-shares, price=quote["price"])

        #deposits the cash
        db.execute("UPDATE users SET cash = cash + :value WHERE id = :id", value=shares * quote["price"],
            id=session["user_id"])

            #Displays portfolio
        flash("Sold")
        return redirect("/")
    # Get
    else:

        rows = db.execute("""SELECT symbol FROM transactions WHERE user_id = :user_id GROUP BY symbol
            HAVING SUM(shares) > 0""", user_id=session["user_id"])
        symbols = [row["symbol"] for row in rows]

        #Will display the sales form
        return render_template("sell.html", symbols=symbols)



def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
