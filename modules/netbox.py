import pynetbox,logging,os
from dotenv import load_dotenv
from duplicity.config import ssl_no_check_certificate
from httplib2.auth import params
from pprint import pprint
from modules.configuration_reader import read_yamls_from_dir,read_yaml_configuration,import_env_params
load_dotenv()
env_params = import_env_params()
logger = logging.getLogger(__name__)

auto_deployer_config = read_yaml_configuration(env_params["CONFIGURATIONS_DIR"] + "auto_deployer.yml")

def create_netbox_connection(netbox_params : dict):
    logger.info(f'Trying to connect to NetBox instance {netbox_params['url']}...')
    try:
        nb = pynetbox.api(url=netbox_params['url'],token=netbox_params['token'])
        if netbox_params["ssl_no_check_certificate"]:
            nb.http_session.verify = False
        logger.info(f'Connection to NetBox instance {netbox_params['url']} successful!')
        return nb
    except:
        logger.error(f'Failed to connect to  NetBox instance {netbox_params['url']}!')
        return False
def get_devices_list_from_nb_instances():
    result={}
    for instance,params in read_yamls_from_dir("netbox_instances/").items():
        if nb:=create_netbox_connection(params):
            matched_devices = []
            if type(params['filters']) == list and len(params['filters']) > 0 :
                logger.info(f'Filters for NetBox instance {params['url']} found!')
                for filter in params['filters'] :
                    (filter_name,filter_value),=filter.items()
                    logger.info(f'Selecting devices from filter \"{filter_name}\" on instance {params['url']}...')
                    filtered_devices = [ get_device_params(device,filter_name) for device in nb.dcim.devices.filter(**filter_value)]
                    for d in filtered_devices:
                        d.update({"filter": filter_name})
                    if len(filtered_devices) == 0:
                        logger.warning(f'No devices found on filter \"{filter_name}\" on instance {params['url']}!')
                    else:
                        logger.info(f'Found {len(filtered_devices)} devices matching filter {filter_name} on instance {params['url']}!')
                    matched_devices.extend(filtered_devices)
            else:
                logger.info(f'No filters NetBox instance {params['url']} applied! Exporting all devices...')
                matched_devices = [ get_device_params(device) for device in nb.dcim.devices.all()]
                for d in matched_devices:
                    d.update({"filter": "all"})
            result.update({instance : matched_devices})
            logger.info(f'Found {len(matched_devices)} devices on instance {params['url']}')
    return result

def get_device_params(nb_device,filter_name="all"):
    result={}
    if auto_deployer_config["cred_matching_method"] == "local":
        mapper_config=read_yaml_configuration(env_params["CONFIGURATIONS_DIR"] + "mapper.yml")
        result.update({"role" : nb_device.role.name, "name" : nb_device.name, "platform" : nb_device.platform.name,
                       "ip_address" : nb_device.primary_ip.address,
                       "transport_method" : mapper_config["filters"][filter_name]["transport_method"],
                       "transport_cred": mapper_config["filters"][filter_name]["transport_cred"]})
        logger.info(f'Successfully matched transport_cred {mapper_config["filters"][filter_name]["transport_cred"]} with device {result["name"]} on filter {filter_name}!')
    elif auto_deployer_config["cred_matching_method"] == "netbox_cf":
        logger.info(f'Netbox cred_matching_method is set.Trying to get custom fiels in netbox...')
        result.update({"role": nb_device.role.name, "name": nb_device.name, "platform": nb_device.platform.name,
                       "ip_address": nb_device.primary_ip.address,
                       "transport_method": nb_device.custom_fields["transport_method"],
                       "transport_cred": nb_device.custom_fields["transport_cred"]})
        logger.info(f'Successfully matched transport_cred {nb_device.custom_fields["transport_cred"]} with device {result["name"]} on filter {filter_name}!')
    return result