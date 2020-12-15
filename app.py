from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy


#
# SETUP/CONFIG
#
# change the classname to reflect the name of your table
# change the columns to reflect the columns you need
# each row of your data will be an instance of this class

#data = jobs_list

app = Flask(__name__)

app.config["ENV"] = 'development'
app.config["SECRET_KEY"]=b'_5#y2L"F4Q8z\n\xec]/'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///indeed_jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#
# DB SETUP
# 

# this set's up our db connection to our flask application
db = SQLAlchemy(app)

# this is our model (aka table)
class JobTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    link = db.Column(db.Text, nullable=False)
    company = db.Column(db.String(255), nullable=False)
    salary = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)

#     def __repr__(self):
#         return f"<Data {self.id} {self.job_title} {self.job_link} {self.job_company}
#          {self.job_salary} {self.job_description}>"    
# #
# VIEWS 
#


# set up your index view to show your "home" page
# it should include:
# links to any pages you have
# information about your data
# information about how to access your data
# you can choose to output data on this page
@app.route('/', methods=['GET'])
def index():
    return f"Indeed.com Job Scraper Program"

# include other views that return html here:
@app.route('/other')
def other():
    return render_template('other.html')

# set up the following views to allow users to make
# GET requests to get your data in json
# POST requests to store/update some data
# DELETE requests to delete some data

# change this to return your data
@app.route('/api', methods=['GET'])
def get_data():
    table = JobTable.query.all()
    # d = {row.id:[row.title,row.link,row.company,
    #     row.salary,row.description]}
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

# change this to allow users to add/update data
@app.route('/api', methods=['POST'])
def add_data():
    for k,v in request.args.items():
        pass
    return jsonify({})
        
# change this to allow the deletion of data
@app.route('/api', methods=['DELETE'])
def delete_data():
    for k,v in request.args.items():
        pass
    return jsonify({})

#
# CODE TO BE EXECUTED WHEN RAN AS SCRIPT
#

if __name__ == '__main__':
    #main()
    app.run(debug=True)
    db.drop_all()
    db.create_all()