from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "expense_tracker_secret"

DB_NAME = "expenses.db"

# ─── Database Setup ────────────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            title     TEXT    NOT NULL,
            amount    REAL    NOT NULL,
            category  TEXT    NOT NULL,
            date      TEXT    NOT NULL,
            note      TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row   # access columns by name
    return conn

# ─── Routes ───────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    conn = get_db()
    cursor = conn.cursor()

    # Filter by category or month
    category_filter = request.args.get("category", "All")
    month_filter    = request.args.get("month", "")

    query  = "SELECT * FROM expenses WHERE 1=1"
    params = []

    if category_filter != "All":
        query += " AND category = ?"
        params.append(category_filter)
    if month_filter:
        query += " AND strftime('%Y-%m', date) = ?"
        params.append(month_filter)

    query += " ORDER BY date DESC"
    expenses = cursor.execute(query, params).fetchall()

    # Summary
    total = sum(e["amount"] for e in expenses)
    by_category = cursor.execute(
        "SELECT category, SUM(amount) as total FROM expenses GROUP BY category"
    ).fetchall()

    conn.close()

    categories = ["Food", "Transport", "Shopping", "Bills", "Health", "Education", "Other"]
    return render_template("index.html",
                           expenses=expenses,
                           total=total,
                           by_category=by_category,
                           categories=categories,
                           selected_category=category_filter,
                           selected_month=month_filter)


@app.route("/add", methods=["GET", "POST"])
def add_expense():
    categories = ["Food", "Transport", "Shopping", "Bills", "Health", "Education", "Other"]

    if request.method == "POST":
        title    = request.form["title"].strip()
        amount   = request.form["amount"].strip()
        category = request.form["category"]
        date     = request.form["date"]
        note     = request.form.get("note", "").strip()

        # Basic validation
        if not title or not amount or not date:
            flash("Please fill in all required fields.", "danger")
            return render_template("add_expense.html", categories=categories)

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            flash("Enter a valid positive amount.", "danger")
            return render_template("add_expense.html", categories=categories)

        conn = get_db()
        conn.execute(
            "INSERT INTO expenses (title, amount, category, date, note) VALUES (?, ?, ?, ?, ?)",
            (title, amount, category, date, note)
        )
        conn.commit()
        conn.close()

        flash(f'Expense "{title}" added successfully!', "success")
        return redirect(url_for("index"))

    today = datetime.today().strftime("%Y-%m-%d")
    return render_template("add_expense.html", categories=categories, today=today)


@app.route("/delete/<int:expense_id>")
def delete_expense(expense_id):
    conn = get_db()
    conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    flash("Expense deleted.", "warning")
    return redirect(url_for("index"))


@app.route("/edit/<int:expense_id>", methods=["GET", "POST"])
def edit_expense(expense_id):
    categories = ["Food", "Transport", "Shopping", "Bills", "Health", "Education", "Other"]
    conn = get_db()
    expense = conn.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()

    if not expense:
        flash("Expense not found.", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        title    = request.form["title"].strip()
        amount   = request.form["amount"].strip()
        category = request.form["category"]
        date     = request.form["date"]
        note     = request.form.get("note", "").strip()

        try:
            amount = float(amount)
        except ValueError:
            flash("Invalid amount.", "danger")
            return render_template("edit_expense.html", expense=expense, categories=categories)

        conn.execute(
            "UPDATE expenses SET title=?, amount=?, category=?, date=?, note=? WHERE id=?",
            (title, amount, category, date, note, expense_id)
        )
        conn.commit()
        conn.close()
        flash("Expense updated!", "success")
        return redirect(url_for("index"))

    conn.close()
    return render_template("edit_expense.html", expense=expense, categories=categories)


# ─── Run ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
