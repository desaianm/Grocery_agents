import json
import streamlit as st
from crewai import Agent, Crew, Process
from crewai_tools import SerperDevTool, WebsiteSearchTool, ScrapeWebsiteTool, FileReadTool
from langchain_community.agent_toolkits.load_tools import load_tools
from agents import Agents
from tasks import Tasks
from notion_client import Client
import requests
import os

class GroceryApp:
    def __init__(self):
        self.NOTION_TOKEN = "secret_uXaIXrtHsgGUL9KX2Dwph4Gj26ZU3CR80TtQJxyp8VB"
        self.DATABASE_ID = "41cd1491d75b488fa6b7f94883366040"
        os.environ['OPENAI_MODEL_NAME'] = 'gpt-4o'

        self.notion = Client(auth=self.NOTION_TOKEN)
        self.database_id = "41cd1491d75b488fa6b7f94883366040"

        with open('websites.json', 'r') as file:
            self.websites = json.load(file)

        with open('list.txt', 'r') as file:
            self.txt_file = file.readlines()

        self.agents = Agents()
        self.tasks = Tasks()

        self.headers = {
            "Authorization": "Bearer " + self.NOTION_TOKEN,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

    def run_crew(self):
        scraper = self.agents.web_scraping_agent()
        json_parser = self.agents.json_parser_agent()

        scraping_task = self.tasks.scraping_task(scraper, json.dumps(self.websites), self.txt_file)
        json_parser_task = self.tasks.json_parser_task(json_parser)

        grocery_crew = Crew(
            agents=[scraper, json_parser],
            tasks=[scraping_task, json_parser_task],
            process=Process.sequential
        )

        result = grocery_crew.kickoff()
        st.write(result)

        raw_result = result.raw

        crew_rows = json.loads(raw_result)
        print(crew_rows)
        # check if the raw_result is a list of dictionaries
        if isinstance(crew_rows, list):
            for row in crew_rows:
                response = self.add_row_to_database(row)
                st.write(response)
        else:
            print("Error: The result is not a list of dictionaries.")

    def add_row_to_database(self, data):
        url = "https://api.notion.com/v1/pages"
        payload = {
            "parent": {"database_id": self.DATABASE_ID},
            "properties": data
        }
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json()

    def retrieve_page_content(self, page_id):
        url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def extract_text_from_blocks(self, blocks):
        text_content = []
        for block in blocks:
            block_type = block.get("type")
            if block_type in ["bulleted_list_item", "numbered_list_item"]:
                text_objects = block[block_type].get("rich_text", [])
                text = " ".join(text_obj.get("plain_text", "") for text_obj in text_objects)
                text_content.append(text)
        return "\n".join(text_content)
    
    def append_to_txt_file(self, new_item):
        with open('list.txt', 'a') as file:
            file.write(new_item + '\n')

    def main(self):
        st.title("Grocery App")
        
        if st.button("Run Crew"):
            page_id = "db336204252b4f9785b826af74ca1500"
            page_content = self.retrieve_page_content(page_id)

            if "results" in page_content:
                all_text = self.extract_text_from_blocks(page_content["results"])
                st.write(all_text)
                
                if all_text not in self.txt_file:
                    st.write("New content detected. Triggering run crew...")
                    self.run_crew()
                    self.append_to_txt_file(all_text)
                else:
                    st.write("No new content. Skipping run crew.")
            else:
                st.write("No content found or error in retrieving page content.")

if __name__ == "__main__":
    app = GroceryApp()
    app.main()