from langchain_community.tools.openweathermap.tool import OpenWeatherMapQueryRun
import asyncio

weather = OpenWeatherMapQueryRun()

async def get_weather_info(location):
    return await asyncio.to_thread(weather.run, location)
