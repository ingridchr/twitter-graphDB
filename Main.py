import LoadJSONFriends
import Neo4jGDBCreator

# Load users from a directory
x = LoadJSONFriends.LoadJSONFriends()
nodes, edges, labels = x.load_graph('~/dataset/')

# Create a Neo4j Graph
graph_db = Neo4jGDBCreator.Neo4jGDBCreator()
graph_db.create_graph(nodes, edges, labels)
