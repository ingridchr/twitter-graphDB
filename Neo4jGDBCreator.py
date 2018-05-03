from py2neo import Graph, Node, Relationship, NodeSelector


class Neo4jGDBCreator:

    # Creates an instance of the Neo4j graph and delete all
    def __init__(self):
        # Here we have to change the location of the GraphDB, by default Graph() redirect to localhost
        self.graph = Graph(password="pass")

        # -------> THIS LINE HAS TO BE REMOVED! <---------
        self.graph.delete_all()

    # Create a Neo4j Graph (user_names: list of users; friends_and_followers: dict [k: user, v: dict])
    def create_graph(self, user_names, friends_and_followers):
        # Begin a transaction
        tx = self.graph.begin()
        # For each user
        for user_name in user_names:
            # Get the node from Neo4j DB
            user_node = self.get_node_by_name(user_name)
            # If it doesn't exist
            if user_node is None:
                # Create a new Node for the user
                user_node = Node("User", name=user_name)
                self.graph.create(user_node)
            # If the user has friends and followers
            if user_name in friends_and_followers.keys():
                print 'Processing the user: ', user_name
                user_friends = friends_and_followers[user_name]["friends"]
                print 'Number of friends: ', len(user_friends)

                # For each user friend
                for user_friend in user_friends:
                    # Get the node from Neo4j DB
                    friend_node = self.get_node_by_name(user_friend)
                    # If it doesn't exist
                    if friend_node is None:
                        # Create a new Node for the user friend
                        friend_node = Node("User", name=user_friend)
                        self.graph.create(friend_node)
                    # Create the relationship btw the user and the friend (user -> IS_FRIEND_OF -> friend)
                    relationship = Relationship(user_node, "IS_FRIEND_OF", friend_node)
                    tx.create(relationship)

                user_followers = friends_and_followers[user_name]["followers"]
                print 'Number of followers: ', len(user_followers)

                # For each user follower
                for user_follower in user_followers:
                    # Get the node from Neo4j DB
                    follower_node = self.get_node_by_name(user_follower)
                    # If it doesn't exist
                    if follower_node is None:
                        # Create a new Node for the user friend
                        follower_node = Node("User", name=user_follower)
                        self.graph.create(follower_node)
                    # Create the relationship btw the user and the friend (user -> IS_FOLLOWED_BY -> friend)
                    relationship = Relationship(user_node, "IS_FOLLOWED_BY", follower_node)
                    tx.create(relationship)
        # Commit the transaction
        tx.commit()

    # Get a Node from de Neo4j graph if it exists
    def get_node_by_name(self, name):
        selector = NodeSelector(self.graph)
        selected = selector.select("User", name=name)
        return selected.first()

    # Run an specific query
    def run_query(self, query):
        tx = self.graph.begin()
        result = self.graph.run(query)
        tx.commit()
        return result
