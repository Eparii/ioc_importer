import json


def get_connection_string(config_path):
    """
    Returns connection string based on data in the provided config file

            Parameters:
                    config_path (str): A path to config file

            Returns:
                    connection_string (str): connection string for the database
    """
    config = open(config_path)
    config_json = json.load(config)
    db_credentials = config_json['database']

    connection_string = f"postgresql://{db_credentials['username']}:{db_credentials['password']}@" \
                        f"{db_credentials['host']}:{db_credentials['port']}/{db_credentials['database']}"

    return connection_string
