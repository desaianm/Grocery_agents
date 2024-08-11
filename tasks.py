from crewai import Agent, Task, Crew, Process


class Tasks:

    def scraping_task(self,agent, websites, items):
        return Task(
            description=(
                f"""
        Websites to search for products: 
        {websites}
        List of items to search for:
        {items}

        Conduct a comprehensive search for the specified grocery items across the provided online stores. For each item:
        1. Identify the best price and the store offering it.
        2. Note any ongoing promotions or bulk-buy discounts.
        3. Look for alternative products or store brands that might offer better value.
        4. Make efficient, complex queries for each item to save time.
        5. Compile the information in a structured JSON format for easy processing.
        6. Provide a maximum of 2 options per item, focusing on major retailers like Walmart, Sobeys, Metro, etc.
        7. Include the following for each option:
           - Item name
           - Price
           - Store name
           - Direct link to the product page
           - Any relevant promotions or discounts
        8. Ensure all prices are in Canadian dollars (CAD).
        9. If a price is not available, use "N/A" as the value.
        """
            ),
            expected_output='A comprehensive list of grocery items with detailed pricing, store information, and product specifics.',
            agent=agent 
)

# List Management Task
    # def list_management_task(self, agent):
    #     return Task(
    #         description=(
                
    #             """
    #             Take the formatted output from the scraping task and create a list of items with the best price and store.
    #             For each product, select a maximum of 2 options based on the best value (considering price, quality, and any promotions).
    #             Create a structured list containing:
    #             1. Item name
    #             2. Best price option(s) (up to 2)
    #             3. Store(s) offering the best price
    #             4. Any relevant promotions or discounts
    #             5. Brief justification for the selection (e.g., "lowest price", "best value considering quality")
    #             Ensure the list is organized for easy readability and further processing.


    #             """
    #         ),
    #         expected_output='A json file',
    #         agent=agent
    #     )

    def json_parser_task(self, agent):
        return Task(
            description=
            """
            Take list of items, extract price,name,link and return a json array of items with the following sample json structure:

            [
            {
                "link": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "https://www.walmart.ca/",
                                "link": {"url": "https://www.walmart.ca/"}
                            }
                        }
                    ]
                },
                "price": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": "10"}
                        }
                    ]
                },
                "Name": {
                    "title": [
                        {
                            "type": "text",
                            "text": {"content": "Sealtest Milk 4l 3.25"}
                        }
                    ]
                }
            }
            ]

            Make sure the output is in json format. do not include any other text or three quotes or json word at start or end of the output.
            """,
            expected_output="json array",
            agent=agent
        )

