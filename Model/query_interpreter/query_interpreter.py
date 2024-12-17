from datetime import datetime
import json
import logging 

class Query_Interpreter:
    def __init__(self, llm_class):
        """
        Initializes the Query_Interpreter with a Gemini LLM instance.
        :param gemini_api_key: API key for the Gemini model.
        """
        self.llm = llm_class

    def extract_json_from_string(self, input_string):
       try:
           # Find the first and last curly brace in the string
           start = input_string.find('{')
           end = input_string.rfind('}') + 1
    
           # Extract the JSON substring
           json_string = input_string[start:end]

           print(json_string)
    
           # Parse the JSON string into a dictionary
           return eval(json_string)
       except (ValueError, json.JSONDecodeError) as e:
           print("Error decoding JSON:", e)
           return None

    def identify_entities(self, user_question):
        """
        Identifies which entities are present in the user query.
        :param user_question: The question asked by the user.
        :return: A list of detected entities (e.g., ['company name', 'terms', 'year']).
        """
        prompt = f"""
        You are a financial assistant tasked with identifying which entities are present in a user's query. 
        The entities are:
        1. company_name (e.g., Apple, Nvidia)
        2. ticker (e.g., AAPL, BABA)
        3. terms (e.g., income, profit, loss, debt)
        4. year (e.g., 2023, 2024)
        5. quarter (e.g., 1, 2)
        6. document (e.g., 10-K, 10-Q, 8-K)
        7. statement (e.g., income, cash flow, balance sheet)

        Your task:
        - Analyze the user's query step-by-step and determine which of these entities are present.
        - Return a list of detected entities in this format:
          ['entity1', 'entity2', ...]

        Examples:
        1. User query: "What is Apple's income in 2023?"
           Output: ['company_name', 'terms', 'year']

        2. User query: "Fetch Tesla's 10-K document for Q2 2022."
           Output: ['company_name', 'document', 'quarter', 'year']

        3. User query: "Show Nvidia's balance sheet."
           Output: ['company_name', 'statement']

        4. User query: "What is the profit for AAPL in 2023 and 2024?"
           Output: ['ticker', 'terms', 'year']

        User query: "{user_question}"
        """
        response = self.llm.call_llm([{"role": "user", "content": prompt}])
        try:
            return eval(response)
        except Exception as e:
            logging.info({"Error in identifying entities": e})
            return [None]

    def extract_company_and_ticker(self, user_question):
        """
        Extracts company names and tickers from the user query.
        :param user_question: The question asked by the user.
        :return: A JSON object with 'company_name' and 'ticker'.
        """
        prompt = f"""
        You are a financial assistant specializing in identifying companies and tickers from user queries.
        Your task:
        - Identify all company names and tickers mentioned in the user's query.
        - Return a JSON object in this format:
          {{'company_name': [list of company names], 'ticker': [list of tickers]}}

        If no company name or ticker is found, return `None` for that key.

        Examples:
        1. User query: "What is Apple's income in 2023?"
           Output: {{'company_name': ['Apple'], 'ticker': [None]}}

        2. User query: "BABA income statement for 2023."
           Output: {{'company_name': [None], 'ticker': ['BABA']}}

        3. User query: "Apple and Nvidia's income over the last 5 years."
           Output: {{'company_name': ['Apple', 'Nvidia'], 'ticker': [None]}}

        4. User query: "Show Tesla (TSLA) and Apple's profit."
           Output: {{'company_name': ['Tesla', 'Apple'], 'ticker': ['TSLA', None]}}

        User query: "{user_question}"
        """
        response = self.llm.call_llm([{"role": "user", "content": prompt}])
        try:
            #return eval(response[3:-4].split("json")[1])
            return self.extract_json_from_string(str(response))
        except Exception as e:
            return {'error': str(e)}

    def extract_time(self, user_question):
        """
        Extracts year and quarter from the user query.
        :param user_question: The question asked by the user.
        :return: A JSON object with 'year' and 'quarter'.
        """

        # Get today's date
        date = datetime.today()
        prompt = f"""
         You are a financial assistant specializing in extracting time information (year and quarter) from user queries.
         Your task:
         - Identify all years and quarters mentioned in the user's query.
         - Handle relative terms like 'last quarter' and 'last year' by calculating the current date.
         - Only return a JSON object in this format:
           {{'year': [list of years], 'quarter': [list of quarters]}}
         - If year or quarter is found return [None] in json value.

         Today is {date}

         Examples:
         1. If today is '2024-12-16':
            - 'curren year' is 2024.
            - 'current quarter' is 4.
            - 'Last quarter' is 3.
            - 'Last year' is 2023.

         2. User query: "What is Apple's income in 2023?"
            Output: {{'year': [2023], 'quarter': [None]}}

         3. User query: "Fetch Tesla's income for Q2 2022."
            Output: {{'year': [2022], 'quarter': ['2']}}

         4. User query: "Show Apple's income statement for the last quarter."
            Output: {{'year': [2024], 'quarter': ['3']}}

         5. User query: "What is Nvidia's profit last year?"
            Output: {{'year': [2023], 'quarter': [None]}}

         User query: "{user_question}
         
         Only return a json in anwer, nothing else"
         """
        response = self.llm.call_llm([{"role": "user", "content": prompt}])
        try:
            # return eval(response[3:-4].split("json")[1])
            return self.extract_json_from_string(response)
        except Exception as e:
            return {'error': str(e)}

    def extract_terms_documents_statements(self, user_question):
        """
        Extracts terms, document names, and statement types from the user query.
        :param user_question: The question asked by the user.
        :return: A JSON object with 'terms', 'document', and 'statement'.
        """
        prompt = f"""
        You are a financial assistant specializing in extracting terms, document names, and statement types from user queries.
        Your task:
        - Identify the financial terms (e.g., income, profit, debt), document names (e.g., 10-K, 10-Q, 8-K), and statement types (income, cash flow, balance sheet) mentioned in the user's query.
        - Return a JSON object in this format:
          {{'terms': [list of terms], 'document': [list of document names], 'statement': [list of statement codes]}}
        - If any of the statement like - income statement, cash flow statement and balance sheet, do not return any terms. 

        Statement codes:
        - "income statement" -> "ic"
        - "cash flow statement" -> "cf"
        - "balance sheet" -> "bs"

        If no value is found for any key, return `None` for that key.

        Examples:
        1. User query: "What is Apple's income in 2023 from the 10-K document?"
           Output: {{'terms': ['income'], 'document': ['10-K'], 'statement': [None]}}

        2. User query: "Show Apple's income from the income statement and cash flow statement in the 10-K."
           Output: {{'terms': ['income'], 'document': ['10-K'], 'statement': ['ic', 'cf']}}

        3. User query: "What is Tesla's profit in the 8-K?"
           Output: {{'terms': ['profit'], 'document': ['8-K'], 'statement': [None]}}

        4. User query: "Show Nvidia's balance sheet."
           Output: {{'terms': [None], 'document': [None], 'statement': ['bs']}}

        5. User query: "Income statement of Nvidia."
           Output: {{'terms': [None], 'document': [None], 'statement': ['ic']}}  (No terms as a income statement is asked.)

        User query: "{user_question}"
        """
        response = self.llm.call_llm([{"role": "user", "content": prompt}])
        try:
            # return eval(response[3:-4].split("json")[1])
            return self.extract_json_from_string(response)
        except Exception as e:
            return {'error': str(e)}
