import json
import os

class DictOptimizer:
    def __init__(self):
        self.idMap = {}  # maps string values to 1-byte IDs
        self.strMap = {}  # maps 1-byte IDs to string values
        self.idCounter = 0  # keeps track of the next available ID

    def addString(self, string):
        if self.idCounter >= 255:  # 1 byte capacity exceeded
            raise Exception("ID capacity exceeded")

        if string not in self.idMap:
            self.idMap[string] = self.idCounter
            self.strMap[self.idCounter] = string
            self.idCounter += 1
        return self.idMap[string]

    def getId(self, string):
        return self.idMap.get(string)

    def getString(self, id):
        return self.strMap.get(id)

    def getAPI(self):
        return [method_name for method_name in dir(self) if callable(getattr(self, method_name))]

    def splitAndStore(self, string):
        """
        Split the input string into chunks of size chunkSize,
        and store each chunk as a separate string.
        """
        chunkSize = 10
        result = []
        chunks = [string[i:i + chunkSize] for i in range(0, len(string), chunkSize)]
        for chunk in chunks:
            result.append(self.addString(chunk))
        return result

    def getChunks(self, idlist):
        """
        Retrieve all chunks that belong to the original string.
        """
        chunks = []
        for i in idlist:
            chunks.append(self.getString(i))
        return chunks

    def save(self, filename):
        data = {
            'idMap': self.idMap,
            'strMap': self.strMap,
            'idCounter': self.idCounter
        }
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
            self.idMap = data['idMap']
            self.strMap = data['strMap']
            self.idCounter = data['idCounter']
        else:
            print("File not found.")