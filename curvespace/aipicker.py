

import os
import sys
import traceback
from json import JSONDecodeError

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from mechanistic.agentic_constructs import sendWithMessage as ai
from mechanistic.mechanistic_layers import BinaryConstruct

def pyfile(file, glob=None, loc=None, onlyCompile = False):
    if glob is None:
        import sys
        glob = sys._getframe().f_back.f_globals
    if loc is None:
        loc = glob

    # It seems that the best way is using tokenize.open(): http://code.activestate.com/lists/python-dev/131251/
    import tokenize
    stream = tokenize.open(file)  # @UndefinedVariable
    try:
        contents = stream.read()
    finally:
        stream.close()

    # execute the script (note: it's important to compile first to have the filename set in debug mode)
    if(onlyCompile):
        compile(contents + "\n", file, 'exec')
    else:
        exec(compile(contents + "\n", file, 'exec'), glob, loc)

def aip(limit, message, history, pickable, testPassed, testFailed):
    import random
    passes = list()
    if(len(pickable) > 0):
        for i in range(3):
            picked = random.randrange(0, len(pickable))
            rnged = pickable[picked]
            tested, passed = limitTest(limit, rnged, testPassed, history, history)
            if (passed):
                passes.append(tested)
            else:
                history.append(testFailed[-1])  # record failure for next pass

    answer = ai(message, history)
    tested, passed = limitTest(limit, answer, testPassed, testFailed, history)
    if (passed):
        history.append(testPassed[-1])
        passes.append(tested)
    else:
        history.append(testFailed[-1])# record failure for next pass

    return passes, tested!= None

def limitTest(tool, string, testPassed, testFailed, history):
    if(tool == "compile"):
        try:
            binCode = BinaryConstruct("", string)
            string = binCode.codeall
            with open("ai-picker_store.txt", 'w') as f:
                f.write(string)
            pyfile("ai-picker_store.txt", onlyCompile=True)
            # no error
            if(string not in testPassed):
                testPassed.append(string)
            return string, True
        except Exception as e:
            traceback.print_exception(e)
            answer = ai(f"what would fix this? \ncode:\n{string}\n\n{str(e)}", testPassed)
            testFailed.append(str(answer))
            return answer, False
    if(tool == "test"):
        for i in range(3):
            try:
                binCode = BinaryConstruct("", string)
                if(binCode.codeall != ""):
                    string = binCode.codeall
                if(string == ""):
                    raise Exception("no code, surround code with '''")
                with open("ai-picker_store.txt", 'w') as f:
                    f.write(string)
                pyfile("ai-picker_store.txt", onlyCompile=False)
                # no error
                if(string not in testPassed):
                    testPassed.append(string)
                return string, True
            except AssertionError as err2:
                traceback.print_exception(err2)
                answer = ai(f"what would fix this? modify code+tests in one? \ncode:\n{string}\n\n{str(err2)}", testPassed)
                string = answer
                testFailed.append(str(answer))
            except Exception as e:
                traceback.print_exception(e)
                answer = ai(f"what would fix this? modify code+tests in one? \ncode:\n{string}\n\n{str(e)}", testFailed)#testPassed)
                string = answer
                testFailed.append(str(answer))
        else:
            return string, False
    if (tool == "agreement"):
        for i in range(3):
            ranswer = ai("Describe agreement that would have to be reached.", history)
            history.append(ranswer)
            answer = ai("Is the reasoning reached? If not what do you think is missing? <<YES>><<NO>> and why", history)
            if("YES" in answer):
                testPassed.append("Agreement reached -"+ranswer + " \n-"+answer)
                return answer, True
            else:
                history.append("reasoning isnt reached: "+answer)
                testFailed.append(str(answer))
        return answer, False
    print("NOT HANDLED TOOL ",tool)
    return None

import json

class FileSaverLoader:
    def __init__(self, filename):
        self.filename = filename
        self.data = {}

    def save(self, data):
        with open(self.filename, 'w') as f:
            json.dump(data, f)

    def load(self):
        try:
            with open(self.filename, 'r') as f:
                return json.load(f,)
        except JSONDecodeError:
            return {}
        except FileNotFoundError:
            return {}

    def get_data(self):
        if("passes" not in self.data):
            self.data["passes"] = []
        if ("fails" not in self.data):
            self.data["fails"] = []
        return self.data

    def set_data(self, data):
        self.data = data

    def save_and_load(self):
        self.save(self.data)
        self.data = self.load()


