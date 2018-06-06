import cypher
import ConfigParser
from os.path import join, dirname


class CypherRunner:

    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read(join(dirname(__file__), "config.ini"))
        password = config.get("configuration", "neo4J_pass")
        self.connection = cypher.Connection("http://neo4j:{}@localhost:7474".format(password))

    def run_cypher_query(self, query):
        data = cypher.run(query, conn=self.connection)
        return data.get_graph()
