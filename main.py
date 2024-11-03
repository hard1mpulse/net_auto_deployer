import os,logging,time
from sys import argv
from modules.configuration_reader import read_yaml_configuration, import_env_params, read_lists_from_dir, \
    read_command_set
from modules.netbox import get_devices_list_from_nb_instances
from modules.transport_methods.ssh import create_ssh_connection, push_command_to_device_via_ssh

env_params=import_env_params()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename=env_params["LOG_FILE"])
logger = logging.getLogger(__name__)
auto_deployer_config = read_yaml_configuration(env_params["CONFIGURATIONS_DIR"] + "auto_deployer.yml")
command_sets={}
for instance,devices in get_devices_list_from_nb_instances().items():
    if auto_deployer_config["deploy_method"] == "all":
        try:
            command_sets.update({"all": argv[1]})
            logger.info(
                f"Selected deploy method \"all\"! Commands in command set in agrument will be send to all devices found!")
        except:
            logger.error(f"Selected deploy method \"all\" but no command set file send as argument")
    elif auto_deployer_config["deploy_method"] == "filters":
        command_sets = read_lists_from_dir("command_sets/")
        logger.info(f"Selected deploy method \"filters\"! Reading command sets list in configurations/command_sets/")
    if auto_deployer_config["deploy_method"] == "all":
        for device in devices:
            if ssh_conn:=create_ssh_connection(device):
                for command in read_command_set("configurations/command_sets/"+command_sets["all"]):
                    command_result=push_command_to_device_via_ssh(ssh_conn,command)
                    if command_result == "":
                        logger.info(f"Command {command} sent to device {device["name"]} and recieved no answer. Seems OK...")
                    elif "error" in command_result or "fault" in command_result:
                        logger.info(f"Command {command} sent to device {device["name"]} and recieved some error message: {command_result}")
                    else:
                        logger.info(f"Command {command} sent to device {device["name"]} and recieved some answer: {command_result}")

    if auto_deployer_config["deploy_method"] == "filters":
        for device in devices:
            if ssh_conn:=create_ssh_connection(device):
                for command in read_command_set("configurations/command_sets/"+device["filter"]+".list"):
                    command_result=push_command_to_device_via_ssh(ssh_conn,command)
                    if command_result == "":
                        logger.info(f"Command {command} sent to device {device["name"]} and recieved no answer. Seems OK...")
                    elif "error" in command_result or "fault" in command_result:
                        logger.info(f"Command {command} sent to device {device["name"]} and recieved some error message: {command_result}")
                    else:
                        logger.info(f"Command {command} sent to device {device["name"]} and recieved some answer: {command_result}")