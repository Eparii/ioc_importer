from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import URL, Source, IP
from utils import is_url, get_iocs, load_json_file, get_connection_string


def get_src(src_name):
    """
       Retrieves or creates a source in the database based on the provided source name.

       Parameters:
           src_name (str): The name or source identifier for which to retrieve or create the source.

       Returns:
           Source: The retrieved or newly created source object.
    """
    src = session.query(Source).filter_by(name=src_name).first()
    if src is None:
        new_source = Source(name=src_name)
        session.add(new_source)
        session.flush()  # Flush the session to generate the ID for the new source
        src = new_source
    return src


def upload_url(addr, src_name):
    """
    Uploads a URL to the database with the corresponding source information.

    Parameters:
        addr (str): The URL address to be uploaded to the database.
        src_name (str): The name or source identifier associated with the URL.

    Returns:
        None
    """
    src = get_src(src_name)
    new_url = URL(
        url=addr,
        id_source=src.id
    )
    session.add(new_url)
    session.commit()


def upload_ip(addr, src_name):
    """
    Uploads an IP address to the database with the corresponding source information.

    Parameters:
        addr (str): The IP address to be uploaded to the database.
        src_name (str): The name or source identifier associated with the IP address.

    Returns:
        None
    """
    src = get_src(src_name)
    new_ip = IP(
        ip_address=addr,
        id_source=src.id
    )
    session.add(new_ip)
    session.commit()


def upload_to_database(addr_list, src_name):
    """
     Uploads a list of addresses to the database, distinguishing between URLs and IP addresses.

     Parameters:
         addr_list (list): A list of addresses (URLs or IP addresses) to be uploaded.
         src_name (str): The name or source identifier for the uploaded addresses.

     Returns: None
    """
    for i, address in enumerate(addr_list):
        if i % 100 == 0 and i != 0:
            print("Currently uploading address " + str(i) + "/" + str(len(addr_list)) + " from source " + src_name)
        if is_url(address):
            upload_url(address, src_name)
        else:
            upload_ip(address, src_name)


if __name__ == '__main__':
    config_path = '../config.json'

    config = load_json_file(config_path)
    engine = create_engine(get_connection_string(config_path))
    Session = sessionmaker(bind=engine)
    session = Session()
    urls = config['urls']
    iocs = get_iocs(urls)

    for source_name in iocs:
        addresses = iocs[source_name]
        upload_to_database(addresses, source_name)
    print('Successfully uploaded given Indicators of Compromise in the database')
