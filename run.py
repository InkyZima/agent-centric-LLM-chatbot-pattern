"""
It's a tool calling agent on loop.

tools:
    create plan
    create eval criteria
    evaluate progress / improvement suggestions
    search web
    call llm (/ create information/report/suggestion)
    communicate to the user
    ask the user (for more info/feedback)

Each time the agent loops, it considers all collected information and everything that happend so far.
"""

from openai import OpenAI
from decorators import delay4, delay8
from dotenv import load_dotenv
import os
from providers.google.google import llm_invoke_google, agent_llm_invoke_google
from llms import getModel, getProvider
from providers.google.tools import all_gemini_tools, ask_user_tool, tell_user_tool, work_on_task_tool
import json
import threading
import queue
import time
from tool_implementations import runTool
from data import getC, setC
load_dotenv(override=True)

DEBUG = True

def printd(text):
    if DEBUG:
        print(text)

askUserAfterXRuns = 3
maxRuns = 6

clients = {}

# llm config
clients["openrouter"] = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"),
)

clients["google"] = OpenAI(
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
  api_key=os.getenv("GOOGLE_API_KEY"),
)


"""List of LLM sizes:
    large-reasoning : state-of-the-art models WITH reasoning
    large: state-of-the-art models WITHOUT reasoning
    medium: fits onto 16GB VRAM
    small: 7-8B params. Can still reasonably to general purpose tasks.
    tiny: ~1.5B to 3B params. Smallest LLMs which reliably do the simplest tasks.

"""



all_tools = []


@delay4
def llm_invoke(input="You are a helpful assistant.", model="large", role="system", tools=all_tools):
    """Simple no-memory llm invocation. Returns just the text response.

    """
    provider = getProvider(model)
    if provider == "google":
        res = llm_invoke_google(input, model, role)
    else:
        res = llm_invoke_openrouter(input, model, role)
    return res

# downstream, agent_llm_invoke is always going to return tool-calling json, while "normal" llm_invoke returns text, and potentially implicitly calls tools (such as when using Gemini with search..). Also, Gemini reasoning doesn't support tool calling, only non-reasoning Gemini does.
@delay4
def agent_llm_invoke(input="You are a helpful assistant.", model="large", role="system", tools=[]):
    """Simple no-memory llm invocation. Returns just the text response.

    """
    provider = getProvider(model)
    if provider == "google":
        res = agent_llm_invoke_google(input, model, role, tools)
    else:
        res = agent_llm_invoke_openrouter(input, model, role)
    return res


def llm_invoke_openrouter(input="You are a helpful assistant.", model="large", role="system", tools=all_tools):
    """LLM invocation logic based on OpenAI spec.

    """
    try:
        provider = getProvider(model)
        completion = clients[provider].chat.completions.create(
            model=getModel(model),
            messages=[
                {
                    "role": "user",
                    "content": input
                }
            ],
        )
        printd("LLM result: " + completion.choices[0].message.content.strip())
        return completion.choices[0].message.content.strip()
    except Exception as e:
        printd("An error occurred when invoking the LLM: %s" % e)
        return ""

def agent_llm_invoke_openrouter(input="You are a helpful assistant.", model="large", role="system", tools=all_tools):
    """LLM invocation logic based on OpenAI spec.

    """
    try:
        provider = getProvider(model)
        completion = clients[provider].chat.completions.create(
            model=getModel(model),
            messages=[
                {
                    "role": "user",
                    "content": input
                }
            ],
        )
        printd("LLM result: " + completion.choices[0].message.content.strip())
        return completion.choices[0].message.content.strip()
    except Exception as e:
        printd("An error occurred when invoking the LLM: %s" % e)
        return ""


def callAgent():
    calledToolsStr = "None."
    c = getC()
    if len(c['calledTools']) > 0 :
        calledToolsStr = ", ".join(c['calledTools'])
    input =f"""
    You are given the following task: {c['taskInstructions']}
    You are a tool calling agent. Decide which tool to use.
    The following tools have been called so far:
    {calledToolsStr}

    Conversation history with the user:
    {c["conversationHistory"]}

    The following prrogress on the task has been made so far:
    {c["currentProgress"]}
    """
    printd("callAgent with calledToolsStr: %s" % calledToolsStr)
    # return agent_llm_invoke(input, "agent-large", tools=all_gemini_tools)
    return agent_llm_invoke(input, "agent-large", tools=[ask_user_tool, tell_user_tool, work_on_task_tool])

def callTool(toolCall):
    # dummy
    return print(toolCall)

# async user input thread

def get_input(input_queue):
    """Function to run in a separate thread to get input."""
    while True:
        user_input = input("User: ") # This will block in the input thread
        if user_input == "exit": break
        c = getC()
        c['conversationHistory'] += "\n" + "User: %s" % user_input
        setC(c)
        input_queue.put(user_input) # Put the input into the queue

input_queue = queue.Queue()
input_thread = threading.Thread(target=get_input, args=(input_queue,))
input_thread.daemon = True # Allow main thread to exit even if input thread is blocked
input_thread.start()

print("Program started, listening for input in the background...")

runCounter = 1
# run the agentLoop
while True:
    user_input = ""
    try:
        user_input = input_queue.get_nowait() # Check queue without blocking
        if user_input == "exit":
            break
    except queue.Empty:
        pass # Simulate other tasks

    toolCall = callAgent()
    try:
        c = getC()
        c["calledTools"].append(toolCall.name)
        setC(c)
        callTool(toolCall) # debug/print
        runTool(toolCall.name, toolCall.args)
        runCounter =+ 1
    except Exception as e:
        print("Agent didn't return a tool call. Agent: %s" % str(toolCall))
        break


# if __name__ == "__main__":
#     while True:
#         user_input = input("User: ")
#         if user_input.lower() == "exit":
#             break
#         print(llm_invoke(user_input, "large"))
