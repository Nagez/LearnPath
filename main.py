import random
import names
import connect
import flaskapp
import GUI

queriesString = ""  # global string to print to the file

# statistic globals in percentage
GirltoBoyRatio = 0.58
# pychometricAVG according to EconomicSocialCluster 1 -> 10 (psychometric score is between 200 to 800)
pychometricAVGESC = [432,516,540,527,555,566,584,610,624,640]
bagrutAVGESC = [80,85,90,90,95,100,105,105,110,115]
locations = ['South','Center','North','Jersualem']

"""
# old unsused ratios 

# student by field ratio (total 100%)
SFR_Humanities = 0.229
SFR_SocialSciences = 0.288
SFR_Law = 0.07
SFR_Medicine = 0.077
SFR_Math = 0.139
SFR_Agriculture = 0.06
SFR_EngineeringAndArchitecture = 0.191

random_degree = random.choices(["Humanities", 'SocialSciences', 'Law', 'Math', 'Social sciences', 'Agriculture',
                                'Engineering and architecture'],
                               [SFR_Humanities, SFR_SocialSciences, SFR_Law, SFR_Medicine, SFR_Math,
                                SFR_Agriculture, SFR_EngineeringAndArchitecture],k=1)

# applicant to accepted ratio
AAR_Humanities = 0.014
AAR_LanguagesLiteraturesAndRegionalStudies = 0.017
AAR_EducationAndTeacherTraining = 0.016
AAR_Arts = 0.016
AAR_SocialSciences = 0.016
AAR_BusinessAndManagement = 0.015
AAR_Law = 0.024
AAR_Medicine = 0.044
AAR_ParaMedicalStudies = 0.023
AAR_MathematicsStatisticsAndComputerSciences = 0.018
AAR_PhysicalSciences = 0.015
AAR_BiologicalSciences = 0.017
AAR_Agriculture = 0.013
AAR_EngineeringAndArchitecture = 0.02

print(random.randrange(1, 20, 1))
 random_isAccepted = random.choices(
            ['Humanities', 'LanguagesLiteraturesAndRegionalStudies', 'EducationAndTeacherTraining',
             'Arts,SocialSciences',
             'BusinessAndManagement', 'Law,Medicine', 'ParaMedicalStudies', 'MathematicsStatisticsAndComputerSciences',
             'PhysicalSciences', 'BiologicalSciences', 'Agriculture', 'EngineeringAndArchitecture'],
            weight = [AAR_Humanities, AAR_LanguagesLiteraturesAndRegionalStudies, AAR_EducationAndTeacherTraining, AAR_Arts,
             AAR_SocialSciences, AAR_BusinessAndManagement,
             AAR_Law, AAR_Medicine, AAR_ParaMedicalStudies, AAR_MathematicsStatisticsAndComputerSciences,
             AAR_PhysicalSciences, AAR_BiologicalSciences,
             AAR_Agriculture, AAR_EngineeringAndArchitecture], k=1)
             
 match(f:Faculty{Name:'Comupter science',ID:'1'}),(c:Class{Name:'math and comupter science',ID:'1'}) create(c)-[of:Offered_In]->(f);
"""

# generate a create applicant query using the statistics
def generateCypherCreateApplicant():
    random_gender = random.choices(['female', 'male'], [GirltoBoyRatio, 1 - GirltoBoyRatio])
    random_SocioEconomicCluster = random.choices([1,2,3,4,5,6,7,8,9,10],[5,5,12,12,9,9,13,13,11,11],k=1)
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
        psyScore = round(random.gauss(pychometricAVGESC[sec-1], 200 / 3))  # get a round score according to gaussian distribution of a score mean of the socialEconomic Cluster
    while bagrutScore <= 60 or bagrutScore >= 120:
        bagrutScore = round(random.gauss(bagrutAVGESC[sec - 1], 200 / 12))
    # print("psyScore: " + str(psyScore) + " avg: " + str(pychometricAVGESC[sec - 1])+"\n"+"bagrutScore: " + str(bagrutScore) + " avg: " + str(bagrutAVGESC[sec - 1]))
    return psyScore, bagrutScore


# run generate applicants and insert them into neo4j
# when clean is true it will delete all existing applicants first then generate new ones
# when clean is true it will export the currently generated create applicant queries into a text file
# quantity indicate how many applicants to add
def createApplicants(clean,export,quantity):
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

            if str(rndClass["PsychometricMinimum"]) == '':
                print("no PsychometricMinimum req")
            else:
                if float(applicant["Psychometric"]) > float(rndClass["PsychometricMinimum"]):
                    print("accepted, Psychometric:" + str(applicant["Psychometric"]) + " > minimum:" + str(rndClass["PsychometricMinimum"]) + "")
                    learnPath.write_matchApplicantToClass(str(applicant.id), str(rndClass.id))
                    continue
                else:
                    print("not accepted by psychometric")

            if str(rndClass["BagrutMinimum"]) == '':
                print("no BagrutMinimum req")
            else:
                if float(applicant["Bagrut"]) > float(rndClass["BagrutMinimum"]):
                    print("accepted, Bagrut:" + str(applicant["Bagrut"]) + " > minimum:" + str(rndClass["BagrutMinimum"]) + "")
                    learnPath.write_matchApplicantToClass(str(applicant.id), str(rndClass.id))
                    continue
                else:
                    print("not accepted by bagrut")
            # various ways to access result information:
            # print(rndClass.id) # get node id
            # print(rndClass.keys()) # get node attributes
            # print(rndClass.values()) # get node attributes value


