
from core.mincore import *
from AnalysisGrid import *
def initAnalysis():
    linking = LinkGrid()
    analysis = AnalysisGrid()
    linking.pad(analysis) #analysis will be stacked bellow
    return linking

linking = LinkGrid.load_grid("first", initAnalysis)


task = '''write code that will allow something like this in py:
        linking = LinkGrid()
        linking.stack(AnalysisGrid()) #analysis will be stacked bellow
        cell = "some data"
        linking.addCell(cell)
        linking.runAnalysis()
        linking.getData(cell) # auto created data from analysis
        analysis.getData(cell) # auto created data from analysis
        '''
task = ai("convert this into short marketing description, dont mention code\n"+task)
task = "implement solution for this\n"+task
linking.addCell(task)
linking.runAnalysis(lambda data: ai(data,rng=1), lambda task: aiLang(task, canZeroShot=False, OUTPUT="many",rng=0.2))
linking.save_grid("first")
print("exit")
while True:
    # pick item
    # contribute
    # conclude
    pass




