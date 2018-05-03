import LoadFriends
import Neo4jGDBCreator

# Load users from a directory
x = LoadFriends.LoadFriends()
nodes, edges = x.load_graph('~/dataset/.twitter_analyzer_users')

# Create a Neo4j Graph
graph_db = Neo4jGDBCreator.Neo4jGDBCreator()
graph_db.create_graph(nodes, edges)
