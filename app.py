#Importing all required modules
from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import create_engine, MetaData
from flask_charts import GoogleCharts, Chart


#Creating the application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
charts = GoogleCharts(app)


#Database Creator
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    address = db.Column(db.String(200))
    med = db.Column(db.String(200))
    pres = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<task %r>' % self.id


#Initialising Home Page
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


#Initialising Database Editor page
@app.route('/index', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_id = request.form['id']       
        task_name = request.form['name']       
        task_age = request.form['age']
        task_gender = request.form['gender']
        task_address = request.form['address']       
        task_med = request.form['med']
        task_pres = request.form['pres']
        new_task = Todo(id=task_id, name=task_name, age=task_age, gender=task_gender, address=task_address, med=task_med, pres=task_pres)
 
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/index')
        except:
            return "There was an error adding the record. Check the data types."
    
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)



@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/index')
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.med = request.form['med']

        try:
            db.session.commit()
            return redirect('/index')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


#Initialising Database Viewer page
@app.route('/view', methods=['POST', 'GET'])
def view():
    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template('database.html', tasks=tasks)


#Initialising link to medplus
@app.route('/medplus', methods=['GET', 'POST'])
def medplus():
    return render_template('medplus.html')


#Initialising link to bigbasket
@app.route('/bigbasket', methods=['GET', 'POST'])
def bigbasket():
    return render_template('bigbasket.html')


#Initialising Statistics page
@app.route("/statistics")
def statistics():
    def stats():
        metadata = MetaData()
        engine = create_engine('sqlite:///test.db')
        metadata.create_all(engine)
    
        with engine.connect() as con:
            contents = con.execute('SELECT med FROM todo')
            lst=[]
            for rec in contents:
                for i in rec:
                    lst.append(i)
            a=lst.count("Nil")
            b=lst.count("Diabetic")
            c=lst.count("Blind")
            d=lst.count("Deaf")
            e=lst.count("Cancer")
            f=lst.count("Astigmatic")
            g=lst.count("Alzheimer")
            return a,b,c,d,e,f,g
    
    a,b,c,d,e,f,g = stats()
    
    med_chart = Chart("PieChart", "med")

    med_chart.options = {
                            "title": "Medical Conditions",
                            "is3D": True,
                            "width": 800,
                            "height": 800
                          }

    med_chart.data.add_column("string", "Medical Condition")
    med_chart.data.add_column("number", "Count")
    med_chart.data.add_row(["Nil", a])
    med_chart.data.add_row(["Diabetic", b])
    med_chart.data.add_row(["Blind", c])
    med_chart.data.add_row(["Deaf", d])
    med_chart.data.add_row(["Cancer", e])
    med_chart.data.add_row(["Astigmatic", f])
    med_chart.data.add_row(["Alzheimers", g])

    med_chart.add_event_listener("select", "my_function")
    return render_template("statistics.html", med_chart=med_chart)


#Initialising Contact Page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')


#Running the app
if __name__ == "__main__":
    app.run(debug=True)