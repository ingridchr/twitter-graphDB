from py2neo import Graph, Node, Relationship, NodeSelector
import ConfigParser
from os.path import join, dirname


class Neo4jGDBCreator:
    i = int()

    # Creates an instance of the Neo4j graph and delete all
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read(join(dirname(__file__), "config.ini"))
        # Here we have to change the location of the GraphDB. By default Graph() redirect to localhost
        self.graph = Graph(password=config.get("configuration", "neo4J_pass"))

        # -------> THIS LINE HAS TO BE REMOVED! <---------
        self.graph.delete_all()

    # Create a Neo4j Graph (user_names: list of users; friends_and_followers: dict [k: user, v: dict])
    def create_graph(self, nodes, edges, labels):
        print labels.keys()
        # Begin a transaction
        tx = self.graph.begin()
        # For each user
        for user_name in nodes:
            # Get the node from Neo4j DB
            user_node = self.get_node_by_name(user_name)
            # If it doesn't exist
            if user_node is None:
                # Create a new Node for the user
                user_node = Node("Primary_User", name=user_name, label=labels.get(user_name))
                self.i += 1
                self.graph.create(user_node)
            # If the user has friends and followers
            if user_name in edges.keys():
                print 'Processing the user: ', user_name

                user_friends = edges[user_name]["friends"]
                print 'Number of friends: ', len(user_friends)
                self.create_relationships(tx, labels, user_friends, user_node)

                user_followers = edges[user_name]["followers"]
                print 'Number of followers: ', len(user_followers)
                self.create_relationships(tx, labels, user_followers, user_node, "left")
        print self.i
        # Commit the transaction
        tx.commit()

    # Create the relationships btw user and friends/followers. direction is 'right' or 'left'
    def create_relationships(self, tx, labels, secondary_user_list, primary_user_node, direction="right"):
        # For each user friend
        print secondary_user_list
        for secondary_user in secondary_user_list:
            # Get the node from Neo4j DB
            secondary_user_node = self.get_node_by_name(secondary_user)
            # If it doesn't exist
            if secondary_user_node is None:
                # Create a new Node for the user friend
                if secondary_user in labels.keys():
                    secondary_user_node = Node("Primary_User", name=secondary_user)
                    self.i += 1
                else:
                    secondary_user_node = Node("Secondary_User", name=secondary_user)
                    self.i += 1

                self.graph.create(secondary_user_node)
            if direction is "right":
                # Create the relationship btw the user and the friend (user -> FOLLOWS -> friend)
                relationship = Relationship(primary_user_node, "FOLLOWS", secondary_user_node)
            else:
                # Create the relationship btw the user and the follower (follower -> FOLLOWS -> user)
                relationship = Relationship(secondary_user_node, "FOLLOWS", primary_user_node)
            tx.create(relationship)

    # Get a Node from de Neo4j graph if it exists
    def get_node_by_name(self, name):
        selector = NodeSelector(self.graph)
        selected = selector.select(name=name)
        return selected.first()

    # Run an specific query
    def run_query(self, query):
        tx = self.graph.begin()
        result = self.graph.run(query)
        tx.commit()
        return result
