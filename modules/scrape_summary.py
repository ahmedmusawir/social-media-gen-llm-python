from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
import os
from decouple import config
from modules.post_generator import SocialMediaPostGenerator
from modules.utils import clean_text, calculate_token_size

# Enable tracing
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_API_KEY"] = config("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = config("LANGCHAIN_PROJECT")
os.environ["OPENAI_API_KEY"] = config("OPENAI_API_KEY")
os.environ["GROQ_API_KEY"] = config("GROQ_API_KEY")
os.environ["ANTHROPIC_API_KEY"] = config("ANTHROPIC_API_KEY")

class ScrapeSummaryGenerator:
    def __init__(self, model_name="gpt-4o", temperature=0, token_limit_threshold=25000):
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        self.token_limit_threshold = token_limit_threshold
        self.summary = None
        self.source_url = None
        self.topic = None
        self.final_token_size = None

    def load_and_clean_documents(self, url):
        loader = WebBaseLoader(url)
        docs = loader.load()

        for doc in docs:
            cleaned_content = clean_text(doc.page_content)
            doc.page_content = cleaned_content
            self.source_url = doc.metadata.get("source")
            self.topic = doc.metadata.get("title")
        
        return docs

    def split_documents(self, docs, chunk_size=2000, chunk_overlap=200):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        return text_splitter.split_documents(docs)

    def summarize(self, docs):
        token_size = calculate_token_size(docs, self.llm)
        print("Total Tokens:", token_size)

        if token_size <= self.token_limit_threshold:
            custom_prompt_template = PromptTemplate(
                input_variables=["context"],
                template="""
                Please summarize the following content, ensuring that the summary is concise and does not exceed {token_limit} tokens.

                Content: {context}

                Summary:
                """,
            )

            summary_chain = create_stuff_documents_chain(llm=self.llm, prompt=custom_prompt_template)
            self.summary = summary_chain.invoke({"context": docs, "token_limit": 5000})
            self.final_token_size = self.llm.get_num_tokens(self.summary)
        else:
            self.summary = f"CONTENT TOKEN SIZE TOO LARGE ... NO MORE THAN {self.token_limit_threshold} ALLOWED, FOUND {token_size}"

    def get_summary_info(self):
        return {
            "summary": self.summary,
            "final_token_size": self.final_token_size,
            "source_url": self.source_url,
            "topic": self.topic,
        }

# Example usage
if __name__ == "__main__":
    generator = SocialMediaPostGenerator()
    docs = generator.load_and_clean_documents("https://cyberizegroup.com/unlock-the-power-of-google-ads-how-to-get-started-with-google-ad-services/")
    split_docs = generator.split_documents(docs)
    generator.summarize(split_docs)
    summary_info = generator.get_summary_info()
    
    # print("Final Custom Summary:", summary_info["summary"])
    # print("Final Summary Token Size:", summary_info["final_token_size"])
    # print("SourceUrl:", summary_info["source_url"])
    # print("Topic:", summary_info["topic"])
