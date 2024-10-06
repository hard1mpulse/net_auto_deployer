import os,yaml
from dotenv import load_dotenv
# load_dotenv()
# conf_dir = os.getenv('CONFIGURATIONS_DIR')
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
    dir_name = os.path.dirname(os.path.abspath(__file__))
    print(dir_name)
    conf_files=[item for item in os.listdir(dir_name+"\.."+directory) if ".yml" in item]
    for file in conf_files:
        params=read_yaml_configuration(dir_name+"\.."+directory+file)
        result.update({file.split('.')[0] : params})
    return result
