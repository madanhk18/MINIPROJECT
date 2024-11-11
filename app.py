import streamlit as st
import os
from flask import Flask
from dotenv import load_dotenv
load_dotenv() 
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi




genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You're a YouTube video summarizer. You will take the transcript text 
and summarize the entire video, providing the important points within 250 words. 
Please provide the summary of the text given here:"""

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join(item["text"] for item in transcript_data)
        return transcript_text

    except Exception as e:
        st.error("Error retrieving transcript: {}".format(e))
        # st.error(f"Error retrieving transcript: {e}")
        return None

def generate_gemini_content(transcript_text, prompt):
    try:
        # Adjust based on genai library's correct model access method
        model=genai.GenerativeModel("models/gemini-pro")
        response = model.generate_content(prompt+ transcript_text)
        return response.text
    except Exception as e:
        st.error(f"Error generating summary: {e}")
        return None
    
st.title("YouTube Transcript to Detailed Notes Converter")
st.write("Steps:")
st.write("1. Go to YouTube video in your Desktop/Laptop")
st.write("2. Right click on the video")
st.write("3. Copy the link address & paste it down below")
st.title("Enter your URL")
youtube_link = st.text_input("Enter YouTube video link")

def split_url_at_ampersand(youtube_link):
    return youtube_link.split("&")[0]

clean_youtube=" "

if clean_youtube:
    clean_youtube_link = split_url_at_ampersand(youtube_link)
    

if clean_youtube_link:
    video_id = clean_youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

    transcript_text = extract_transcript_details(clean_youtube_link)
    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        if summary:
            st.markdown("## Detailed Notes:")
            st.write(summary)
