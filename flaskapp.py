from flask import Flask,request,render_template,redirect
import connect

app = Flask(__name__)  # init app
learnPath = connect.connection("bolt://localhost:7687", "neo4j", "1234")  # connect to database


@app.route('/')  # the url /
def home():
    return render_template('LearnPathHome.html') # get the html file named LearnPathHome, must be in templates folder


@app.route('/show', methods=["GET"])
def show():
    if request.method == "GET":
        Institution = learnPath.write_getAllQuery("Institution")
    return render_template('show.html', list=Institution, typeList="Institutions")


@app.route('/show/<variable>', methods=["GET"])
def show2(variable):
    if request.method == "GET":
        if int(variable) > 6:
            res = learnPath.getClassesFromFaculty(variable)
            return render_template('showClass.html', list=res, typeList="Classes")
        else:
            res = learnPath.getFacultiesFromUni(variable)
    print(res)
    return render_template('show.html', list=res, typeList="Faculties")


@app.route('/showClass', methods=["GET", "POST"])
def showClass():
    if request.method == "GET":
        availableClasses = learnPath.findMatchTroughName('Or Nagar', 'Computer science')

    return render_template('showClass.html', list=availableClasses)


@app.route('/cool') # the url /cool
def hi():
    return 'Hi cool'

"""
            <li><a href="{{ url_for('page2') }}">Add an applicant</a></li>
            <li><a href="{{ url_for('page2') }}">Connect friend</a></li>
MATCH (f:Faculty)-[o:Offered_In]-(c:Class) where ID(f)=id return c
"""
