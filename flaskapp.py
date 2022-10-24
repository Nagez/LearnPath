from flask import Flask, request, render_template, flash
import connect

app = Flask(__name__)  # init app
learnPath = connect.connection("bolt://localhost:7687", "neo4j", "1234")  # connect to database
app.secret_key = b'%#s(&2p5_cakpas4==52f5vp1&5@j&o-^jx@mf_(h6hdal0gq_'  # secret key for flash (flask alert)


@app.route('/')  # the url /
def base():
    return render_template('basePage.html')  # get the html file named basePage, must be in templates folder


@app.route('/AddApplicant')  # the url /
def home1():
    return render_template('addApplicant.html')  # get the html file named addApplicant, must be in templates folder


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


@app.route('/showClass0', methods=["GET"])  # the url /
def showClass0():
    if request.method == "GET":
        return render_template('showClass0.html') # get the html file named showClass0, must be in templates folder


@app.route('/showClass0/pst', methods=["POST"])
def showClass():
    if request.method == "POST":
        # getting input with name = class in HTML form
        inputClass = request.form.get("class")
        # getting input with name = fname in HTML form
        first_name = request.form.get("fname")
        # getting input with name = lname in HTML form
        last_name = request.form.get("lname")
        availableClasses = learnPath.findMatchTroughName(first_name+' '+last_name, inputClass)

    return render_template('showClass.html', list=availableClasses)


@app.route('/welcome')
def welcome():
    return render_template('welcome.html', list=list)


@app.route('/statistics/<option>', methods=["GET"])
def statistics(option):
    options = ["Most popular classes", "Average scores in each institution's faculty", "Average scores in similar classes", "Percentage of accepted applicants in each area"]
    if request.method == "GET":
        if option == '0':
            list = []
        if option == '1':
            list = learnPath.getMostPopularClasses()
        if option == '2':
            list = learnPath.getAverageInFaculties()
        if option == '3':
            list = learnPath.getAverageInSimilar()
        if option == '4':
            list = learnPath.getAcceptedInAreaPercent()

    return render_template('listTemplate.html', options=options, list=list)

@app.route('/showClassbyID', methods=["GET"])  # the url /
def findByClassAndIDpage():
    if request.method == "GET":
        return render_template('findbyClass&ID.html') # get the html file named findbyClass&ID, must be in templates folder

@app.route('/showClassbyIDfun', methods=["POST"])
def showClassbyIDfun():
    if request.method == "POST":
        # getting input with name = class in HTML form
        inputClass = request.form.get("class")
        # getting input with name = ID in HTML form
        ID = request.form.get("ID")
        availableClasses = learnPath.findMatchIDTroughName(ID, inputClass)

    return render_template('showClass.html', list=availableClasses)


@app.route('/showClassUsingFriendsByName', methods=["GET"])  # the url /
def findByClassAndNameByFriendpage():
    if request.method == "GET":
        return render_template('findByFriend_Name.html') # get the html file named findByFriend_Name, must be in templates folder

@app.route('/showClassbyNameUsingFriends', methods=["POST"])
def showClassbyNameUsingFriends():
    if request.method == "POST":
        # getting input with name = fname in HTML form
        first_name = request.form.get("fname")
        # getting input with name = lname in HTML form
        last_name = request.form.get("lname")
        availableClasses = learnPath.findMatchTroughFriend(first_name+' '+last_name)

    return render_template('friendsAlgoResult.html', list=availableClasses)

@app.route('/areaPopularityForm', methods=["GET"])
def findByAreaPopularitypage():
    if request.method == "GET":
        return render_template('findByAreaPopularityForm.html') # get the html file named findByAreaPopularityForm, must be in templates folder

@app.route('/areaPopularityResult', methods=["POST"])
def showClassbyAreaPopularity():
    if request.method == "POST":
        # getting input with name = fname in HTML form
        first_name = request.form.get("fname")
        # getting input with name = lname in HTML form
        last_name = request.form.get("lname")
        availableClasses = learnPath.findMatchTroughAreaPopularity(first_name+' '+last_name)

    return render_template('AreaPopularityAlgoRes.html', list=availableClasses)

@app.route('/friendPathForm', methods=["GET"])
def findByfriendPathpage():
    if request.method == "GET":
        return render_template('FriendPathAlgoForm.html')  # get the html file named FriendPathAlgoForm, must be in templates folder

@app.route('/friendPathFormResult', methods=["POST"])
def showClassbyfriendPath():
    if request.method == "POST":
        # getting input with name = fname in HTML form
        first_name = request.form.get("fname")
        # getting input with name = lname in HTML form
        last_name = request.form.get("lname")
        # getting input with name = edges in HTML form
        edges = request.form.get("edges")
        availableClasses = learnPath.findMatchTroughFriendPath(first_name+' '+last_name, edges)

    return render_template('friendPathAlgoResult.html', list=availableClasses)
# @app.route('/SimilarAlgoForm', methods=["GET"])  # the url /
# def goToSimilarForm():
#     if request.method == "GET":
#         return render_template('SimilarAlgoForm.html') # get the html file named showClass0, must be in templates folder
# @app.route('/testt', methods=["POST"])  # the url /cool
# def similarRes():
#     if request.method == "POST":
#         fname = request.form.get("fname")
#         lname = request.form.get("lname")
#         className = request.form.get("class")
#         tags = learnPath.returnSimilar(className)
#         list=[]
#         for i in range(len(tags)):
#             classes = learnPath.returnClassWithConnection(className, tags[i])
#             list.append(classes)
#         print(tags)
#         return 'Hi cool'

