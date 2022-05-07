import random

queriesString = "" #global string to print to the file

#statistic globals in precentage
GirltoBoyRatio = 58
# student by field ratio (total 100%)
SFR_Humanities = 22.9
SFR_SocialSciences = 28.8
SFR_Law = 7
SFR_Medicine = 7.7
SFR_Math = 13.9
SFR_Agriculture = 0.6
SFR_EngineeringAndArchitecture = 19.1
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


#random_number = random.choices(['female', 'male'], [GirltoBoyRatio,100-GirltoBoyRatio])
#random_number = random.choices(['accepted', 'rejected'], [SFR_SocialSciences,100-SFR_SocialSciences])
#random_number = random.choices(['accepted', 'rejected'], [SFR_SocialSciences,100-SFR_SocialSciences])
random_number = random.choices(['Humanities','LanguagesLiteraturesAndRegionalStudies','EducationAndTeacherTraining','Arts,SocialSciences',
                                'BusinessAndManagement','Law,Medicine','ParaMedicalStudies','MathematicsStatisticsAndComputerSciences',
                                'PhysicalSciences','BiologicalSciences','Agriculture','EngineeringAndArchitecture'],
[AAR_Humanities,AAR_LanguagesLiteraturesAndRegionalStudies,AAR_EducationAndTeacherTraining,AAR_Arts,AAR_SocialSciences,AAR_BusinessAndManagement,
AAR_Law,AAR_Medicine,AAR_ParaMedicalStudies,AAR_MathematicsStatisticsAndComputerSciences,AAR_PhysicalSciences,AAR_BiologicalSciences,
AAR_Agriculture,AAR_EngineeringAndArchitecture])


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def generateCypherCreate():
    global queriesString
    for name in ["Alice", "Bob", "Carol"]:
        print(random.randrange(1, 20, 1))
        queriesString = queriesString + "CREATE (student:Student name:"+name+") RETURN student\n"
        #queriesString = queriesString + "CREATE (student:Student name:"+name+") RETURN student\n"

# age bagrut psycometri residence hobby ethnicity
if __name__ == '__main__':
    print_hi('Learn Path git. Welcome good sir.')
    f = open("Cypher.txt", "w")  #"a" - Append - will append to the end of the file, "w" - Write - will overwrite any existing content
    generateCypherCreate()
    print("query:\n"+queriesString)
    f.write(queriesString)
    f.close()


