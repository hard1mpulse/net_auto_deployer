import logging,os
from dotenv import load_dotenv
from modules.configuration_reader import read_yaml_configuration,import_env_params

load_dotenv()

conf_dir,backup_dir,logfile=import_env_params()


logger = logging.getLogger(__name__)

backuper_config=read_yaml_configuration(conf_dir+"backuper.yml")
def write_backup(backup: str,device: str,backuper_config):
    backuper_config = read_yaml_configuration(conf_dir + "backuper.yml")
    if "local" in backuper_config["storage_method"]:
        logger.info(f"Local storage method selected for backup! Saving backup of device {device} locally to {backup_dir}/local ...")
        with open(backup_dir+"local/"+device+".backup","w") as file:
            file.write(backup)