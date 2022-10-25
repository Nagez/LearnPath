from neo4j import GraphDatabase

class connection:

    # init connection
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    # close connection
    def close(self):
        self.driver.close()

    # return all applicants
    def getAllApplicants(self):
        with self.driver.session() as session:
            result = session.run("MATCH (a:Applicant) RETURN a")  # Query
            return [record["a"] for record in result]

    # return a class connected to a faculty that contain the argument string(faculty) in the faculty name
    def read_findClassFromFaculty(self, faculty):
        with self.driver.session() as session:
            return session.read_transaction(self.__findClassFromFaculty, faculty)
    @staticmethod
    def __findClassFromFaculty(tx, faculty):
        result = tx.run("MATCH(f:Faculty)<-[:Offered_In]-(c:Class)"
                        "WHERE f.Name CONTAINS '"+ faculty +"'"
                        "RETURN c")
        return [record["c"] for record in result]


    # get all faculties of a specific university id
    def getFacultiesFromUni(self, id):
        with self.driver.session() as session:
            return session.read_transaction(self.__getFacultiesFromUni, id)

    @staticmethod
    def __getFacultiesFromUni(tx, id):
        result = tx.run("MATCH(i: Institution)-[w: Within]-(f:Faculty) where ID(i) = "+id+" return f")
        return [record["f"] for record in result]


    # get all classes of a specific faculties id
    def getClassesFromFaculty(self, id):
        with self.driver.session() as session:
            return session.read_transaction(self.__getClassesFromFaculty, id)
    @staticmethod
    def __getClassesFromFaculty(tx, id):
        result = tx.run("MATCH(f: Faculty)-[o: Offered_In]-(c:Class) where ID(f) = " + id + " return c")
        return [record["c"] for record in result]


    # write a query (mainly used to create applicant)
    def write_matchApplicantToClass(self, applicantID, classID):
        with self.driver.session() as session:
            session.write_transaction(self.__matchApplicantToClass, applicantID, classID)

    @staticmethod
    def __matchApplicantToClass(tx, applicantID,classID):
        result = tx.run("MATCH(a:Applicant),(c:Class) "
                        "where id(a)="+applicantID+" and id(c)="+classID+" "
                        "set a.Degree = c.Name CREATE(a)-[ac:Accepted_To]->(c) ")
        return result

