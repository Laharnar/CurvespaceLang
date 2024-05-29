import io
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import ollama
import datetime
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'core/')))
from mechanistic_layers import BinaryConstruct

from groq import Groq
groqClient = Groq(api_key="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")


isGroq = True # false not implemented
usedModel = "llama3:70b"  # "phi3" # "gemma:2b" # mixtral
groqRandomness = 0.4
print(usedModel)
workContextStored = ""
USEREXPDELAY = 6

def setModel(model):
    global usedModel
    usedModel = model

def extract_codes(text):
    ttext = text
    if ("```python" in text):
        ttext = text.split("```python")[1].split("```")[0]
    if("```"in text):
        ttext = text.split("```")[1].split("```")[0]
    return ttext

def setDelayRate(rate):
    global USEREXPDELAY
    USEREXPDELAY = rate

# im missing append variation with multipass parsing
def sendWithFull(commands):
    aiexe(commands) # no mem


def sendWithFileSave(question, loadContextFile = "context/history_" + str(
        datetime.date.today()) + ".json", saveContextFile = "context/history_" + str(
        datetime.date.today()) + ".json", addContextFiles = list(), sending = True, character = ""):
    return sendrecvQ2(question, loadContextFile, saveContextFile, addContextFiles, sending, character)

def sendWithMessage(question, history=list(), name =None, customDelay = 0, rng = groqRandomness):
    return sendandrecv(question, history, name, customDelay, rng)

def sendandrecv(question, history=list(), name=None, customDelay=-1, rng=1):
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
        timeout=10,
        top_p=1,
        stream=True,
        stop=None,
    )

    #stream = ollama.chat(
    #    model=usedModel,
    #    messages=x, # {'role': 'user', 'content': question}
    #    stream=True,
    #    keep_alive=1
    #)
    #
    answer = ""
    tokens = 0

    for chunk in stream:
        if(isGroq):
            print(chunk.choices[0].delta.content or "", end="")
            answer += chunk.choices[0].delta.content or ""
        else: # ollama
            print(chunk['message']['content'], end='', flush=True)
            answer += chunk["message"]["content"]
        tokens+=1

        if(requestAbort()):
            break
    print("\ntokens:",tokens)
    return answer


def passableUserLoop(currentMessage):
    fixing = list()
    fixing.append(currentMessage)
    while(True):
        x = input()
        if("pass" in x):
            return fixing[-1]
        else:
            answer = sendWithMessage(x, fixing)
            fixing.append(answer)

def accessContext(question, defaultContext):
    contextes = list()

    # CONTEXT
    if "multicontext=" in question:
        start = question.rfind("multicontext=")
        end = question.find("\n", start)
        context = question[start: end]
        question = question[:start] + question[start + end:]
        contextFiles = context.split("=")[1]
        contextes = contextFiles.split(",")

    elif "context=" in question:
        start = question.rfind("context=")
        end = question.find("\n", start)
        end2 = question.find(" ", start)
        if(end == -1):
            end = end2
        if(end2 == -1):
            end2 = end
        end = min(end, end2)
        context = question[start: end]
        question = question[:start] + question[end:]
        contextFile = context.split("=")[1]
        contextFile = contextFile.split("\n")[0].strip()
        contextes.append(contextFile)
    else:
        if (defaultContext != ""):
            contextes.append(defaultContext)

    return contextes, question

def prepareSending(question, loadContextFile, saveContextFile, addContextFilesByNames=list(), character=None):
    # loads files
    q0 = question
    if(isinstance(question, dict)):
        if(len(question) == 2):
            question, addContextFilesByNames, character = question["request"], question["context"], character
        else:
            question, addContextFilesByNames, character = question["request"], question["context"], question["name"]
    today="context/history_"+str(datetime.date.today())+".json"
    if (loadContextFile == ""):
        loadContextFile = today
    if (saveContextFile == ""):
        saveContextFile = today

    print("quid?-->AI:", question)
    # first context file : daily history, same as output
    qOriginal = question
    firstFile = loadContextFile
    contextes, questionMinusEvent = accessContext(question, firstFile)
    question = questionMinusEvent

    contextSaveFile = saveContextFile
    # CONTEXT

    if "contextSave=" in question: # in action
        start = question.rfind("contextSave=")
        end = question.find("\n", start)
        if(end == -1):
            context = question[start:]
        else: context = question[start: end]
        # doesnt parse last " well, eats it incorrectly
        question = question[:start] + question[end:]
        contextSaveFile = context.split("=")[1].replace("\"", "", 2)
        contextSaveFile = contextSaveFile.split("\n")[0].strip()
    print("CONTEXT SAVE...", contextSaveFile)

    for i in addContextFilesByNames:
        contextes.append(i)

    conxOfChunks = list()
    for conx in contextes:
        print("CONTEXT... ", conx)
        if(conx == ""):
            print("ERRORR empty contexts", contextes)
            continue
        chunks = localContext(conx)
        conxOfChunks.append(chunks)
    return question, contextSaveFile, conxOfChunks, firstFile

