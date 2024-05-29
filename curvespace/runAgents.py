
# ai sethistory=context/agnt_impl_now1.json

# ai: create one run example
import sys
import threading

import sys
import threading
import time
import os

# ai nocontext: in python implement file observer
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

'''
# ai: describe prompt that would give this format
AiAgent:
  Properties:
    running: Boolean
  Methods:
    - startAgent   Start the agent with a given configuration
    - inner_run    The inner loop of the agent
    - close        Close the agent
    - is_running   Check if the agent is still running
  Relationships:
    - observer     FileObserver     The observer that monitors the file for changes

"Write a semi-structured representation of an `AiAgent` class in a markdown-like format. The representation should include:
* A header with the class name `AiAgent`
* A section for `Properties` that lists the agent's properties, with each property on a new line and using the format `property_name: property_type`
* A section for `Methods` that lists the agent's methods, with each method on a new line and including the following information:
	+ Method name and description
	+ Any parameters or arguments in the format `param_name: param_type`
* A section for `Relationships` that lists the agent's relationships, with each relationship on a new line and including the following information:
	+ Relationship name
	+ Relationship type (e.g. `FileObserver`)
	+ Relationship description"
# ok==
'''
# ai: observing doesnt seem to work, dispath gets triggered immediately, but then when i change file, nothing changes
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
class FileObserver(Observer):
    def __init__(self, file_path, callback):
        super(FileObserver, self).__init__()
        print(file_path, "(folder, no file)")
        self.file_path = file_path
        self.last_modified_time = 0
        self.callback = callback

    def on_modified(self, event):
        current_modified_time = os.path.getmtime(self.file_path)
        print(current_modified_time)
        if current_modified_time > self.last_modified_time:
            self.last_modified_time = current_modified_time
            print("Agent detecting change in "+self.file_path)
            self.callback()

class AiAgent(FileSystemEventHandler):
    def __init__(self, name, config=""):
        if( "/" in name):
            splitt = name.split("/")
            self.name = splitt[-1]
            path = ("".join(splitt[0:-1]))+"/"
        else:
            self.name = name
            path = ""
        self.running = True
        self.configAgent(config)
        self.memorySize = -1 # disabled, use internal

        self.wasEdited = 0
        if(self.name != ""):
            self.name = "_"+self.name
        self.agentInputFile = f"{path}agent{self.name}_in.txt"
        self.agentOutFile = f"{path}agent{self.name}_output.txt"

    def on_modified(self, event):
        print("AiAgent: dispatch method called", event)

        rightPath = self.agentInputFile
        if event.src_path.endswith(rightPath):
            if (self.wasEdited > 0):
                self.wasEdited-=1
                return
            print("writing")
            contents = ""
            while (True):
                try:
                    with open(self.agentInputFile, "a") as file:
                        pass
                    with open(self.agentInputFile, "r") as file:
                        contents = file.read()
                except PermissionError:
                    print("premission err")
                    time.sleep(1)
                    continue
                except FileNotFoundError:
                    print(f"Error: File {self.agentInputFile} (33) not found.")
                break

            self.main_execution_loop(contents)
            self.wasEdited = 2

    def main_execution_loop(self, contents):
        while(True):
            prompt = "# a"+ f"i: {self.configQuestion}\n Question: {contents} \n# o"+"k--"

            print("agent prompt ",  prompt," <END>")
            from agentic_constructs import aiexe
            promptSetup = { "prompt":prompt, "mem_size":self.memorySize}
            answer = aiexe(promptSetup) +"\n"

            try:
                with open(self.agentOutFile, "a") as file:
                    file.write(answer)
                return answer
            except PermissionError:
                print(f"Error: Permission denied when writing to {self.agentOutFile}.")
            time.sleep(1)

    def startAgent(self):
        self.thread = threading.Thread(target=self.inner_run)
        self.thread.start()
        return
    def configAgent(self, config):
        print("Configuring agent", self.name) #config)
        self.config = config
        if "mem_len" in config:
            id = config.find("mem_len:")
            end = config.find("\n", id)
            sub = config.substring(id, end)
            num = int(sub)
            self.memorySize = num
        self.configQuestion = f"Play the role of an agent that has this configuration for this question. \nConfiguration Settings: \n{self.config}"

    def inner_run(self):
        path = os.path.dirname(os.path.abspath(self.agentInputFile))
        observer = Observer()
        observer.schedule(self, path, recursive=True)
        observer.start()

        while self.running:
            print("Agent is still observing path...", path)
            time.sleep(5)

    def close(self):
        print("Closing agent")
        self.running = False
        self.thread.join()
        print("Agent has been stopped.\t", self.name)

    def is_running(self):
        return self.running


