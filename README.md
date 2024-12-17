# Financial Data Bot

## Overview
The **Financial Data Bot(USA)** is a chatbot designed to provide users with insights and answers from company-reported financial data, such as income statements, balance sheets, and more. With a user-friendly interface, you can:

1. Ask questions about a specific company's financial data.
3. Receive data-driven suggestions and insights.

---

## Key Features
- **Question Answering:** Ask simple financial questions for a given company and get precise answers.
- **Data-Driven Suggestions:** Receive actionable insights and suggestions based on the company's financial performance.

---

## Technology Stack

The Financial Data Bot leverages the latest advancements in AI and data processing technologies:

- **Retrieval-Augmented Generation (RAG):** For accurate and context-aware responses.
- **Large Language Models (LLMs):** Powered by **Google Gemini** or **OpenAI** models for natural language understanding.
- **Data Processing:** Efficient handling of financial data using **Pandas** and custom scripts.
- **APIs:** To fetch, process, and serve up-to-date financial data.
- **Streamlit:** For creating an intuitive and interactive web application.
- **PostgreSQL:** For robust and scalable data storage and retrieval.
- **Python:** The backbone of the application, powering logic, data processing, and integrations.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/financial-data-bot.git
   cd financial-data-bot
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory and configure the following:
   ```env
   API_KEY=<Your_API_Key>
   DATABASE_URL=<Your_Postgres_Database_URL>
   LLM_PROVIDER=<OpenAI_or_Google_Gemini>
   ```

4. Start the application:
   ```bash
   streamlit run app.py
   ```

---

## Usage

- **Ask Questions:** Enter a company name and a financial query (e.g., "What is the revenue of Company X in 2023?").
- **Get Insights:** Ask for suggestions such as "What are the key financial risks for Company Y?"

---

## Folder Structure
```
financial-data-bot/
├── app.py              # Streamlit application entry point
├── main.py             # Model code
├── Data/               # Sample data and datasets
├── Models/             # Scripts for LLM and RAG integration
├── Database/           # PostgreSQL setup and queries
├── utils/              # Helper functions and scripts and LLM
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## Future Enhancements
- Expand support for more complex financial queries.
- Integrate additional data sources, such as live stock prices.
- Support multi-language queries and responses.
- Add more visualization options (e.g., heatmaps, bubble charts).

---

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push to the branch:
   ```bash
   git commit -m "Added feature"
   git push origin feature-name
   ```
4. Open a pull request on GitHub.

---