# Match algorithms #
    # using an applicant name, find matching class trough his friend connection
    def findMatchTroughFriend(self, Name):
        with self.driver.session() as session:
            return session.read_transaction(self.__findMatchTroughFriend, Name)

    @staticmethod
    def __findMatchTroughFriend(tx, Name):
        str = "MATCH(a: Applicant{Name: '"+Name+"'})-[f:Friend]-(a2)-[r:Accepted_To]->(c:Class)--(:Faculty)--(i:Institution)" \
              " WHERE a.Bagrut>=c.BagrutMinimum or a.Psychometric>=c.PsychometricMinimum" \
              " return distinct c,i,collect(a2.Name) as Friends ,count(f) as Strength order by Strength desc"
        result = tx.run(str)
        print("\nMatch trough friend\n" + str)
        table = []
        for res in result:
            dc = {}
            className = res["c"]["Name"]
            institutionName = res["i"]["Name"]
            friends = res["Friends"]
            strength = res["Strength"]
            dc.update({"Class": className, "Institution": institutionName, "Friends": friends})
            table.append(dc)

        return table


    # match for applicant available classes using a class name search and get classes that contain that name, classes that connected to faculties with that name and similar classes (using applicant Name)
    def findMatchTroughName(self, ApplicantName, className):
        with self.driver.session() as session:
            return session.read_transaction(self.__findMatchTroughName, ApplicantName, className)

    @staticmethod
    def __findMatchTroughName(tx, ApplicantName,className):
        str="MATCH (f:Faculty)-[]-(c:Class) optional match (c)-[Similar]-(c1:Class)"\
            "with c,c1 where (toLower(c.Name) CONTAINS  toLower('"+className+"') or toLower(f.Name) CONTAINS toLower('"+className+"'))"\
            "WITH collect(c)+collect(c1) AS cl unwind cl AS classes MATCH(a: Applicant{Name: '"+ApplicantName+"'})"\
            "MATCH (classes)--(f:Faculty)--(i:Institution)"\
            "RETURN DISTINCT classes, i.Name, classes.BagrutMinimum - a.Bagrut as BagrutDiff, classes.PsychometricMinimum - a.Psychometric as PsychometricDiff order by BagrutDiff"
        print("\nMatch trough name search\n" + str)
        result = tx.run(str)
        table = []
        for res in result:
            dc = {}
            className = res["classes"]["Name"]
            bagrutDiff = res["BagrutDiff"]
            psychometricDiff = res["PsychometricDiff"]
            institution = res["i.Name"]
            dc.update({"Class": className, "Institution":institution, "Bagrut Difference": bagrutDiff, "Psychometric Difference": psychometricDiff})
            table.append(dc)

        return table


    # match for applicant available classes using a class name search and get classes that contain that name, classes that connected to faculties with that name and similar classes (using applicant ID)
    def findMatchIDTroughName(self, ApplicantID, className):
        with self.driver.session() as session:
            return session.read_transaction(self.__findMatchIDTroughName, ApplicantID, className)

    @staticmethod
    def __findMatchIDTroughName(tx, ApplicantID, className):
        str="MATCH (f:Faculty)-[]-(c:Class) optional match (c)-[Similar]-(c1:Class) " \
            "with c,c1 where (toLower(c.Name) CONTAINS  toLower('"+className+"') or toLower(f.Name) CONTAINS toLower('"+className+"'))" \
            " WITH collect(c)+collect(c1) AS cl unwind cl AS classes " \
            "MATCH(a: Applicant) Where id(a)="+ApplicantID+" MATCH (classes)--(f:Faculty)--(i:Institution)  " \
            "RETURN DISTINCT classes, i.Name, classes.BagrutMinimum - a.Bagrut as BagrutDiff, classes.PsychometricMinimum - a.Psychometric as PsychometricDiff order by BagrutDiff"
        print("\nMatch trough name search with applicant ID\n" + str)
        result = tx.run(str)
        table = []
        for res in result:
            dc = {}
            className = res["classes"]["Name"]
            bagrutDiff = res["BagrutDiff"]
            psychometricDiff = res["PsychometricDiff"]
            institution = res["i.Name"]
            dc.update({"Class": className, "Institution": institution, "Bagrut Difference": bagrutDiff, "Psychometric Difference": psychometricDiff})
            table.append(dc)

        return table
        # return [record["classes"] for record in result]


    # recommand by most popular classes in the applicant's location he can apply to
    def findMatchTroughAreaPopularity(self, ApplicantName):
        with self.driver.session() as session:
            return session.read_transaction(self.__findMatchTroughAreaPopularity, ApplicantName)

    @staticmethod
    def __findMatchTroughAreaPopularity(tx, ApplicantName):
        str = "MATCH (i:Institution)-[]-(f:Faculty)-[]-(c:Class)"\
              " optional match (c)<-[r:Accepted_To]-(a1:Applicant)"\
              " with c,i,count(r) as AcceptedQuantity"\
              " match (a:Applicant{Name:'"+ApplicantName+"'})"\
              " where i.Area=a.Area and (a.Bagrut>=c.BagrutMinimum or a.Psychometric>=c.PsychometricMinimum)"\
              " return c,i,AcceptedQuantity order by AcceptedQuantity desc"
        print("\nMatch trough most popular classes in the applicant's location he can apply to\n" + str)
        result = tx.run(str)
        table = []
        for res in result:
            dc = {}
            className = res["c"]["Name"]
            institutionName = res["i"]["Name"]
            acceptedQuantity = res["AcceptedQuantity"]
            dc.update({"Class": className, "Institution": institutionName, "Accepted Quantity": acceptedQuantity})
            table.append(dc)

        return table


    # general recommandation using path lenghts from a friend to a class including similars and friend of friend, can be adjusted to show more
    def findMatchTroughFriendPath(self, ApplicantName,k):
        with self.driver.session() as session:
            return session.read_transaction(self.__findMatchTroughFriendPath, ApplicantName,k)

    @staticmethod
    def __findMatchTroughFriendPath(tx, ApplicantName,k):
        str = "MATCH (a:Applicant{Name:'"+ApplicantName+"'})-[r:Friend]-(a2:Applicant),(c:Class)--()--(i:Institution), path = ((a2)-[*.."+k+"]->(c)) "\
              "RETURN distinct c,i,length(path) as Priority ORDER BY Priority asc"
        print("\nfindMatchTroughFriendPath\n" + str)
        result = tx.run(str)
        table = []
        for res in result:
            dc = {}
            className = res["c"]["Name"]
            institutionName = res["i"]["Name"]
            bagrutMinimum = res["c"]["BagrutMinimum"]
            psychometricMinimum = res["c"]["PsychometricMinimum"]
            priority = res["Priority"]
            dc.update({"Class": className, "Institution": institutionName, "Bagrut Minimum": bagrutMinimum, "Psychometric Minimum": psychometricMinimum, "Priority": priority})
            table.append(dc)

        return table


    # all classes with sufficient score and both null, order by avg scores of accepted applicants
    def findMatchTroughAcceptedAVG(self, ApplicantName):
        with self.driver.session() as session:
            return session.read_transaction(self.__findMatchTroughAcceptedAVG, ApplicantName)

    @staticmethod
    def __findMatchTroughAcceptedAVG(tx, ApplicantName):
        str = "MATCH (i:Institution)-[]-(f:Faculty)-[]-(c:Class)"\
              "optional match (c)<-[r:Accepted_To]-(a1:Applicant)"\
              "match (a:Applicant)"\
              "where a.Name='"+ApplicantName+"' and (a.Bagrut>=c.BagrutMinimum or a.Psychometric>=c.PsychometricMinimum  or (c.PsychometricMinimum is null and c.BagrutMinimum is null))"\
              "return c,i,count(a1) as NumOfAccepted, round(avg(a1.Bagrut),2) as AcceptedApplicantsBagrutAVG, round(avg(a1.Psychometric),2) as AcceptedApplicantsPsychometrictAVG order by AcceptedApplicantsPsychometrictAVG "

        print("\nfindMatchTroughAcceptedAVG\n" + str)
        result = tx.run(str)
        table = []
        for res in result:
            dc = {}
            className = res["c"]["Name"]
            institutionName = res["i"]["Name"]
            numOfAccepted = res["NumOfAccepted"]
            acceptedApplicantsBagrutAVG = res["AcceptedApplicantsBagrutAVG"]
            acceptedApplicantsPsychometrictAVG = res["AcceptedApplicantsPsychometrictAVG"]
            dc.update({"Class": className, "Institution": institutionName, "Number of Accepted": numOfAccepted,
                       "Bagrut Average": acceptedApplicantsBagrutAVG, "Psychometric Average": acceptedApplicantsPsychometrictAVG})
            table.append(dc)

        return table


    # get all of the nodes of type var
    def write_getAllQuery(self, var):
        with self.driver.session() as session:
            return session.write_transaction(self.__write_getAllQuery,var)
    @staticmethod
    def __write_getAllQuery(tx, var):
        result = tx.run("MATCH(v:"+var+")"
                        "RETURN v")
        return [record["v"] for record in result]

    # connect similar nodes
    def write_similarNodes(self,str1,str2, tag):
        with self.driver.session() as session:
            session.write_transaction(self.__write_similarNodes, str1, str2, tag)

    @staticmethod
    def __write_similarNodes(tx, str1,str2, tag):
        result = tx.run("MATCH(c:Class)"
                        "MATCH(c1:Class)"                     
                        "WHERE c.Name CONTAINS '"+str1+"' and c1.Name CONTAINS '"+str2+"' and id(c)<>id(c1)"
                        "MERGE (c)-[:Similar{Tag:'"+tag+"'}]-(c1)")
        return result


    # get a list of all applicants ids that learn in the same faculty at the same institution
    def getApplicantsInSameFaculty(self):
        with self.driver.session() as session:
            return session.read_transaction(self.__getApplicantsInSameFaculty)

    @staticmethod
    def __getApplicantsInSameFaculty(tx):
        result = tx.run("MATCH(a:Applicant)-[r:Accepted_To]-(c:Class)-[o:Offered_In]-(f:Faculty),(a2:Applicant)-[r2:Accepted_To]-(c2:Class)-[o2:Offered_In]-(f2:Faculty)"
                        " where id(f)=id(f2)"
                        " return id(a) as RES, id(a2) as RESS")
        return result.values("RESS","RES")


    # get a list of Most popular classes
    def getMostPopularClasses(self):
        with self.driver.session() as session:
            return session.read_transaction(self.__getMostPopularClasses)

    @staticmethod
    def __getMostPopularClasses(tx):
         str = "MATCH (i:Institution)-[]-(f:Faculty)-[]-(c:Class)<-[r:Accepted_To]-(a:Applicant)" +\
               "RETURN c.Name as ClassName,i.Name as InstitutionName, i.Area as Area, count(distinct r) as NumOfAcceptedApplicants ORDER BY NumOfAcceptedApplicants DESC"
         print(str)
         result = tx.run(str)
         table = []
         for res in result:
             dc = {}
             className = res["ClassName"]
             institutionName = res["InstitutionName"]
             area = res["Area"]
             numOfAcceptedApplicants = res["NumOfAcceptedApplicants"]
             dc.update({"Class":className,"Institution":institutionName,"Area":area,"Amount of Accepted Applicants":numOfAcceptedApplicants})
             table.append(dc)

         return table


    # average score in each faculty in each institution
    def getAverageInFaculties(self):
        with self.driver.session() as session:
            return session.read_transaction(self.__getAverageInFaculties)

    @staticmethod
    def __getAverageInFaculties(tx):
        str = "match (c:Class)-[]-(f:Faculty)-[]-(i:Institution)"+\
              "return i.Name as InstitutionName, f.Name as FacultyName, round(avg(c.BagrutMinimum),2) as AverageBagrutMinimum, round(avg(c.PsychometricMinimum),2) as AveragePsychometricMinimum"
        print(str)
        result = tx.run(str)
        table = []
        for res in result:
            dc = {}
            institutionName = res["InstitutionName"]
            facultyName = res["FacultyName"]
            avgB = res["AverageBagrutMinimum"]
            avgP = res["AveragePsychometricMinimum"]
            dc.update({"Institution": institutionName, "Faculty": facultyName,  "Average Bagrut Minimum": avgB,  "Average Psychometric Minimum": avgP})
            table.append(dc)

        return table


    # average score in similar classes
    def getAverageInSimilar(self):
        with self.driver.session() as session:
            return session.read_transaction(self.__getAverageInSimilar)

    @staticmethod
    def __getAverageInSimilar(tx):
        str = "match (c:Class)-[r:Similar]-(c1:Class) with r.Tag as tag ,collect(distinct c) as nodes unwind nodes as classes " +\
              "return round(avg(classes.BagrutMinimum),2) as AverageBagrutMinimum, round(avg(classes.PsychometricMinimum),2) as AveragePsychometricMinimum, count(classes) as ClassesQuantity, tag as Tag order by AverageBagrutMinimum desc"
        print(str)
        result = tx.run(str)
        table = []
        for res in result:
            dc = {}
            avgB = res["AverageBagrutMinimum"]
            avgP = res["AveragePsychometricMinimum"]
            classesQuantity = res["ClassesQuantity"]
            tag = res["Tag"]
            dc.update({"Average Bagrut Minimum": avgB, "Average Psychometric Minimum": avgP, "Classes Quantity": classesQuantity, "Tag": tag})
            table.append(dc)

        return table


    # percentage of accepted in each area
    def getAcceptedInAreaPercent(self):
        with self.driver.session() as session:
            return session.read_transaction(self.__getAcceptedInAreaPercent)

    @staticmethod
    def __getAcceptedInAreaPercent(tx):
        result = tx.run("match (a:Applicant)-[r:Accepted_To]->(c:Class) with count(a) as total"
                        " match (a:Applicant)-[r:Accepted_To]->(c:Class)"
                        " return a.Area as Area ,count(a) as QuantityOfAcceptedApplicants ,round(((toFloat(count(a))/total)*100),2) as Percent order by Percent desc")
        table = []
        for res in result:
            dc = {}
            area = res["Area"]
            quantityOfAcceptedApplicants = res["QuantityOfAcceptedApplicants"]
            percent = res["Percent"]
            dc.update({"Area": area, "Quantity Of Accepted Applicants": quantityOfAcceptedApplicants, "Percent": percent})
            table.append(dc)

        return table


    # get a list of all applicants ids that learn in the same faculty at the same institution
    def getApplicantsInSameArea(self,location):
        with self.driver.session() as session:
            return session.read_transaction(self.__getApplicantsInSameArea,location)

    @staticmethod
    def __getApplicantsInSameArea(tx,location):
        result = tx.run("MATCH(a:Applicant{Area:'"+location+"'}) return id(a) AS applicantID")
        return result.values("applicantID")


    # friend relation between two applicants using their ids
    def newFriends(self,id1,id2,tag):
        with self.driver.session() as session:
            return session.write_transaction(self.__newFriends,id1,id2,tag)

    @staticmethod
    def __newFriends(tx,id1,id2,tag):
        str="MATCH (a:Applicant),(a2:Applicant) WHERE id(a)="+id1+" and id(a2)="+id2+" merge(a)-[f:Friend{Tag:'"+tag+"'}]-(a2)"
        # print(str)
        result = tx.run(str)
        return result


    # general write query (mainly used to create applicant)
    def write_Query(self, query):
        with self.driver.session() as session:
            session.write_transaction(self.__write_Query, query)
    @staticmethod
    def __write_Query(tx, query):
        # print(query)
        result = tx.run(query)
        return result


    # general read query
    def read_Query(self, query):
        with self.driver.session() as session:
            session.read_transaction(self.__read_Query, query)
    @staticmethod
    def __read_Query(tx, query):
        result = tx.run(query)
        return result

# generate new applicant
    def generateCypherCreateCustomApplicant(self, gender, psychometric, bagrut, area, name):
        with self.driver.session() as session:
            applicantQuery = "CREATE (a:Applicant{Name:'" + name + "' ,Gender:'" + gender + "' ,Bagrut: " + bagrut + ", Psychometric: " + str(psychometric) + ", Area: '" + area + "', Faculty: '', Degree: ''}) return a"
            print(applicantQuery)
            result = session.run(applicantQuery)
            return [record["a"] for record in result]
