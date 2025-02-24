from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch, FunctionDeclaration
import os
from llms import getModel
from .tools import weather_tool


def llm_invoke_google(input="You are a helpful assistant.", model="large-reasoning-search", role="system", tools=[]):
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    withSearch = "search" in model

    google_search_tool = Tool(
        google_search = GoogleSearch()
    )
    toolsArray = []
    if withSearch:
        toolsArray.append(google_search_tool)

    try:
        response = client.models.generate_content(
            model=getModel(model),
            contents=input if not withSearch else "Utilize web search for this task.\n\n" + input,
            config=GenerateContentConfig(
                tools=toolsArray
            )
        )

        return response.candidates[0].content.parts[0].text

    except Exception as e:
        print("An error occurred when invoking the LLM: %s" % e)
        return ""
    


def agent_llm_invoke_google(input="You are a helpful assistant.", model="agent-large", role="system", tools=[]):
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    try:
        response = client.models.generate_content(
            model=getModel(model),
            contents=input,
            config=GenerateContentConfig(
                tools=tools
                # tools=tools if len(tools) > 0 else toolsArray # dual use: if llm_invoke_google is used by the agentLoop, there is no real tool calling by Google, just a tool-calling reply. If llm_invoke_google is used on the instruction of the agent, then use GoogleSearch if desired.
            )
        )

        return response.candidates[0].content.parts[-1].function_call
        
    except Exception as e:
        print("An error occurred when invoking the LLM: %s" % e)
        return ""