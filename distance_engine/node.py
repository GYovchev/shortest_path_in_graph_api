class Node():
    id: str

    def __init__(self, id):
        self.id = id

    def to_dictionary(self):
        return {
            "id": self.id
        }