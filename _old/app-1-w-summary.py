import streamlit as st
from modules.scrape_summary import SocialMediaPostGenerator

st.set_page_config(layout="wide")

# Title of the App
st.title("Social Media Post Generator w/ Langchain, GPT 4o and Dal-E v3")

# URL Input
url = st.text_input("Enter the URL of the post:")

if st.button("Generate Summary"):
    if url:
        generator = SocialMediaPostGenerator()
        docs = generator.load_and_clean_documents(url)
        split_docs = generator.split_documents(docs)
        generator.summarize(split_docs)
        summary_info = generator.get_summary_info()

        # Display the summary info
        # st.subheader("Summary Information")
        # st.text(f"Final Summary: {summary_info['summary']}")
        # st.text(f"Final Summary Token Size: {summary_info['final_token_size']}")
        # st.text(f"Source URL: {summary_info['source_url']}")
        # st.text(f"Topic: {summary_info['topic']}")

        # Temporary block for testing purposes
        st.subheader("Summary (Temporary Block for Testing)")
        st.write(summary_info["summary"])

        st.subheader("Final Summary Token Size")
        st.write(summary_info["final_token_size"])

        st.subheader("Source URL")
        st.write(summary_info["source_url"])

        st.subheader("Topic")
        st.write(summary_info["topic"])
    else:
        st.warning("Please enter a URL.")
