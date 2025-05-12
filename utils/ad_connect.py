import os
import configparser
from ldap3 import Server, Connection, ALL
from getpass import getpass
from colorama import init, Fore

init(autoreset=True)

def connect_to_ad():
    # Load configuration
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Get domain controller and base DN, with environment variable overrides
    domain_controller = os.getenv('AD_DOMAIN_CONTROLLER', config['DEFAULT']['domain_controller'])
    base_dn = os.getenv('AD_BASE_DN', config['DEFAULT']['base_dn'])

    # Prompt for credentials
    username = input("Enter AD username: ")
    password = getpass("Enter AD password: ")

    try:
        # Create LDAP server and connection
        server = Server(domain_controller, get_info=ALL)
        conn = Connection(server, user=f"{username}@{domain_controller.split('.')[0]}.com", password=password, auto_bind=True)
        print(Fore.GREEN + "Successfully connected to Active Directory")
        return conn
    except Exception as e:
        print(Fore.RED + f"Failed to connect to AD: {str(e)}")
        raise