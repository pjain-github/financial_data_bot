import logging
import json
from Utils.llm import Gemini
from Utils.chat_history_processing import get_historical_questions
from Model.router.router import Router
from Model.rewriter.chat_history import ChatHistory
from Model.small_talk.small_talk import Small_Talk
from Model.query_interpreter.query_interpreter import Query_Interpreter
from Model.retriver.retriver import get_simple_data, get_series_data, get_documents_from_edger
from Model.synthesizer.synthesizer import Synthesizer
from Model.company_mapper.company_mapper import company_mapper
import os
from itertools import product
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key
gemini_api_key = os.getenv('GEMINI_API_KEY')

def financial_bot(query: str, chat_history: json, gemini_api_key: str):

    # LLM
    llm = Gemini(api_key = gemini_api_key) 

    chat_history = get_historical_questions(chat_history) 

    try:
        # Query Rewriter
        rewriter = ChatHistory(llm_class=llm)
        new_question = rewriter.query_rewriter(chat_history=chat_history, query=query)
        logging.info({"Rewriter answer": new_question})
        print(new_question)
    except Exception as e:
        logging.info({"Error in query rewriter":e})
        return "Sorry, google gemini is down for this application"

    # Router
    try:
        router = Router(llm)
        router_result = router.categorize_question(new_question)
        logging.info({"Router result": router_result})
        print(router_result)
    except Exception as e:
        logging.info({"Error in rotuer":e})
        return "Sorry, google gemini is down for this application and we are unable to router your queries"

    # Small Talk
    if router_result['type'] == "small talk":
        try:
            small_talk = Small_Talk(llm_class=llm)
            ans = small_talk.small_talk(new_question)

            return ans
        except Exception as e:
            logging.info({"Error in Small Talk module": e})
            return "Hi. We are facing some difficulty connecting to the google server."
    
    else:
        query = {
            'company_name': [None],
            'ticker': [None],
            'terms' : [None],
            'year' : [None],
            'quarter' : [None],
            'statement' : [None],
            'document': [None]
        }

        qi = Query_Interpreter(llm)    
        # Identify entities in the user query
        entities = qi.identify_entities(user_question=new_question)
        print(entities)
        # Extract company names and tickers if they are mentioned in the entities
        if 'company_name' in entities or 'ticker' in entities:

            try:
                company_data = qi.extract_company_and_ticker(user_question=new_question)
                query['company_name'] = company_data['company_name']
                query['ticker'] = company_data['ticker']

                logging.info({"Company Data": company_data})
                print(company_data)
            except Exception as e:
                logging.info({"Error extracting company detauls": e})
                print(e)

        # Extract terms, document names, and statements if they are mentioned in the entities
        if 'terms' in entities or 'document' in entities or 'statement' in entities:
            
            try:
                terms_data = qi.extract_terms_documents_statements(user_question=new_question)
                query['terms'] = terms_data['terms']        
                query['statement'] = terms_data['statement']
                query['document'] = terms_data['document']

                logging.info({"Terms, Documents, and Statements Data": terms_data})
                print(terms_data)
            except Exception as e:
                logging.info({"Error extracting document detauls": e})
                print(e)

        # Extract year and quarter if they are mentioned in the entities
        if 'year' in entities or 'quarter' in entities:

            try:
                time_data = qi.extract_time(user_question=new_question)
                query['year'] = time_data["year"]
                query['quarter'] = time_data["quarter"]

                logging.info({"Time Data": time_data})
                print(time_data)
            except Exception as e:
                logging.info({"Error extracting time detauls": e})
                print(e)
    
        if query['terms'] == None or query['terms']==[None]:
            query['terms'] = []

        for keys in query.keys():
            if query[keys] == None:
                query[keys] = [None]
    # 
    data = "No data found"

    # Company Mapper
    if query['company_name'][0]:
        for company in query['company_name']:
            company_ticker = company_mapper(company)[0]['ticker']
            logging.info({f"Company Ticker for {company}": company_ticker})
            print({f"Company Ticker for {company}": company_ticker})

            if query['ticker'] == [None]:
                query['ticker'] = []
            
            if company_ticker not in query['ticker']:
                query['ticker'].append(company_ticker)

    if router_result['type'] == 'simple variables' or router_result['type'] == 'simple reports':
        # data = get_reported_financials(ticker = query['ticker'], values= query['terms'], year=query['year'], quarter=query['quarter'], source=query['document'], category=query['statement'])
        data = get_simple_data(query, llm)
        logging.info({"Data": data})
        print(data)
    
    if router_result['type'] == 'series variables' or router_result['type'] == 'series reports':
        data = get_series_data(query, llm)
        logging.info({"Data": data})
        print(data)

    if router_result['type'] == 'documents':
        data = get_documents_from_edger(question=query)

    try:

        synthesizer = Synthesizer(llm = llm)
        ans = synthesizer.synthesize_answer(user_question=new_question, data= data)
    
    except Exception as e:
        print(e)
        logging.info({"Error is answer":e})
        ans = "Sorry, we are facing some issues. Will be back soon!"     

    # if router_result['graph']:
    #     # code = synthesizer.create_chart(user_question=new_question, answer=ans)
    #     pass

    return ans

# chat_hst = [{'role': 'user', 'content': 'Can you get income statement and balance sheet for AAPL for 2024?'}]
# ans = financial_bot(query="Can you also get me 10-K document for Apple for 2024?", chat_history=[], gemini_api_key=gemini_api_key)
# print(ans)


