import streamlit as st
from modules.post_generator import SocialMediaPostGenerator
from modules.scrape_summary import ScrapeSummaryGenerator
from modules.utils import download_image  # Import the download_image function
from modules.image_generator import ImageGenerator

st.set_page_config(layout="wide")

# Title of the App
st.title("Social Media Post Generator w/ Langchain, GPT 4o and Dal-E v3")

# Initialize session state variables if they don't exist
if "twitter_posts" not in st.session_state:
    st.session_state.twitter_posts = []
if "facebook_posts" not in st.session_state:
    st.session_state.facebook_posts = []
if "twitter_image_url" not in st.session_state:
    st.session_state.twitter_image_url = None
if "facebook_image_url" not in st.session_state:
    st.session_state.facebook_image_url = None
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""

# URL Input
url = st.text_input("Enter the URL of the post:")

# Placeholder for the summary
summary_placeholder = st.empty()

if st.button("Generate Social Media Posts"):
    if url:
        # Display loading spinners while generating posts
        with st.spinner('Generating summary and posts...'):
            try:
                # Initialize the generator
                generator = ScrapeSummaryGenerator()
                # Extract and summarize the content
                docs = generator.load_and_clean_documents(url)
                split_docs = generator.split_documents(docs)
                generator.summarize(split_docs)
                summary_info = generator.get_summary_info()
                st.session_state.summary = summary_info["summary"]
                st.session_state.topic = summary_info["topic"]
                st.session_state.source_url = summary_info["source_url"]

                # Initialize post generator
                post_generator = SocialMediaPostGenerator()
                # Generate social media posts
                social_media_posts = post_generator.generate_social_media_posts(st.session_state.summary, st.session_state.topic, st.session_state.source_url)

                # Save posts to session state
                st.session_state.twitter_posts = social_media_posts["branches"]["twitter"]
                st.session_state.facebook_posts = social_media_posts["branches"]["facebook"]

                # Optionally display the summary info for debugging/testing purposes
                summary_placeholder.subheader("Summary Information (Temporary Block)")
                summary_placeholder.text(f"Final Summary: {st.session_state.summary}")
                summary_placeholder.text(f"Topic: {st.session_state.topic}")
                summary_placeholder.text(f"Source URL: {st.session_state.source_url}")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    else:
        st.warning("Please enter a URL.")

# Two-column layout for Twitter and Facebook posts
col1, col2 = st.columns(2)

# Custom CSS for styling the code block
custom_css = """
    <style>
    .st-emotion-cache-16nrs4v {
        height: 500px !important;
        border: 5px solid lightgray;
        padding: 10px !important;
    }    
    .stCode {
        padding-top: 50px !important;
        border: 5px solid gray;
        border-radius: 5px;
        background-color: #f0f0f0 !important;
        color: #333 !important;
    }
    </style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Display the Twitter posts and image generation
with col1:
    st.subheader("Twitter Posts")
    for idx, post in enumerate(st.session_state.twitter_posts):
        st.code(post["tweet"], language="text")
    
    # Generate Twitter Image button (disabled until Twitter posts are generated)
    if st.session_state.twitter_posts:
        if st.button("Generate Twitter Image", key="generate_twitter_image"):
            with st.spinner('Generating Twitter image...'):
                image_generator = ImageGenerator()
                st.session_state.twitter_image_url = image_generator.create_image(f"Generate an image suitable for a Twitter post about {st.session_state.topic}. {st.session_state.summary}", size="1024x1024")

    # Display Twitter image if generated
    if st.session_state.twitter_image_url:
        st.image(st.session_state.twitter_image_url, caption="Twitter Image", use_column_width=True)
        img_data = download_image(st.session_state.twitter_image_url)
        st.download_button(label="Download Twitter Image", data=img_data, file_name="twitter_image.png", mime="image/png")

# Display the Facebook posts and image generation
with col2:
    st.subheader("Facebook Posts")
    for idx, post in enumerate(st.session_state.facebook_posts):
        if isinstance(post, dict) and "fb_post" in post:
            st.code(post["fb_post"], language="text")
        else:
            st.error(f"Error in generating Facebook post {idx+1}. Please try regenerating.")    
    
    # Generate Facebook Image button (disabled until Facebook posts are generated)
    if st.session_state.facebook_posts:
        if st.button("Generate Facebook Image", key="generate_facebook_image"):
            with st.spinner('Generating Facebook image...'):
                image_generator = ImageGenerator()
                st.session_state.facebook_image_url = image_generator.create_image(f"Generate an image suitable for a Facebook post about {st.session_state.topic}. {st.session_state.summary}", size="1024x1024")

    # Display Facebook image if generated
    if st.session_state.facebook_image_url:
        st.image(st.session_state.facebook_image_url, caption="Facebook Image", use_column_width=True)
        img_data = download_image(st.session_state.facebook_image_url)
        st.download_button(label="Download Facebook Image", data=img_data, file_name="facebook_image.png", mime="image/png")
