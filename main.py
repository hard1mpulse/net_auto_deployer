import os,logging
from modules.configuration_reader import read_yamls_from_dir,read_yaml_configuration
from modules.configuration_reader import import_env_params
from modules.netbox import get_devices_list_from_nb_instances
from modules.transport_methods.ssh import create_ssh_connection, get_backup_from_device_via_ssh
from modules.backuper import write_backup
from dotenv import load_dotenv
load_dotenv()

conf_dir,backup_dir,logfile=import_env_params()
backuper_config = read_yaml_configuration(conf_dir + "backuper.yml")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename=logfile)
logger = logging.getLogger(__name__)

nb_instances=read_yamls_from_dir('netbox_instances/')
for instance,devices in get_devices_list_from_nb_instances(nb_instances).items():
    for device in devices:
        if ssh_conn:=create_ssh_connection(device):
            write_backup(get_backup_from_device_via_ssh(ssh_conn),device["name"],backuper_config)