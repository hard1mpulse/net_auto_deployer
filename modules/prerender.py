from modules.transport_methods.ssh import push_command_to_device_via_ssh,create_ssh_connection
from modules.configuration_reader import read_yaml_configuration,import_env_params
import os,yaml,logging,textfsm
from dotenv import load_dotenv
logger = logging.getLogger(__name__)

env_params=import_env_params()

def read_tfsm_template(file: str):
    with open(env_params["TEMPLATES_DIR"]+"tfsm_templates/"+file+".fsm") as tfsm_template:
        try:
            logger.info(f'Trying to read fsm template {file}...')
            fsm = textfsm.TextFSM(tfsm_template)
            logger.info(f'Fsm template {file} was readed successfully!')
            return fsm
        except:
            logger.critical(f'Fsm template {file} wasnt readed!')
            return False
def check_prerender(nb_instance,device):
    conf=read_yaml_configuration(env_params["CONFIGURATIONS_DIR"]+"netbox_instances"+nb_instance+".yml")
    if device['filter'] in conf['prerender'].keys():
        logger.info(f'For device {device['name']} found prerenders!')
        return conf['prerender'][device['filter']]
    else:
        logger.info(f'For device {device['name']} not found matched prerenders!')
        return False

def get_prerender_params(prerender: list,device: dict):
    result={}
    if ssh:=create_ssh_connection(device):
        for method in prerender:
            if template:=read_tfsm_template(method['tfsm_template']):
                command_output=push_command_to_device_via_ssh(ssh,method['command'])
                render_result = template.ParseText(command_output)
                if len(render_result) == 1:
                    result.update(dict(zip(template.header, render_result[0])))
                    logger.info(f'Data from template {method['tfsm_template']} using command {method['command']} found!')
                elif len(render_result) == 0:
                    logger.error(f'No data found from template {method['tfsm_template']} using command {method['command']}!')
                else:
                    result.update(dict(zip(template.header, render_result[0])))
                    logger.warning(f'Too much entries found with template {method['tfsm_template']} using command {method['command']}! Try to optimize your tfsm template! Adding only first entry...')
            else:
                logger.error(f'No template {method['tfsm_template']} found! Put you file in {env_params["CONFIGURATIONS_DIR"]}/templates/tfsm_templates')
        return result
