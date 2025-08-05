import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import os

# Optional: OpenAI integration
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None
    st.warning("OpenAI library not found. To use OpenAI models, please install it: `pip install openai`")

st.set_page_config(layout="wide")
st.title("AI Quora Answer Generator")

with st.sidebar:
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
    
    quora_urls = []
    if "organic" in search_results:
        for result in search_results["organic"]:
            if "link" in result and "quora.com" in result["link"]:
                quora_urls.append(result["link"])
    return quora_urls

def scrape_quora_answer(url):
    try:
        # api_url = f"https://api.webscrapingapi.com/v1?api_key={webscrapingapi_key}&url={url}" # Removed WebScrapingAPI call
        response = requests.get(url, timeout=10) # Reverted to direct requests.get
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Attempt to find the main answer content. This might need refinement
        # based on Quora's ever-changing HTML structure.
        answer_div = soup.find('div', class_=lambda x: x and ('AnswerBase'.lower() in x.lower() or 'AnswerItem'.lower() in x.lower()))
        if answer_div:
            return answer_div.get_text(separator="\n").strip()
        else:
            # Fallback for other potential answer structures
            # Look for paragraphs or text within common content areas
            paragraphs = soup.find_all('p')
            if paragraphs:
                return "\n".join([p.get_text(separator="\n").strip() for p in paragraphs if p.get_text(separator="\n").strip()])
        return ""
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching {url}: {e}") # Reverted error message
        return ""
    except Exception as e:
        st.error(f"Error parsing {url}: {e}") # Reverted error message
        return ""

if st.button("Generate Answer"):
    if not google_api_key:
        st.warning("Please enter your Gemini API Key.")
    elif not serper_api_key:
        st.warning("Please enter your Serper API Key.")
    elif not question:
        st.warning("Please enter a question.")
    else:
        st.success("Processing your request...")
        
        st.info("Searching Quora for relevant answers...")
        quora_links = search_quora_with_serper(question, serper_api_key)
        
        if not quora_links:
            st.warning("Could not find any relevant Quora answers. Please try a different question.")
        else:
            st.info(f"Found {len(quora_links)} Quora links. Scraping answers...")
            collected_answers = []
            for i, link in enumerate(quora_links[:10]): # Limit to first 10 for now
                st.text(f"Scraping {i+1}/{min(len(quora_links), 10)}: {link}")
                answer_text = scrape_quora_answer(link)
                if answer_text:
                    collected_answers.append(f"Answer from {link}:\n{answer_text}\n---")
            
            if not collected_answers:
                st.warning("Could not extract answers from the found Quora links.")
            else:
                st.info("Generating new answer with LLM...")
                try:
                    prompt = f"Given the following Quora answers to the question '{question}', synthesize a comprehensive and well-structured answer. Ensure the answer is natural, engaging, and incorporates insights from multiple sources. Aim for a professional but accessible tone.\n\nCollected Answers:\n" + "\n".join(collected_answers) + "\n\nGenerated Quora Answer:"
                    
                    genai.configure(api_key=google_api_key)
                    model = genai.GenerativeModel(gemini_model)
                    response = model.generate_content(prompt)
                    st.subheader(f"Generated Quora Answer ({gemini_model}):")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error generating content with LLM: {e}")