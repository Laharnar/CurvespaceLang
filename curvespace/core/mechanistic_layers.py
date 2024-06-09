def binaryParser(question = "", answer = ""):
    # dont edit question and answer
    from collections import defaultdict

    class AIbit:
        def __init__(self, question, answer, toBit, isOne = False):
            self.isOne = isOne
            if(toBit != None and toBit(question, answer)):
                self.isOne =True

        def __bool__(self):
            return self.isOne
        def aiOr(self, bit):
            return AIbit("", "", None, self.isOne or bit.isOne)

        def aiAnd(self, bit):
            return AIbit("", "", None, self.isOne and bit.isOne)

    answer = answer.replace("```python", "```") #for multi code its annoying
    i1=question
    i2=answer

    def qORa(word):
        return AIbit(i1, i2, lambda q, a: word in q or word in a) # OR

    # parsing
    hasJsonWord = qORa("json")
    hasIf = qORa("if")
    hasEq = qORa("=")

    hasCurlyBrackets = AIbit(i1, i2, lambda q, a: "{" in a and "}" in a)
    hasParentheses = AIbit(i1, i2, lambda q, a: "(" in a and ")" in a)
    hasTripleMarker = AIbit(i1, i2, lambda q, a: "```" in a)
    hasTripleMarkerDuo = AIbit(i1, i2, lambda q, a: a.count("```") >= 2)
    hasTripleMarkerPython = AIbit(i1, i2, lambda q, a: "```python" in a)
    hasSingleMarkerPython = AIbit(i1, i2, lambda q, a: "`" in a)
    hasDirectArrayAssign = AIbit(i1, i2, lambda q, a: "= [" in a)
    hasPrint = AIbit(i1, i2, lambda q, a: "print" in a)
    hasOneLine = AIbit(i1, i2, lambda q, a: "One-line" in a)
    hasDocs = AIbit(i1, i2, lambda q, a: "Documentation" in a)
    hasMinuses = AIbit(i1, i2, lambda q, a: a.count("-") > 0)

    hasUnity = qORa("unity")
    hasScene = qORa("scene")
    hasSetup = qORa("setup")
    hasScript = qORa("script")
    hasPython = qORa("python")
    assumeFuncCall = qORa("()")
    hasDef = qORa("def")
    hasColon = qORa(":")

    hasMission = qORa("mission")

    hasCorrect = qORa("correct")
    hasFind = qORa("find")
    hasAdd = qORa("add")

    hasNew = qORa("new")
    hasObject = qORa("object")

    hasHow = qORa("how")
    hasThis = qORa("this")
    hasWork = qORa("work")
    hasHere = qORa("here")
    hasAnd = qORa("and")
    hasThere = qORa("there")
    hasThat = qORa("that")

    blockOr = qORa("BLOCKOR")
    blockAnd = qORa("BLOCKAND")
    blockNot = qORa("BLOCKNOT")
    block1 = qORa("BLOCK1")

    hasPutTogether = qORa("put together")
    miniLines = hasSingleMarkerPython
    guessPython = hasDirectArrayAssign or hasPrint or assumeFuncCall or miniLines

    def extractOneLiner(a):
        if not hasOneLine and not hasDocs:
            return ""
        if(hasOneLine):
            start_idx = a.find("One-line")
            end_idx = a.find("\n", start_idx)
            end_idx2 = a.find("\n", end_idx)
            return a[end_idx:end_idx2]
        elif(hasDocs):
            start_idx = a.find("Documentation")
            end_idx = a.find("\n", start_idx)
            end_idx2 = a.find("\n", end_idx)
            return a[end_idx:end_idx2]
        return None

    def extractPyCode(a, i):
        if(a.count("```") < (i+1)*2):
            return None
        code = None
        try:
            if (hasTripleMarkerPython):
                second = a.split("```python")[1 + i]
                code = second.split("```")[0]
            elif hasTripleMarkerDuo and hasPython:  # python mentioned
                code = a.split("```")[1 + i*2]
            elif hasTripleMarkerDuo and hasDef and hasColon and hasParentheses:  # seems like python function
                code = a.split("```")[1 + i*2]
            elif hasTripleMarkerDuo and guessPython: # guesswork
                code = a.split("```")[1 + i*2]

        except Exception as e:
            import traceback
            traceback.print_exception(e)
            #getPyCode1(a)
        return code

    def extractText(a, i):
        if(a.count("```") < (i+1)*2):
            return None
        text = None
        try:
            if hasTripleMarkerDuo:
                text = a.split("```")[1 + i*2]

        except Exception as e:
            import traceback
            traceback.print_exception(e)
            #getPyCode1(a)
        return text

    def getPyDefFnName(a):
        try:
            if(hasDef and hasParentheses):
                fnname = a.split("def")[1].split("(")[0]
                return fnname.strip()
        except Exception as e:
            import traceback
            traceback.print_exception(e)
            print(a)
        return None

    def getOneLinerList(answer):
        if(not hasMinuses):
            return []
        listed = list()
        for i in answer.split("\n"):
            if("-" in i):
                listed.append(i.strip("-").strip())
        return listed

    oneLiner = extractOneLiner(answer)
    code1 = extractPyCode(answer, 0)
    code2 = extractPyCode(answer, 1)
    code3 = extractPyCode(answer, 2)
    text = extractText(answer, 0)
    fnName = getPyDefFnName(answer)
    listed = getOneLinerList(answer)
    # ==================================
    # loading

    binaryLayer = defaultdict()

    # code
    binaryLayer["hasJson"] = hasJsonWord
    binaryLayer["hasCurly"] = hasCurlyBrackets
    binaryLayer["has{}"] = hasCurlyBrackets
    binaryLayer["has()"] = hasParentheses
    binaryLayer["has```"] = hasTripleMarker
    binaryLayer["has if"] = hasIf
    binaryLayer["has="] = hasEq
    binaryLayer["hasTripleMarker"] = hasTripleMarker

    # unity
    binaryLayer["unity"] = hasUnity
    binaryLayer["scene"] = hasScene
    binaryLayer["script"] = hasScript

    # logic
    binaryLayer["and"] = hasAnd

    # reasoning
    binaryLayer["correct"] = hasCorrect
    binaryLayer["find"] = hasFind
    binaryLayer["how"] = hasHow

    # intent
    binaryLayer["setup"] = hasSetup
    binaryLayer["add"] = hasAdd
    binaryLayer["put together"] = hasPutTogether

    # identify
    binaryLayer["object"] = hasObject
    binaryLayer["new"] = hasNew
    binaryLayer["work"] = hasWork

    # locations
    binaryLayer["here"] = hasHere
    binaryLayer["this"] = hasThis
    binaryLayer["there"] = hasThere
    binaryLayer["that"] = hasThat


    # work
    binaryLayer["mission"] = hasMission

    # binary
    binaryLayer["BLOCKNOT"] = blockNot
    binaryLayer["BLOCK1"] = block1
    binaryLayer["BLOCKOR"] = blockOr
    binaryLayer["BLOCKAND"] = blockAnd

    binaryLayer["code1"] = code1
    binaryLayer["code2"] = code2
    binaryLayer["code3"] = code3
    binaryLayer["fnName"] = fnName
    binaryLayer["hasCode"] = (hasTripleMarker and not hasJsonWord) or code1
    binaryLayer["hasOneLiner"] =hasOneLine
    binaryLayer["text"] =text
    binaryLayer["oneLiner"] =oneLiner
    binaryLayer["list"] =listed


    example='''
    generate sample for these words
    BLOCKAND, BLOCKOR, BLOCKNOT
    
    based on this example(use has.., func = qORa)
    
    hasUnity = qORa("unity")
    hasScene = qORa("scene")
    hasSetup = qORa("setup")
    
    binaryLayer["unity"] = hasUnity
    binaryLayer["scene"] = hasScene
    binaryLayer["script"] = hasScript

    self.hasCode = self.binaryLayer["hasCode"]
    self.hasIf = self.binaryLayer["has if"]
    self.hasTComm = self.binaryLayer["has```"]

    '''

    return binaryLayer


