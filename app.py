from flask import Flask, render_template, request, redirect
import sqlite3
from model import predict

app = Flask(__name__)

def get_db():
    return sqlite3.connect("database.db")


@app.route('/')
def home():
    return redirect('/login')


# ---------------- REGISTER ----------------

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = get_db()

        conn.execute(
            "INSERT INTO users VALUES (?,?)",
            (username, password)
        )

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')


# ---------------- LOGIN ----------------

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = get_db()

        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cur.fetchone()

        conn.close()

        if user:
            return redirect('/dashboard')

        return "Invalid Login"

    return render_template('login.html')


# ---------------- DASHBOARD ----------------

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    result = None

    if request.method == 'POST':

        patient_name = request.form['patient_name']

        age = int(request.form['age'])

        sex_text = request.form['sex']
        sex = 1 if sex_text == "M" else 0

        bp = int(request.form['bp'])
        chol = int(request.form['chol'])
        maxhr = int(request.form['maxhr'])
        oldpeak = float(request.form['oldpeak'])

        data = [
            age,
            sex,
            bp,
            chol,
            maxhr,
            oldpeak
        ]

        pred = predict(data)

        if pred == 0:

            if bp < 130 and chol < 220:
                result = "NORMAL"
            else:
                result = "WARNING"

        else:

            if bp > 170 or chol > 300 or oldpeak > 3:
                result = "CRITICAL"
            else:
                result = "WARNING"

        conn = get_db()

        conn.execute(
        """
        INSERT INTO patients
        (
        patient_name,
        age,
        sex,
        bp,
        chol,
        maxhr,
        oldpeak,
        result
        )
        VALUES(?,?,?,?,?,?,?,?)
        """,
        (
        patient_name,
        age,
        sex_text,
        bp,
        chol,
        maxhr,
        oldpeak,
        result
        )
        )

        conn.commit()
        conn.close()

    return render_template(
        "dashboard.html",
        result=result
    )
@app.route('/history')
def history():

    search = request.args.get("search","")

    conn = get_db()
    cur = conn.cursor()

    if search:

        cur.execute("""
        SELECT *
        FROM patients
        WHERE patient_name LIKE ?
        OR id LIKE ?
        ORDER BY id DESC
        """,
        ("%"+search+"%","%"+search+"%"))

    else:

        cur.execute("""
        SELECT *
        FROM patients
        ORDER BY id DESC
        """)

    data = cur.fetchall()

    conn.close()

    return render_template(
        "history.html",
        data=data,
        search=search
    )

@app.route('/delete/<int:id>')
def delete(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM patients WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/history')
# ---------------- REPORT ----------------

@app.route('/report/<int:id>')
def report(id):

    conn = get_db()

    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM patients WHERE id=?",
        (id,)
    )

    patient = cur.fetchone()

    conn.close()

    return render_template(
        "report.html",
        patient=patient
    )


if __name__ == "__main__":
    app.run(debug=False)

