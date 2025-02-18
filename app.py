import streamlit as st
from dotenv import load_dotenv

load_dotenv()#loadall the environment variables
import google.generativeai as genai
import os

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLR_API_KEY"))

prompt="""You are a Youtube video summarize. 
    You will be taking the transcript text and summarizing the entire video and providing 
    the entire video the important summary in points within250 words.
    TPlease Provide the Summary of the text given here : """




#getting the transcript data from ytb videos
def extract_transcript_details(youtube_video_url):
    try: 
        video_id=youtube_video_url.split("=")[1]
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)
        transcript=""
        for i in transcript_text:
            transcript+=""+i["text"]

        return transcript

    except Exception as e:
        raise e

#getting the summary based on Prompt from Gemini Pro
def genearte_gemini_content(transcript_text,prompt):

    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt + transcript_text)

    return response.text



st.title("Youtube Transcript to detailed Notes Converter")

youtube_link=st.text_input("Enter Youtibe Video Link:")
if youtube_link:
    video_id=youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg",use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        summary=genearte_gemini_content(transcript_text,prompt)
        st.markdown("## Deatiled Notes :")
        st.write(summary)












