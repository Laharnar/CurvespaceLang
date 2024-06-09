import pickle
class AnalysisCell:
    def __init__(self, data):
        self.data = data
        self.has_run = False
        self.result = None

class AnalysisGrid:
    def __init__(self):
        self.context = None
        self.cells = {}

    def add_cell(self, data):
        if data in self.cells:
            return self.cells[data]
        else:
            cell = AnalysisCell(data)
            self.cells[data] = cell
            return cell

    def removeCell(self, data):
        if (data in self.cells):
            del self.cells[data]

    def runAnalysis(self, analysis_func):
        for i in self.cells:
            cell = self.cells[i]
            if cell.result is None:
                # Perform analysis here
                cell.result = analysis_func(cell.data)  # Replace with actual analysis code
                cell.has_run = True
            else:
                print(i, " --> exiting shard")

    def save_grid(self, filename):
        if(not filename.endswith(".pkl")):
            filename+=".pkl"
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    def add_list(self, items):
        for i in items:
            self.add_cell(i)

    def getData(self, cell):
        return self.cells[cell]

    @classmethod
    def load_grid(cls, filename):
        if(not filename.endswith(".pkl")):
            filename+=".pkl"
        try:
            with open(filename, 'rb') as f:
                return pickle.load(f)
        except:
            return AnalysisGrid()

class LinkGrid:
    def __init__(self):
        self.cells = {}
        self.linkedGrid = None

    def pad(self, grid):
        self.linkedGrid = grid

    def addCell(self, data):
        self.cells.setdefault(data, [])

    def runAnalysis(self, analysis_func, branching_func):
        if(self.linkedGrid == None):
            print("Set linking grid")
            return
        for i in self.cells:
            if(len(self.cells[i]) == 0):
                answers = branching_func(i)
                for chunk in answers:
                    self.cells[i].append(chunk)
            else: print(i, "->using existing analysis")
            for j in self.cells[i]:
                if j not in self.linkedGrid.cells:
                    self.linkedGrid.add_cell(j)

        self.linkedGrid.runAnalysis(analysis_func)

    def removeCell(self, data):
        if data in self.cells:
            for i in self.cells[data]:
                self.linkedGrid.removeCell(i)
            del self.cells[data]

    def getLinkData(self, cell):
        return self.cells[cell]

    def getData(self, cell, attrib="result"):
        items = list()
        for i in self.cells[cell]:
            cell = self.linkedGrid.getData(i)
            if(attrib == "result"):
                cell = cell.result
            items.append(cell)
        return items

    def save_grid(self, filename):
        if(not filename.endswith(".pkl")):
            filename+=".pkl"
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def load_grid(cls, filename, initIfEmpty):
        if(not filename.endswith(".pkl")):
            filename+=".pkl"
        try:
            with open(filename, 'rb') as f:
                return pickle.load(f)
        except:
            return initIfEmpty()

# Example usage
grid = AnalysisGrid()
def analysis_func(data):
    # dummy analysis function that returns the square of the input
    return data ** 2


def testing(cell):
    print(cell)
    return "ANALYZED:"+str(cell)

def branch_3(data):
    import core.mincore as ai
    def split_string_into_3(s):
        third_len = len(s) // 3
        part1 = s[:third_len]
        part2 = s[third_len:2 * third_len]
        part3 = s[2 * third_len:]
        return part1, part2, part3

    answer = ai.ai("plan for this task\n" + str(data))
    answers = split_string_into_3(answer)
    return answers

grid.runAnalysis(analysis_func)
# Save the grid to a file
grid.save_grid('analysis_grid.pkl')