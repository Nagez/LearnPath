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
            return render_template('showClass.html', list=res)

@app.route('/', methods=["GET", "POST"])
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
        learnPath.generateCypherCreateCustomApplicant(Gender, Psychometric, Bagrut, Area, first_name+' '+last_name)

    return render_template("LearnPathHome.html")

@app.route('/showClass0', methods=["GET"])  # the url /
def showClass0():
    if request.method == "GET":
        return render_template('showClass0.html') # get the html file named LearnPathHome, must be in templates folder

@app.route('/showClass0/pst', methods=["POST"])
def showClass():
    if request.method == "POST":
        # getting input with name = fname in HTML form
        first_name = request.form.get("fname")
        # getting input with name = lname in HTML form
        last_name = request.form.get("lname")
        availableClasses = learnPath.findMatchTroughName(first_name+' '+last_name, 'Computer science')

    return render_template('showClass.html', list=availableClasses)


@app.route('/statistics', methods=["GET"])
def statistics():
    # if request.method == "GET":
        # availableClasses = learnPath.
    return 'statistics'



@app.route('/cool') # the url /cool
def hi():
    return 'Hi cool'

"""
            <li><a href="{{ url_for('page2') }}">Add an applicant</a></li>
            <li><a href="{{ url_for('page2') }}">Connect friend</a></li>
MATCH (f:Faculty)-[o:Offered_In]-(c:Class) where ID(f)=id return c
"""
