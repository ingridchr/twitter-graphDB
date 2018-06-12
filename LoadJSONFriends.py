import json
from os import listdir
from os.path import isdir, isfile, join


class LoadJSONFriends:
    """
    This class loads a graph from a JSON file
    """

    def __init__(self):
        pass

    # Load a graph from a directory with files (one file for each user)
    def load_graph(self, directory):
        """
        Load a graph from all the JSON files included on a directory
        :param directory: str
        :return:
                set
                    All the primary users
                dict
                    Friends and followers of each primary user represented by a dict (keys: users' names) of dict (keys:
                    "friends" and " followers"): ["user_name_1", ["friends", friends_list | "followers", followers_list] | ...]
                dict
                    Labels of the primary users (keys: users' names)
        """
        print
        print "--------------- USERS IN JSON FILE ---------------"
        print
        # A dict of dict --> ["user_name_1", ["friends", friends_list | "followers", followers_list] | ...]
        friends_and_followers = dict()
        # A Set of primary users nodes (to avoid duplicated)
        primary_users = set()
        # A dict of labels
        primary_users_labels = dict()

        # Get all the directories from a path
        directories = [d for d in listdir(directory) if isdir(join(directory, d))]
        for directory_name in directories:
            # Get all the files from a path
            files_list = [f for f in listdir(join(directory, directory_name)) if isfile(join(join(directory,
                                                                                                  directory_name), f))]
            # for each file (user)
            for file_name in files_list:
                try:
                    # Split file_name to get user_name and extension
                    user_name = file_name.split(".")[0].split("-")[0]
                    extension = file_name.split(".")[1]

                    # Check if extension is a ".json" file
                    if extension == "json":
                            # Load the dict for that user (friends and followers)
                            user_data = self.get_json(join(join(directory, directory_name), file_name))[user_name]

                            # Create a dict of friends and followers
                            friends_and_followers_dic = dict()
                            friends_and_followers_dic["friends"] = user_data['friends']
                            friends_and_followers_dic["followers"] = user_data['followers']

                            # Add to edges dict the user's dict of followers/friends (key: user_name)
                            friends_and_followers[user_name] = friends_and_followers_dic

                            # Add all the nodes if they're not exist (Primary users)
                            primary_users.add(user_name)
                            print 'User Name:', user_name, '- Label:', user_data['label']
                            primary_users_labels[user_name] = user_data['label']
                except(OSError, IOError):
                    pass
        return primary_users, friends_and_followers, primary_users_labels

    # Load an specific file - return a json: {"user_name"{"friends": {friends_list}, "followers":{followers_list}}
    @staticmethod
    def get_json(file_directory):
        """
        Get a JSON file
        :param file_directory
        :return:
                json
        """
        with open(file_directory) as f:
            data = json.load(f)
        return data


