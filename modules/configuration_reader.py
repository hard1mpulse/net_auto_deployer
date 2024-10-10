import os,yaml
from dotenv import load_dotenv
load_dotenv()
def import_env_params():
    load_dotenv()
    if os.getenv('CONFIGURATIONS_DIR').startswith('/'):
        conf_dir=os.getenv('CONFIGURATIONS_DIR').startswith('/')
    else:
        conf_dir=os.path.dirname(os.path.abspath(__file__))+"/../"+os.getenv('CONFIGURATIONS_DIR')
    if os.getenv('BACKUPS_DIR').startswith('/'):
        backup_dir=os.getenv('BACKUPS_DIR').startswith('/')
    else:
        backup_dir=os.path.dirname(os.path.abspath(__file__))+"/../"+os.getenv('BACKUPS_DIR')
    if os.getenv('LOGFILE').startswith('/'):
        logfile=os.getenv('LOGFILE').startswith('/')
    else:
        logfile=os.path.dirname(os.path.abspath(__file__))+"/../"+os.getenv('LOGFILE')
    return conf_dir,backup_dir,logfile

conf_dir,backup_dir,logfile=import_env_params()

def read_yaml_configuration(configuration_file : str):
    with open(configuration_file, 'r') as stream:
        try:
            config=yaml.safe_load(stream)
            return config
        except yaml.YAMLError:
            print(yaml.YAMLError)
            return False
def read_yamls_from_dir(directory : str):
    result={}
    conf_files=[item for item in os.listdir(conf_dir+directory) if ".yml" in item]
    for file in conf_files:
        params=read_yaml_configuration(conf_dir+directory+file)
        result.update({file.split('.')[0] : params})
    return result