# create an example friend connection
def friendDemo():
    # two example applicants with a friend connection (one with a connection to a degree and one without)
    learnPath.write_Query("MATCH (a:Applicant{Name: 'Shaked Wagner'})MATCH (b:Applicant{Name: 'Or Nagar'}) DETACH DELETE a,b") # to prevent duplicates
    learnPath.write_Query("CREATE(a: Applicant{Name: 'Shaked Wagner', Gender: 'Male', Bagrut: 120, Psychometric: 800, Area: 'Center', Faculty: 'Engineering',Degree: 'Computer Engineering'})")
    learnPath.write_Query("CREATE(a: Applicant{Name: 'Or Nagar', Gender: 'Male', Bagrut: 102, Psychometric: '', Area: 'Center', Faculty: '', Degree: ''})")
    learnPath.write_Query("MATCH (a:Applicant{Name: 'Shaked Wagner'})MATCH(c:Class{Name: 'Computer Engineering',ID:'5'})MERGE(a)-[r:Accepted_To]->(c)")
    learnPath.write_Query("MATCH(a: Applicant{Name: 'Or Nagar'}),(a2:Applicant{Name:'Shaked Wagner'})merge(a)-[f:Friend]-(a2)")


# connect similar nodes
def connectSimilars():
    learnPath.write_Query("MATCH p=()-[r:Similar]->() detach delete r")  # delete current (to prevent duplicate)

    similarList = ["Engineering", "Chemistry", "Food", "Physics", "Civil", "Geo", "Computer", "Math", "Stat"]
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
    NaturalSimilarList = ["Bio", "Life", "Physics", "Chemistry","Earth", "astronomy"]

    """
    #
    SocialScienceSimilarList = ["Anthropology", "Area studies", "Business", "Civics", "Communication", "Criminology", "Demography", "Development",
                                "Economics", "Education", "Environmental", "Folkloristics", "Gender", "Geography", "History", "Industrial relations",
                                "Information", "International relations", "Law", "Library", "Linguistics", "Media", "Political", "Psychology",
                                "Public administration", "Sociology", "Social work", "Sustainable development"]
    """

    # list of the tag lists
    tagList = [HealthSimilarList, EconomySimilarList, BuildSimilarList, BiologySimilarList, NaturalSimilarList]
    # list of the tag names
    tagNames = ["Health", "Economy", "Build", "Biology", "Natural"]

    # connect similar nodes for all tags
    for i, list in enumerate(tagList):
        similarTagList(list, tagNames[i])


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
    createApplicants(True, False, 200)
    connectApplicants(True, 1)
    friendDemo()
    connectSimilars()


if __name__ == '__main__':
    print('Learn Path. Welcome.')
    learnPath = connect.connection("bolt://localhost:7687", "neo4j", "1234") # connect to database
    #initConnections()  # can run only once

    # get all faculties
    # faculties = learnPath.write_getAllQuery("Faculty")
    # print("Faculties list: ")
    # for faculty in faculties:22
    #     print(faculty["Name"])

    # get all classes
    # classes = learnPath.write_getAllQuery("Class")
    # print("Classes list: ")
    # for _class in classes:
    #     print(_class["Name"])

    # example to find a degree trough a friend reference
    ApplicantName = 'Or Nagar'
    friendsClasses = learnPath.findMatchTroughFriend(ApplicantName)
    print(""+ApplicantName+" friends Classes ("+str(len(friendsClasses))+"): ")
    for _class in friendsClasses:
        print(_class)

    # example to find a degree using the Similar connection and tags
    availableClasses = learnPath.findMatchTroughName(ApplicantName, 'Computer science')
    print(""+ApplicantName+" available Classes ("+str(len(availableClasses))+"): ")
    for _class in availableClasses:
        print(_class)

    learnPath.close()  # close the connection to the database

    ## GUI ##
    app=GUI.App()

    def Init_event():
        if app.check_box_1.get() == 1: #Create
           # print(1)
            if app.check_box_info1.get()==1:# Delete Existing
                print(1.1)
            if app.check_box_info2.get()==1:# Export to File
                print(1.2)

        if app.check_box_2.get() == 1: # Connect Applicants
            print("")
            if app.check_box_info3.get()==1: #Delete Existing
                print("Connect Applicants: Delete Existing")

        if app.check_box_3.get() == 1:
            print("run friendDemo")
            friendDemo()

        if app.check_box_4.get() == 1:
            print("run connectSimilars")
            connectSimilars()

    def App_event():
        flaskapp.app.run()  # app.run(debug=True) for debugging

    app.button_1.command = Init_event
    app.button_2.command = App_event
    app.start()
