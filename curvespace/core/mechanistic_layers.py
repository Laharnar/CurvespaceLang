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

    def getPyCode(a):
        return extractPyCode(a, 0)
    def getPyCode1(a):
        return extractPyCode(a, 1)
    oneLiner = extractOneLiner(answer)
    code1 = getPyCode(answer)
    code2 = getPyCode1(answer)
    code3 = extractPyCode(answer, 2)
    fnName = getPyDefFnName(answer)
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
    binaryLayer["oneLiner"] =oneLiner


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
#from agentic_constructs import sendWithMessage
#a = sendWithMessage("")
#bin = BinaryConstruct(q, a)
#if (bin.hasJson):
#    pass