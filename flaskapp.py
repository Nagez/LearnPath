from flask import Flask, request, render_template, flash
import connect

app = Flask(__name__)  # init app
learnPath = connect.connection("bolt://localhost:7687", "neo4j", "1234")  # connect to database
app.secret_key = b'%#s(&2p5_cakpas4==52f5vp1&5@j&o-^jx@mf_(h6hdal0gq_'


@app.route('/')  # the url /
def base():
    return render_template('basePage.html')  # get the html file named basePage, must be in templates folder


@app.route('/AddApplicant')  # the url /
def home1():
    return render_template('addApplicant.html')  # get the html file named LearnPathHome, must be in templates folder


@app.route('/show', methods=["GET"])
def show():
    if request.method == "GET":
        Institution = learnPath.write_getAllQuery("Institution")
    return render_template('show.html', list=Institution, typeList="Institutions")


@app.route('/show/<type>/<variable>', methods=["GET"])
def show2(variable,type):
    if request.method == "GET":
        # print(variable)
        # print(type)
        # type = request.args.get(type)
        if type == 'Institutions':
            res = learnPath.getFacultiesFromUni(variable)
            # print(list(res[0].labels)[0])
            # typeOfList = list(res[0].labels)[0]
            return render_template('show.html', list=res, typeList='Faculties')
        if type == 'Faculties':
            res = learnPath.getClassesFromFaculty(variable)
            return render_template('ClassLearnHome.html', list=res)


@app.route('/added1', methods=["GET", "POST"])
def gfg():
    if request.method == "POST":
        # getting input with name = fname in HTML form
        first_name = request.form.get("fname")
        # getting input with name = lname in HTML form
        last_name = request.form.get("lname")
        # getting input with name = Area in HTML form
        Area = request.form['Area']
        # getting input with name = Gender in HTML form
        Gender = request.form['Gender']
        # getting input with name = Psychometric in HTML form
        Psychometric = request.form.get("Psychometric")
        # getting input with name = Bagrut in HTML form
        Bagrut=request.form.get("Bagrut")
        # Creating new applicant
        applicant = learnPath.generateCypherCreateCustomApplicant(Gender, Psychometric, Bagrut, Area, first_name+' '+last_name)
        print(applicant[0].id)
        flash("Applicant was successfully added ! Applicant Name: "+f"{applicant[0]._properties['Name']}"+"     Applicant ID : "+f"{applicant[0].id}");
    return render_template("addApplicant.html")


def homePage():
    print("hi")


@app.route('/showClass0', methods=["GET"])  # the url /
def showClass0():
    if request.method == "GET":
        return render_template('showClass0.html') # get the html file named showClass0, must be in templates folder


@app.route('/showClass0/pst', methods=["POST"])
def showClass():
    if request.method == "POST":
        # getting input with name = fname in HTML form
        first_name = request.form.get("fname")
        # getting input with name = lname in HTML form
        last_name = request.form.get("lname")
        availableClasses = learnPath.findMatchTroughName(first_name+' '+last_name, 'Computer science')

    return render_template('showClass.html', list=availableClasses)


@app.route('/welcome')
def welcome():
    return render_template('welcome.html', list=list)


@app.route('/statistics', methods=["GET"])
def statistics():
    if request.method == "GET":
        list = learnPath.getMostPopularClasses()

    return render_template('listTemplate.html', list=list)


@app.route('/cool')  # the url /cool
def hi():
    return 'Hi cool'

"""
            <li><a href="{{ url_for('page2') }}">Add an applicant</a></li>
            <li><a href="{{ url_for('page2') }}">Connect friend</a></li>
MATCH (f:Faculty)-[o:Offered_In]-(c:Class) where ID(f)=id return c
"""
