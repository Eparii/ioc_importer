import json
import requests
from tldextract import extract
import re


def load_json_file(json_path):
    """
    Loads a JSON file and returns it as a dictionary.

    Parameters:
        json_path (str): The path to the JSON file.

    Returns:
        json_file (dict): The contents of the JSON file as a dictionary.
    """
    file = open(json_path)
    json_file = json.load(file)
    return json_file


def get_connection_string(config_path):
    """
    Returns connection string based on data in the provided json config file

            Parameters:
                    config_path (str): A path to the config file

            Returns:
                    connection_string (str): A connection string for the database
    """
    config_json = load_json_file(config_path)
    db_credentials = config_json['database']

    connection_string = f"postgresql://{db_credentials['username']}:{db_credentials['password']}@" \
                        f"{db_credentials['host']}:{db_credentials['port']}/{db_credentials['database']}"

    return connection_string


def get_iocs(urls):
    iocs_dict = {}
    for url in urls:
        addresses = []
        extracted = extract(url)
        response = requests.get(url)
        data = response.text
        lines = [line for line in data.splitlines() if not line.startswith('#')]
        for line in lines:
            address = get_address(line)
            if address is not None:
                addresses.append(address)
        iocs_dict[extracted.domain] = addresses
    return iocs_dict


def is_url(address):
    pattern_url = r'https?:\/\/\S+'
    if re.match(pattern_url, address):
        return True
    else:
        return False


def get_address(string):
    # Matches IPs and URLs until the first occurrence of whitespace, double quotation mark or hashtag
    pattern = r'(https?:\/\/[^\"\s#]+)|((\d{1,3}\.){3}\d{1,3})'
    address = re.search(pattern, string)
    if address is not None:
        return address.group(0)
