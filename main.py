from modules.configuration_reader import read_yaml_configuration
from modules.netbox import create_netbox_connection
import os
from dotenv import load_dotenv
load_dotenv()
conf_dir = os.getenv('CONFIGURATIONS_DIR')

for instance,params in read_yaml_configuration(conf_dir).items():
    print(create_netbox_connection(params))
