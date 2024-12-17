import finnhub
import logging
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the API key
finnhub_api_key = os.getenv('FINNHUB_API_KEY')

def financials_reported(ticker, freq):
    """
    Retrieves financial reports for a given ticker and frequency using the Finnhub API.

    Parameters:
        finhub_api_key (str): Finnhub API key.
        ticker (str): Stock ticker symbol.
        freq (str): Frequency of financial reports (e.g., 'annual', 'quarterly').

    Returns:
        dict: Financial reports data, or None if an error occurs.
    """
    try:
        # Create a client instance
        finnhub_client = finnhub.Client(api_key=finnhub_api_key)
        
        # Retrieve financial data
        output = finnhub_client.financials_reported(symbol=ticker, freq=freq)
        
    except Exception as e:
        print(e)
        logging.info({"Error in financials_reported": e})
        return None
    
    finally:
        # Cleanup logic (if applicable) could go here
        del finnhub_client  # Explicitly delete the client to free resources

    return output

def calculate_year_and_quarter(entry):
    """
    Calculates the year and quarter for a dictionary if they are not provided.
    """
    if 'year' not in entry or not entry['year'] or 'quarter' not in entry or not entry['quarter']:
        if 'filedDate' in entry and entry['filedDate']:
            filed_date = datetime.strptime(entry['filedDate'], '%Y-%m-%d %H:%M:%S')
            year = filed_date.year
            month = filed_date.month

            # Assign year and quarter based on the filing date
            entry['year'] = year
            if 2 <= month <= 4:
                entry['quarter'] = 1
            elif 5 <= month <= 7:
                entry['quarter'] = 2
            elif 8 <= month <= 10:
                entry['quarter'] = 3
            else:  # November to January
                entry['quarter'] = 4