def sendrecv(question, loadContextFile = "context/history_"+str(datetime.date.today())+".json", saveContextFile="context/history_"+str(datetime.date.today())+".json", addContextFiles = list(), sending =True, character=""):
    return sendrecvQ2(question, loadContextFile, saveContextFile, addContextFiles, sending, character)[0]

def sendrecvQ2(question, loadContextFile = "context/history_"+str(datetime.date.today())+".json", saveContextFile="context/history_"+str(datetime.date.today())+".json", addContextFiles = list(), sending =True, character=""):
    q0 = question
    question, contextSaveFile, conxOfChunks, usedLoad = prepareSending(question, loadContextFile, saveContextFile, addContextFiles, character)
    # run with context chunks
    answers = ""
    for chunks in conxOfChunks:
        answer = ""
        if(sending):
            print("WAITING... ", question, chunks)
            answer = sendandrecv(question, chunks, character)
        else: print("SKIPPING...", question)
        answers += answer+"\n&>\n"
    answers = answers[0:len(answers)-4]
    saveToHistory(contextSaveFile, question, answers)
    return answers, question

def constructHistory(contentChunks, fileName = "context/temp.json", edit='a'):
    if(isinstance(contentChunks, list)):
        temp = "\n===================================\n".join(contentChunks)
    else: temp = contentChunks + "\n===================================\n"
    saveToFile(fileName, temp, edit)
    return fileName

def localContext(filePath):
    try:

        import os
        print("GETTING CONTEXT...", filePath)

        if os.path.dirname(filePath):
            os.makedirs(os.path.dirname(filePath), exist_ok=True)

            dir_path = os.path.dirname(filePath)
            if not os.path.exists(dir_path):
                print("FAILED TO CREATE DIRECTORY...", dir_path, filePath)
                time.sleep(6)

        with open(filePath, 'a') as file:
            pass

        with open(filePath, 'r') as file:
            lines = file.read()
            #lines = lines.replace("---->", "")
            chunks = lines.split("\n***********************************\n")
            # loads up to 2 **** lines for recent context
            CHUNKSTOLOAD = HISTORYLD = 4
            n = CHUNKSTOLOAD
            if(len(chunks) > n):
                subchunks = chunks[-(n+1):]
                subchunks = "\n===================================\n".join(subchunks)
                subchunks.strip("\n===================================\n")
                chunks = subchunks
            elif(chunks == ['']): # for empty
                if(lines == ''):
                    chunks.clear()
                else:
                    chunks = lines
            if(len(chunks) > 0):
                chunks = "".join(chunks)
                chunks = chunks.split("===================================\n")
                while("" in chunks):
                    chunks.remove("")

            return chunks
    except io.UnsupportedOperation as ee:
        print("unsupported operation", ee)
        pass
    except Exception as e:
        import traceback
        traceback.print_exception(e)
        print("exception", e)
        time.sleep(1)
        pass
    return list()

def saveToHistory(historyFile, question, answer):
    if(historyFile == ""):
        return
    qa = question +"\n---->\n" + answer
    try:
        maxxed = False
        counted = 0
        with open(historyFile, 'a') as file:
            pass
        with open(historyFile, 'r') as file:
            lines = file.readlines()
            for i in lines:
                if "===============" in i:
                    counted += 1
                if "***************" in i:
                    maxxed = True
                    counted = 0
    except io.UnsupportedOperation as ee:
        print("unsupported operation", ee)
        pass
    except Exception as e:
        import traceback
        traceback.print_exception(e)
        print("exception", e)
        time.sleep(1)
        pass
    MAXCT = 3
    if((counted % MAXCT) == 0 and counted > 0):
        saveToFile(historyFile, qa + "\n***********************************\n", 'a');
    else:
        saveToFile(historyFile, qa + "\n===================================\n", 'a');

def saveToFile(fileOut, answer, io):
    # io: 'a', 'w', 'r'
    try:
        with open(fileOut, io) as file:
            file.writelines(answer)
    except io.UnsupportedOperation as ee:
        print("unsupported operation", ee)
        pass
    except Exception as e:
        print("exception", e)
        time.sleep(1)
        pass


def readMemLine(memory, i, sep=":"):
    # parses mem lines in middle of "ai" + reads that file
    if "mem"+sep in i:
        def parseMem(line):
            # parse example: "mem: conciseai.txt more info"
            contents = line.split(sep)[1].strip()
            memory_path = contents.split(" ")[0]
            return memory_path

        memory_path = parseMem(i)
        print("mem"+sep, memory_path)
        try:
            with open(memory_path, 'r') as file:
                memoryFile = file.read()
                memory.append(memoryFile)
        except FileNotFoundError as af:
            print(af)
        return True
    return False

