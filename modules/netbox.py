import pynetbox,logging,os
from dotenv import load_dotenv

from modules.configuration_reader import read_yamls_from_dir
load_dotenv()
conf_dir = os.getenv('CONFIGURATIONS_DIR')
logger = logging.getLogger(__name__)

def create_netbox_connection(netbox_params : dict):
    logger.info(f'Trying to connect to NetBox instance {netbox_params['url']}...')
    try:
        nb = pynetbox.api(netbox_params['url'],netbox_params['token'])
        logger.info(f'Connection to NetBox instance {netbox_params['url']} successful!')
        return nb
    except:
        logger.error(f'Failed to connect to  NetBox instance {netbox_params['url']}!')
        return False
def get_devices_list_from_nb_instances(nb_instances: list):
    result={}
    for instance,params in read_yamls_from_dir("netbox_instances/").items():
        if nb:=create_netbox_connection(params):
            matched_devices = []
            if type(params['filters']) == list :
                logger.info(f'Filters for NetBox instance {params['url']} found!')
                for filter in params['filters'] :
                    (filter_name,filter_value),=filter.items()
                    logger.info(f'Selecting devices from filter \"{filter_name}\" on instance {params['url']}...')
                    filtered_devices = [ get_device_params(device) for device in nb.dcim.devices.filter(**filter_value)]
                    if len(filtered_devices) == 0:
                        logger.warning(f'No devices found on filter \"{filter_name}\" on instance {params['url']}!')
                    else:
                        logger.info(f'Found {len(filtered_devices)} devices matching filter {filter_name} on instance {params['url']}!')
                    matched_devices.extend(filtered_devices)
            else:
                logger.info(f'No filters NetBox instance {params['url']} applied! Exporting all devices...')
                matched_devices = [ get_device_params(device) for device in nb.dcim.devices.all()]
            result.update({instance : matched_devices})
            logger.info(f'Found {len(matched_devices)} devices on instance {params['url']}')
    return result

def get_device_params(nb_device):
    result={}
    result.update({"role" : nb_device.role.name, "name" : nb_device.name, "platform" : nb_device.platform.name, "ip_address" : nb_device.primary_ip.address, "transport_method" : nb_device.custom_fields["transport_method"],"transport_cred" : nb_device.custom_fields["transport_cred"]})
    return result