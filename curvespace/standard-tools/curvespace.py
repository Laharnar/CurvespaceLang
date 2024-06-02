import os
import sys
import traceback
import json

from core import agentic_constructs

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../core/')))

from core.mechanistic_layers import BinaryConstruct
import core.agentic_constructs as ai

def getBranchesFrom(category, depth=5):
    pass

def collapseSameCategories(curve):
    pass

def multiConversation(histories):
    pass

class ConversationCurveSpace:
    def __init__(self, conversationHistory):
        # analyzes whole conversation at once
        pass

def autoCurves(message):
    pass

def autoCurvesLong(history):
    pass

class CurveGraphGeneral:
    def __init__(self, cats, message):
        # CurveGraph...
        pass

class CurveGraph:
    def __init__(self, categories=list()):
        self.categories = categories
        self.timeItems = list()

    def characterParser(self, message):
        cat = self.categories
        values = self.timeItems
        for i in range(len(message)):
            c = message[i]
            if(c not in cat):
                cat.append(c)
            values.append(c)
        return self

    def tokenParser(self, message):
        cat = self.categories
        values = self.timeItems
        for i in range(len(message)):
            c = message[i]
            if(c not in cat):
                cat.append(c)
            values.append(c)
        return self


    def catLastWordParser(self, message):
        cat = self.categories
        values = self.timeItems
        import re
        splitted_message = re.split(r'[ .\n]+', message)
        message = splitted_message
        if("" not in cat):
            cat.append("")
        minLength = self.getMinLength()
        last = cat.index("")
        for i in range(len(message)):
            c = message[i]
            for j in range(len(cat)):
                if(c in cat[j] and len(c) >= minLength): # in because items can be split
                    values.append([cat[j], c])
            else:
                values.append([cat[last], c])

        return self


    # assume that data items are in categories. cat = data, EXACT
    def asString(self):
        lines = []
        minLen = self.getMinLength()
        for i in self.categories:
            lines.append(f"{i:<{minLen}}:")
        lines.append(("-"* minLen)+":"+("- " * len(self.timeItems))+" ->t")
        for i in self.timeItems:
            idx = self.categories.index(i)
            lines[idx] += ". "
            for j in range(len(self.categories)):
                if(j == idx):
                    continue
                lines[j]+="  "
        return "\n".join(lines)

    def getMaxLength(self):
        maxLength= 0
        for i in self.categories:
            maxLength = max(len(i), maxLength)
        return maxLength

    def getMinLength(self):
        minLength= 1000000
        for i in self.categories:
            if(i != ""):
                minLength = min(len(i), minLength)
        return minLength

    # assume format is [categories] [[category, data]], where category-data isnt directly connected, but cat-cat is
    def asStringDisconnectedCats(self):
        lines = []
        maxCat = self.getMaxLength()
        for i in self.categories:
            lines.append(f"{i:<{maxCat}}:")
        lines.append(("-"*maxCat)+" "+("- " * len(self.timeItems))+" ->t")
        for i in self.timeItems:
            idx = self.categories.index(i[0])
            lines[idx] += ". "
            for j in range(len(self.categories)):
                if(j == idx):
                    continue
                lines[j]+="  "
        return "\n".join(lines)

    def columnSegments(message):
        segmentSize = 1000
        segments = []
        for i in range(0, len(message), segmentSize):
            segments.append(message[i:i+segmentSize])
        return segments

    # check if cat.CONTAINS data. partial is supported. AB <- A | B
    def asString2(self):
        lines = []
        for i in self.categories:
            lines.append(i+"\t|")
        lines.append("\t "+(" -" * len(self.timeItems))+" ->t")
        for i in self.timeItems:
            for j in range(len(self.categories)):
                if(i in self.categories[j]):
                    lines[j] += " ."
                    continue
                lines[j] += "  "
        return "\n".join(lines)

    def loadGraphData(self, isFull=False):
        lines = list()
        for i in self.timeItems:
            for j in range(len(self.categories)):
                if(i in self.categories[j]):
                    lines.append([self.categories[j], i])
                else:
                    if(isFull):
                        lines.append([None, None])
        return lines

    def collapseSymbols(self):
        modified = list()
        for i in range(0, len(self.categories)-1, 2):
            # get categories
            category = self.categories[i].isalpha()
            category2 = self.categories[i+1].isalpha()

            # parse
            if (category == category2 and category == True):
                modified.append(self.categories[i]+self.categories[i+1])
            else:
                modified.append(self.categories[i])
                modified.append(self.categories[i+1])
        self.categories = modified

    def collapseWordNonWord(self):
        modified = list()
        for i in range(0, len(self.categories), 2):
            # get categories
            category = self.categories[i].isalpha()
            if(i == len(self.categories)-1):
                modified.append(self.categories[i])
                continue

            category2 = self.categories[i+1].isalpha()

            # parse
            if (category == category2): ## true-true or false-false
                modified.append(self.categories[i]+self.categories[i+1])
            else:
                modified.append(self.categories[i])
                modified.append(self.categories[i+1])
        self.categories = modified

    def createConvertible(self):
        return self.loadGraphData(False)

    def convertedCatTo(self):
        catNew = list()
        for j in range(len(data)):
            i = data[j]
            if (i[0][0].isalpha()):
                catNew.append(["word", i[0]])
            elif (i[0][0].isdigit()):
                catNew.append(["number", i[0]])
            else:
                catNew.append(["undef", i[0]])

        return ["word", "number", "undef"], catNew, data

    def convertToStandard(self):
        cats, conv, convChar = self.convertedCatTo()
        for i in range(len(convChar)):
            data, char = convChar[i]
            convChar[i] = [conv[i][0], char]
        self.categories = cats
        self.timeItems = convChar

    def lineSegments(self, message):
        segmentSize = 1000
        segments = []
        for i in range(0, len(message), segmentSize):
            segments.append(message[i:i + segmentSize])
        return segments

    def columnSegments(self, message, columns=20):
        split = message.split("\n")
        chunks = list()
        for offsets in range(0, len(split[0]), columns):
            chunk = list()
            for j in split:
                idx = j.index(":")
                piece = j[0:idx + 1] + j[idx + 1 + offsets:idx + columns + offsets]
                chunk.append(piece)
            chunks.append("\n".join(chunk))
        return chunks

    def getAPI(self):
        """
        Returns a list of methods (functions) of the class instance
        """
        return [method_name for method_name in dir(self) if callable(getattr(self, method_name))]