def unpackRecvActions(requestLines, torm):
    for i in requestLines:
        if "!!#" in i:
            torm.append(i)
    for i in torm:
        requestLines.remove(i)
    return len(torm)

def parse_line(line):
    # Parse line into action, request, run times, and mode
    parts = line.split(':')
    run_times = 1
    mode = "ai1"
    if len(parts) > 1:
        # Get action on right of ai
        aiplusaction = parts[0]
        if("ai" not in aiplusaction):
            aiplusaction = parts[1]
        action = aiplusaction.split(marker + ' ai')[1].strip()
        if ("-" in action):
            numberAct = action.split(" ")[0]
            number = numberAct[1:].strip()[0]
            run_times = int(number)
            mode = "ai2"
        request = ":".join(parts[1:]).strip()
    else:
        action = line.split(marker + ' ai')[1].strip()
        request = ""
        run_times = 1
    return action, request, run_times, mode

def parse_header(line):
    global marker
    # Find header for section: # ai action: multiline request \n ok--
    if line.__contains__(marker + 'ai-'):
        action, request, run_times, mode = parse_line(line)
        return action, request, run_times, mode
    if line.__contains__(marker + ' ai'):
        return parse_line(line)
    return None, None, None, None

def extractExecutableSection(line, marker, lines, lineId):
    # collectes single command
    lineOfAI = -1
    requestLines = list()
    found = 0
    action = ""
    mode = "ai1"
    request = None
    if line.__contains__(marker + ' ok--'):
        # go upwards until hitting "ai"
        for i in range(lineId):
            action, request, times, mode = parse_header(lines[lineId - i - 1])

            # normal line
            if (request == "" or request == None):
                requestLines.insert(0, lines[lineId - i - 1])
            else:  # header line, ai1, or ai2
                requestLines.insert(0, request + "\n")
            if (mode != None):
                found = times
                lineOfAI = lineId - i - 1
                break
    return requestLines, lineOfAI, found, action, mode, request

