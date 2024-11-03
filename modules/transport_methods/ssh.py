import logging
from netmiko import ConnectHandler
from modules.mapper import platform_to_device_type_mapper,device_type_to_commands_mapper
from modules.configuration_reader import read_yamls_from_dir


logger = logging.getLogger(__name__)

def create_ssh_connection (device : dict):
    credentials = read_yamls_from_dir('credentials/')
    if device["transport_cred"] in credentials.keys() and credentials[device["transport_cred"]]["transport_method"] == device["transport_method"] :
        logger.info(f'For device {device['name']} found associated credential {device["transport_cred"]}')
        used_cred=credentials[device["transport_cred"]]
        del used_cred["transport_method"]
    else:
        logger.error(f'For device {device['name']} not found associated credential or credential transport method doesnt match with device! ')
        return False
    connection_params={}
    connection_params.update(used_cred)
    connection_params.update({'ip': device["ip_address"].split('/')[0]})

    if device["platform"] in platform_to_device_type_mapper:
        connection_params.update({'device_type':platform_to_device_type_mapper[device["platform"]]})
    else:
        connection_params.update({'device_type': device["platform"]})

    try:
        ssh_connection=ConnectHandler(**connection_params)
    except:
        logger.error(f'Failed connection to device {device['name']} using cred {device['transport_cred']} using transport method {device['transport_method']}!!!')
        return False
    return ssh_connection

# def get_backup_from_device_via_ssh(ssh_session):
#     try:
#         backup=ssh_session.send_command(device_type_to_commands_mapper[ssh_session.device_type]["get_backup"])
#         return backup
#     except:
#         logger.error(f'Failed to get backup from device {device['name']} using command {device_type_to_commands_mapper[ssh_session.device_type]["get_backup"]}!!!')
#         return False

def push_command_to_device_via_ssh(ssh_session,command: list):
    command_result=ssh_session.send_command(command)
    return command_result