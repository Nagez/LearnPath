import random
import threading
from tkinter import DISABLED, NORMAL
import names
import connect
import flaskapp
import GUI

queriesString = ""  # global string to print to the file

# statistic globals in percentage
GirltoBoyRatio = 0.58
# psychometricAVG according to EconomicSocialCluster 1 -> 10 (psychometric score is between 200 to 800)
psychometricAVGESC = [432,516,540,527,555,566,584,610,624,640]
bagrutAVGESC = [80,85,90,90,95,100,105,105,110,115]
locations = ['South', 'Center', 'North', 'Jerusalem']


# generate a create applicant query using the statistics
def generateCypherCreateApplicant():
    random_gender = random.choices(['Female', 'Male'], [GirltoBoyRatio, 1 - GirltoBoyRatio])
    random_SocioEconomicCluster = random.choices([1,2,3,4,5,6,7,8,9,10],[5,5,12,12,9,9,13,13,11,11],k=1) # get random EconomicSocialCluster according to statistics
    faculty = getRandomFacultyBySEC(random_SocioEconomicCluster[0])
    random_psyScore, random_bagrutScore = getRandomScore(random_SocioEconomicCluster[0])
    random_area = random.choices(locations)
    applicantQuery = "CREATE (a:Applicant{Name:'"+names.get_full_name(gender=random_gender[0])+"' ,Gender:'"+random_gender[0]+"' ,Bagrut: "+str(random_bagrutScore)+", Psychometric: "+str(random_psyScore)+", Area: '"+random_area[0]+"', Faculty: '"+faculty+"', Degree: ''})\n" #, isAccepted: "+random_isAccepted+" , hobby: '', ethnicity: ''
    return applicantQuery


# get random faculty with the probability of a given sec
# sec: social economic cluster (values 1 to 10)
def getRandomFacultyBySEC(sec):
    faculties =  ['Social Sciences', 'Engineering', 'Education', 'Economics and Business Administration',
             'Math', 'Computer Science', 'Medicine', 'Law', 'Agriculture', 'Art', 'Social Sciences', 'Exact Science', 'Humanities', 'Medicine']
    random_faculty = 'none'
    if sec == 1 or sec == 2:
        random_faculty = random.choices(faculties, [12.3, 10.7, 32.6, 15.9, 1.6, 4, 8.4, 4.3, 3.2, 2, 2, 1.1, 1.6, 0.3], k=1)
    if sec == 3 or sec == 4:
        random_faculty = random.choices(faculties, [18.3, 15.7, 21.0, 13.3, 1.7, 5, 8.2, 6.1, 3.3, 2.6, 1.9, 1, 1.2, 0.6], k=1)
    if sec == 5 or sec == 6:
        random_faculty = random.choices(faculties, [19.2, 19.4, 17.6, 12.4, 3.3, 6, 6.1, 5.2, 3.1, 2.7, 2.4, 1.1, 1, 0.6], k=1)
    if sec == 7 or sec == 8:
        random_faculty = random.choices(faculties, [20.5, 19.4, 12.3, 11.1, 3.2, 8, 4.9, 5.1, 4.5, 3.9, 2.7, 1.9, 1.3, 1.2], k=1)
    if sec == 9 or sec == 10:
        random_faculty = random.choices(faculties, [21.1, 18.5, 8.2, 10.1, 2.9, 10, 4.4, 5.4, 5, 5.8, 2.8, 2.6, 1.4, 1.8], k=1)

    return random_faculty[0]


# get a gaussian random score around the average score of a given sec
# sec: social economic cluster (values 1 to 10)
def getRandomScore(sec):
    bagrutScore = 1  # placeholder init
    psyScore = 1
    while psyScore <= 200 or psyScore >= 800:
        psyScore = round(random.gauss(psychometricAVGESC[sec-1], 200 / 3))  # get a round score according to gaussian distribution of a score mean of the socialEconomic Cluster
    while bagrutScore <= 60 or bagrutScore >= 120:
        bagrutScore = round(random.gauss(bagrutAVGESC[sec - 1], 200 / 12))
    # print("psyScore: " + str(psyScore) + " avg: " + str(psychometricAVGESC[sec - 1])+"\n"+"bagrutScore: " + str(bagrutScore) + " avg: " + str(bagrutAVGESC[sec - 1])) # for debug
    return psyScore, bagrutScore


