llms = {
    "large-reasoning-search": {
        "provider": "google",
        "model": "gemini-2.0-flash-thinking-exp" # "google/gemini-2.0-flash-thinking-exp:free" for openrouter
    },
    "large-reasoning": {
        "provider": "google",
        "model": "gemini-2.0-flash-thinking-exp" # "google/gemini-2.0-flash-thinking-exp:free" for openrouter
    },
    "large-search": {
        "provider": "google",
        "model": "gemini-2.0-flash" # "google/gemini-2.0-flash-thinking-exp:free" for openrouter
    },
    "agent-large": {
        "provider": "google",
        "model": "gemini-2.0-flash" # "google/gemini-2.0-flash-exp:free" for openrouter
    },
    "large": {
        "provider": "google",
        "model": "gemini-2.0-flash" # "google/gemini-2.0-flash-exp:free" for openrouter
    },
    "medium": {
        "provider": "openrouter",
        "model": "mistralai/mistral-small-24b-instruct-2501:free"
    },
    "small": {
        "provider": "openrouter",
        "model": "mistralai/mistral-7b-instruct:free"
    },
    "tiny": {
        "provider": "openrouter",
        "model": "mistralai/mistral-7b-instruct:free"
    },
}

def getModel(modelString):
    return llms[modelString]["model"]

def getProvider(modelString):
    return llms[modelString]["provider"]