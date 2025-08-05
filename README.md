# AI Quora Answer Generator

This is a free and open-source tool designed for Quora professionals to quickly generate comprehensive answers to Quora questions. Leveraging AI models and web search, it researches existing content and synthesizes a well-structured answer.

## Features

*   **AI-Powered Answer Generation**: Utilizes Google Gemini's latest Flash model (`gemini-2.5-flash`) to generate high-quality answers.
*   **Quora Research**: Searches Quora for relevant answers using the Serper API.
*   **Snippet-Based Synthesis**: Extracts and synthesizes information from search result snippets, providing a robust solution without direct (and often blocked) page scraping.
*   **User-Friendly Interface**: Built with Streamlit, providing an intuitive web UI for easy interaction.
*   **API Key Input**: Users can easily provide their Gemini and Serper API keys directly in the application's UI.

## How It Works

1.  **Search Quora**: The tool uses your provided Serper API key to perform a Google search, specifically targeting `site:quora.com` for your given question. This fetches relevant Quora links and their accompanying search snippets (short summaries).
2.  **Snippet Collection**: Instead of attempting to scrape the full content of each Quora page (which is often blocked by Quora's anti-bot measures), the tool collects the valuable summary snippets directly from the Serper API's search results.
3.  **AI Answer Generation**: These collected snippets are then fed into the `gemini-2.5-flash` model along with your original question. The AI synthesizes a comprehensive and engaging answer based on the information gathered from these snippets.

## Setup and Installation

Follow these steps to set up and run the AI Quora Answer Generator on your local machine.

### 1. Clone the Repository

If you haven't already, clone this GitHub repository to your local machine:

```bash
git clone https://github.com/uniqueumesh/alwrity-quora-answer-generator.git
cd alwrity-quora-answer-generator
```

### 2. Create a Virtual Environment (Recommended)

It's highly recommended to use a virtual environment to manage dependencies:

```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browsers (Crucial for Scraping)

Even though we're primarily using snippets, Playwright might still be used for certain parts or if future enhancements require browser automation. **This is a crucial step to ensure the underlying Playwright library can function if needed.**

In your terminal, run:

```bash
playwright install
```

### 5. Obtain API Keys

You will need two API keys:

*   **Google Gemini API Key**:
    *   Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
    *   Sign in with your Google account.
    *   Click "Get API key in a new project" or "Create API Key" to generate a new key.
*   **Serper API Key**:
    *   Go to the [Serper API website](https://serper.dev/).
    *   Sign up for a free account.
    *   Your API key will be available in your dashboard.

### 6. Run the Streamlit Application

Once you have your API keys and all dependencies are installed, run the Streamlit application:

```bash
streamlit run quora_answer_generator.py
```

This command will open the application in your default web browser (usually at `http://localhost:8501`).

### 7. Use the Tool

In the Streamlit application:

1.  Enter your **Gemini API Key** in the designated input field.
2.  Enter your **Serper API Key** in the designated input field.
3.  Type your **Quora question** into the text area.
4.  Click the **"Generate Answer"** button.

The tool will then search Quora, collect snippets, and generate a comprehensive answer using the Gemini AI model.

## Contributing

As an open-source project, contributions are highly welcome! If you have ideas for improvements, bug fixes, or new features, feel free to open issues or submit pull requests.

## License

This project is licensed under the [LICENSE](LICENSE) file.
