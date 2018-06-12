import cypher
import ConfigParser
from os.path import join, dirname


class CypherRunner:
    """
    This class is used to use the cypher library which is NetworkX compatible.
    """

    def __init__(self):
        """
        Creates a Connection using the cypher library.

        The results given by cypher lib are NetworkX compatible! :)
        """
        config = ConfigParser.ConfigParser()
        config.read(join(dirname(__file__), "config.ini"))
        password = config.get("configuration", "neo4J_pass")
        self.connection = cypher.Connection("http://neo4j:{}@localhost:7474".format(password))

    def run_cypher_query(self, query):
        """
        Runs a Cypher query
        :param query
        :return:
                ResultSet (cypher)
        """
        data = cypher.run(query, conn=self.connection)
        return data.get_graph()
