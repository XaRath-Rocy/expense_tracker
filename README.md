# 💰 Expense Tracker — Flask + SQLite

A full-stack web app to track daily expenses with category filtering, monthly view, and spending breakdown.

---

## 🛠️ Tech Stack
| Layer    | Technology          |
|----------|---------------------|
| Frontend | HTML, CSS, Bootstrap 5 |
| Backend  | Python, Flask       |
| Database | SQLite (built-in)   |

---

## 🚀 How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python app.py

# 3. Open browser and go to
http://127.0.0.1:5000
```

---

## 📁 Project Structure
```
expense_tracker/
├── app.py               ← Flask routes & logic
├── expenses.db          ← SQLite database (auto-created)
├── requirements.txt     ← Python packages
├── static/
│   └── style.css        ← Custom CSS styles
└── templates/
    ├── base.html        ← Common layout (navbar, flash messages)
    ├── index.html       ← Dashboard with table & summary
    ├── add_expense.html ← Add new expense form
    └── edit_expense.html← Edit existing expense
```

---

## ✨ Features
- ✅ Add / Edit / Delete expenses
- ✅ Categories: Food, Transport, Shopping, Bills, Health, Education, Other
- ✅ Filter by category or month
- ✅ Total spending summary cards
- ✅ Progress bars showing spending per category
- ✅ Flash messages for user feedback
- ✅ Fully responsive UI (Bootstrap 5)

---

## 🎓 Common Viva Questions & Answers

**Q: What is Flask?**
A: Flask is a lightweight Python web framework used to build web applications. It follows the WSGI standard and uses Jinja2 for templating.

**Q: What is SQLite?**
A: SQLite is a lightweight, file-based relational database. No server setup needed — the entire database is stored in a single `.db` file.

**Q: What is a route in Flask?**
A: A route maps a URL to a Python function. For example, `@app.route('/add')` means visiting `/add` calls the `add_expense()` function.

**Q: What is Jinja2 templating?**
A: Jinja2 lets us use Python-like syntax (loops, conditions, variables) inside HTML files using `{{ }}` and `{% %}` tags.

**Q: How does Flask handle form data?**
A: Flask reads POST form data via `request.form['field_name']`. For GET parameters, we use `request.args.get('key')`.

**Q: What is the MVC pattern?**
A: Model-View-Controller — Model (database/data), View (HTML templates), Controller (Flask routes). Our app follows this pattern.

**Q: What does `app.secret_key` do?**
A: It is used to sign session cookies and flash messages securely. Without it, Flask cannot store session data.

**Q: What is `sqlite3.Row`?**
A: It makes database rows behave like dictionaries, so we can access columns by name (e.g., `row['title']`) instead of index.
