from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ======= MySQL Configuration =======
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Your MySQL password
    'database': 'skilllink'
}

# ======= Home Page =======
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index_redirect():
    return redirect(url_for('home'))  # ✅ redirect to home


# ======= About =======
@app.route('/about')
def about():
    return render_template('about.html')


# ======= Contact =======
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        email = request.form['email']
        message = request.form['message']

        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        cur.execute("INSERT INTO contact(email, message) VALUES(%s, %s)", (email, message))
        conn.commit()
        cur.close()
        conn.close()

        flash("Message sent successfully!", "success")
        return redirect(url_for('contact'))

    return render_template('contact.html')


# ======= Post Job =======
@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        budget = request.form['budget']

        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        cur.execute("INSERT INTO jobs(title, description, budget) VALUES(%s, %s, %s)", (title, description, budget))
        conn.commit()
        cur.close()
        conn.close()

        flash("Job posted successfully!", "success")
        return redirect(url_for('jobs'))

    return render_template('post_job.html')


# ======= Jobs Page =======
@app.route('/jobs')
def jobs():
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute("SELECT id, title, description, budget FROM jobs")
    jobs = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('jobs.html', jobs=jobs)


# ======= Apply for Job =======
@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def apply(job_id):
    if request.method == 'POST':
        name = request.form['name']
        skills = request.form['skills']
        portfolio = request.form['portfolio']

        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO applications(job_id, name, skills, portfolio) VALUES(%s, %s, %s, %s)",
            (job_id, name, skills, portfolio)
        )
        conn.commit()
        cur.close()
        conn.close()

        flash("Application submitted successfully!", "success")
        return redirect(url_for('jobs'))

    return render_template('apply.html', job_id=job_id)


# ======= Messages =======
@app.route('/messages', methods=['GET', 'POST'])
def messages():
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()

    if request.method == 'POST':
        sender = "You"
        message = request.form['message']
        cur.execute("INSERT INTO messages(sender, message) VALUES(%s, %s)", (sender, message))
        conn.commit()
        flash("Message sent!", "success")
        return redirect(url_for('messages'))

    cur.execute("SELECT sender, message FROM messages ORDER BY id DESC")
    msgs = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('message.html', messages=msgs)

@app.route('/dashboard')
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jobs")
    jobs = cur.fetchall()

    cur.execute("SELECT * FROM applications")
    applications = cur.fetchall()

    cur.execute("SELECT * FROM freelancers")
    freelancers = cur.fetchall()

    cur.execute("SELECT * FROM contact")
    contacts = cur.fetchall()
    cur.close()

    return render_template(
        'admin_dashboard.html',
        jobs=jobs,
        applications=applications,
        freelancers=freelancers,
        contacts=contacts
    )
# ======= Run App =======
if __name__ == '__main__':
    print("✅ Flask server starting on http://127.0.0.1:5000 ...")
    app.run(debug=True)