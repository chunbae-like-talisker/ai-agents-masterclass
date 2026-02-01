from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

MODEL = LiteLlm("openai/gpt-4o-mini")


def get_weather(city: str) -> str:
    return f"The weather in {city} is 30 degrees Celsius."


def conver_units(degrees: int) -> str:
    return f"{degrees} degrees Celsius is {degrees * 1.8 + 32} degrees Fahrenheit."


geo_agent = Agent(
    name="GeoAgent",
    instruction="You help the user with geographic questions",
    model=MODEL,
    description="Transfer to this agent when you have a geographic question",
)


weather_agent = Agent(
    name="WeatherAgent",
    instruction="You help the user with weather related questions",
    model=MODEL,
    tools=[
        get_weather,
        conver_units,
    ],
    sub_agents=[
        geo_agent,
    ],
)

root_agent = weather_agent
