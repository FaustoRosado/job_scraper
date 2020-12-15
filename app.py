from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["ENV"] = 'development'
app.config["SECRET_KEY"]=b'_5#y2L"F4Q8z\n\xec]/'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///indeed_jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class JobTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    link = db.Column(db.Text, nullable=False)
    company = db.Column(db.String(255), nullable=False)
    salary = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)

@app.route('/', methods=['GET'])
def home():
    table = JobTable.query.all()
    d = []
    for row in table:
        job_dict = {
            "title" : row.title,
            "link" : row.link,
            "company" : row.company,
            "salary" : row.salary,
            "description" : row.description
        }
        d.append(job_dict)
    return render_template("home.html", data=d)

@app.route('/api', methods=['GET'])
def get_data():
    table = JobTable.query.all()
    d = []
    for row in table:
        job_dict = {
            "title" : row.title,
            "link" : row.link,
            "company" : row.company,
            "salary" : row.salary,
            "description" : row.description
        }
        d.append(job_dict)
    return jsonify(d)

if __name__ == '__main__':
    app.run(debug=True)
