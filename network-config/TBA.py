import meraki
import requests
import json
import os

# client
api_key = os.environ['MERAKI_API_KEY']
dashboard = meraki.DashboardAPI(
    api_key = api_key,
    output_log = False,
    print_console = False
)
org = dashboard.organizations.getOrganizations()

# actions