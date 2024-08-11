import os
from crewai import Agent
from crewai_tools import SerperDevTool, WebsiteSearchTool, ScrapeWebsiteTool, FileReadTool
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_anthropic import ChatAnthropic
import json
from langchain_community.tools.tavily_search import TavilySearchResults

tavily_search = TavilySearchResults(k=5)

with open('websites.json', 'r') as file:
    websites = json.load(file)



# Initialize the web scraping tool
scraping_tool = SerperDevTool()

# Initialize the database connection tool
# database_tool = SQLAlchemyTool(connection_string="sqlite:///grocery_list.db")


class Agents():
# Web Scraping Agent
    def web_scraping_agent(self):
        return Agent(
            role='Advanced Product Scraper',
            goal='Conduct comprehensive searches across multiple grocery stores to find the best prices and detailed information for specified items.',
            verbose=True,
            memory=True,
            backstory=(
                """
                You're a highly skilled data analyst specializing in e-commerce and grocery pricing. 
                Your expertise lies in quickly navigating various online platforms, comparing prices, 
                and extracting detailed product information. You're known for your ability to find 
                hidden deals and accurately track price fluctuations in real-time.
                make sure to add price and link to the output.
                
                """
            ),
            tools=[scraping_tool],
            max_iterations=1,
        )

# # List Management Agent
#     def list_management_agent(self):
#         return Agent(
#             role='Intelligent List Curator',
#             goal='Compile and maintain a sophisticated grocery list with real-time price updates and comprehensive product details.',
#             verbose=True,
#             memory=True,
#             backstory=(
#                 "You're an efficiency expert with a background in database management and consumer behavior analysis. "
#                 "Your mission is to create and maintain the most user-friendly and cost-effective grocery lists. "
#                 "You excel at organizing data, spotting trends in pricing, and providing valuable insights to shoppers."
#             ),
#             tools=[],
#         )
    def json_parser_agent(self):
        return Agent(
            role='JSON Parser',
            goal='Parse the JSON output for storing in the database',
            backstory=(
                "You're an expert at parsing JSON data and storing it in a database. "
                "You're known for your attention to detail and ability to extract and store information accurately."
            ),
            verbose=True,
            memory=True,
            tools=[],
        )

# Web Scraping Task
