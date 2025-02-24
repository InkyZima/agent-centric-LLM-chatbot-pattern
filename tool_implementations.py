from providers.google.google import llm_invoke_google
from providers.google.tools import all_gemini_tools_names
import json
from data import getC, setC
import time


"""
TODO:
ask user should write both question and answer to memory (object). callAgent system prompt should include this conversation history.

Implement the remaining functions (such as search, project plan).

Spawn a secondary thread with input(); the result gets written to an c["interrupt"]; this variable gets checked by the agent loop on reach run, in order to react to it.

"""

def ask_user(toolArgs):
    c = getC()
    c['conversationHistory'] += "\n" + "AI: %s" % toolArgs['question']
    setC(c)
    print("AI: %s" % toolArgs['question'])
    print("User: ")
    while True:
        if "User: " in getC()["conversationHistory"].split("\n")[-1]:
            return True
        else:
            time.sleep(1)

def tell_user(toolArgs):
    c = getC()
    c['conversationHistory'] += "\n" + "AI: %s" % toolArgs['task_result']
    setC(c)
    print("AI: %s" % toolArgs['task_result'])
    print("User: ")
    while True:
        if "User: " in getC()["conversationHistory"].split("\n")[-1]:
            return True
        else:
            time.sleep(1)

def work_on_task_tool(toolArgs):
    c = getC()
    input =f"""
    You are given the following task: {toolArgs['task']}
    For context: This task is part of the following project: {c['taskInstructions']}
    Work on this task.
    """
    c['currentProgress'] += llm_invoke_google(input)
    setC(c)


toolNames = ["ask_user", "tell_user", "work_on_task"]
toolImplementationFunctions = [ask_user, tell_user, work_on_task_tool]

runToolObj = dict(zip(toolNames, toolImplementationFunctions,))


def runTool(toolName, toolArgs):
    return runToolObj[toolName](toolArgs)

if __name__ == "__main__":
    print(runToolObj)