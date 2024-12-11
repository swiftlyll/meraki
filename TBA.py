import meraki
import requests
import json

# import pandas as pd # for json to csv

api_key = os.environ["MERAKI_API_KEY"]
dashboard = meraki.DashboardAPI(api_key)
org = dashboard.organizations.getOrganizations()

for key in org:
    orgId = key['id']

networks = dashboard.organizations.getOrganizationNetworks(orgId,total_pages='all')
# networksReadable = json.dumps(networks, indent=4) # string data for read-only formatting, use $networks for data extraction
# print(networksReadable)

for network in networks:
    networkName = network['name']
    networkId = network['id']
    one = type(networkId)
    print(one)
    wirelessClients = dashboard.wireless.getNetworkWirelessClientsConnectionStats(networkId=networkId,timespan=86400) # 86400 = 24 hour search period

    # maybe use this as a way to format data?
    for client in wirelessClients:
        clientMAC = ""
        clientConnStat = ""
    
    wirelessClients = json.dumps(wirelessClients, indent=4)


    print('Network is ', networkName, "with network ID", networkId, ".")
    print('Client list: ')
    print(wirelessClients)