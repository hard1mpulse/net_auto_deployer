import os,logging,time
from modules.configuration_reader import read_yamls_from_dir, read_yaml_configuration,import_env_params
from modules.netbox import get_devices_list_from_nb_instances
from modules.transport_methods.ssh import create_ssh_connection, get_backup_from_device_via_ssh
from modules.backuper import write_backup, push_backups_to_git

env_params=import_env_params()
backuper_config = read_yaml_configuration(env_params["CONFIGURATIONS_DIR"] + "backuper.yml")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename=env_params["LOG_FILE"])
logger = logging.getLogger(__name__)
for instance,devices in get_devices_list_from_nb_instances().items():
    for device in devices:
        if ssh_conn:=create_ssh_connection(device):
            write_backup(get_backup_from_device_via_ssh(ssh_conn),device["name"])

if "github" in backuper_config["storage_method"]:
    push_backups_to_git()
