from models import URL, Source, IP
from utils import get_connection_string

if __name__ == "__main__":
    print(get_connection_string('../config.json'))
