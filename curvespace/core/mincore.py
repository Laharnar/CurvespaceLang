import time

import groq
from groq import Groq
groqClient = Groq(api_key="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")

isGroq = True # false not implemented
usedModel = "llama3:70b"  # "phi3" # "gemma:2b" # mixtral
groqRandomness = 0.4
print(usedModel)
workContextStored = ""
USEREXPDELAY = 6

import threading
import time
from queue import Queue

queue = Queue()

def inputRecording_thread():
    while True:
        # do something
        user_input = input("'q'+enter stops AI ")
        if user_input.lower() == 'q':
            queue.put("abort")

def start_new_thread():
    my_thread = threading.Thread(target=inputRecording_thread)
    my_thread.start()

start_new_thread()


def requestAbort():
    if not queue.empty():

        # If there's something in the queue, get out of here
        print("Thread aborted")
        queue.pop()
        return True
    return False

def sendWithMessage(question, history=list(), name ="None", customDelay = 0, rng = groqRandomness, join =True):
    answer = sendandrecv(question, history, name, customDelay, rng)
    if(join):
        return "".join(answer)
    else:
        return answer

class Prompts:
    @classmethod
    def listItems(cls):
        return "List all names from this(list format: '-'):\n"

def sendandrecv(question, history=list(), name="None", customDelay=-1, rng=1):
    # ollama models
    # qwen:0.5b:   for speed bad answer
    # stable-code:   for fast code
    # mistral: pretty good
    # dolphin-mistral: pretty good lastest
    global USEREXPDELAY

    if(question == ""):
        print("AI WARNING: empty question")
        return ""
    if(USEREXPDELAY > 0 and customDelay == -1):
        time.sleep(USEREXPDELAY)
    elif(customDelay > 0):
        time.sleep(customDelay)
    items = list()
    for i in history:
        if(isinstance(i, str)):
            if ( i != ""):
                items.append({'role':'user', 'content':i, 'name':name}) # 'name':'Doe'
        else:
            items.append(i)
    if (isinstance(question, str)):
        items.append({'role':'user', 'content':question, 'name':name})
    else:
        if(isinstance(i, list)):
            for j in i:
                items.append(j)
        else:
            items.append(i)
    global usedModel
    while True:
        try:
            if(usedModel == "llama3:8b"):
                groqmodel = "llama3-8b-8192"
            elif(usedModel=="llama3:70b"):
                groqmodel = "llama3-70b-8192"
            elif(usedModel=="mixtral"):
                groqmodel = "mixtral-8x7b-32768"
            elif (usedModel == "gemma"):
                groqmodel = "gemma-7b-it"
            stream = groqClient.chat.completions.create(
                model=groqmodel,
                messages= items,
                #[
                    #{
                    #    "role": "user",  # "system"
                    #    "content": "potato is great",
                    #    "name": "Joe"
                    #}
                #],
                temperature=rng,
                max_tokens=800,
                timeout=20,
                top_p=1,
                stream=True,
                stop=None,
            )
            break
        except groq.BadRequestError as e:
            import traceback
            traceback.print_exception(e)
            break
        except Exception as e:
            import traceback
            traceback.print_exception(e)
            print("model failed")
            if (usedModel == "llama3:8b"):
                usedModel = "llama3:70b"
            elif (usedModel == "llama3:70b"):
                usedModel = "mixtral"
            elif (usedModel == "mixtral"):
                usedModel = "gemma"
            elif (usedModel == "gemma"):
                usedModel = "llama3:8b"
            print("new model", usedModel)

    #stream = ollama.chat(
    #    model=usedModel,
    #    messages=x, # {'role': 'user', 'content': question}
    #    stream=True,
    #    keep_alive=1
    #)
    #
    answer = []
    tokens = 0

    for chunk in stream:
        if(isGroq):
            print(chunk.choices[0].delta.content or "", end="")
            answer.append(chunk.choices[0].delta.content or "")
        else: # ollama
            print(chunk['message']['content'], end='', flush=True)
            answer += chunk["message"]["content"]
        tokens+=1

        if(requestAbort()):
            break
    print("\ntokens:",tokens)
    return answer

ai = sendWithMessage
def aiLang(task, canZeroShot=True, maxMem = 16, OUTPUT="1", solutions=list(), rng= 0.55):
    languages = list()
    result = list()
    answer = ai("+add <<SOLVED>> if its solved.=>\n"+task, history=solutions, rng=rng)
    result.append(task)
    result.append(answer)
    steps=1
    if(canZeroShot and "SOLVED" in answer):
        return answer
    language = ai("create new language for this\n" + task, history=solutions, rng=rng)
    solutions.append(task)
    result.append(language)
    solutions.append(language)
    steps=2
    while("SOLVED" not in answer):

        # it feels like this has just the right balance of prioritization and openness. removing "task" loses some
        # creating new language for every step alleviates on previous failures
        # this specific solution just FEELS like something else, like much more solid
        # concept of interjecting languages work to guide more
        # "solved" and solution, help with guiding to goal
        answer = ai("describe state of task, what was done so far, and prediction for how much work is left in ideal scenario.", [task, answer, "using language to complete task", language], rng=rng)
        language = ai("create new language for this", [task, answer], rng=rng)
        solutions = solutions[-maxMem:]
        solutions.append(answer)
        solutions.append(language)
        result.append(answer)
        result.append(language)
        answer = ai("implement and validate solution with provided language. reply <<SOLVED>> if it's solved.\n", solutions, rng=rng)
        steps+=2
    print("steps", steps)
    result.append(answer)
    result.append("steps "+ str(steps))
    if(OUTPUT == "1"):
        return answer
    return result