# run generate applicants and insert them into neo4j
# when clean is true it will delete all existing applicants first then generate new ones
# when clean is true it will export the currently generated create applicant queries into a text file
# quantity indicate how many applicants to add
def createApplicants(clean,export,quantity):
    learnPath.write_Query("match(c: Class)  where(c.PsychometricMinimum = '') set c.PsychometricMinimum = null")
    learnPath.write_Query("match (c:Class)  where(c.BagrutMinimum='') set c.BagrutMinimum=null")
    global queriesString
    if clean == True:
        learnPath.write_Query("MATCH (a:Applicant) detach delete a")
    for i in range(quantity):  # range indicate number of applicants
        applicantQuery = generateCypherCreateApplicant()  # create the students
        learnPath.write_Query(applicantQuery)
        queriesString = queriesString + applicantQuery
    if export == True:
        f = open("Cypher.txt", "w")  #"a" - Append - will append to the end of the file, "w" - Write - will overwrite any existing content
        print("Generated applicant queries:\n" + queriesString)
        f.write(queriesString) # write applicant queries to text file
        f.close()
    print('Done creating applicants')


# create Accepted_To relation between applicants and classes according to bagrut/psychometric scores
# when clean is true it will delete all existing Accepted_To, used to prevent duplicate relations
# quantity is how many classes will the applicant try to get into
def connectApplicants(clean,quantity):
    if clean == True:
        learnPath.write_Query("MATCH p=()-[r:Accepted_To]->() detach delete r")
    print("All current applicants: ")
    applicants = learnPath.getAllApplicants()
    for applicant in applicants:
        print("\napplicant: ")
        print(applicant)  # all the nodes info
        print("random class/es: ")
        if str(applicant["Faculty"]) == '':
            print("\napplicant has no faculty ")
            continue
        res = learnPath.read_findClassFromFaculty(str(applicant["Faculty"]))
        for i in range(quantity):
            rndClass = random.choice(res)  # choose a random node from the result array
            print(rndClass)  # all the node info
            print(rndClass["PsychometricMinimum"])
            if str(rndClass["PsychometricMinimum"]) == 'None':
                print("no PsychometricMinimum req")
            else:
                if float(applicant["Psychometric"]) > float(rndClass["PsychometricMinimum"]):
                    print("accepted, Psychometric:" + str(applicant["Psychometric"]) + " > minimum:" + str(rndClass["PsychometricMinimum"]) + "")
                    learnPath.write_matchApplicantToClass(str(applicant.id), str(rndClass.id))
                    continue
                else:
                    print("not accepted by psychometric")

            if str(rndClass["BagrutMinimum"]) == 'None':
                print("no BagrutMinimum req")
            else:
                if float(applicant["Bagrut"]) > float(rndClass["BagrutMinimum"]):
                    print("accepted, Bagrut:" + str(applicant["Bagrut"]) + " > minimum:" + str(rndClass["BagrutMinimum"]) + "")
                    learnPath.write_matchApplicantToClass(str(applicant.id), str(rndClass.id))
                    continue
                else:
                    print("not accepted by bagrut")
            # various ways to access result information:
            # rndClass.id # get node id
            # rndClass.keys() # get node attributes
            # rndClass.values() # get node attributes value
    print('Done connecting applicants')


