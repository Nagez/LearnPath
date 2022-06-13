import random

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

    # write a query (mainly used to create applicant)
    def write_Query(self, query):
        with self.driver.session() as session:
            session.write_transaction(self.__write_Query, query)
    @staticmethod
    def __write_Query(tx, query):
        result = tx.run(query)
        return result