class Company_Reported_Financials:

    def __init__(self, ticker: str, freq: str):
        self.ticker = ticker
        self.freq = freq

        try:
            self.json_value = financials_reported(ticker=self.ticker, freq=self.freq)
            self.df = self.create_frame(self.json_value)
        except Exception as e:
            print(e)
            logging.info({"Error in company_basic_financials":e})
            self.json_value = None

    def create_frame(self, json_dict):

        """
    Converts a list of dictionaries into a DataFrame with the specified format.
    Ensures year and quarter are calculated if missing.
    """
        rows = []

        symbol = json_dict.get('symbol', '')
        cik = json_dict.get('cik', '')

        for entry in json_dict['data']:
            # Calculate year and quarter if not available
            calculate_year_and_quarter(entry)
            # Extract common fields

            year = entry.get('year', '')
            quarter = entry.get('quarter', '')
            form = entry.get('form', '')
            filed_date = entry.get('filedDate', '')

            report = entry.get('report', {})
            for category, items in report.items():
                for item in items:
                    row = {
                        'symbol': symbol,
                        'cik': cik,
                        'year': year,
                        'quarter': quarter,
                        'form': form,
                        'filedDate': filed_date,
                        'category': category,
                        'label': item.get('label', ''),
                        'value': item.get('value', ''),
                        'unit': item.get('unit', '')
                    }
                    rows.append(row)

        df = pd.DataFrame(rows)

        return df


    def get_available_metrics(self, year=None, quarter=None):
        """
        Gets available metrics based on year and quarter, or latest available data.

        Args:
            year (int, optional): The year to filter by. Defaults to None.
            quarter (int, optional): The quarter to filter by. Defaults to None.

        Returns:
            np.ndarray: An array of unique available metrics.
        """
        try:
            if year and quarter:
                # If both year and quarter are provided, filter by both
                available_metrics = self.df[(self.df['year'] == year) & (self.df['quarter'] == quarter)]['label'].unique()
            elif year and not quarter:
                # If only year is provided, filter by year and get latest quarter
                filtered_df = self.df[self.df['year'] == year]
                latest_quarter = filtered_df['quarter'].max()  # Get latest quarter for the year
                available_metrics = filtered_df[filtered_df['quarter'] == latest_quarter]['label'].unique()
            else:
                # If neither year nor quarter are provided, get latest available data
                latest_year = self.df['year'].max()  # Get latest year
                filtered_df = self.df[self.df['year'] == latest_year]
                latest_quarter = filtered_df['quarter'].max()  # Get latest quarter for the latest year
                available_metrics = filtered_df[filtered_df['quarter'] == latest_quarter]['label'].unique()

            return available_metrics

        except Exception as e:
            print(e)
            logging.info({"Error in get_available_metrics": e})
            return None

    # def get_label_data(self, label, year=None, quarter=None):
    #     """
    #     Extracts data for a specific label, filtering by year and quarter if provided.

    #     Args:
    #         label (str): The label to extract data for.
    #         year (int, optional): The year to filter by. Defaults to None.
    #         quarter (int, optional): The quarter to filter by. Defaults to None.

    #     Returns:
    #         pandas.DataFrame or pandas.Series: The filtered DataFrame or Series containing data for the label.
    #     """
    #     try:
    #         filtered_df = self.df[self.df['label'] == label]

    #         if year and quarter:
    #             # Filter by year and quarter
    #             filtered_df = filtered_df[(filtered_df['year'] == year) & (filtered_df['quarter'] == quarter)]
    #         elif year and not quarter:
    #             # Filter by year and get latest quarter
    #             filtered_df = filtered_df[filtered_df['year'] == year]
    #             latest_quarter = filtered_df['quarter'].max()
    #             filtered_df = filtered_df[filtered_df['quarter'] == latest_quarter]
    #         elif not year and quarter:
    #             # Filter by quarter and get latest year
    #             filtered_df = filtered_df[filtered_df['quarter'] == quarter]
    #             latest_year = filtered_df['year'].max()
    #             filtered_df = filtered_df[filtered_df['year'] == latest_year]
    #         else:
    #             # Get latest available data
    #             latest_year = filtered_df['year'].max()
    #             filtered_df = filtered_df[filtered_df['year'] == latest_year]
    #             latest_quarter = filtered_df['quarter'].max()
    #             filtered_df = filtered_df[filtered_df['quarter'] == latest_quarter]

    #         return filtered_df

    #     except Exception as e:
    #         print(e)
    #         logging.info({"Error in get_label_data": e})
    #         return None

    def get_label_data(self, label=None, year=None, quarter=None, category=None):
        """
        Extracts data for a specific label, filtering by year, quarter, and category if provided.

        Args:
            label (str, optional): The label to extract data for. Defaults to None.
            year (int, optional): The year to filter by. Defaults to None.
            quarter (int, optional): The quarter to filter by. Defaults to None.
            category (str, optional): The category to filter by (e.g., "income statement", "cashflow", "balance sheet"). Defaults to None.

        Returns:
            pandas.DataFrame or pandas.Series: The filtered DataFrame or Series containing data for the specified filters.
        """
        try:
            filtered_df = self.df

            # Filter by label if provided
            if label:
                filtered_df = filtered_df[filtered_df['label'] == label]

            # Filter by category if provided
            if category:
                filtered_df = filtered_df[filtered_df['category'] == category]

            if year and quarter:
                # Filter by year and quarter
                filtered_df = filtered_df[(filtered_df['year'] == year) & (filtered_df['quarter'] == quarter)]
            elif year and not quarter:
                # Filter by year and get the latest quarter
                filtered_df = filtered_df[filtered_df['year'] == year]
                latest_quarter = filtered_df['quarter'].max()
                filtered_df = filtered_df[filtered_df['quarter'] == latest_quarter]
            elif not year and quarter:
                # Filter by quarter and get the latest year
                filtered_df = filtered_df[filtered_df['quarter'] == quarter]
                latest_year = filtered_df['year'].max()
                filtered_df = filtered_df[filtered_df['year'] == latest_year]
            else:
                # Get the latest available data
                latest_year = filtered_df['year'].max()
                filtered_df = filtered_df[filtered_df['year'] == latest_year]
                latest_quarter = filtered_df['quarter'].max()
                filtered_df = filtered_df[filtered_df['quarter'] == latest_quarter]

            return filtered_df

        except Exception as e:
            print(e)
            logging.info({"Error in get_label_data": e})
            return None
  
    def get_label_series(self, label=None, frequency='annual', category=None):
        """
        Returns a series of data for a specific label based on the frequency.

        Args:
            label (str): The label to extract data for.
            frequency (str, optional): The frequency of the data ('yearly' or 'quarterly'). Defaults to 'yearly'.

        Returns:
            pandas.DataFrame: A DataFrame containing the series of data for the label.
        """
        try:
            if category:
                filtered_df = self.df[self.df['category'] == category]
            else:
                filtered_df = self.df

            if label:
                filtered_df = filtered_df[filtered_df['label'] == label]

            if frequency == 'quarterly':
                # Return all quarterly data
                return filtered_df
            elif frequency == 'annual':
                # Return latest quarter data for each year
                yearly_data = filtered_df.groupby('year')['quarter'].max().reset_index()
                series_data = pd.merge(yearly_data, filtered_df, on=['year', 'quarter'], how='left')
                return series_data
            else:
                raise ValueError("Invalid frequency. Choose 'annual' or 'quarterly'.")

        except Exception as e:
            print(e)
            logging.info({"Error in get_label_series": e})
            return None