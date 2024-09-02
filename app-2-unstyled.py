import streamlit as st
from modules.post_generator import SocialMediaPostGenerator
from modules.scrape_summary import ScrapeSummaryGenerator

st.set_page_config(layout="wide")

# Title of the App
st.title("Social Media Post Generator w/ Langchain, OpenAI GPT 4o and Dal-E v3")

# URL Input
url = st.text_input("Enter the URL of the post:")

# Placeholder for the summary
summary_placeholder = st.empty()

if st.button("Generate Social Media Posts"):
    if url:
        # Display loading spinners while generating posts
        with st.spinner('Generating summary and posts...'):
            # Initialize the generator
            generator = ScrapeSummaryGenerator()
            # Assume you already have a method to extract and summarize the content
            docs = generator.load_and_clean_documents(url)
            split_docs = generator.split_documents(docs)
            generator.summarize(split_docs)
            summary_info = generator.get_summary_info()
            summary = summary_info["summary"]
            topic = summary_info["topic"]
            source_url = summary_info["source_url"]

            # Initialize post generator
            post_generator = SocialMediaPostGenerator()
            # Generate social media posts
            social_media_posts = post_generator.generate_social_media_posts(summary, topic, source_url)

            # Two-column layout for Twitter and Facebook posts
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Twitter Posts")
                twitter_posts = social_media_posts["branches"]["twitter"]
                for post in twitter_posts:
                    st.write(post["tweet"])

            with col2:
                st.subheader("Facebook Posts")
                facebook_posts = social_media_posts["branches"]["facebook"]
                for post in facebook_posts:
                    st.write(post["fb_post"])

            # Optionally display the summary info for debugging/testing purposes
            summary_placeholder.subheader("Summary Information (Temporary Block)")
            summary_placeholder.text(f"Final Summary: {summary}")
            summary_placeholder.text(f"Topic: {topic}")
            summary_placeholder.text(f"Source URL: {source_url}")

    else:
        st.warning("Please enter a URL.")
