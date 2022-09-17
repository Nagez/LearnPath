from neo4j import GraphDatabase

class connection:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    # example for printing a message and creating message node
    def print_greeting(self, message):
        with self.driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message)
            print(greeting)
    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]

    # return an applicant given the id of the node
    def showoneapplicant(self):
        with self.driver.session() as session:
            result = session.run("MATCH (n) where id(n) = 393 or id(n) = 395 RETURN n")  # Query
            return [record["c"] for record in result]

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
        result = tx.run("MATCH(a: Applicant{Name: '"+Name+"'})-[f:Friend]-(a2)-[r:Accepted_To]->(c:Class) WHERE a.Bagrut>=c.BagrutMinimum or a.Psychometric>=c.PsychometricMinimum return c")
        return [record["c"] for record in result]

    # match for applicant available classes using a class name search and get classes that contain that name, classes that connected to faculties with that name and similar classes
    def findMatchTroughName(self, ApplicantName, className):
        with self.driver.session() as session:
            return session.read_transaction(self.__findMatchTroughName, ApplicantName, className)

    @staticmethod
    def __findMatchTroughName(tx, ApplicantName,className):
        result = tx.run("MATCH(a: Applicant{Name: '"+ApplicantName+"'}) MATCH(c:Class)-[Offered_In]-(f:Faculty) MATCH(c:Class)-[Similar]-(c1:Class) WHERE (toLower(c.Name) CONTAINS  toLower('"+className+"') or toLower(f.Name) CONTAINS  toLower('"+className+"')) and (a.Bagrut>=c.BagrutMinimum or a.Psychometric>=c.PsychometricMinimum) and (a.Bagrut>=c1.BagrutMinimum or a.Psychometric>=c1.PsychometricMinimum) return c,c1")
        return result

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

    # general write query (mainly used to create applicant)
    def write_Query(self, query):
        with self.driver.session() as session:
            session.write_transaction(self.__write_Query, query)
    @staticmethod
    def __write_Query(tx, query):
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
