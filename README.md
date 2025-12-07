# Outlook-mail-fetcher-and-summarizer-Bot-

Absolutely\! Here is a comprehensive README.md for your GitHub repository, based on the provided files (`app.py`, `config.py`, `email_fetcher.py`, and `langchain_email_qa.py`).

-----

# 📨 Outlook Email Query App

This is a Streamlit application that allows you to fetch your Microsoft Outlook emails for a specific day using the **Microsoft Graph API** and then ask questions about their content using **LangChain** and a **Large Language Model (LLM)** .

-----

## 🚀 Features

  * **Outlook Integration:** Securely authenticates with your Microsoft account using the Device Code Flow (via `msal`) to access your Outlook mail.
  * **Date Filtering:** Fetches emails received only within a selected 24-hour period.
  * **LangChain QA:** Uses LangChain's **Retrieval-Augmented Generation (RAG)** pipeline to embed the fetched email content and answer user questions.
  * **Streamlit UI:** Provides a simple web interface for date selection, email fetching, and querying.

-----

## 🛠️ Prerequisites

Before running the application, you need to set up the following:

1.  **Python:** Ensure you have Python 3.8+ installed.
2.  **Microsoft Entra ID (Azure AD) App Registration:**
      * Register a new application in the Azure Portal.
      * Note your **Client ID** (Application ID).
      * Under **API Permissions**, add the following **Delegated Permissions** for Microsoft Graph:
          * `User.Read`
          * `Mail.Read`
      * (Optional but recommended for public client apps) Ensure the application type is set to "Public client" in the Authentication settings.
3.  **OpenAI API Key:** You will need a valid OpenAI API key for the embedding and LLM features.

-----

## ⚙️ Installation and Setup

### 1\. Clone the repository

```bash
git clone <repository_url>
cd outlook-email-query-app
```

### 2\. Install dependencies

```bash
pip install -r requirements.txt
```

*(Note: You will need to create a `requirements.txt` file based on the imports in the code, which should include `streamlit`, `msal`, `requests`, `langchain`, `langchain-community`, `langchain-openai`, and `chromadb`.)*

### 3\. Configure API Keys and IDs

Update the placeholders in the following files:

#### `config.py`

Replace the placeholder with your Azure AD application's Client ID:

```python
# config.py
CLIENT_ID = "YOUR_AZURE_AD_CLIENT_ID" # Replace this
AUTHORITY = "https://login.microsoftonline.com/common" 
SCOPES = ["User.Read", "Mail.Read"]
GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0/me/messages"
```

#### `app.py`

Replace the placeholder with your OpenAI API Key:

```python
# app.py
# ...
# Set OpenAI Key
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY" # Replace this
# ...
```

-----

## 💻 How to Run

1.  Open your terminal in the project directory.

2.  Run the Streamlit application:

    ```bash
    streamlit run app.py
    ```

3.  The application will open in your web browser.

## 🔑 Authentication Process

When you click the **"Fetch Emails"** button:

1.  The `email_fetcher.py` script attempts to get an access token using the **Device Code Flow** (public client application).

2.  The console where you ran `streamlit run app.py` will display a message similar to:

    > To sign in, use a web browser to open the page [https://microsoft.com/devicelogin](https://www.google.com/search?q=https://microsoft.com/devicelogin) and enter the code **XXXX-XXXX-XXXX** to authenticate.

3.  **You must follow the instructions in the console** to sign in with your Microsoft account and grant the necessary permissions (`User.Read` and `Mail.Read`).

4.  Once authenticated, the app will proceed to fetch your emails.

-----

## 📂 File Structure

| File | Description |
| :--- | :--- |
| `app.py` | The main Streamlit application file. Handles the UI, state, and coordinates the fetching and QA processes. |
| `config.py` | Stores configuration variables like `CLIENT_ID`, `AUTHORITY`, and API `SCOPES`. |
| `email_fetcher.py` | Contains functions for Microsoft Graph authentication (`get_user_token`) and fetching emails for a specific date (`fetch_emails_for_day`). |
| `langchain_email_qa.py` | Sets up the LangChain RAG pipeline. Converts emails into documents, splits text, creates OpenAI embeddings, builds a Chroma vector store, and initializes the `RetrievalQA` chain. |
| `requirements.txt` | List of Python dependencies (You'll need to create this). |
| `chroma_db/` | (Generated at runtime) Local directory where the email embeddings are persisted by ChromaDB. |
