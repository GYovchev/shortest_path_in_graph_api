from .exception import InvalidLinkWeight


class EdgeAttributes:
    weight: float

    def __init__(self, weight):
        if weight < 0:
            raise InvalidLinkWeight()
        self.weight = weight

    def to_dictionary(self):
        return {
            "weight": self.weight
        }


class Edge:
    source: str
    target: str
    weight: int

    def __init__(self, source, target, attributes: EdgeAttributes):
        self.source = source
        self.target = target
        self.attributes = attributes

    def to_dictionary(self):
        return {
            "source": self.source,
            "target": self.target,
            "attributes": self.attributes.to_dictionary()
        }