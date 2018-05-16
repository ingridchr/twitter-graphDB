import LoadJSONFriends
import Neo4jGDBCreator
from os.path import join, dirname
import ConfigParser

# Load users from a directory
x = LoadJSONFriends.LoadJSONFriends()

config = ConfigParser.ConfigParser()
config.read(join(dirname(__file__), "config.ini"))

nodes, edges, labels = x.load_graph(config.get("configuration", "dataSet_path"))

# Create a Neo4j Graph
graph_db = Neo4jGDBCreator.Neo4jGDBCreator()
graph_db.create_graph(nodes, edges, labels)
