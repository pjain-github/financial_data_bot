from Model.retriver.functions import get_reported_financials, get_reported_financials_series
from Data.edgar import get_requested_document
import logging

def generate_combinations_from_keys_simple(query):
    # Initialize an empty list to store the combinations
    combinations = []

    # Iterate through the nested structure based on specific keys
    # Handle default empty lists for missing or None keys
    ticker_list = query.get('ticker', [None])
    year_list = query.get('year', [None])
    quarter_list = query.get('quarter', [None])
    document_list = query.get('document', [None])
    statement_list = query.get('statement', [None])
    terms_list = query.get('terms')

    # Iterate through all possible combinations
    for ticker in ticker_list:
        for year in year_list:
            for quarter in quarter_list:
                for document in document_list:
                    for statement in statement_list:
                        # Create a dictionary for each combination
                        combination = {
                            'ticker': ticker,
                            'year': year,
                            'quarter': quarter,
                            'document': document,
                            'statement': statement,
                            'terms': terms_list
                        }
                        combinations.append(combination)
    return combinations

def generate_combinations_from_keys_seires(query):
    # Initialize an empty list to store the combinations
    combinations = []

    # Iterate through the nested structure based on specific keys
    # Handle default empty lists for missing or None keys
    ticker_list = query.get('ticker', [None])
    document_list = query.get('document', [None])
    statement_list = query.get('statement', [None])
    terms_list = query.get('terms')

    # Iterate through all possible combinations
    for ticker in ticker_list:
        for document in document_list:
            for statement in statement_list:
                # Create a dictionary for each combination
                combination = {
                    'ticker': ticker,
                    'document': document,
                    'statement': statement,
                    'terms': terms_list
                }
                combinations.append(combination)
    return combinations


def get_simple_data(question, llm_class):

    ans = []

    queries = generate_combinations_from_keys_simple(question)
    logging.info({"queries": queries})
    print(queries)

    for query in queries:
        ans.append(get_reported_financials(llm_class= llm_class, ticker = query['ticker'], values= query['terms'], year=query['year'], quarter=query['quarter'], source=query['document'], category=query['statement']))
    return ans

def get_series_data(question, llm_class):

    ans = []
    queries = generate_combinations_from_keys_seires(question)
    logging.info({"queries": queries})

    for query in queries:        
        ans.append(get_reported_financials_series(llm_class= llm_class, ticker = query['ticker'], values= query['terms'], frequency = 'annual', source=query['document'], category=query['statement']))
    return ans

def get_documents_from_edger(question):
    ans = []

    queries = generate_combinations_from_keys_simple(question)
    logging.info({"queries": queries})

    print(queries)

    for query in queries:        
        ans.append(get_requested_document(document=query['document'], year=query['year'], quarter=query['quarter'], ticker = query['ticker']))
            
    return ans

    