def recognize_and_process(line, lines, lineId, file, memFile, knownMem, limits, torm, alwaysSavePath = ""):
    global marker

    action = ""
    # lineOfAi: in lines, not in sectionlines
    sectionLines, lineOfAI, foundTimes, action, mode, request = extractExecutableSection(line, marker, lines, lineId)
    # UP: GETTING DATA

    # DOWN: EXECUTING DATA -- send action
    def parseExecuteSection(lineOfAI, request):
        modifications = []

        if(mode == "ai2"):
            unpackRecvActions(sectionLines, torm)
            print("YES FOUND IS 0?", foundTimes)
            from arrow_agent import chainshots
            answer = chainshots(foundTimes, sectionLines, workContextStored, workContextStored)
            modifications.append((marker+" ok--", answer+"\n"+marker+" ok=="))
            return True, modifications, lineOfAI


        # early break if no ai
        if(foundTimes == 0 or (":" not in lines[lineOfAI])):
            return False, [], lineOfAI

        section = "\n".join(sectionLines)
        from runAgents import agentexe
        ran, answer = agentexe(action, section, keepconf=("+conf" in action))
        if (ran):
            if (answer != None):
                modifications.append((marker+" ok--", marker+" ok==\n"+answer))
            else:
                modifications.append((marker + " ok--", marker + " ok=="))
            return True, modifications, lineOfAI

        msgSent = False

        # process
        additional = ""
        printAdd = ""
        if ('\'' in action or "work" in action):
            additional += " memory: " + memFile
            printAdd += "(+MEM)"

        def extractMem(lines, memList):
            for k in lines:
                if ("mem=" in k):
                    readMemLine(memList, k, "=")
                else:
                    # this way lines stay near memory that calls on them, even if mem is in middle of it
                    memList.append(k)
        memList = list()
        context = list()
        alwaysAdd = ""
        for i in lines:
            # action of alwaysadd
            if "alwaysadd" in i and "ai" in i and ":" in i:
                for j in range(i + 1, len(lines)):
                    if "ok--" in lines[j]:
                        requestLines1, lineOfAI1, found1, action1, request1 = extractExecutableSection(line, marker, lines, lineId)
                        extractMem(requestLines1, memList)
                        alwaysAdd += "always:\n".join(requestLines1)+"\n===================================\n"
                        break


        # filter out which request lines to keep
        extractMem(sectionLines, memList)
        additional += "\n".join(memList)

        def readLast(lineOfAI, seekCompiled=False):
            if (seekCompiled):
                ending = "=="
            else:
                ending = "--"
            previousLine = lineOfAI
            for i in range(previousLine):
                if lines[previousLine - i].__contains__(marker + ' ok' + ending):
                    previousLine = previousLine - i
                    break
            lastLines = list()
            for i in range(previousLine):
                action, request, found, times, mode = parse_header(lines[previousLine - i - 1])
                if (found):
                    lastLines.insert(0, request)
                else:
                    lastLines.insert(0, lines[previousLine - i - 1])
                if (found):
                    lineOfAI = previousLine - i - 1
                    break
            else:
                lastLines.clear()
            return lastLines, lineOfAI

        #not duplicate request
        request = additional
        if(alwaysAdd != ""):
            context.append(alwaysAdd)

        if 'file' in action:
            context.append(file)
            printAdd += "(+FILE)"

        if ("file" == action):
            print("WAITING FOR AI... ", printAdd)
            request = {"request":request, "context":context}
            answer = sendrecv(request, )
            modifications.append((marker + " ok--", answer + "\n" + marker + " ok=="))
        if( "nocontext" in action):
            if(len(context) > 0):
                print("NOCONTEXT...")
                context.clear()


        if 'last' in action:
            lastLines, lineOfAI = readLast(lineOfAI-1, True)
            compiledRequest = request+str("\n".join(lastLines))
            request = compiledRequest
            printAdd += "(+LAST)"

        if 'last2' in action:
            lastLines, lineOfAI = readLast(lineOfAI-1, True)
            lastLines2, lineOfAI = readLast(lineOfAI-1, True)
            compiledRequest = request + str("\n".join(lastLines)) + str("\n".join(lastLines2))
            request = compiledRequest
            printAdd += "(+LAST2)"

        if 'last3' in action:
            lastLines, lineOfAI = readLast(lineOfAI-1, True)
            lastLines2, lineOfAI = readLast(lineOfAI-1, True)
            lastLines3, lineOfAI = readLast(lineOfAI-1, True)

            compiledRequest = request + str("\n".join(lastLines)) + str("\n".join(lastLines2)) + str("\n".join(lastLines3))
            request = compiledRequest
            printAdd += "(+LAST3)"

        if 'approx' in action:
            request += " \n -Only approximate result. \n -accuracy everywhere isnt required \n -separate things that are accurate for sure, and approximate"
            printAdd += "(+APPROX)"

        if 'docs' in action:
            prompt = "ai file:what are public functions in this file? add brief explanation of each function."
            msgSent = True
            print("WAITING FOR AI... request:", request + prompt)
            request = {"request":request + prompt, "context":context}
            answer = sendrecv(request)
            modifications.append((marker+" ok--", answer+"\n"+marker+" ok=="))
        if 'short' in action:
            instruction = "instruction: write same thing, but in way shorter form. make sure meaning is preserved. Its fine to copy more complicated parts, because perserving quality is more important, than length of text."
            msgSent = True
            print("WAITING FOR AI(+SHORT)... request:", request + instruction)
            request = {"request":request + instruction, "context":context}
            answer = sendrecv(request)
            modifications.append((marker+" ok--", answer+"\n"+marker+" ok=="))
        if 'chain' in action:
            question, chain = chainQuestionToList(request)
            print("WAITING FOR AI(+CHAIN)+" + action + "... request:", request)
            answer = runChain(question, chain)
            modifications.append((marker+" ok--", answer+"\n"+marker+" ok=="))
            msgSent = True
        if 'line-by-line' in action:
            lastLines = request.split("\n")
            answer = ""
            for i in lastLines:
                compiledRequest = str(i)
                if(compiledRequest == ""):
                    continue
                compiledRequest += ""
                print("WAITING FOR AI(+line-by-line)...  request:", compiledRequest)
                answer += sendrecv({"request": compiledRequest, "context": context}) + "\n"
            modifications.append((marker+" ok--", answer+"\n"+marker+" ok=="))
            msgSent = True
        if "save=" in action:
            def saveAuto(action):
                fileOut = action.split("=")[1].split(" ")[0].strip()
                print("WAITING FOR AI(+SAVE)+"+action+"... request:", request)
                request = {"request": request, "context": context}
                answer = sendrecv(request)
                modifications.append((marker + " ok--", marker + " ok=="))

                saveToFile(fileOut, answer, 'a')
            saveAuto(action)
            msgSent = True
        if "replace=" in action:
            def replaceAuto(action):
                fileOut = action.split("=")[1].split(" ")[0].strip()
                print("WAITING FOR AI(+REPLACE)+"+action+"... request:", request)
                request = {"request": request, "context": context}
                answer = sendrecv(request)
                modifications.append((marker + " ok--", marker + " ok=="))
                try:
                    with open(fileOut, 'w') as file:
                        ff = file.read()
                        ff = ff.replace(request, answer)
                        file.writelines(ff)
                except io.UnsupportedOperation as ee:
                    print("unsupported operation", ee)
                    pass
                except Exception as e:
                    print("exception", e)
                    time.sleep(1)
                    pass
            replaceAuto(action)
            msgSent = True

        if 'reply' in action:
            msgSent = True
            print("WAITING FOR AI... (+REPLY) request:", request)
            textPart = request
            request = {"request": request, "context": context}
            answer = sendrecv(request)
            modifications.append((textPart.strip("\n"), answer + "\n"))
            modifications.append((marker + " ok--", marker + " ok==\n"))

        if 'code' in action:
            # maybe doesnt work, applies save at end
            msgSent = True
            print("WAITING FOR AI... (+CODE) request:", request)

            request = {"request": request+ ''' Clear start. Implement as if you are senior dev. IMPORTANT:
                                            - provide conceptual entry and exit point that clearly link to request 
                                            - focus on making functions, that are then connected
                                            - internally make an outline how to code this 
                                            - focus on important parts, add necessary details
                                            - dont overexplain
                                            - avoid explanation if possible
                                            - verify it's correct \n''', "context": context}
            answer = sendrecv(request)
            modifications.append((marker + " ok--", marker + " ok==\n"+answer))

        if 'cod-fun' in action:
            # maybe doesnt work, applies save at end
            msgSent = True
            print("WAITING FOR AI... (+FUNCTIONAL_CODE) request:", request)

            request = {"request": request+ ''' Clear start. Implement as if you are senior functional programmer. IMPORTANT:
                                            - write code, prefer functions
                                            - plan this as series of inputs-outputs
                                            - consider working with analogy "landmark-bridge-landmark", where you set landmarks, and make a bridge connecting them
                                            - dont overexplain
                                            - reason why it's correct \n''', "context": context}
            answer = sendrecv(request)
            modifications.append((marker + " ok--", answer+"\n"+marker + " ok==\n"))
        if 'split' in action:
            call = "check text above and split it in 2 reasonably. use =========== as separator."
            msgSent = True
            print("WAITING FOR AI... (+SPLIT) request:", request)
            request = {"request": request + call, "context": context}
            answer = sendrecv(request)
            modifications.append((marker + " ok--", marker + " ok==\n" + answer))

        if 'api-gen' in action:
            call = "you are coder that is working on this specific part of code. imagine you have values like a tree and this is one of the leafes. you have access to this API"
            # maybe doesnt work, applies save at end
            msgSent = True
            print("WAITING FOR AI... (+API-GENERATE) request:", request)
            request = {"request": request + call, "context": context}
            answer = sendrecv(request )
            modifications.append((marker + " ok--", marker + " ok==\n" + answer))
        if 'tree=' in action:
            path = action.split("=")[1].strip("\"")

            def list_directory_hierarchy(folder):
                print("looking at hierarchy", folder)
                content = ""
                for root, dirs, files in os.walk(folder):
                    level = root.replace(folder, '').count(os.sep)
                    indent = '+' * 2 * (level)
                    line = f"{indent}{os.path.basename(root)}/"
                    print(line)
                    content += f"{line}\n"
                    sub_indent = '+' * 2 * (level + 1)
                    for file in files:
                        line = f"{sub_indent}{file}"
                        print(line)
                        content += f"{line}\n"
                return content
            hierarchy = list_directory_hierarchy(path) + "\n"
            hieFile = constructHistory(hierarchy, edit='w')
            request = {"request": request, "context": context}
            answer = sendrecv(request, loadContextFile=hieFile)
            modifications.append((marker + " ok--", answer + "\n" + marker + " ok=="))
            msgSent = True

        if 'api' in action:
            from lined_agent import apiRequest
            call = apiRequest(request)
            msgSent = True
            print("WAITING FOR AI... (+API) ")
            request = {"request": call, "context": context}
            answer = sendrecv(request)
            from lined_agent import apiReceive
            if(apiReceive(answer)):
                modifications.append((marker + " ok--", answer+"\n"+marker + " ok=="))
            else:
                modifications.append((marker + " ok--", marker + "ok--\n"+marker+" ok=="))
        inserting=False
        if "insert" in action:
            inserting = True

            lastStored = "Not found."
            for ik in knownMem:
                if (ik["request"] == sectionLines[0]):
                    lastStored = ik["answer"]
                    break
            print("INSERTING last")
            modifications.append((marker + " ok--", lastStored +"\n"+ marker + " ok=="))
        if "chat" in action:
            lastAnswer = ""
            while(True):
                print("direct:")
                ainput = input()
                request = {"request": "consider this input for next step" + ainput + " last answer:" + lastAnswer, "context": context}
                answer = sendrecv(request)
                lastAnswer = answer
                next = input("next?(y/n)")
                if (next == "n"):
                    modifications.append((marker + " ok--", answer + "\n" + marker + " ok=="))
                    break
        if 'extract' in action:
            # empty to just get result back
            request = {"request": request, "context": context}
            answer = sendrecv(request, workContextStored, workContextStored,sending= False)
            modifications.append((marker + " ok--", marker + " ok=="))
            msgSent = True

        if ('nocontext' in action):
            if(len(context) > 0):
                print("NOCONTEXT...")
                context.clear()
        if '' == action or action=="work" or action=='last' or (not msgSent and not inserting):
                msgSent = True
                print("WAITING FOR AI... "+printAdd)
                preRequest = request
                maxMem = -1
                if "mem_size" in limits:
                    maxMem = limits["mem_size"]
                if(maxMem > -1):
                    context = context[: (-maxMem)]
                print("MEM limit:", maxMem, "->", len(context))
                request = {"request": request, "context": context}
                if 'nohistory' in action or 'nocontext' in action:
                    answer, qo = sendrecvQ2(request, "")
                else:
                    if(workContextStored != ""):
                        answer, qo = sendrecvQ2(request, workContextStored, workContextStored)
                    else: answer, qo = sendrecvQ2(request)
                    if (alwaysSavePath):
                        saveToHistory(alwaysSavePath, qo, answer)

                if('next' in action):
                    modifications.append((marker + " ok--", marker + " ok==\n"+marker +" ai:" + answer + marker +" ok-- "))
                if("modify"in action):
                    sepAnswerEnd = "=======\n"+ answer+"\n"+marker+" ok=="
                    modifications.append((marker + " ok--", sepAnswerEnd))
                if('after' in action):
                    endAnswer = marker+" ok==\n"+answer
                    modifications.append((marker+" ok--", endAnswer))
                else:
                    modifications.append((marker+" ok--", answer+"\n"+marker+" ok=="))
                knownMem.append({"request": sectionLines[0],"answer": answer})
        if "sleep=" in action:
            items = action.split(" ")
            for i in items:
                if("sleep=" in i):
                    toActivate = action.split("=")[1]
                    time.sleep(int(toActivate))
                    break

        if(inserting):
            msgSent = True


        return msgSent, modifications, lineOfAI
    return parseExecuteSection(lineOfAI, request)

