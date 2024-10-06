import pynetbox

def create_netbox_connection(netbox_params : dict):
    nb = pynetbox.api(netbox_params['url'],netbox_params['token'])
    return nb