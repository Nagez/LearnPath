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
AAR_Humanities = 1.4
AAR_LanguagesLiteraturesAndRegionalStudies = 1.7
AAR_EducationAndTeacherTraining = 1.6
AAR_Arts = 1.6
AAR_SocialSciences = 1.6
AAR_BusinessAndManagement = 1.5
AAR_Law = 2.4
AAR_Medicine = 4.4
AAR_ParaMedicalStudies = 2.3
AAR_MathematicsStatisticsAndComputerSciences = 1.8
AAR_PhysicalSciences = 1.5
AAR_BiologicalSciences = 1.7
AAR_Agriculture = 1.3
AAR_EngineeringAndArchitecture = 2


#random_number = random.choices(['female', 'male'], [GirltoBoyRatio,100-GirltoBoyRatio])
#random_number = random.choices(['accepted', 'rejected'], [SFR_SocialSciences,100-SFR_SocialSciences])
#random_number = random.choices(['accepted', 'rejected'], [SFR_SocialSciences,100-SFR_SocialSciences])

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


