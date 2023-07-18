from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import URL, Source, IP
from utils import is_url, get_iocs, load_json_file, get_connection_string


def get_src(src_name):
    src = session.query(Source).filter_by(name=src_name).first()
    if src is None:
        new_source = Source(name=src_name)
        session.add(new_source)
        session.flush()  # Flush the session to generate the ID for the new source
        src = new_source
    return src


def upload_url(addr, src_name):
    src = get_src(src_name)
    new_url = URL(
        url=addr,
        id_source=src.id
    )
    session.add(new_url)
    session.commit()


def upload_ip(addr, src_name):
    src = get_src(src_name)
    new_ip = IP(
        ip_address=addr,
        id_source=src.id
    )
    session.add(new_ip)
    session.commit()


def upload_to_database(addr_list, src_name):
    for address in addr_list:
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
