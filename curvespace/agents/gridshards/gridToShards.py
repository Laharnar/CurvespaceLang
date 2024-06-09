
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
linking.removeCell(task)
task = ai("convert this into short marketing description, dont mention code\n"+task)
linking.removeCell(task)
task = "implement solution for this\n"+task
linking.removeCell(task)
linking.addCell(task)
linking.runAnalysis(lambda data: ai(data,rng=1), lambda task: aiLang(task, canZeroShot=False, OUTPUT="many",rng=0.2))
linking.save_grid("first")
print("exit")
exit()
linking.runAnalysis(testing, branch_3)
print(linking.getLinkData(cell)) # auto created data from analysis
print(linking.getData(cell)) # auto created data from analysis
answer = ai(task)
answer2 = aiCharLong(task, "senior programmer", "precise, pragmatic, has both broad and small view", canZeroShot=False)

plan = answer.split("\n")
results = list()

exit()
import AnalysisGrid as AlyGrid
import AnalysisGrid

grid = AlyGrid.AnalysisGrid.load_grid("shards")
grid.run_analysis(aiLang)
for i in plan:
    if isinstance(i, str):
        shard = aiLang(i)
        plan[plan.index(i)] = (i, shard)

grid.save_grid("shards")