# create an example friend connection
def friendDemo():
    # two example applicants with a friend connection (one with a connection to a degree and one without)
    learnPath.write_Query("MATCH (a:Applicant{Name: 'Shaked Wagner'})MATCH (b:Applicant{Name: 'Or Nagar'})MATCH (c:Applicant{Name: 'Harry Potter'})MATCH (d:Applicant{Name: 'Tom Riddle'})  DETACH DELETE a,b,c,d") # to prevent duplicates
    learnPath.write_Query("CREATE(a: Applicant{Name: 'Shaked Wagner', Gender: 'Male', Bagrut: 120, Psychometric: 800, Area: 'Center', Faculty: 'Engineering',Degree: 'Computer Engineering'})")
    learnPath.write_Query("CREATE(a: Applicant{Name: 'Or Nagar', Gender: 'Male', Bagrut: 102, Area: 'Center', Faculty: '', Degree: ''})")
    learnPath.write_Query("CREATE(a: Applicant{Name: 'Harry Potter', Gender: 'Male', Bagrut: 100, Psychometric: 700, Area: 'North', Faculty: 'Engineering',Degree: 'Computer Engineering'})")
    learnPath.write_Query("CREATE(a: Applicant{Name: 'Tom Riddle', Gender: 'Male',Bagrut: 80, Psychometric: 750, Area: 'North', Faculty: 'Engineering',Degree: 'Computer Science'})")
    learnPath.write_Query("MATCH (a:Applicant{Name: 'Shaked Wagner'})MATCH(c:Class{Name: 'Computer Engineering',ID:'5'})MERGE(a)-[r:Accepted_To]->(c)")
    learnPath.write_Query("MATCH (a:Applicant{Name: 'Harry Potter'})MATCH(c:Class{Name: 'Computer Engineering',ID:'5'})MERGE(a)-[r:Accepted_To]->(c)")
    learnPath.write_Query("MATCH (a:Applicant{Name: 'Tom Riddle'})MATCH(c:Class{Name: 'Computer Science',ID:'5'})MERGE(a)-[r:Accepted_To]->(c)")
    learnPath.write_Query("MATCH(a: Applicant{Name: 'Or Nagar'}),(a2:Applicant{Name:'Shaked Wagner'})merge(a)-[f:Friend]-(a2)")
    learnPath.write_Query("MATCH(a: Applicant{Name: 'Or Nagar'}),(a2:Applicant{Name:'Harry Potter'})merge(a)-[f:Friend]-(a2)")
    learnPath.write_Query("MATCH(a: Applicant{Name: 'Or Nagar'}),(a2:Applicant{Name:'Tom Riddle'})merge(a)-[f:Friend]-(a2)")
    learnPath.write_Query("MATCH(a: Applicant{Name: 'Harry Potter'}),(a2:Applicant{Name:'Tom Riddle'})merge(a)-[f:Friend]-(a2)")

# make randomized friend connections by location and institution and a few completely random
def simulateFriends():
    learnPath.write_Query("MATCH p=()-[r:Friend]->() DETACH DELETE r") # to prevent duplicates

    print('connecting friends by same location')
    # add random friends that are from the same areas
    for location in locations:
        applicantsL = learnPath.getApplicantsInSameArea(location)
        random.shuffle(applicantsL)  # shuffles the id's to randomize
        for i in range(0,int(len(applicantsL)/4),2): # make some portion of them friends, jumps of two
            learnPath.newFriends(str(applicantsL[i][0]), str(applicantsL[i+1][0]),"location")

    # add random friends that go to the same faculty of the same institution
    print('connecting friends by same faculty')
    applicantsF = learnPath.getApplicantsInSameFaculty()
    applicantsSample = random.sample(applicantsF,int((len(applicantsF))/10)) # take random pairs of students
    for i in range(len(applicantsSample)):
        learnPath.newFriends(str(applicantsSample[i][0]),str(applicantsSample[i][1]),"faculty")

    # add randomized friends
    print('connecting randomized friends')
    applicantsR = learnPath.write_getAllQuery("Applicant")
    random.shuffle(applicantsR) # take random pairs of students
    for i in range(0,int(len(applicantsR)/10),2):
        learnPath.newFriends(str(applicantsR[i].id), str(applicantsR[i+1].id), "rand")

    friendDemo()
    print('Done connecting friends')
    # MATCH (a:Applicant)-[r:Friend]->(a2:Applicant) RETURN a.Name as Applicant, count(distinct r) as num_of_friends ORDER BY num_of_friends DESC  # check number of friends


