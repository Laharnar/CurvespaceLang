import time
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
    x = list()
    for i in history:
        if(isinstance(i, str)):
            if ( i != ""):
                x.append({'role':'user', 'content':i, 'name':name}) # 'name':'Doe'
        else:
            x.append(i)
    if (isinstance(question, str)):
        x.append({'role':'user', 'content':question, 'name':name})
    else:
        x.append(i)
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
                messages= x,
                #[
                    #{
                    #    "role": "user",  # "system"
                    #    "content": "potato is great",
                    #    "name": "Joe"
                    #}
                #],
                temperature=rng,
                max_tokens=800,
                timeout=12,
                top_p=1,
                stream=True,
                stop=None,
            )
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
def aiLang(task, canZeroShot=True):
    solutions = list()
    languages = list()
    answer = ai("+add <<SOLVED>> if its solved.=>\n"+task)
    steps=1
    if(canZeroShot and "SOLVED" in answer):
        return answer
    solutions.append(task)
    language = ai("create new language for this\n" + task)
    solutions.append(language)
    steps=2
    while("SOLVED" not in answer):

        # it feels like this has just the right balance of prioritization and openness. removing "task" loses some
        # creating new language for every step alleviates on previous failures
        # this specific solution just FEELS like something else, like much more solid
        # concept of interjecting languages work to guide more
        # "solved" and solution, help with guiding to goal
        answer = ai("describe state of task, what was done so far, and prediction for how much work is left in ideal scenario.", [task, answer, "using language to complete task", language])
        language = ai("create new language for this", [task, answer])
        solutions.append(answer)
        solutions.append(language)
        answer = ai("implement and validate solution with provided language. reply <<SOLVED>> if it's solved.\n", solutions)
        steps+=2
    print("steps", steps)
    return answer

def getTodosUserInc():
    answer = ai("extract TODOs. add <<USER>> if user should do these things.", [answer])
    if( "USER" in answer):
        print("WAITING USER")
        input()

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
        subhearts = list(hearts[:-4])
        for i in [character, personality, answer]:
            subhearts.append(i)
        heart = ai("react to it in character", subhearts)
        if("<<ABORT>>" in heart):
            break
        metas = ai("describe it in character what are abstract abstractions in this", [character, personality, heart])
        hearts.append(metas)
        hearts.append(heart)
        view = ai("describe layout and view in character", [character, personality, answer, metas])
        language = ai("create new language for this", [task, metas, answer, view])
        solutions.append(view)
        solutions.append(language)
        solutions.append(answer)
        answer = ai("implement and validate solution with provided language. reply <<SOLVED>> if it's solved.\n", solutions)
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
        subhearts = list(hearts[:-4])
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
        solutions = solutions[:-6]
        solutions.append(view)
        solutions.append(language)
        solutions.append(answer)
        answer = ai("implement and validate solution with provided language. reply <<SOLVED>> if it's solved.\n", solutions)
        steps+=6
    print("steps", steps)
    return answer