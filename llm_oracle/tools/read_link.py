from typing import Optional

from langchain.agents import Tool

from llm_oracle.link_scraping import scrape_text, chunk_and_strip_html
from llm_oracle import llm


class ReadLinkWrapper:
    def __init__(self, model: Optional[llm.LLMModel] = None):
        self.model = model

    def run(self, query: str) -> str:
        if query.endswith(".pdf"):
            return "Cannot read links that end in pdf"
        chunks = chunk_and_strip_html(scrape_text(query), 4000)
        return "\n".join(chunks)


def get_read_link_tool(**kwargs) -> Tool:
    read_link = ReadLinkWrapper(**kwargs)
    return Tool(
        name="Read Link",
        func=read_link.run,
        description="useful to read and extract the contents of any link. the input should be a valid url starting with http or https",
    )
