from core.mincore import *
from core.mechanistic_layers import BinaryConstruct as Bin
#idea is to read file with code, save code in memory, select parts of code, and execute it

def aiFileCode(filename, additional=None, lang="py"):

    test = f"write {lang} code that reads utf-8 '{filename}' and saves result into string 'x'"
    answer = ai(test)
    cc = Bin("", answer)
    global x
    x = cc.code1
    memory = cc.code1
    history = list()
    history.append(test)
    history.append(answer)
    history.append(memory)
    x = ""
    exec(memory, globals())
    history.append(x)
    if(additional is not None):
        answer = ai("what are definitions, copy examples and usage samples\n"+additional, [x])
        history.append(answer)
    return history

history = aiFileCode("nonlogic2.py")
x = ""
answer = ai("use interpretor to construct this sentence: 'sky is often blue' in ambigous way, and assign answer to x", history)
cc = Bin("", answer).code1
exec(history[-1]+"\n"+cc, globals())
print(" nice")
print(x)