# connect similar nodes
def connectSimilars():
    learnPath.write_Query("MATCH p=()-[r:Similar]->() detach delete r")  # delete current (to prevent duplicate)

    similarList = ["Engineering", "Chemistry", "Food", "Physics", "Civil", "Geo", "Computer", "Math", "Stat", "Israel"]
    for str in similarList:
        learnPath.write_similarNodes(str, str, str)
    # Health tag
    HealthSimilarList = ["Health", "physiotherapy", "Nutrition", "Communication Disorders", "Brain", "Cognit", "nurs",
                         "Med", "pharm", "Disorder", "dent", "Therapy", "diet"]
    # Economy tag
    EconomySimilarList = ["Industr", "Manag", "Econom", "Business", "account"]
    # Build tag
    BuildSimilarList = ["Architecture", "Build", "Civil"]

    # Biology tag
    BiologySimilarList = ["Bio", "Life"]

    # Natural tag (Natural Science)
    NaturalSimilarList = ["Bio", "Life", "Physics", "Chemistry","Earth", "astronomy", "Natural"]

    # Social tag
    SocialSimilarList = ["psychology", "philosophy", "soci", "human", "communication"]

    # History tag
    HistorySimilarList= ["History", "Bible", "Archeology", "Ancient", "Anthropology", "Middle East", "Israel"]

    # Culture tag
    CultureSimilarList = ["Literature", "Hebrew", "Language", "Linguistics", "English", "Art"]

    # Earth tag
    EarthSimilarList = ["geography", "geology", "earth", "environment"]

    # list of the tag lists
    tagList = [HealthSimilarList, EconomySimilarList, BuildSimilarList, BiologySimilarList, NaturalSimilarList, SocialSimilarList, HistorySimilarList, CultureSimilarList, EarthSimilarList]
    # list of the tag names
    tagNames = ["Health", "Economy", "Build", "Biology", "Natural", "Social", "History", "Culture", "Earth"]

    # connect similar nodes for all tags
    for i, list in enumerate(tagList):
        similarTagList(list, tagNames[i])
    print('Done connecting similars')

# connect similar nodes to the given Tag
# similarList is the list of relevant key strings for this tag
# Tag is the desired similar relation tag
def similarTagList(similarList, Tag):
    i = len(similarList)
    for str1 in range(i):  # connect each string in the list to the others
        j = 0
        i = i - 1
        for str2 in range(i):
            learnPath.write_similarNodes(similarList[i], similarList[j], Tag)
            j = j + 1


# main function for initializing the database
def initConnections():
    # generate and connect the applicants
    createApplicants(True, False, 300)
    connectApplicants(True, 1)
    simulateFriends()
    connectSimilars()


if __name__ == '__main__':
    print('Learn Path. Welcome.')
    learnPath = connect.connection("bolt://localhost:7687", "neo4j", "1234")  # connect to database
    #initConnections()  # can run only once
    learnPath.close()  # close the connection to the database

    # GUI #
    app = GUI.App()


