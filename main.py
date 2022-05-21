import random
import names
import numpy as np
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
"""

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def generateCypherCreate():
    global queriesString
    index=1
    for i in range(8):
        random_gender = random.choices(['female', 'male'], [GirltoBoyRatio, 1 - GirltoBoyRatio])
        random_SocioEconomicCluster = random.choices([1,2,3,4,5,6,7,8,9,10],[5,5,12,12,9,9,13,13,11,11],k=1)
        faculty = getRandomFacultyBySEC(random_SocioEconomicCluster[0])
        random_psyScore, random_bagrutScore = getRandomScore(random_SocioEconomicCluster[0])
        random_area = random.choices(locations)

        queriesString = queriesString + "CREATE (applicant"+str(index)+":Applicant Name:'"+names.get_full_name(gender=random_gender[0])+"' ,Gender:'"+random_gender[0]+"' ,Bagrut: '"+str(random_bagrutScore)+"', Psychometric: '"+str(random_psyScore)+"', Area: '"+random_area[0]+"', Degree: '"+faculty+"')\n" #, isAccepted: "+random_isAccepted+" , hobby: '', ethnicity: ''
        index += 1

#sec- social economic cluster 1 to 10
def getRandomFacultyBySEC(sec):
    faculties =  ['Social Sciences', 'Engineering and architecture', 'Education', 'Economics and Business Administration',
             'Math', 'Computer Science', 'Medicine', 'Law', 'Agriculture', 'Art', 'Social sciences', 'Exact Science', 'Humanities', 'Medicine']
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
        psyScore = round(random.gauss(pychometricAVGESC[sec-1], 200 / 2.5)) #get a round score according to gaus disterbution of a score mean of the socialEconomic Cluster
    while bagrutScore <= 60 or bagrutScore >= 120:
        bagrutScore = round(random.gauss(bagrutAVGESC[sec - 1], 200 / 4))
    return psyScore, bagrutScore

if __name__ == '__main__':
    print_hi('Learn Path. Welcome good sir.')
    f = open("Cypher.txt", "w")  #"a" - Append - will append to the end of the file, "w" - Write - will overwrite any existing content
    generateCypherCreate()
    print("query:\n"+queriesString)
    f.write(queriesString)
    f.close()


