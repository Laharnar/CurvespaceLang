import os
import sys
import traceback
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../core/')))
from core.agentic_constructs import sendWithMessage as ai

agent1 = "Exploration bot"
agent2 = "Entertainment bot"
agent3 = "Knowledge bot"

task = "write me bedtime story with teddy bears"
question = task

import curves.curvespace as curves
while(True):
    conv = curves.CurveConversation()
    answer = ai(agent1+":"+question,join=False)
    conv.prompt(answer)
    answer = ai(agent2+":"+"".join(answer),join=False)
    conv.prompt(answer)
    answer = ai(agent3+":"+"".join(answer),join=False)
    conv.prompt(answer)

