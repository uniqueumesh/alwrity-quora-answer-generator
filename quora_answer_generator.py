import streamlit as st
import requests
from bs4 import BeautifulSoup # Keep BeautifulSoup for potential future use or if any basic parsing is needed on snippets
import google.generativeai as genai
import os
# from playwright.sync_api import sync_playwright # Removed Playwright import
# import asyncio # Removed asyncio import

# Removed Playwright/asyncio fix
# if os.name == 'nt': # Check if the operating system is Windows
#     asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

st.set_page_config(layout="wide")
st.title("AI Quora Answer Generator")

st.header("API Configuration")
google_api_key = st.text_input("Gemini API Key", type="password")
serper_api_key = st.text_input("Serper API Key", type="password")
# openai_api_key = st.text_input("OpenAI API Key", type="password") # Removed OpenAI API Key input
    
# Removed Model Selection section
# st.header("Model Selection")
# gemini_model = st.selectbox(
#     "Choose LLM Model",
#     ("gemini-2.0-pro", "gemini-2.0-flash", "gemini-2.5-pro", "gemini-2.5-flash") # Removed OpenAI option
# )

st.header("Quora Question")
question = st.text_area("Enter the Quora question here:")

# Default to gemini-2.5-flash as the model
gemini_model = "gemini-2.5-flash"

def search_quora_with_serper(query, serper_api_key):
    url = "https://google.serper.dev/search"
    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }
    payload = {
        "q": query + " site:quora.com",
        "num": 10 # Requesting 10 results to ensure we get enough Quora answers
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    search_results = response.json()
    
    quora_snippets = []
    if "organic" in search_results:
        for result in search_results["organic"]:
            if "snippet" in result and "quora.com" in result["link"]:
                quora_snippets.append(f"Source: {result["link"]}\nSnippet: {result["snippet"]}\n---")
    return quora_snippets

# Removed scrape_quora_answer function as we are now using snippets from Serper

if st.button("Generate Answer"):
    if not google_api_key:
        st.warning("Please enter your Gemini API Key.")
    elif not serper_api_key:
        st.warning("Please enter your Serper API Key.")
    elif not question:
        st.warning("Please enter a question.")
    else:
        st.success("Processing your request...")
        
        with st.spinner("Searching Quora for relevant snippets..."):
            # Now we collect snippets instead of trying to scrape full pages
            collected_snippets = search_quora_with_serper(question, serper_api_key)
        
        if not collected_snippets:
            st.warning("Could not find any relevant Quora snippets. Please try a different question or keywords.")
        else:
            st.info(f"Found {len(collected_snippets)} Quora snippets. Generating answer...")
            
            with st.spinner("Generating new answer with LLM..."):
                try:
                    prompt = f"Given the following search result snippets from Quora discussions related to the question '{question}', synthesize a comprehensive and well-structured answer. Focus on integrating insights from these snippets. Aim for a professional but accessible tone.\n\nCollected Snippets:\n" + "\n".join(collected_snippets) + "\n\nGenerated Quora Answer:"
                    
                    genai.configure(api_key=google_api_key)
                    model = genai.GenerativeModel(gemini_model)
                    response = model.generate_content(prompt)
                    st.subheader(f"Generated Quora Answer ({gemini_model}):")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error generating content with LLM: {e}")