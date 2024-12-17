import requests
import pandas as pd
from io import BytesIO
from zipfile import ZipFile

email = "official.jain.pratik@gmail.com"
headers = {'User-Agent': email}

def get_ticker_data(headers=headers):
    try:
        # Fetch the ticker data from the SEC
        response = requests.get(
            "https://www.sec.gov/files/company_tickers.json",
            headers=headers
        )
        response.raise_for_status()  # Ensure the request was successful

        # Create DataFrame from the JSON response
        ticker_df = pd.DataFrame(response.json()).T

        return ticker_df
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch data from the SEC: {e}")
    except Exception as e:
        raise RuntimeError(f"An error occurred: {e}")

def get_cik_from_ticker(companyTicker, headers):
    try:
        # Fetch the ticker data from the SEC
        response = requests.get(
            "https://www.sec.gov/files/company_tickers.json",
            headers=headers
        )
        response.raise_for_status()  # Ensure the request was successful

        # Create DataFrame from the JSON response
        ticker_df = pd.DataFrame(response.json()).T

        # Add zero-padded CIK numbers
        ticker_df['cik_number'] = ticker_df['cik_str'].astype(str).str.zfill(10)

        # Check if the ticker exists
        match = ticker_df[ticker_df['ticker'] == companyTicker.upper()]
        if match.empty:
            raise ValueError(f"Ticker '{companyTicker}' not found.")

        # Return the first matching CIK number
        return match['cik_number'].iloc[0]
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch data from the SEC: {e}")
    except Exception as e:
        raise RuntimeError(f"An error occurred: {e}")
    
def get_filing_metadata(cik, headers):
    try:
        # Fetch the filing metadata from the SEC
        response = requests.get(
            f'https://data.sec.gov/submissions/CIK{cik}.json',
            headers=headers
        )
        response.raise_for_status()  # Ensure the request was successful

        # Parse the JSON response
        data = response.json()

        # Validate the presence of necessary keys
        if 'cik' not in data or 'filings' not in data or 'recent' not in data['filings']:
            raise ValueError("Unexpected response structure from SEC API.")

        # Return relevant metadata
        return data['cik'], data['filings']['recent']

    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch filing metadata from the SEC: {e}")
    except ValueError as e:
        raise RuntimeError(f"Data validation error: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")
    
def get_custom_quarter(date):
    """Assign quarters based on custom month ranges."""
    month = date.month
    if 2 <= month <= 4:
        return 1
    elif 5 <= month <= 7:
        return 2
    elif 8 <= month <= 10:
        return 3
    else:  # Covers November to January
        return 4

def get_quarter(date):
    """Assign quarters based on custom month ranges."""
    month = date.month
    if 1 <= month <= 3:
        return 1
    elif 4 <= month <= 6:
        return 2
    elif 7 <= month <= 9:
        return 3
    else:  # Covers November to January
        return 4

def get_all_recent_forms(recent_filings, headers):
    try:
        # Convert recent filings to a DataFrame
        df = pd.DataFrame.from_dict(recent_filings)

        return df
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")
    
def get_link(cik, accessionNumber, primaryDocument):
    try:
        # Validate inputs
        if not (cik and accessionNumber and primaryDocument):
            raise ValueError("One or more inputs are missing.")

        # Construct the SEC document URL
        accessionNumber = str(accessionNumber).replace("-", "")
        url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accessionNumber}/{primaryDocument}"

        return url

    except ValueError as e:
        raise RuntimeError(f"Input validation error: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")
    
def get_available_documents(allForms):
    try:
        # Validate input DataFrame
        if 'form' not in allForms.columns or 'reportDate' not in allForms.columns:
            raise ValueError("The input DataFrame must contain 'form' and 'reportDate' columns.")

        # Get unique document types
        document_types = allForms['form'].unique()

        # Add a custom quarter column based on the filing date
        # For 10-K/A, 10-Q/A, 8-K/A
        allForms['quarter'] = allForms['reportDate'].apply(
            lambda x: get_custom_quarter(pd.to_datetime(x))
        )

        # Build a dictionary mapping document types to filing dates
        document_types_dict = {
            doc_type: allForms[allForms['form'] == doc_type]['filingDate'].tolist()
            for doc_type in document_types
        }

        return document_types_dict

    except ValueError as e:
        raise RuntimeError(f"Data validation error: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")


def get_document(allForms, document_type, headers, year, cik_number, quarter=None, month=None):
    forms = allForms[allForms['form'] == document_type]

    if not year:
        # Extract the latest year from the 'reportDate' column
        latest_date = forms['reportDate'].max()
        year = int(latest_date[:4]) 

    if year:
        forms = forms[forms['reportDate'].str.startswith(str(year))]

    if quarter:
        forms = forms[forms['quarter'] == quarter]

    if month:
        forms = forms[forms['reportDate'].str.startswith(f"{year}-{month:02d}")]

    forms['url'] = forms.apply(
        lambda row: get_link(
            cik=cik_number,
            accessionNumber=row['accessionNumber'],
            primaryDocument=row['primaryDocument']
        ),
        axis=1
    )

    return forms

def get_requested_document(document, year, quarter, ticker):
    cik = get_cik_from_ticker(companyTicker=ticker, headers=headers)
    cik_number, recent_filings = get_filing_metadata(cik, headers)
    allForms = get_all_recent_forms(recent_filings, headers)
    available_docs = get_available_documents(allForms)
    docs = get_document(allForms, document, headers, year, quarter=quarter, cik_number=cik_number)

    docs_dict = docs.to_dict(orient='records')

    return docs_dict

# ans = get_requested_document(document="10-Q", year= None, quarter = None, ticker = "AAPL")
# print(ans)