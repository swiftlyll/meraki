# Author: K M
# Date: December 13, 2024
# Github: https://github.com/swiftlyll/

import meraki
import json
import csv
import os
from datetime import datetime

# client
api_key = os.environ["MERAKI_API_KEY"]
dashboard = meraki.DashboardAPI(
    api_key = api_key,
    output_log = False,
    print_console = False
)

# organization
org = dashboard.organizations.getOrganizations()
org_id = org[0].get('id')
org_name = org[0].get('name')
org_customer_number = org[0]['management']['details'][0].get('value')

# networks
networks_detailed = dashboard.organizations.getOrganizationNetworks(org_id,total_pages='all')
networks = {}

for index, network in enumerate(networks_detailed):
    network_id = network.get('id')
    network_name = network.get('name')

    # dynamically assign letter increment
    network_index = chr(65 + index)
    networks[f'Network {network_index}'] = {'Id':network_id,'Name':network_name}

# inventory
print('Gathering network device information')
inventory = dashboard.organizations.getOrganizationInventoryDevices(org_id,total_pages='all')
# inventory = json.dumps(inventory,indent=4)
# print(inventory)

network_devices = []

for device in inventory:
    # loop reset
    device_network, device_name, device_type, device_model, device_serial_number, device_mac_address, device_order_number, device_claim_date = '', '', '', '', '', '', '', ''

    # info
    device_network = device.get('networkId')
    device_name = device.get('name')
    device_type = device.get('productType')
    device_model = device.get('model')
    device_serial_number = device.get('serial')
    device_mac_address = device.get('mac')
    device_order_number = device.get('orderNumber','Not Available')
    device_claim_date = device.get('claimedAt')

    for key in networks.keys():
        if networks[key].get('Id') == device_network:
            device_network = networks[key].get('Name')

    if device_name == '':
        device_name = device_mac_address

    network_devices.append({
        'Network':device_network,
        'Device Name':device_name,
        'Type':device_type,
        'Model':device_model,
        'Serial Number':device_serial_number,
        'MAC Address':device_mac_address,
        'Order Number':device_order_number,
        'Claim Date':device_claim_date
    })

# csv
print("Generating CSV file") 
date = datetime.now().strftime('%Y%m%d')
file_name = f'meraki_inventory_{date}.csv'
working_directory = os.getcwd()
with open(file=file_name, mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file,network_devices[0].keys())
    writer.writeheader()   
    writer.writerows(network_devices)
print(f"Successfully generated {file_name} in directory {working_directory}")

input("Press 'Enter' to exit")