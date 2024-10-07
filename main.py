from modules.configuration_reader import read_yamls_from_dir
from modules.netbox import get_devices_list_from_nb_instances
import os,logging
from dotenv import load_dotenv
load_dotenv()
conf_dir = os.getenv('CONFIGURATIONS_DIR')
logfile = os.getenv('LOGFILE')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename=logfile)
logger = logging.getLogger(__name__)

nb_instances=read_yamls_from_dir(conf_dir+'/netbox_instances/')
print(get_devices_list_from_nb_instances(nb_instances))


