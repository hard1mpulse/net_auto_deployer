import os,logging,time,pprint
from sys import argv
from modules.configuration_reader import read_yaml_configuration, import_env_params, read_lists_from_dir, \
    read_command_set
from modules.netbox import get_devices_list_from_nb_instances
from modules.transport_methods.ssh import create_ssh_connection, push_command_to_device_via_ssh
from modules.prerender import get_prerender_params


env_params=import_env_params()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename=env_params["LOG_FILE"])
logger = logging.getLogger(__name__)
auto_deployer_config = read_yaml_configuration(env_params["CONFIGURATIONS_DIR"] + "auto_deployer.yml")
rendered_data={}
for instance,devices in get_devices_list_from_nb_instances().items():
    instance_conf=read_yaml_configuration(env_params["CONFIGURATIONS_DIR"]+"netbox_instances/"+instance+".yml")
    pprint.pp(instance_conf['prerenders'])
    for device in devices:
        if device['filter'] in instance_conf['prerenders']:
            rendered_data.update({device['name'] : get_prerender_params(instance_conf['prerenders'][device['filter']],device)})


pprint.pp(rendered_data)



