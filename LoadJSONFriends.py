import json
from os import listdir
from os.path import isfile, join


class LoadJSONFriends:

    def __init__(self):
        pass

    # Load a graph from a directory with files (one file for each user)
    def load_graph(self, path):
        # A dict of dict --> ["user_name_1", ["friends", friends_list | "followers", followers_list] | ...]
        edges = dict()
        # A Set of nodes (to avoid duplicated)
        nodes = set()
        # A dict of labels
        labels = dict()

        # Get all the files from a path
        files_list = [f for f in listdir(path) if isfile(join(path, f))]

        # for each file (user)
        for file_name in files_list:
            try:
                # Split file_name to get user_name and extension
                user_name = file_name.split(".")[0].split("-")[0]
                extension = file_name.split(".")[1]

                # Check if extension is a ".picklefriends" file
                if extension == "json":
                    # Load the dict for that user (friends and followers)
                    user_data = self.get_json(join(path, file_name))[user_name]
                    print user_data

                    # Create a dictonary of friends and followers
                    friends_and_followers_dic = dict()
                    friends_and_followers_dic["friends"] = user_data['friends']
                    friends_and_followers_dic["followers"] = user_data['followers']

                    # Add to edges dict the user's dict of followers/friends (key: user_name)
                    edges[user_name] = friends_and_followers_dic

                    # Add all the nodes if they're not exist (user, friends and followers)
                    nodes.add(user_name)
                    nodes.update(user_data["friends"])
                    nodes.update(user_data["followers"])

                    labels[user_name] = user_data["label"]
            except(OSError, IOError):
                pass
        return nodes, edges, labels

    # Load an specific file - return a json: {"user_name"{"friends": {friends_list}, "followers":{followers_list}}
    @staticmethod
    def get_json(file_name):

        with open(file_name) as f:
            data = json.load(f)

        return data