# function for initiating The functions that were selected in GUI
    def init_event():
        if app.check_box_1.get() == 1:  # Create
            if (app.entry.get().count(" ") == 0 or app.entry.get() == "") and app.entry.get() != "" and app.entry.get().count(".") == 0:
                try:
                    num = int(app.entry.get())
                    if num > -1:
                        app.button_1.configure(text="Wait")
                        app.button_1.configure(state=DISABLED)
                        # destroy entry3 if it exists
                        if app.entry3.winfo_exists() == 1:
                            app.entry3.destroy()
                        # num >-1 and deleting
                        if app.check_box_info1.get() == 1 and app.check_box_info2.get() == 1:  # Delete and Export to File
                            # run createApplicants
                            createApplicants(True, True, num)
                            app.button_1.configure(state=NORMAL)
                            app.button_1.configure(text="Run Init")
                        # num > -1 and not deleting
                        elif app.check_box_info1.get() == 1 and app.check_box_info2.get() == 0:  # Delete Existing only
                            # run createApplicants
                            createApplicants(True, False, num)
                            app.button_1.configure(state=NORMAL)
                            app.button_1.configure(text="Run Init")
                        elif app.check_box_info1.get() == 1 and app.check_box_info2.get() == 0:  # Export to file only
                            # run createApplicants
                            createApplicants(False, True, num)
                            app.button_1.configure(state=NORMAL)
                            app.button_1.configure(text="Run Init")
                        # no delete and no export
                        else:
                            # run createApplicants
                            createApplicants(False, False, num)
                            app.button_1.configure(state=NORMAL)
                            app.button_1.configure(text="Run Init")
                    # invalid input(num<-1)
                    else:
                        app.entry3Fun()
                # Not an integer
                except ValueError:
                    app.entry3Fun()

            # invalid input(spaces/empty string)
            else:
                app.entry3Fun()

        if app.check_box_2.get() == 1:  # Connect Applicants
            # check if input is valid (no spaces, no empty input, no "." input)
            if (app.entry2.get().count(" ") == 0 or app.entry2.get() == "") and app.entry2.get() != "" and app.entry2.get().count(".") == 0:
                try:
                    num = int(app.entry2.get())
                    if num > -1:
                        app.button_1.configure(text="Wait")
                        app.button_1.configure(state=DISABLED)
                        # destroy entry3 if it exists
                        if app.entry4.winfo_exists() == 1:
                            app.entry4.destroy()
                        # num >-1 and deleting
                        if app.check_box_info3.get() == 1:  # Delete Existing
                            # run connectApplicants
                            connectApplicants(True, num)
                            app.button_1.configure(state=NORMAL)
                            app.button_1.configure(text="Run Init")
                        else:
                            # num > -1 and not deleting
                            # run connectApplicants
                            connectApplicants(False, num)
                            app.button_1.configure(state=NORMAL)
                            app.button_1.configure(text="Run Init")

                    else:
                        # invalid input(num<-1)
                        app.entry4Fun()
                except ValueError:
                    # Not an integer
                    app.entry4Fun()

            else:
                # invalid input(spaces/empty string)
                app.entry4Fun()

        if app.check_box_3.get() == 1:
            print("run simulateFriends")
            app.button_1.configure(text="Wait")
            app.button_1.configure(state=DISABLED)
            simulateFriends()
            app.button_1.configure(state=NORMAL)
            app.button_1.configure(text="Run Init")

        if app.check_box_4.get() == 1:
            print("run connectSimilars")
            app.button_1.configure(text="Wait")
            app.button_1.configure(state=DISABLED)
            connectSimilars()
            app.button_1.configure(state=NORMAL)
            app.button_1.configure(text="Run Init")


# function for starting flask webapp
    def app_event():
        flaskapp.app.run()  # app.run(debug=True) for debugging

    # threads #

    # create thread function for init_event function
    def init_thread_function():
        # create a new instance of the thread with the same configuration
        init_event_thread = threading.Thread(target=init_event)

        # check if thread is alive
        if not init_event_thread.is_alive():
            # print(init_event_thread.is_alive())
            init_event_thread.start()


    # create thread function for app_event function
    def app_thread_function():
        # create a new instance of the thread with the same configuration
        app_event_thread = threading.Thread(target=app_event)

        # check if thread is alive
        if not app_event_thread.is_alive():
            # print(app_event_thread.is_alive())
            app_event_thread.start()


    # assign functions to buttons in GUI
    app.button_1.command = init_thread_function
    app.button_2.command = app_thread_function

    app.start()
