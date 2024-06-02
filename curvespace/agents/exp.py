import os
import sys
import traceback
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../core/')))
from core.agentic_constructs import sendWithMessage as ai, Prompts
from core.mechanistic_layers import BinaryConstruct as Bin

agent1 = "Exploration bot"
agent2 = "Entertainment bot"
agent3 = "Knowledge bot"

task = "write me bedtime story with teddy bears"
question = task



import curves.curvespace as curves

while(True):
    conv = curves.CurveConversation()
    graphItem = conv.prompt(question)
    x = graphItem.asString()
    print(x)
    for i in graphItem.columnSegments(x):
        print(i)
    answer = ai(agent1 + ":" + question, join=False)
    graphItem = conv.prompt(answer)
    answer1 = "".join(answer)
    answer = ai(Prompts.listItems()+"".join(answer))
    conv.listed(Bin("", answer).list, answer1)
    print(graphItem.asStringDisconnectedCats())
    print(len(graphItem.asStringDisconnectedCats()))
    items = graphItem.lineSegments(graphItem.asStringDisconnectedCats())
    for i in items[:-1]:
        print(i)
        ai("analyze this. this is known format where each row represent category. dots represent data point, and category on left describes line, and '-' represents indexing/time.\n"+i)

    break

