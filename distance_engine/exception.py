class InvalidLinkWeight(Exception):
    def __init__(self):
        super(InvalidLinkWeight, self).__init__("Weight of a link should be a non-negative number")


class BadGraphDictionaryData(Exception):
    def __init__(self,  description):
        super(BadGraphDictionaryData, self).__init__(description)


class NodeDoesntExist(Exception):
    def __init__(self,  node_id: str):
        super(NodeDoesntExist, self).__init__("Node with id {} doesn't exist".format(node_id))


class NoPathExists(Exception):
    def __init__(self,  id1: str, id2: str):
        super(NoPathExists, self).__init__("No path exists between nodes {} and {}".format(id1, id2))
