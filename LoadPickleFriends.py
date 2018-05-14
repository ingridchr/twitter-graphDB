import pickle
from os import listdir
from os.path import isfile, join


class LoadPickleFriends:

    def __init__(self):
        pass

    # Load a graph from a directory with files (one file for each user)
    def load_graph(self, path):
        # A dict of dict --> ["user_name_1", ["friends", friends_list | "followers", followers_list] | ...]
        edges = dict()
        # A Set of nodes (to avoid duplicated)
        nodes = set()

        # Get all the files from a path
        files_list = [f for f in listdir(path) if isfile(join(path, f))]

        # for each file (user)
        for file_name in files_list:
            try:
                # Split file_name to get user_name and extension
                user_name = file_name.split(".")[0]
                extension = file_name.split(".")[1]

                # Check if extension is a ".picklefriends" file
                if extension == "picklefriends":
                    # Load the dict for that user (friends and followers)
                    friends_and_followers_dic = self.unpickle(join(path, file_name))
                    user_friends = friends_and_followers_dic.get("friends")
                    user_followers = friends_and_followers_dic.get("followers")

                    # Add to edges dict the user's dict of followers/friends (key: user_name)
                    edges[user_name] = friends_and_followers_dic

                    # Add all the nodes if they're not exist (user, friends and followers)
                    nodes.add(user_name)
                    nodes.update(user_friends)
                    nodes.update(user_followers)
            except(OSError, IOError):
                pass
        return nodes, edges

    # Load an specific file - return a dictonary: ["friends", friends_list | "followers", followers_list]
    @staticmethod
    def unpickle(file_name):
        with open(file_name, 'rb') as fo:
            friends_and_followers_dic = pickle.load(fo)
        return friends_and_followers_dic






