import json
from Data.finhub import Company_Reported_Financials

def get_match(list_of_values, list_of_variable, llm_class):

    prompt = f"""
        You are given a list of values and a list of variables. Find the best match of variables amoung the list of values.
        The variable represents a financial constant that the user is interested in.

        Return the best match of variables from the list of values.

        List of values: {list_of_values}
        List of variables: {list_of_variable}

        Return answer in the json format as following: """ + """
        {variable1: match1, variable2: match2, variable3: match3}
        """

    response = llm_class.call_llm(prompt)

    return response


def extract_json_from_string(input_string):
    try:
        # Find the first and last curly brace in the string
        start = input_string.find('{')
        end = input_string.rfind('}') + 1

        # Extract the JSON substring
        json_string = input_string[start:end]

        # Parse the JSON string into a dictionary
        return json.loads(json_string)
    except (ValueError, json.JSONDecodeError) as e:
        print("Error decoding JSON:", e)
        return None

def get_reported_financials(llm_class, ticker: str, values: list, year=None, quarter=None, source=None, category=None):
    """
    Retrieves reported financials for a given ticker, values, year, and quarter, considering the source.

    Args:
        ticker (str): The stock ticker symbol.
        values (list): A list of financial metrics to retrieve.
        year (int, optional): The year to filter by. Defaults to None.
        quarter (int, optional): The quarter to filter by. Defaults to None.
        source (str, optional): The source of the data ('10-K' or '10-Q'). Defaults to None.

    Returns:
        dict: A dictionary containing the requested financial data.
    """
    answers = {}

    frequencies = ['annual', 'quarterly']
    if source == '10-K':
        frequencies = ['annual']  # Only search in annual data for 10-K
    elif source == '10-Q':
        frequencies = ['quarterly']  # Only search in quarterly data for 10-Q

    for freq in frequencies:
        reported_financials = Company_Reported_Financials(ticker=ticker, freq=freq)

        if len(values) > 0:
            # Filter metrics based on year and quarter for available metrics
            metrics_available = reported_financials.get_available_metrics(year, quarter)

            response = get_match(list(metrics_available), values, llm_class)
            matches = extract_json_from_string(response)

            if matches:
                for variable, labels in matches.items():
                    if variable not in answers:
                        answers[variable] = {}

                    for label in labels:  # Iterate over each label in the list of labels
                        data = reported_financials.get_label_data(label=label, year=year, quarter=quarter, category=category)
                        if answers[variable].get(label) is None:
                            answers[variable][label] = [data]
                        else:
                            answers[variable][label].append(data)

        else:
            data = reported_financials.get_label_data(label=None, year=year, quarter=quarter, category=category)

            if "values" not in answers:
                answers["values"] = [data]
            else:
                answers["values"].append(data)

    return answers

def get_reported_financials_series(llm_class, ticker: str, values: list, frequency="annual", source=None, category=None):
    """
    Retrieves reported financials for a given ticker, values, considering the source.

    Args:
        ticker (str): The stock ticker symbol.
        values (list): A list of financial metrics to retrieve.
        source (str, optional): The source of the data ('10-K' or '10-Q'). Defaults to None.

    Returns:
        dict: A dictionary containing the requested financial data.
    """
    answers = {}

    if source == '10-K' and frequency == 'quarterly':
        freq = None
    elif source == '10-K':
        freq = 'annual'
    elif source == '10-Q':
        freq = 'quarterly'
    elif frequency == 'quarterly':
        freq = 'quarterly'
    else:
        freq = frequency

    if len(values)>0:

        reported_financials = Company_Reported_Financials(ticker=ticker, freq=freq)

        # Filter metrics based on year and quarter for available metrics
        metrics_available = reported_financials.get_available_metrics()

        response = get_match(list(metrics_available), values, llm_class)
        matches = extract_json_from_string(response)

        if matches:
            for variable, labels in matches.items():
                if variable not in answers:
                    answers[variable] = {}

                for label in labels:  # Iterate over each label in the list of labels
                    data = reported_financials.get_label_series(label=label, frequency=frequency, category=category)
                    if answers[variable].get(label) is None:
                        answers[variable][label] = [data]
                    else:
                        answers[variable][label].append(data)

    else:
        data = reported_financials.get_label_series(label=None, frequency=frequency, category=category)

        if "values" not in answers:
            answers["values"] = [data]
        else:
            answers["values"].append(data)

    return answers
