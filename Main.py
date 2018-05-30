import Neo4jGDBCreator
from os.path import join, dirname
import ConfigParser
import CypherRunner
import networkx as nx
import time
import LoadJSONFriends
import numpy as np


def load_neo4jdb():
    global config, graph_db
    # Load config.ini
    config = ConfigParser.ConfigParser()
    config.read(join(dirname(__file__), "config.ini"))
    # Get a Neo4j Graph from DB host
    graph_db = Neo4jGDBCreator.Neo4jGDBCreator()


def create_neo4j_graph_from_json():
    x = LoadJSONFriends.LoadJSONFriends()

    # Load users from a directory
    nodes, edges, labels = x.load_graph(config.get("configuration", "dataSet_path"))

    # Create a neo4j Graph DB
    graph_db.create_graph(nodes, edges, labels)


def print_sna_metrics(g):

    print
    start_time = time.time()
    degree_centrality = nx.degree_centrality(g)
    print("Degree Centrality spent %s seconds" % (time.time() - start_time))
    user = max(degree_centrality, key=degree_centrality.get)
    print 'User with maximum Degree Centrality:', user, '- Value:', degree_centrality.get(user)
    print 'Average Degree Centrality:', np.array(degree_centrality.values()).mean()

    print
    start_time = time.time()
    closeness_centrality = nx.closeness_centrality(g)
    print("Closeness Centrality spent %s seconds" % (time.time() - start_time))
    user = max(closeness_centrality, key=closeness_centrality.get)
    print 'User with maximum Closeness Centrality:', user, '- Value:', closeness_centrality.get(user)
    print 'Average Closeness Centrality:', np.array(closeness_centrality.values()).mean()

    print
    start_time = time.time()
    betweenness_centrality = nx.betweenness_centrality(g)
    print("Betweenness Centrality spent %s seconds" % (time.time() - start_time))
    user = max(betweenness_centrality, key=betweenness_centrality.get)
    print 'User with maximum Betweenness Centrality:', user, '- Value:', betweenness_centrality.get(user)
    print 'Average Betweenness Centrality:', np.array(betweenness_centrality.values()).mean()

    print
    start_time = time.time()
    print 'Graph Density:', nx.density(g)
    print("Density spent %s seconds" % (time.time() - start_time))

    print
    start_time = time.time()
    square_clustering = nx.square_clustering(g)
    print("Square Clustering spent %s seconds" % (time.time() - start_time))
    user = max(square_clustering, key=square_clustering.get)
    print 'User with maximum Square Clustering:', user, '- Value:', square_clustering.get(user)
    print 'Average Square Clustering:', np.array(square_clustering.values()).mean()

    print
    start_time = time.time()
    print 'Nodes\' Degree:', nx.degree(g)
    print("Degree spent %s seconds" % (time.time() - start_time))


def __init__():
    # Load a Neo4j GB from host
    load_neo4jdb()

    # -------> THIS LINE HAS TO BE REMOVED IF A NEO4JDB HAS ALREADY BEEN CREATED! <---------
    # Create a new graph
    # create_neo4j_graph_from_json()

    query = """
            MATCH p = ()-[]-() 
            RETURN p
            """
    # Run a cypher query
    runner = CypherRunner.CypherRunner()
    print
    g = runner.run_cypher_query(query)

    print
    print 'Nodes:', g.number_of_nodes()
    print 'Edges:', g.number_of_edges()

    # Get SNA metrics from query result
    print_sna_metrics(g)


__init__()