def applyModifications(lastState, currentState, modifications, lineOfAI, torm):

    commands = lastState
    lines = currentState
    precondition = commands[lineOfAI]
    foundI = -1
    endI = -1
    for i, line in enumerate(lines):
        if (precondition in line):
            foundI = i
        if(foundI != -1 and "ok--" in line):
            endI = i
            break
    if (foundI != -1):
        recv = commands[foundI:endI]
        unpackRecvActions(recv, torm)
        handled = list()
        for i in torm:
            if("!!#put" in i):
                for j in recv:
                    modifications.append((j, ""))
                modifications.append((i, ""))
                modifications.append(("# ok==", ""))
                handled.append(i)
        for i in handled:
            torm.remove(i)
        for i in torm: # remove recv actions
            modifications.append((i, ""))
        for indexing in modifications:


            for j, line in enumerate(lines):
                x = line.find(indexing[0])
                if (x == -1):
                    continue
                toReplace = j
                wasReplaced = lines[toReplace]
                lines[toReplace] = lines[toReplace].replace(indexing[0],
                                                            indexing[1])
                if(wasReplaced != lines[toReplace]):
                    break
                else:
                    print("potential replace error? line:", toReplace, lines[toReplace], indexing)
                    pass
    return lines

def parseAiFile(memory, commands, allFile, knownMem=list(), limits = dict(), afterActions=list(), alwaysSavePath=""):
    currentTime = datetime.datetime.now()

    changed = False
    id = 0
    compiledMemory = "".join(memory)
    modifications = list()
    lineOfAI = -1

    sections = getSections(allFile, marker)
    print(sections)
    # todo: for unhandled sections, run handleSection
    # then re-read file and  --> +sections = getSections(allFile, marker)
    # find matching sections
    # apply modifications to sections
    # run packSection, on all sections, that handles !!#

    # ==> from section get action
    # - get optional, mem, context, limits
    # - cleanup modifications to section
    # - pass modified + action
    # return -- apply modifications
    for command in commands:
        changed, modifications, lineOfAI = recognize_and_process(command.strip(), commands, id, allFile, compiledMemory,
                                                              list(), limits, afterActions, alwaysSavePath)
        if (changed):
            print()
            break
        id += 1

    return modifications, lineOfAI, changed, currentTime


