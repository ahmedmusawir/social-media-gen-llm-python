from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.schema.runnable import RunnableParallel, RunnableLambda
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

class SocialMediaPostGenerator:
    def __init__(self, model_name="gpt-4o", temperature=0.7):
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)

    def generate_twitter_posts_chain(self, summary, topic, url):
        # Define the data structure for Twitter posts
        class Tweet(BaseModel):
            tweet: str = Field(description="Text content of a Twitter post")

        parser = JsonOutputParser(pydantic_object=Tweet)

        template = """
        {summary_str}
        
        Based on the above content about {topic}, craft three highly engaging, concise, and impactful Twitter posts.
        Ensure each tweet:
        - Is within Twitter's 280-character limit, including the URL.
        - Includes relevant hashtags related to {topic}.
        - Has a brief call to action, encouraging followers to engage or learn more.
        - Includes the following URL at the end of each tweet: {url}.
        - Uses a tone that is both professional and approachable.
        - Focus on the text, keeping each message engaging and concise.
        
        {format_instructions}

        TWITTER POSTS (in JSON format):
        """
        
        prompt_template = PromptTemplate(
            template=template,
            input_variables=["summary_str", "url"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        # Combine the prompt and LLM into a sequence
        twitter_chain = prompt_template | self.llm | parser

        # Create input for the chain
        input_data = {"summary_str": summary, "topic": topic, "url": url}

        # Invoke the chain
        return twitter_chain.invoke(input_data)

    def generate_facebook_posts_chain(self, summary, topic, url):
        # Define the data structure for Facebook posts
        class FB_Post(BaseModel):
            fb_post: str = Field(description="Text content of a Facebook post")

        parser = JsonOutputParser(pydantic_object=FB_Post)

        template = """
        {summary_str}

        Based on the above content about {topic}, craft three highly engaging and informative Facebook posts.
        Ensure each post:
        - Is engaging and encourages interaction, such as likes, comments, and shares.
        - Can be more detailed and longer than a tweet, with a narrative or story-like structure.
        - Includes a clear call to action, encouraging followers to engage or learn more.
        - Includes the following URL at the end of the post: {url}.
        - Uses a tone that is professional, yet conversational and approachable.
        - Optionally includes relevant hashtags related to {topic}.
        
        {format_instructions}

        FACEBOOK POSTS (in JSON format):
        """
        
        prompt_template = PromptTemplate(
            template=template,
            input_variables=["summary_str", "url"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        # Combine the prompt and LLM into a sequence
        facebook_chain = prompt_template | self.llm | parser

        # Create input for the chain
        input_data = {"summary_str": summary, "topic": topic, "url": url}

        # Invoke the chain
        # return facebook_chain.invoke(input_data)

        try:
            # Invoke the chain
            return facebook_chain.invoke(input_data)
        except Exception as e:
            # Log the error and return a structured error message
            print(f"Error generating Facebook posts: {e}")
            return {"fb_post": f"Error generating Facebook posts: {e}"}

    def generate_social_media_posts(self, summary, topic, url):
        twitter_chain = RunnableLambda(lambda x: self.generate_twitter_posts_chain(summary, topic, url))
        facebook_chain = RunnableLambda(lambda x: self.generate_facebook_posts_chain(summary, topic, url))
        
        parallel_chain = RunnableParallel(branches={"twitter": twitter_chain, "facebook": facebook_chain})
        
        result = parallel_chain.invoke({"summary_str": summary, "url": url})
        return result


# Example usage
if __name__ == "__main__":
    generator = SocialMediaPostGenerator()
    summary = "This is a sample summary of an article discussing AI's impact on modern technology."
    topic = "AI and Technology"
    url = "https://example.com/blog-post"

    # Generate both Twitter and Facebook posts in parallel
    social_media_posts = generator.generate_social_media_posts(summary, topic, url)

    # Output the results
    twitter_posts = social_media_posts["branches"]["twitter"]
    facebook_posts = social_media_posts["branches"]["facebook"]

    print("Twitter Posts:")
    for post in twitter_posts:
        print(post["tweet"])

    print("\nFacebook Posts:")
    for post in facebook_posts:
        print(post["fb_post"])
