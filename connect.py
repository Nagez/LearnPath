import random

from neo4j import GraphDatabase

class HelloWorldExample:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    # doesnt show anything
    def checkConnection(self):
        self.driver.verify_connectivity()

    def showoneapplicant(self):
        with self.driver.session() as session:
            # result = session.run("MATCH (n) where id(n) = 393 or id(n) = 395 RETURN n")  # Query
            result = session.run("MATCH(f:Faculty)<-[:Offered_In]-(c:Class)"
                                 "WHERE f.Name CONTAINS 'Engineering'"
                                 "RETURN c")
            return [record["c"] for record in result]

    def read_findClassFromFaculty(self, faculty):
        with self.driver.session() as session:
            return session.read_transaction(self.findClassFromFaculty, faculty)

    @staticmethod
    def findClassFromFaculty(tx, faculty):
        result = tx.run("MATCH(f:Faculty)<-[:Offered_In]-(c:Class)"
                        "WHERE f.Name CONTAINS '$faculty'"
                        "RETURN c", faculty=faculty)
        return [record["c"] for record in result]

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


if __name__ == "__main__":
    greeter = HelloWorldExample("bolt://localhost:7687", "neo4j", "1234")
    # greeter.checkConnection() # not working
    # greeter.print_greeting("hello, world")
    res = greeter.showoneapplicant()
    # res = greeter.read_findClassFromFaculty('Engineering')
    # print(res)
    for i in range(5):
        r = random.choice(res)
        print(r)
        print(r.id)
        print(r.keys())
        print(r.values())

    greeter.close()