# ============================== NEW
def getSections(file_text, marker ="#"):
    sections = []
    in_section = False
    section_text = ''
    handled = False
    incomplete = False

    lines = file_text.splitlines()
    for i, line in enumerate(lines):
        line = line.strip()
        if marker in line:
            if line.strip().startswith(marker+" ai"):
                in_section = True
            elif line.strip().startswith( marker+" ok"):
                in_section = False
                section_text += line + '\n'
                if '--' in section_text:
                    handled = False
                elif '==' in section_text:
                    handled = True
                sections.append({"section":section_text, "complete":handled})
                print(section_text)
                section_text = ""
        if in_section:
            section_text += line + '\n'
    return sections

def fileGetSections(file_path):
    with open(file_path, 'r') as file:
        file_text = file.read()
    return getSections(file_text)
# ==============================

# for external, no memory function, runs actions
# parses single exact command.
# for text prefer parseText()
# requires "ai: formatting"
def aiexe(commands):
    memSize = -1
    if isinstance(commands, dict):
        memSize = commands["mem_size"]
        commands = commands["prompt"]

    print("\r" in commands)
    if(isinstance(commands, str)):
        commands = commands.split("\n")
    print("processing:", commands)
    allFile = "\n".join(commands)

    # preload memory
    memFiles = list()
    for i in commands:
        readMemLine(memFiles, i)

    limits = {"mem_size":memSize}
    afterActions = list()
    modifications, lineOfAI, save, currentTime = parseAiFile(memFiles, commands, allFile, limits=limits, afterActions=afterActions)

    if (save):
        print(currentTime, "end processing", str(datetime.datetime.now()),
              "duration", str(datetime.datetime.now() - currentTime))

    lines = applyModifications(commands, commands, modifications, lineOfAI, afterActions)
    return "\n".join(lines)