def getAPI(object):
    """
    Returns a list of methods (functions) of the class instance
    """
    return [method_name for method_name in dir(object) if callable(getattr(object, method_name))]

import json

class CurveConversation:
    def __init__(self):
        self.conversationGraphs = list()

    def listed(self, alreadyRdy, question):
        listed = CurveGraph(alreadyRdy).catLastWordParser(question)
        self.conversationGraphs.append(listed)

    def prompt(self, answer):
        prompted = CurveGraph().tokenParser(answer)
        self.conversationGraphs.append(prompted)
        return prompted

    def history(self, history):
        for i in history:
            self.prompt(i)

    def getAPI(self):
        """
        Returns a list of methods (functions) of the class instance
        """
        return [method_name for method_name in dir(self) if callable(getattr(self, method_name))]

class CurveSpace:
    def __init__(self):
        self.curveCatTimes = []

    def add_curve_cat_time(self, curve_cat_time):
        self.curveCatTimes.append(curve_cat_time)

    def remove_curve_cat_time(self, curve_cat_time):
        self.curveCatTimes.remove(curve_cat_time)

    def save(self, filename):
        data = []
        for curve_cat_time in self.curveCatTimes:
            curve_data = {
                'categories': curve_cat_time.categories,
                'timeItems': curve_cat_time.timeItems
            }
            data.append(curve_data)
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    @classmethod
    def load(cls, filename):
        curve_space = cls()
        with open(filename, 'r') as f:
            data = json.load(f)
            for curve_data in data:
                categories = curve_data['categories']
                time_items = curve_data['timeItems']
                curve_cat_time = CurveGraph(categories)
                curve_cat_time.timeItems = time_items
                curve_space.add_curve_cat_time(curve_cat_time)
        return curve_space


def findStableCategories():
    # goes up in layers, generating meta until it finds stability of orbits
    pass

def findCommonCategories(prompt1, prompt2):
	# return 2 curves, and common category/ies
    # A) generate categories with ai
    # B) auto plug into known curvespace, and it finds common categories
	pass

def aiToCurve(message):
    graph = CurveGraph().characterParser(message)
    print(graph.asString())
    return graph


if __name__ == "__main__":
    someText = "parser.print_parsed_text()"
    while(True):
        user = input()
        #answer = ai.sendWithMessage(user)
        graph = CurveGraph().characterParser(user)
        print(graph.asString())
        graph.collapseWordNonWord()
        print(graph.asString2())
        graph.collapseWordNonWord()
        print(graph.asString2())
        print()
        data = graph.loadGraphData()
        graph.convertToStandard()

        print(graph.asStringDisconnectedCats())
        x = graph.asStringDisconnectedCats()
        answer = ai.sendWithMessage(user + "\nbellow is graph representing above sentence. dots represent instances of characters fitting in that category, and t represents time change\n"+x)
        break

        print(graph.asString2())
        graph = CurveGraph().characterParser(answer)
        print(graph.asString())
        expert = "As an expert list maker, please list each abstraction, as part of json surround entire list with ```.\n"+"List meta abstractions from this:\n"
        answer22 = ai.sendWithMessage(expert+user)
        answer23 = ai.sendWithMessage(expert+answer)
        expert = "As an expert list maker, make an abstraction list out of this abstraction list, as part of json surround entire list with ```.\n"+"This is text:\n"
        for i in range(100):
            answer22 = ai.sendWithMessage(expert + answer22)
            answer23 = ai.sendWithMessage(expert + answer23)