saver = FileSaverLoader('example1.json')
saver.set_data(saver.load())
print(saver.get_data())  # {'key1': 'value1', 'key2': 'value2'}

history = list()
pickable = list()
testPassed = list(saver.get_data()["passes"])
testFailed = list(saver.get_data()["fails"])

def runLoop(limit, message, history=history):
    while True:
        answers, passed = aip(limit, message, history, pickable, testPassed, testFailed)
        for i in answers:
            history.append(i)
            print(i)

        if (passed):
            testPassed.append(history[-1])
            break
        else:
            testFailed.append(history[-1])

def testLoop(limit, message, history=history):
    answer, passed = limitTest(limit, message, testPassed, testFailed, history)
    while not passed:
        answers, passed = aip(limit, message, history, pickable, testPassed, testFailed)
        for i in answers:
            history.append(i)
            print(i)

        if (passed):
            testPassed.append(history[-1])
            break
        else:
            testFailed.append(history[-1])

def writeTestedCode(request):
    runLoop("compile", request, history)
    answer1 = history[-1]
    runLoop("compile", "write tests for previous code with 'assert ... test'. assume tested code doesnt need imports.", history)
    answer2 = history[-1]
    b2 = BinaryConstruct("", answer2)
    answer2 = b2.mkMainTestable(answer2)
    answer, passed = limitTest("test", answer1+"\n"+answer2, testPassed, testFailed, history)
    history.append(answer)
    runLoop("compile", "get only code, without tests")
    answer = history[-1]
    print(answer)
    saver.get_data()["passes"] = testPassed
    saver.get_data()["fails"] = testFailed
    saver.save_and_load()
    return answer
#
if __name__ == '__main__':



    while(True):

        print("user input")
        userInput = input()

        #answer = writeTestedCode("write me python bit functions bitAnd, bitOr, and bitNot. if they already exist, dont write anything, write about lorem ipsum.")
        #tools = history[-1]
        tools = str(saver.get_data()["passes"])
        #history.append("You are an intelligent AI working on multistep solutions, going from existing tools to higher and higher abstractions.")
        #history.append(userInput)
        #answer = ai("prepare plan", history)
        history.clear()
        #history.append(answer)
        history.append(tools)
        #history.append(userInput) #"Work on implementing graphs in python by picking tool/s")
        #answer = ai("Which existing tool/s would you use to implement task?", history)
        writeTestedCode(userInput)

        '''
        print("user input")
        userInput = input()

        if(not "NO" in userInput):
            #answer = writeTestedCode("write me python bit functions bitAnd, bitOr, and bitNot. if they already exist, dont write anything, write about lorem ipsum.")
            #tools = history[-1]
            tools = str(saver.get_data()["passes"])
            history.append("You are an intelligent AI working on multistep solutions.")
            history.append("Use computer science and bits to code.")
            history.append(userInput)
            answer = ai("prepare rules", history)
            history.clear()
            history.append(answer)
            history.append(tools)
            history.append(userInput) #"Work on implementing graphs in python by picking tool/s")
            answer = ai("Pick existing tool/s to progress on task", history)
            writeTestedCode(userInput)
        else:
            tools = str(saver.get_data()["passes"])
            history.clear()
            history.append(tools)
            answer = ai(userInput, history)
        '''


#runLoop("agreement", "You are an AI working on multistep solutions. Figure out what that means.")
#runLoop("agreement", "You are an AI working on multistep solutions with only tools given to you. You are an AI converting lower connections with higher abstractions. Plan out next step for implementation of A* algorithm in python. Figure out what that means.")
#aii = "You are an AI working on multistep solutions with only tools given to you. You are an AI converting lower connections with higher abstractions. Plan out next step for implementation of A* algorithm in python"
#history.append(aii)
#history.append(ai(aii))
#answer = writeTestedCode("Pick tool/s. And write.")
