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

from google.genai.types import Tool, FunctionDeclaration

# Specify a function declaration and parameters for an API request
get_current_weather_func = FunctionDeclaration(
    name="get_current_weather",
    description="Get the current weather in a given location",
    # Function parameters are specified in JSON schema format
    parameters={
        "type": "object",
        "properties": {"location": {"type": "string", "description": "Location"}},
    },
)

# Define a tool that includes the above get_current_weather_func
weather_tool = Tool(function_declarations=[get_current_weather_func],)


get_search_web_func = FunctionDeclaration(
    name="search_web",
    description="Search the web",
    parameters={
        "type": "object",
        "properties": {"search_query": {"type": "string", "description": "What to search for"}},
    },
)
search_tool = Tool(function_declarations=[get_search_web_func],)

ask_user_func = FunctionDeclaration(
    name="ask_user",
    description="Ask the user a question / for further information",
    parameters={
        "type": "object",
        "properties": {"question": {"type": "string", "description": "What to ask the user for"}},
    },
)
ask_user_tool = Tool(function_declarations=[ask_user_func],)

tell_user_func = FunctionDeclaration(
    name="tell_user",
    description="Tell the user the task completion result",
    parameters={
        "type": "object",
        "properties": {"task_result": {"type": "string", "description": "What to tell the user"}},
    },
)
tell_user_tool = Tool(function_declarations=[tell_user_func],)

create_plan_func = FunctionDeclaration(
    name="create_plan",
    description="Project planner for solving complex tasks",
    parameters={
        "type": "object",
        "properties": {"project": {"type": "string", "description": "What project/task to plan"}},
    },
)
create_plan_tool = Tool(function_declarations=[create_plan_func],)


create_eval_criteria_func = FunctionDeclaration(
    name="create_evaluation_criteria",
    description="Create evaluation criteria for judging if a task has been done well",
    parameters={
        "type": "object",
        "properties": {"task": {"type": "string", "description": "The task for which completion evaluation criteria shall be created"}},
    },
)
create_eval_criteria_tool = Tool(function_declarations=[create_eval_criteria_func],)

work_on_task_func = FunctionDeclaration(
    name="work_on_task",
    description="Work on the task/project",
    parameters={
        "type": "object",
        "properties": {"task": {"type": "string", "description": "The task/project to work on"}},
    },
)
work_on_task_tool = Tool(function_declarations=[work_on_task_func],)


all_gemini_tools = [weather_tool, search_tool, ask_user_tool, tell_user_tool, create_plan_tool, create_eval_criteria_tool, work_on_task_tool]

all_gemini_tools_names = [element.function_declarations[0].name for element in all_gemini_tools]


if __name__ == "__main__":
    print(str(ask_user_tool.function_declarations[0].name))
