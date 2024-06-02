
tools=[
    "t001:category-time plot graph",
    "t002:word-memory optimizer and saver",
    "t003:categorized-chunk tracker with sources",
    "t004:code extractor",
    "t005:word tracker with sources"
]

prompts=[
    "designation000 -> tells type of prompt, plus it's id",
    "p001:summarize text"
]



#replace condition with correct

#replace code with correct
#if(condition)
    #code



#produce1
from core.mincore import sendWithMessage as ai
from core.mechanistic_layers import BinaryConstruct as Bin

possible=["<", ">", "or", "=", "and", "(", ")", "not", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
state = "x = 5\n"+"a = 10\n"+"y = 0"
structure = """if (condition):
                   pass
            """
answer = ai("fill out condition in python, where it checks if a is larger than x\n"+state+"\n"+structure, join=False)
code = Bin(" ", "".join(answer)).codeall
checking = str(code)
checking = checking.replace("if", "")
checking = checking.replace(":", "")
checking = checking[:checking.index("pass")]
checking = checking.replace(state, "")
split = checking.split()
print(split)
for i in split:
    for j in i:
        if(j in state or j in possible):
            continue
        else:
            raise Exception("invalid code: " + j +" "+ i)

print(checking)
print(answer)
