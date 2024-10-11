import logging,os,time
from modules.configuration_reader import read_yaml_configuration,import_env_params


env_params=import_env_params()


logger = logging.getLogger(__name__)

backuper_config=read_yaml_configuration(env_params["CONFIGURATIONS_DIR"]+"backuper.yml")
def write_backup(backup: str,device: str):
    backuper_config = read_yaml_configuration(env_params["CONFIGURATIONS_DIR"] + "backuper.yml")
    if "local" in backuper_config["storage_method"]:
        logger.info(f"Local storage method selected for backup! Saving backup of device {device} locally to {env_params["BACKUPS_DIR"]}local ...")
        with open(env_params["BACKUPS_DIR"]+"local/"+device+".backup","w") as file:
            file.write(backup)
    if "github" in backuper_config["storage_method"]:
        logger.info(f"Github storage method selected for backup! Saving backup of device {device} locally to {env_params["GITHUB_DIR"]}...")
        with open(env_params["GITHUB_DIR"]+device+".backup","w") as file:
            file.write(backup)

def push_backups_to_git():
    if os.system(f'cd {env_params["GITHUB_DIR"]} && git add *.backup  && git commit -m "Added backups from {time.strftime("%d-%m-%Y")}" && git push -u origin master') == 0:
        logger.info(f"Successfully pushed backups to github from directory {env_params["GITHUB_DIR"]}!")
    else:
        logger.info(f"Some error recieved while pushing backups to github from directory {env_params["GITHUB_DIR"]}!")