def runChain(question, chain):
    answer = ""
    final = ""
    for i in chain:
        subanswer= ""
        if(answer != ""):
            subanswer = answer + "\n"
        subanswer += "# ai"+i +". Original question:" +question
        if(answer != ""):
            subanswer += " Next lines are conversation so far. "
        quest = subanswer + " \n# ok--"
        answer = aiexe(quest)
        final = answer
        print("END PASS ==================")
    return final

def chainQuestionToList(input_string):
    lines = input_string.split("\n")
    chain = []
    firstLine = lines[0]
    nextLines = lines[1:-1]
    if(":" in firstLine):
        question = firstLine.split(":")[1]
    else:
        question = firstLine
    for line in nextLines:
        chain.append(line)
    return question, chain

class ProjectTracker(FileSystemEventHandler):
    def __init__(self, extensions):
        super().__init__()
        self.knownMem = list()
        self.extensions = extensions

    def on_modified(self, event):
        def process_command_file(file_path):
            print("processing file", file_path, datetime.datetime.now())
            try:
                with open(file_path, 'r') as file:
                    commands = file.readlines()
            except PermissionError as pe:
                print("permission error?", pe, "Check if folder has read only permission(right click/properties).")
                return ""
            except UnicodeDecodeError as ude:
                import traceback
                traceback.print_exception(ude)
                return ""
            return commands

        if any(event.src_path.endswith(ext) for ext in self.extensions):
            saveFile = event.src_path
            commands = process_command_file(saveFile)

            modifications, lineOfAI, afterActions = self.parseText(commands)
            save = False
            if(len(modifications) > 0 and lineOfAI > -1):
                save = True
            if (save):
                # after it's done, file might already be updated, so reload it
                while (True):
                    try:
                        with open(saveFile, 'r') as file:
                            lines = file.readlines()
                            lines = applyModifications(commands, lines, modifications, lineOfAI, afterActions)

                        break
                    except io.UnsupportedOperation as ee:
                        print("unsupported operation", ee)
                        time.sleep(1)
                        pass
                    except Exception as e:
                        import traceback
                        traceback.print_exception(e)
                        print("exception", e)
                        time.sleep(1)
                        pass
                while (True):
                    try:
                        with open(saveFile, 'w') as file:
                            file.writelines(lines)
                            break
                    except io.UnsupportedOperation as ee:
                        print("unsupported operation", ee)
                        time.sleep(1)
                        pass
                    except Exception as e:
                        import traceback
                        traceback.print_exception(e)
                        print("exception", e)
                        time.sleep(1)
                        pass

            else:
                print("end processing(pass)")

    def parseText(self, commands):
        allFile = "".join(commands)

        # preload memory
        memory = list()
        for i in commands:
            readMemLine(memory, i)

        global workContextStored
        workContextStored = ""
        alwaysSave= ""
        # the other call doesnt have set history
        for i in commands:
            if ("sethistory=" in i):
                items = i.split(" ")
                for k in items:
                    if ("sethistory=" in k):
                        workContextStored = k.split("=")[1].strip("\n:")
                        print("SETTING history:", workContextStored)
                    if ("extrasave=" in k):
                        alwaysSave = k.split("=")[1].strip("\n:")

        # restrict recent memory
        if(len(self.knownMem)>10):
            self.knownMem.pop(0)

        afterActions = list()
        modifications, lineOfAI, save, currentTime = parseAiFile(memory, commands, allFile, self.knownMem, afterActions=afterActions, alwaysSavePath= alwaysSave)

        print(currentTime, "end processing", str(datetime.datetime.now()),
                  "duration", str(datetime.datetime.now() - currentTime))
        return modifications, lineOfAI, afterActions

    def start_tracking(self, folder_path):
        observer = Observer()
        observer.schedule(self, folder_path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()


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
        pass


def start_new_thread():
    my_thread = threading.Thread(target=inputRecording_thread)
    my_thread.start()


def requestAbort():
    if not queue.empty():

        # If there's something in the queue, get out of here
        print("Thread aborted")
        queue.pop()
        return True
    return False


import subprocess
import traceback

def run_ollama_command(installModel):
    # Conceptual entry point: Define the command to run
    cmd = "ollama pull "+installModel

    try:
        # Run the command using subprocess
        process = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
        output = process.stdout.decode().strip()
        if process.returncode != 0:
            print(f"Error: {output}")
            exit(process.returncode)
        else:
            print(output)
    except Exception as e:
        traceback.print_exception(e)
        print(f"Error: {str(e)}")
        exit(1)
#default marker
marker = "#"




if __name__ == "__main__":
    mode = "auto"
    #mode = "manual"
    print("1(local input) or 2(rpg) or 3(chat) or 4(custom_path) or 5(pull llama3) or 6(pull any model) or 7(install instructions)")
    if(mode == "auto"):
        inp = "1"
    else:
        inp = input()
    if((inp == "") or (inp == "\n")):
        inp = "1"
        print("switched to '1'")
    if(inp == "7"):
        print("NEW (fast): 1. run pip install groq")
        print("OLD(ollama): 1. go to link:   https://ollama.com/", "\n2. and install ollama", "\n3. rerun this script with (5)")
        time.sleep(15)
    if (inp == "5"):
        run_ollama_command("llama3")
        print("1(local input) or 2(rpg) or 3(chat) or 4(custom_path)")
        inp = input()
    elif (inp == "6"):
        print("write model(like llama3)")
        model = input()
        model.strip()
        run_ollama_command(model)
        print("1(local input) or 2(rpg) or 3(chat) or 4(custom_path)")
        inp = input()

    if(inp =="1"):
        folder_path = "/"
        while (True):
            if not os.path.isdir(folder_path):
                print("Folder doesnt exist. Double check path.")
            else:
                break
            print("(path)", folder_path)
            inp = input().strip()
            if (inp != "" and ":" in inp):
                folder_path = inp
        marker = "#"
        start_new_thread()
    elif(inp == "3"):
        history= list()
        while(True):
            print("ask")
            answer = sendandrecv(input(), history)
            history.append(answer)
            print("----------------------")
            print(answer)
        pass
    elif(inp == "4"):
        folder_path = ""
        while (True):
            print("Write path: H:\\Test\\Bla")
            inp = input().strip()
            if (inp != "" and ":" in inp):
                folder_path = inp

            if not os.path.isdir(folder_path):
                print("Folder doesnt exist. Double check path.")
            else:
                break
    elif(inp == "2"):
        folder_path = "H:\\2022\\2DTurnBasedRPG\\Assets"
        while (True):
            if not os.path.isdir(folder_path):
                print("Folder doesnt exist. Double check path.")
            else:
                break
            print("(path)", folder_path)
            inp = input().strip()
            if (inp != "" and ":" in inp):
                folder_path = inp
        marker = "//"
        start_new_thread()
    else:
        print("input not supported", inp)
    print("start-")
    print("daily: ", "app" + str(datetime.date.today().day) + ".py")
    extensions = ['.txt', '.cs', 'plow.py', '.json', '.yaml', 'analyze.py', "optimal.py", "_agent.py", "app.py", "tree.py",
                  "app" + str(datetime.date.today().day) + ".py", "app_py.py", 'groq_layer2.py']
    tracker = ProjectTracker(extensions)
    tracker.start_tracking(folder_path)
    print("Shutting down in 8 seconds...")
    time.sleep(8)


# basically idea is to have external file, call it as
# ai agent="filename":awaken context
# ok==
#
# this opens window where agent is operating independently of everything else. window is only ui, the rest runs in background
# - question is how to run this
#--- it should be run in way that's easy to integrate in other uis
#--- it should be easy to close, sort of like docker
#--- it should work with files only
#--- it should run either part of ai handling script, or entirely new script with specific startup arguments(2)
#----- (2) this might be best achieved with running cmd. should be easier to port too.
#----- (2) seems better option for maintainability and stability
#----- (2) for preventing agi code duplication, im running only 1 configuration, and then locking all further ones. only main llm can open agents
#-------- this is achieved by having external file for running agents, that doesnt have any special logic in it