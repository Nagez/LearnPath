import random
import names
import connect

queriesString = "" #global string to print to the file

#statistic globals in precentage
GirltoBoyRatio = 0.58
#pychometricAVG according to EconomicSocialCluster 1 -> 10 (psychometric score is between 200 to 800)
pychometricAVGESC = [432,516,540,527,555,566,584,610,624,640]
bagrutAVGESC = [80,85,90,90,95,100,105,105,110,115]
locations = ['South','Center','North','Jersualem']

"""
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

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def generateCypherCreateApplicant():
    random_gender = random.choices(['female', 'male'], [GirltoBoyRatio, 1 - GirltoBoyRatio])
    random_SocioEconomicCluster = random.choices([1,2,3,4,5,6,7,8,9,10],[5,5,12,12,9,9,13,13,11,11],k=1)
    faculty = getRandomFacultyBySEC(random_SocioEconomicCluster[0])
    random_psyScore, random_bagrutScore = getRandomScore(random_SocioEconomicCluster[0])
    random_area = random.choices(locations)
    applicantQuery = "CREATE (a:Applicant{Name:'"+names.get_full_name(gender=random_gender[0])+"' ,Gender:'"+random_gender[0]+"' ,Bagrut: '"+str(random_bagrutScore)+"', Psychometric: '"+str(random_psyScore)+"', Area: '"+random_area[0]+"', Faculty: '"+faculty+"', Degree: ''})\n" #, isAccepted: "+random_isAccepted+" , hobby: '', ethnicity: ''
    return applicantQuery


#sec- social economic cluster 1 to 10
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

def getRandomScore(sec):
    bagrutScore = 1 # placeholder init
    psyScore = 1
    while psyScore <= 200 or psyScore >= 800:
        psyScore = round(random.gauss(pychometricAVGESC[sec-1], 200 / 3)) #get a round score according to gaussian distribution of a score mean of the socialEconomic Cluster
    while bagrutScore <= 60 or bagrutScore >= 120:
        bagrutScore = round(random.gauss(bagrutAVGESC[sec - 1], 200 / 12))
    # print("psyScore: " + str(psyScore) + " avg: " + str(pychometricAVGESC[sec - 1])+"\n"+"bagrutScore: " + str(bagrutScore) + " avg: " + str(bagrutAVGESC[sec - 1]))
    return psyScore, bagrutScore

# run generate applicants and insert them into neo
# when is clean true it will delete all existing applicants first then generate new ones
def createApplicants(clean,quantity):
    global queriesString
    if clean == True:
        learnPath.write_Query("MATCH (a:Applicant) detach delete a")
    for i in range(quantity):  # range indicate number of applicants
        applicantQuery = generateCypherCreateApplicant()  # create the students
        learnPath.write_Query(applicantQuery)
        queriesString = queriesString + applicantQuery

# create Accepted_To relation between applicants and classes according to bagrut/psychometric scores
# quantity is how many classes will the applicant try to get into
def connectApplicants(quantity):
    print("All current applicants: ")
    applicants = learnPath.getAllApplicants()
    for applicant in applicants:
        print("\napplicant: ")
        print(applicant)  # all the nodes info
        print("random class/es: ")
        res = learnPath.read_findClassFromFaculty(str(applicant["Faculty"]))
        # various ways to access result information
        for i in range(quantity):
            rndClass = random.choice(res)  # choose a random node from the result array
            print(rndClass)  # all the node info

            if str(rndClass["PsychometricMinimum"]) == '':
                print("no PsychometricMinimum req")
            else:
                if float(applicant["Psychometric"]) > float(rndClass["PsychometricMinimum"]):
                    print("accepted, Psychometric:" + applicant["Psychometric"] + " > minimum:" + rndClass["PsychometricMinimum"] + "")
                    learnPath.write_matchApplicantToClass(str(applicant.id), str(rndClass.id))
                    continue
                else:
                    print("not accepted by psychometric")

            if str(rndClass["BagrutMinimum"]) == '':
                print("no BagrutMinimum req")
            else:
                if float(applicant["Bagrut"]) > float(rndClass["BagrutMinimum"]):
                    print("accepted, Bagrut:" + applicant["Bagrut"] + " > minimum:" + rndClass["BagrutMinimum"] + "")
                    learnPath.write_matchApplicantToClass(str(applicant.id), str(rndClass.id))
                    continue
                else:
                    print("not accepted by bagrut")
            # print(rndClass.id) # get node id
            # print(rndClass.keys()) # get node attributes
            # print(rndClass.values()) # get node attributes value


if __name__ == '__main__':
    print_hi('Learn Path. Welcome good sir.')
    f = open("Cypher.txt", "w")  #"a" - Append - will append to the end of the file, "w" - Write - will overwrite any existing content
    learnPath = connect.connection("bolt://localhost:7687", "neo4j", "1234") # connect to database

    # get all faculties
    faculties = learnPath.write_getAllQuery("Faculty")
    #print("Faculties list: ")
    #for faculty in faculties:
    #    print(faculty["Name"])

    # get all classes
    classes = learnPath.write_getAllQuery("Class")
    #print("Classes list: ")
    #for _class in classes:
    #    print(_class["Name"])

    # generate and connect the applicants
    createApplicants(True,200)
    connectApplicants(1)

    # print("query:\n" + queriesString)
    f.write(queriesString) # write applicant queries to text file
    f.close()
    learnPath.close()

