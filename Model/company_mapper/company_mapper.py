from Data.edgar import get_ticker_data
from fuzzywuzzy import process
import pandas as pd

def company_mapper(company_name, top_n=1):
    ticker_df = get_ticker_data()

    matches = process.extract(company_name, ticker_df['title'], limit=top_n)
    
    # Create a result list containing the matching tickers and scores
    result = [
        {'ticker': ticker_df.loc[ticker_df['title'] == match[0], 'ticker'].values[0], 'title': match[0], 'score': match[1]}
        for match in matches
    ]
    
    return result


    