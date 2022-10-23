from neo4j import GraphDatabase

class connection:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

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


    # write a query (mainly used to create applicant)
    def write_matchApplicantToClass(self, applicantID,classID):
        with self.driver.session() as session:
            session.write_transaction(self.__matchApplicantToClass, applicantID,classID)

    @staticmethod
    def __matchApplicantToClass(tx, applicantID,classID):
        result = tx.run("MATCH(a:Applicant),(c:Class) "
                        "where id(a)="+applicantID+" and id(c)="+classID+" "
                        "set a.Degree = c.Name CREATE(a)-[ac:Accepted_To]->(c) ")
        return result


    # using an applicant name, find matching class trough his friend connection
    def findMatchTroughFriend(self, Name):
        with self.driver.session() as session:
            return session.read_transaction(self.__findMatchTroughFriend, Name)

    @staticmethod
    def __findMatchTroughFriend(tx, Name):
        str = "MATCH(a: Applicant{Name: '"+Name+"'})-[f:Friend]-(a2)-[r:Accepted_To]->(c:Class)--(:Faculty)--(i:Institution)" \
              " WHERE a.Bagrut>=c.BagrutMinimum or a.Psychometric>=c.PsychometricMinimum" \
              " return distinct c,i,collect(a2.Name) as Friends ,count(f) as Strengh order by Strengh desc"
        result = tx.run(str)
        print("\nMatch trough friend\n" + str)
        table = []
        for res in result:
            dc = {}
            className = res["c"]["Name"]
            institutionName = res["i"]["Name"]
            friends = res["Friends"]
            strengh = res["Strengh"]
            dc.update({"ClassName": className, "InstitutionName": institutionName, "Friends": friends,
                       "Strengh": strengh})
            table.append(dc)

        return table


    # match for applicant available classes using a class name search and get classes that contain that name, classes that connected to faculties with that name and similar classes (using applicant Name)
    def findMatchTroughName(self, ApplicantName, className):
        with self.driver.session() as session:
            return session.read_transaction(self.__findMatchTroughName, ApplicantName, className)

    @staticmethod
    def __findMatchTroughName(tx, ApplicantName,className):
        str = "MATCH (i:Institution)-[]-(f:Faculty)-[]-(c:Class) optional match (c)-[Similar]-(c1:Class)"\
               "with c,c1 where (toLower(c.Name) CONTAINS  toLower('"+className+"') or toLower(f.Name) CONTAINS toLower('"+className+"'))"\
               "WITH collect(c)+collect(c1) AS cl unwind cl AS classes MATCH(a: Applicant{Name: '"+ApplicantName+"'})"\
               "RETURN DISTINCT classes, (classes.BagrutMinimum - a.Bagrut) as BagrutDiff, (classes.PsychometricMinimum - a.Psychometric) as PsychometricDiff order by BagrutDiff"
        print("\nMatch trough name search\n" + str)
        result = tx.run(str)
        return [record["classes"] for record in result]


    # match for applicant available classes using a class name search and get classes that contain that name, classes that connected to faculties with that name and similar classes (using applicant ID)
    def findMatchIDTroughName(self, ApplicantID, className):
        with self.driver.session() as session:
            return session.read_transaction(self.__findMatchIDTroughName, ApplicantID, className)

    @staticmethod
    def __findMatchIDTroughName(tx, ApplicantID, className):
        str = "MATCH(a: Applicant), (c:Class)-[Offered_In]-(f:Faculty), (c:Class)-[Similar]-(c1:Class)" + \
                        " WHERE ID(a)="+ApplicantID+" and ((toLower(c.Name) CONTAINS  toLower('"+className+"') or toLower(f.Name) CONTAINS toLower('"+className+"')) and (a.Bagrut>=c.BagrutMinimum or a.Psychometric>=c.PsychometricMinimum) and (a.Bagrut>=c1.BagrutMinimum or a.Psychometric>=c1.PsychometricMinimum))"+\
                        " WITH collect(c)+collect(c1) AS cl unwind cl AS classes"+\
                        " RETURN DISTINCT classes "
        print("\nMatch trough name search with applicant ID\n" + str)
        result = tx.run(str)
        return [record["classes"] for record in result]


    # match for applicant available classes using a class name search and get classes that contain that name, classes that connected to faculties with that name and similar classes
    def findMatchTroughID(self, ApplicantID, className):
        with self.driver.session() as session:
            return session.read_transaction(self.__findMatchTroughID, ApplicantID, className)

    @staticmethod
    def __findMatchTroughID(tx, ApplicantID,className):
        str = "MATCH (i:Institution)-[]-(f:Faculty)-[]-(c:Class) optional match (c)-[Similar]-(c1:Class)MATCH(a: Applicant)"\
              "where (toLower(c.Name) CONTAINS  toLower('"+className+"') or toLower(f.Name) CONTAINS toLower('"+className+"')) and ID(a)="+ApplicantID+""\
              "WITH a,collect(c)+collect(c1) AS cl unwind cl AS classes"\
              "RETURN DISTINCT classes, (classes.BagrutMinimum - a.Bagrut) as BagrutDiff, (classes.PsychometricMinimum - a.Psychometric) as PsychometricDiff order by BagrutDiff "
        print("\nMatch trough id search\n" + str)
        result = tx.run(str)
        return [record["classes"] for record in result]


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
             dc.update({"ClassName":className,"InstitutionName":institutionName,"Area":area,"NumOfAcceptedApplicants":numOfAcceptedApplicants})
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
            dc.update({"InstitutionName": institutionName, "FacultyName": facultyName,  "AverageBagrutMinimum": avgB,  "AveragePsychometricMinimum": avgP})
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
            dc.update({"AverageBagrutMinimum": avgB, "AveragePsychometricMinimum": avgP, "ClassesQuantity": classesQuantity, "Tag": tag})
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
            dc.update({"Area": area, "QuantityOfAcceptedApplicants": quantityOfAcceptedApplicants, "Percent": percent})
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


    def generateCypherCreateCustomApplicant(self, gender, psychometric, bagrut, area, name):
        with self.driver.session() as session:
            applicantQuery = "CREATE (a:Applicant{Name:'" + name + "' ,Gender:'" + gender + "' ,Bagrut: " + bagrut + ", Psychometric: " + str(psychometric) + ", Area: '" + area + "', Faculty: '', Degree: ''}) return a"
            print(applicantQuery)
            result = session.run(applicantQuery)
            return [record["a"] for record in result]
