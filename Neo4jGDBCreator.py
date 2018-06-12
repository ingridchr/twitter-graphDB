from py2neo import Graph, Node, Relationship, NodeSelector
import ConfigParser
from os.path import join, dirname


class Neo4jGDBCreator:
    """
    This class creates a Neo4j GraphDB using the py2neo library
    """

    def __init__(self):
        """
        Creates an instance of the Neo4j graph and delete all.
        """
        config = ConfigParser.ConfigParser()
        config.read(join(dirname(__file__), "config.ini"))
        # If it is not explicitly indicated the neo4j url, by default Graph() redirect to localhost
        self.graph = Graph(config.get("configuration", "neo4j_url"), user=config.get("configuration", "neo4j_user"),
                           password=config.get("configuration", "neo4J_pass"))
        self.secondary_users_count = 0
        self.relationships_count = 0
        # -------> THIS LINE HAS TO BE REMOVED IF A NEO4JDB HAS ALREADY BEEN CREATED!! <---------
        self.graph.delete_all()

    def create_graph(self, primary_users, friends_and_followers, primary_users_labels):
        """
            Creates a Neo4j Graph

            Parameters
            ----------
            primary_users : set
                Primary nodes of the graph
            friends_and_followers : dict
                The edges of the graph represented with a dict (keys: users' names)
                of dict (keys: "friends" and " followers"):
                    ["user_name_1", ["friends", friends_list | "followers", followers_list] | ...]

            primary_users_labels : dict
                Labels of the primary nodes (keys: users' names)
        """
        print
        print "--------------- CREATED GRAPH ---------------"
        # For each user
        for user_name in primary_users:
            tx = self.graph.begin()
            # Get the node from Neo4j DB
            user_node = self.get_node_by_name(user_name)
            # If it doesn't exist the Node
            if user_node is None:
                # Create a Primary User Node
                user_node = self.create_primary_user_node(primary_users_labels, user_name)
                self.graph.create(user_node)
            # If the user has friends and followers (Primary_User)
            if user_name in friends_and_followers.keys():
                print
                print 'Processing the primary user: ', user_name

                user_friends = friends_and_followers[user_name]["friends"]
                print 'Number of friends: ', len(user_friends)
                self.create_relationships(user_node, user_friends, primary_users_labels.keys(), tx, primary_users_labels)

                user_followers = friends_and_followers[user_name]["followers"]
                print 'Number of followers: ', len(user_followers)
                self.create_relationships(user_node, user_followers, primary_users_labels.keys(), tx,
                                          primary_users_labels, "left")
            tx.commit()
            n = self.get_node_by_name(user_name)
            print "User_name_values", n.values()
        self.print_graph_summary(primary_users)

    def create_primary_user_node(self, primary_users_labels, user_name):
        """
        Creates a primary user node
        :param primary_users_labels: dict
        :param user_name: str
        :return:
        """
        label_how, label_what = self.get_label_how_and_label_what(primary_users_labels.get(user_name))
        # Create a new Node for the user
        user_node = Node("Primary_User", name=user_name, label_how=label_how, label_what=label_what)
        return user_node

    def print_graph_summary(self, primary_users):
        """
        Prints a summary of the Graph (considering the data in the JSON file - not the created Graph)
        :param primary_users: 
        :return: 
        """
        print
        print
        print 'Number of primary users:', len(primary_users)
        print 'Number of secondary users:', self.secondary_users_count
        print 'Number of relationships:', self.relationships_count

    @staticmethod
    def get_label_how_and_label_what(user_labels):
        """
        Gets label_how and label_what given a str separated by '-'
        :param user_labels: str
        :return:
        """
        split_user_labels = user_labels.split('-')
        label_how = split_user_labels[0]
        if len(split_user_labels) > 1:
            label_what = split_user_labels[1]
        else:
            label_what = ""
        return label_how, label_what

    # Create the relationships btw user and friends/followers. direction is 'right' or 'left'
    def create_relationships(self, primary_user_node, secondary_users, primary_users, tx, labels, direction="right"):
        """
            Creates all the relationships btw a primary user and a list of friends/followers

            Parameters
            ----------

            primary_user_node : Node

            secondary_users : list
                All the friends (or followers) of the primary user

            primary_users : list
                All the primary users (used to check if a follower or friend is a primary user too)

            tx: Transaction
                An open Transaction (py2neo) to create the relationships

            direction: str
                This flag is used to determine the direction of the relationship
         """
        # For each user friend
        for secondary_user in secondary_users:
            # Get the node from Neo4j DB
            secondary_user_node = self.get_node_by_name(secondary_user)
            # If it doesn't exist
            if secondary_user_node is None:
                # Create a new Node for the user friend
                # Check if it is a primary or a secondary user
                if secondary_user in primary_users:
                    secondary_user_node = self.create_primary_user_node(labels, secondary_user)
                else:
                    secondary_user_node = Node("Secondary_User", name=secondary_user)
                    self.secondary_users_count += 1

                self.graph.create(secondary_user_node)
            if direction is "right":
                # Create the relationship btw the user and the friend (user -> FOLLOWS -> friend)
                relationship = Relationship(primary_user_node, "FOLLOWS", secondary_user_node)
                if len(list(self.graph.match(start_node=primary_user_node, end_node=secondary_user_node,
                                             rel_type="FOLLOWS"))) > 0:
                    print "Relationship already exists"
            else:
                # Create the relationship btw the user and the follower (follower -> FOLLOWS -> user)
                relationship = Relationship(secondary_user_node, "FOLLOWS", primary_user_node)
                if len(list(self.graph.match(start_node=secondary_user_node, end_node=primary_user_node,
                                             rel_type="FOLLOWS"))) > 0:
                    print "Relationship already exists"
            self.relationships_count += 1

            tx.create(relationship)

    # Get a Node from de Neo4j graph if it exists
    def get_node_by_name(self, name):
        """
            Gets a Node by the user's name

            Parameters
            ----------
            name : str
                A user's name

            Returns
            -------
            Node
                Returns a Node (py2neo) if it exists in the graph
        """
        selector = NodeSelector(self.graph)
        selected = selector.select(name=name)
        return selected.first()

    # Run an specific query
    def run_query(self, query):
        """
            Runs a query

            Parameters
            ----------
            query : str

            Returns
            -------
            Graph
                The query result
        """
        tx = self.graph.begin()
        result = self.graph.run(query)
        tx.commit()
        return result
