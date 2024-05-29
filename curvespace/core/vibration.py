
import os
import sys
import traceback
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'core/')))

from agentic_constructs import sendWithMessage as ai
from mechanistic_layers import BinaryConstruct

print("ask something")
user = input()
history = list()

print()
def wave(question, repetitions = 5):
    wave = list()
    answer = ai(question)
    for i in range(repetitions):
        history = list()
        history.append(question)
        history.append(answer)
        answer2 = ai("i need detailed explanation of connection between A and B. \nmake sure answer stands independently, and is clear and precise in a way that it can be used as connection.", history)
        wave.append(answer2)
        history = list()
        history.append(user)
        history.append(answer)
        answer2 = ai("i need detailed explanation of connection between A and B, but backwards, going from B to A. \nmake sure answer stands independently, and is clear and precise in a way that it can be used as connection", history)
        wave.append(answer2)

    return wave

def waveBlended(question, repetitions, blending = 1):
    wave = list()
    count = 0
    answer = ai(question)
    history = list()
    for i in range(repetitions):
        if (count <= 0):
            count = blending
            history.clear()
            history.append(question)
            history.append(answer)
        answer2 = ai("i need detailed explanation of connection between A and B. \nmake sure answer stands independently, and is clear and precise in a way that it can be used as connection.", history)
        wave.append(answer2)
        history.append(answer2)
        count -= 1
        if (count <= 0):
            count = blending
            history.clear()
            history.append(question)
            history.append(answer)
        answer2 = ai("i need detailed explanation of connection between A and B, but backwards, going from B to A. \nmake sure answer stands independently, and is clear and precise in a way that it can be used as connection", history)
        wave.append(answer2)
        history.append(answer2)
        count -= 1

    return wave

def waveReask(question, repetitions, reasks, blending=1):
    wave = list()
    count = 0
    answer = ai(question)
    history = list()
    for j in range(reasks):
        for i in range(repetitions):
            if(count <= 0):
                count = blending
                history.clear()
                history.append(question)
                history.append(answer)
            answer2 = ai("i need detailed explanation of connection between A and B. \nmake sure answer stands independently, and is clear and precise in a way that it can be used as connection.", history)
            wave.append(answer2)
            history.append(answer2)
            count -= 1
            if(count <= 0):
                count = blending
                history.clear()
                history.append(question)
                history.append(answer)
            answer2 = ai("i need detailed explanation of connection between A and B, but backwards, going from B to A. \nmake sure answer stands independently, and is clear and precise in a way that it can be used as connection", history)
            wave.append(answer2)
            history.append(answer2)
            count -= 1
        answer = ai(question, wave)
        wave.append(answer)
        history.append(answer)

    return wave

#answer = waveBlended(user, 3)
answer = waveReask(user, 20, 5, 8)
print(answer)