def ailoop(start):
    history = list()
    history.append(start)
    while(True):
        print("next:")
        x = input()
        if(".exit" in x):
            return
        answer = ai(x, history)
        history.append(x)
        history.append(answer)

def getTodosUserInc(answer):
    if(isinstance(answer, list)):
        answer = ai("extract TODOs. add <<USER>> if user should do these things.", answer)
    else:
        answer = ai("extract TODOs. add <<USER>> if user should do these things.", [answer])
    if( "USER" in answer):
        print("WAITING USER")
        return answer, input()
    return answer, ""

def aiCharLong(task, character, personality, canZeroShot=True):
    # character with infinte context
    solutions = list()
    languages = list()
    answer = ai("+add <<SOLVED>> if its solved.=>\n"+task)
    steps=1
    if(canZeroShot and "SOLVED" in answer):
        return answer
    solutions.append(task)
    language = ai("create new language for this\n" + task)
    solutions.append(language)
    hearts = list()
    steps=2
    metas = ai("what are meta-meta 5 layers in this", [character, personality, answer])
    view = ai("describe layout and view", [answer, language, metas])
    while("SOLVED" not in answer and steps > 2):

        # it feels like this has just the right balance of prioritization and openness. removing "task" loses some
        # creating new language for every step alleviates on previous failures
        # this specific solution just FEELS like something else, like much more solid
        # concept of interjecting languages work to guide more
        # "solved" and solution, help with guiding to goal
        answer = ai("describe state of task, what was done so far, and prediction for how much work is left in ideal scenario.", [task, answer, "using language to complete task", language, view])
        subhearts = list(hearts[-4:])
        for i in [character, personality, answer]:
            subhearts.append(i)
        heart = ai("react to it in character", subhearts)
        if("<<ABORT>>" in heart):
            print("ABORTING!!")
            break
        metas = ai("describe it in character what are abstract abstractions in this", [character, personality, heart])
        hearts.append(metas)
        hearts.append(heart)
        view = ai("describe layout and view in character", [character, personality, answer, metas])
        language = ai("create new language for this", [task, metas, answer, view])
        solutions.append(view)
        solutions.append(language)
        solutions.append(answer)
        # add interpretor solution first, then actual solution
        # use intermediate interpreted solution
        #  part A: interpretable solution with provided language, part B: usage of interpretor, part C: interpretor in py
        # these 3 should be split in multiple messages
        answer = ai("implement and validate solution with provided language. add interpretor solution first, then actual solution. reply <<SOLVED>> if it's solved.\n", solutions)
        print("impl end")
        #answer = ai("implement and validate solution with provided language. reply <<SOLVED>> if it's solved.\n", solutions)
        steps+=6
    print("steps", steps)
    return answer

def aiChar(task, character, personality, canZeroShot=True):
    # character with limited context
    solutions = list()
    languages = list()
    answer = ai("+add <<SOLVED>> if its solved.=>\n"+task)
    steps=1
    if(canZeroShot and "SOLVED" in answer):
        return answer
    solutions.append(task)
    language = ai("create new language for this\n" + task)
    solutions.append(language)
    hearts = list()
    steps=2
    metas = ai("what are meta-meta 5 layers in this", [character, personality, answer])
    view = ai("describe layout and view", [answer, language, metas])
    while("SOLVED" not in answer or steps <= 2):

        answer = ai("describe state of task, what was done so far, and prediction for how much work is left in ideal scenario.", [task, answer, "using language to complete task", language, view])
        subhearts = list(hearts[-4:])
        for i in [character, personality, answer]:
            subhearts.append(i)
        heart = ai("react to it in character, and it's accuracy", subhearts)
        if("<<ABORT>>" in heart):
            break
        metas = ai("describe it in character what are abstract abstractions in this", [character, personality, heart])
        hearts.append(metas)
        hearts.append(heart)
        view = ai("describe layout and view in character", [character, personality, answer, metas])
        language = ai("create new language for this", [task, metas, answer, view])
        solutions = solutions[-6:]
        solutions.append(view)
        solutions.append(language)
        solutions.append(answer)
        answer = ai("implement and validate solution with provided language. reply <<SOLVED>> if it's solved.\n", solutions)
        steps+=6
    print("steps", steps)
    return answer