class BinaryConstruct:
    def __init__(self, q, a, outputFile = ""):
        # some code
        self.binaryLayer = binaryParser(q, a)
        self.outputFile = outputFile

        # masking
        self.hasJson = self.binaryLayer["hasJson"]
        self.hasBrackets = self.binaryLayer["has{}"]
        self.hasParentheses = self.binaryLayer["has()"]
        self.hasCode = self.binaryLayer["hasCode"]
        self.hasIf = self.binaryLayer["has if"]
        self.hasTComm = self.binaryLayer["has```"]
        self.hasEq = self.binaryLayer["has="]
        self.hasUnity = self.binaryLayer["unity"]
        self.hasScene = self.binaryLayer["scene"]
        self.hasCorrect = self.binaryLayer["correct"]
        self.hasFind = self.binaryLayer["find"]

        self.hasHow = self.binaryLayer["how"]
        self.hasThis = self.binaryLayer["this"]
        self.hasWork = self.binaryLayer["work"]
        self.hasHere = self.binaryLayer["here"]
        self.hasThis = self.binaryLayer["this"]
        self.hasAnd = self.binaryLayer["and"]
        self.hasThere = self.binaryLayer["there"]
        self.hasThat = self.binaryLayer["that"]

        self.hasPutTogether = self.binaryLayer["put together"]

        self.blockOr = self.binaryLayer["BLOCKOR"]
        self.blockAnd = self.binaryLayer["BLOCKAND"]
        self.block1 = self.binaryLayer["BLOCK1"]
        self.blockNot = self.binaryLayer["BLOCKNOT"]
        self.code1 = self.binaryLayer["code1"]
        self.code2 = self.binaryLayer["code2"]
        self.code3 = self.binaryLayer["code3"]
        self.fnName = self.binaryLayer["fnName"]
        self.hasOneLiner = self.binaryLayer["hasOneLiner"]
        self.oneLiner = self.binaryLayer["oneLiner"]
        self.list = self.binaryLayer["list"]
        self.text = self.binaryLayer["text"]
        self.codeall = ""
        if(self.code1 != None):
            self.codeall += self.code1
        if (self.code2 != None):
            self.codeall += self.code2
        if (self.code3 != None):
            self.codeall += self.code3

    def list(self):
        for i in self.binaryLayer:
            print(i, self.binaryLayer[i])

    def write(self, data):
        with open(self.outputFile, 'a') as f:
            f.write(data + '\n')

    def read(self):
        with open(self.outputFile, 'r') as f:
            return f.read()
        return None


