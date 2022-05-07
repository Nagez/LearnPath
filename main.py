import random

queriesString = "" #global string to print to the file

#statistic globals in precentage
GirltoBoyRatio = 0.58
# student by field ratio (total 100%)
SFR_Humanities = 0.229
SFR_SocialSciences = 0.288
SFR_Law = 0.07
SFR_Medicine = 0.077
SFR_Math = 0.139
SFR_Agriculture = 0.06
SFR_EngineeringAndArchitecture = 0.191
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

"""
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
    for name in ["Alice", "Bob", "Carol"]:
        random_gender = random.choices(["female", "male"], [GirltoBoyRatio, 1 - GirltoBoyRatio])
        random_degree = random.choices(["Humanities", 'SocialSciences', 'Law', 'Math', 'Social sciences', 'agriculture',
                                        'Engineering and architecture'],
                                       [SFR_Humanities, SFR_SocialSciences, SFR_Law, SFR_Medicine, SFR_Math,
                                        SFR_Agriculture, SFR_EngineeringAndArchitecture],k=1)

        queriesString = queriesString + "CREATE (student"+str(index)+":Student Name:"+name+" ,Gender:"+random_gender[0]+" ,Bagrut: '', Psychometric: '', residence: '', hobby: '', ethnicity: '', Degree: "+random_degree[0]+")\n" #, isAccepted: "+random_isAccepted+"
        index += 1

if __name__ == '__main__':
    print_hi('Learn Path git. Welcome good sir.')
    f = open("Cypher.txt", "w")  #"a" - Append - will append to the end of the file, "w" - Write - will overwrite any existing content
    generateCypherCreate()
    print("query:\n"+queriesString)
    f.write(queriesString)
    f.close()


