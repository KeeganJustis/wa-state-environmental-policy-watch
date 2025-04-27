import requests
import os
import logging
from langchain_community.document_loaders import WebBaseLoader
from langchain.chat_models import init_chat_model
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
import dotenv
import getpass

dotenv.load_dotenv()

os.environ["LANGSMITH_TRACING"] = "true"

if not os.environ.get("ANTHROPIC_API_KEY"):
    os.environ["ANTHROPIC_API_KEY"] = getpass.getpass("Enter API key for Anthropic: ")


def get_news_content(url):
    try:
        loader = WebBaseLoader(url)
        logging.info(f"Loading content from {url}")
        return list(loader.lazy_load())
    except requests.exceptions.InvalidSchema as e:
        logging.error(f"Error loading URL {url}: {e}")
        return []


def analyze_news_content(websites_content):
    try:
        llm = init_chat_model("claude-3-5-sonnet-latest", model_provider="anthropic")
        prompt = ChatPromptTemplate.from_template("If blank put \"\", Otherwise write a concise summary of new laws in the legislature for the following:\\n\\n{context}")
        documents  = get_news_content(websites_content)
        chain = create_stuff_documents_chain(llm, prompt)
        logging.info(f"analzing news content")
        result = chain.invoke({"context": documents})
        return result
    except Exception as e:
        logging.error(f"Error analyzing news content: {e}")
        return ""
    # return websites_content.metadata['source'] , result
    
def analyze_all_summaries(list_of_summaries):
    summaries = [analyze_news_content(summary) for summary in list_of_summaries]
    all_summaries = ",".join(summaries)
    logging.info(f"analzing all content")
    final_result = analyze_news_content(all_summaries)
    return final_result
    
    
        