"""
create language for navigating over data (strings, or images)
for example, for text, it would move to next chracter, for iamges to next pixel

-
What a fascinating idea!

Let's create a language for navigating over data. I'll outline a basic syntax and semantics for this language, and we can expand on it as needed.

**Language Name:** `DataNav` (short for Data Navigation)

**Syntax:**

`DataNav` is a command-based language. Each command consists of a verb (action) and an optional argument.

**Verbs (Actions):**

1. `MOVE`: Move to a specific position in the data.
	* Argument: `INDEX` (integer) or `RELATIVE` (e.g., `NEXT`, `PREVIOUS`, `FIRST`, `LAST`)
2. `SEEK`: Jump to a specific position in the data.
	* Argument: `INDEX` (integer)
3. `STEP`: Move a certain number of steps in a specific direction.
	* Argument: `COUNT` (integer) and `DIRECTION` (e.g., `FORWARD`, `BACKWARD`)
4. `SCAN`: Search for a specific pattern or value in the data.
	* Argument: `PATTERN` (string or regex) and optional `START_INDEX` (integer)
5. `EXTRACT`: Extract a subset of data.
	* Argument: `START_INDEX` (integer), `END_INDEX` (integer), and optional `STEP` (integer)

**Argument Types:**

* `INDEX`: An integer value representing a position in the data.
* `RELATIVE`: A keyword indicating a relative movement (e.g., `NEXT`, `PREVIOUS`, `FIRST`, `LAST`).
* `COUNT`: An integer value indicating the number of steps to move.
* `DIRECTION`: A keyword indicating the direction of movement (e.g., `FORWARD`, `BACKWARD`).
* `PATTERN`: A string or regex pattern to search for in the data.

**Examples:**

**Text Navigation**

* `MOVE NEXT` : Move to the next character in the text.
* `SEEK 10` : Jump to the 10th character in the text.
* `STEP 5 FORWARD` : Move 5 characters forward in the text.
* `SCAN "hello" START 5` : Search for the pattern "hello" starting from the 5th character in the text.
* `CEXTRACT 5` : Extract the substring for next 5 characters.
* `EXTRACT 5 10` : Extract the substring from the 5th to the 10th character (inclusive).

**Image Navigation**

* `MOVE NEXT PIXEL` : Move to the next pixel in the image.
* `SEEK (10, 20)` : Jump to the pixel at coordinates (10, 20) in the image.
* `STEP 3 PIXELS RIGHT` : Move 3 pixels to the right in the image.
* `SCAN "RGB(255, 0, 0)" START (10, 10)` : Search for the color red (RGB(255, 0, 0)) starting from the pixel at coordinates (10, 10) in the image.
* `EXTRACT (10, 10) (20, 20)` : Extract the subimage from coordinates (10, 10) to (20, 20) (inclusive).

This is a basic outline of the `DataNav` language."""
class PartialMechanism:

    # implement interpretor, and test it on example of iterating over text
    class DataNavInterpreter:
        def __init__(self, data):
            self.data = data
            self.position = 0

        def execute(self, command):
            verb, *args = command.split()
            if verb == 'MOVE':
                if args[0] == 'NEXT':
                    self.position += 1
                elif args[0] == 'PREVIOUS':
                    self.position -= 1
                elif args[0].isdigit():
                    self.position = int(args[0])
            elif verb == 'SEEK':
                self.position = int(args[0])
            elif verb == 'STEP':
                count = int(args[0])
                direction = args[1]
                if direction == 'FORWARD':
                    self.position += count
                elif direction == 'BACKWARD':
                    self.position -= count
            elif verb == 'SCAN':
                pattern = args[0]
                start_index = int(args[1])
                self.position = self.data.find(pattern, start_index)
                if self.position == -1:
                    self.position = start_index
            elif verb == 'EXTRACT':
                start_index = int(args[0])
                end_index = int(args[1])
                step = int(args[2]) if len(args) > 2 else 1
                if end_index >= len(self.data):
                    end_index = len(self.data) - 1
                return self.data[start_index:end_index + 1:step]
            elif verb == 'CEXTRACT':
                start_index = self.position
                count = int(args[0])
                end_index = start_index+count
                if end_index >= len(self.data):
                    end_index = len(self.data)
                return self.data[start_index:end_index]

            return self.position

        def get_current_char(self):
            if self.position < len(self.data):
                return self.data[self.position]
            return None

        @classmethod
        def tests(cls):
            # Test the interpreter
            data = "Hello, World!"
            interpreter = cls(data)

            # Move to the next character
            print(interpreter.execute("MOVE NEXT"))  # Output: 1
            print(interpreter.get_current_char())  # Output: e

            # Move to the 5th character
            interpreter.execute("SEEK 4")
            print(interpreter.get_current_char())  # Output: o

            # Step 2 characters forward
            interpreter.execute("STEP 2 FORWARD")
            print(interpreter.get_current_char())  # Output: ,

            # Scan for the pattern "World"
            interpreter.execute("SCAN World 5")
            print(interpreter.get_current_char())  # Output: W

            # Extract the substring from the 5th to the 10th character (inclusive)
            result = interpreter.execute("EXTRACT 4 10")
            print(result)  # Output: , Worl

            result = interpreter.execute("CEXTRACT 5") #World
            print(result)

            """This implementation supports the basic commands: `MOVE`, `SEEK`, `STEP`, `SCAN`, `EXTRACT`, 'CEXTRACT'.

            Feel free to modify and extend this implementation to support more features and data types!"""


#PartialMechanism.DataNavInterpreter.tests()

def fileExample():
    with open("example.txt", "r") as file:
        # Loop over each line in the file
        for line in file:
            # Remove the newline character at the end of each line
            line = line.strip()
            # Do something with the line, like print it
            print(line)


def imageExample():
    from PIL import Image

    # Open an image file
    img = Image.open('image.jpg')

    # Get the dimensions of the image
    width, height = img.size

    # Loop over each pixel in the image
    for x in range(width):
        for y in range(height):
            # Get the pixel at position (x, y)
            pixel = img.getpixel((x, y))

            # Do something with the pixel value
            print(f'Pixel at ({x}, {y}): {pixel}')

            # You can also modify the pixel value
            # img.putpixel((x, y), (255, 0, 0))  # Set the pixel to red

#from agentic_constructs import sendWithMessage
#a = sendWithMessage("")
#bin = BinaryConstruct(q, a)
#if (bin.hasJson):
#    pass