import yaml
import os

class AiAgentParser:

    def parseConfig(self, config_file):
        print("Parsing configuration file:", config_file)
        if not os.path.exists(config_file):
            print("Config file does not exist")
            return None
        x =''' 
        yaml:
        AI SETUP:
            name: joe
            core: |+
            look for pure, distiled, true, correct, information
            act: |+
            after finding something, store it in memory
            memory: agent_mem.txt
            monitoring: app_py.py
            writing: app_py.py
        '''
        # assume config file is yaml, read it
        with open(config_file, 'r') as f:
            config = f.read()# yaml.safe_load(f)

        return config

def temporarySetup():
    allAgents = list()
    file = "x.txt"
    opened = "asdf\n// ai agent=agent.yaml:test 123\n// ok--\npotato"
    section = "// ai agent=agent.yaml:test 123\n// ok--\n"
    action = "agent=agent.yaml"
    agentexe(action, section, allAgents)
    closeAll(allAgents)

def agentexe(action, wholesection, allAgents = list(), keepconf=False):
    startedNew, agentPath = parseAgentAction(action, wholesection)
    if(startedNew):
        agent = setupAgent(agentPath, allAgents, True, False)
        with open(agent.agentInputFile, "w") as file:
            file.write(wholesection)
        answer = agent.main_execution_loop(wholesection)
        if(keepconf == False):
            answer.find(wholesection)
            answerNoConf = answer.replace(agent.configQuestion, "")
            answer = answerNoConf
        return answer != None, answer
    return False, None

def closeAll(allAgents):
    print("Closing all agents")
    for agent in allAgents:
        print("Closing agent:", agent)
        # implementation of closing agent
        # for example, you can use join method of thread
        try:
            agent.running = False
            agent.thread.join()
            print("Agent has been stopped.")
        except:
            print("Failed to stop agent.")
    print("All agents have been stopped.")

def parseAgentAction(action, section):
    filePath = None
    if "agent=" in action:
        split = action.split(" ")
        for i in split:
            if "agent=" in i:
                if i.startswith('agent="'):
                    filePath = i[7:-1]
                elif "=" in i:
                    filePath = i.split("=")[1]
                else:
                    filePath = i

    if filePath == None:
        return False, None
    return True, filePath

    print("Parsing runtime file...")
    try:
        agentParser = AiAgentParser()
        config = agentParser.parseConfig(filePath)
        # config should be dictionary of values
        agent = AiAgent("")
        agent.startAgent(config)
        return True, agent
    except Exception as e:
        print("Error parsing runtime file:", str(e))
        return False, None

def setupAgent(extraAgent="agent.yaml", agents = list(), keepRunning = False, observer = True):
    try:
        config_agent = AiAgentParser()
        config_file = extraAgent


        config = config_agent.parseConfig(config_file)
        if("." not in extraAgent):
            extraAgent+=".yaml"
        name = "" if extraAgent=="agent.yaml" else extraAgent.split(".")[0]
        print("opening agent", extraAgent, name)
        # Start the agent
        agent = AiAgent(name, config)
        if(observer):
            agent.startAgent()
            agents.append(agent)

        if(not keepRunning):
            # Wait for a few seconds to see the agent running
            time.sleep(150)

            # Close the agent
            agent.close()
        return agent
    except Exception as e:
        import traceback
        traceback.print_exception(e)
        print(f"Error: {e}")

if __name__ == "__main__":
    temporarySetup()
