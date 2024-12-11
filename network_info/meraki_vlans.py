# Author: K M
# Date: December 10, 2024
# Github: https://github.com/swiftlyll/

import meraki
import json
import csv
import os

# client
api_key = os.environ["MERAKI_API_KEY"]
dashboard = meraki.DashboardAPI(
    api_key = api_key,
    output_log = False,
    print_console = False
)

# organization
orgs = dashboard.organizations.getOrganizations()
for org in orgs:
    org_id = org['id']
    org_name = org['name']
    org_customer_number = org['management']['details'][0]['value']

############################################################
##### In the event there is more than one organization #####
############################################################

# organizations = {}
# for index, org in enumerate(orgs):
#     org_id = org['id']
#     org_name = org['name']
#     org_customer_number = org['management']['details'][0]['value']
    
#     # dynamically assign letter increment e.g. OrgA, OrgB, OrgC, etc.
#     org_index = chr(65 + index) # 65 equals 'A'   
#     organizations[f'Org {org_index}'] = {'Id':org_id,'Name':org_name,'Customer Number':org_customer_number}

############################################################
################### Optional excerpt end ###################
############################################################

# networks
networks_detailed = dashboard.organizations.getOrganizationNetworks(org_id,total_pages='all')
networks = {}

for index, network in enumerate(networks_detailed):
    network_id = network['id']
    network_name = network['name']

    # dynamically assign letter increment
    network_index = chr(65 + index)
    networks[f'Network {network_index}'] = {'Id':network_id,'Name':network_name}

# fetch configured VLANs per network
all_vlans = []

for network_info, network in networks.items(): # access network info for each network entry directly, instead of having to manually specify 'network["Network A"]'
    print(f'Gathering data for VLANs configured in network {network["Name"]}')
    vlans = dashboard.appliance.getNetworkApplianceVlans(network['Id'])
    # vlans_pretty = json.dumps(vlans, indent=4)
    # print(vlans_pretty)
    
    for vlan in vlans:
        static_range = vlan.get('reservedIpRanges','N/A')
        static_range_start, static_range_end, static_range_comment = 'N/A', 'N/A', 'N/A'
        
        # below "if" checks if the list is not empty, this prevents the error "IndexError: list index out of range" when using [0]
        if static_range:
            static_range_start = static_range[0].get('start','N/A')
            static_range_end = static_range[0].get('end','N/A')
            static_range_comment = static_range[0].get('comment','N/A')

        all_vlans.append({
            'Network': network["Name"], 
            'VLAN ID': vlan["id"], 
            'VLAN Name': vlan['name'], 
            'Subnet': vlan['subnet'], 
            'Interface IP': vlan['applianceIp'],
            'DHCP Handling': vlan['dhcpHandling'],
            'DHCP Lease Time': vlan.get('dhcpLeaseTime','N/A'),
            'Static Range Start': static_range_start,
            'Static Range End': static_range_end,
            'Static Range Description': static_range_comment
        })

print("Generating CSV file")        
with open('test.csv', mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file,all_vlans[0].keys())
    writer.writeheader()   
    writer.writerows(all_vlans)
print("Successfully generated CSV file")

input("Press 'Enter' to exit")