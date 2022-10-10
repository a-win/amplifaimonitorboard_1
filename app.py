import datetime
from azure.mgmt.monitor import MonitorManagementClient
from azure.identity import ClientSecretCredential
from 

subscription_id = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
resource_group_name = 'xxxx-xxxxx'
vm_name = 'xxxxxxxxxx'

resource_id = (
    "subscriptions/{}/"
    "resourceGroups/{}/"
    "providers/Microsoft.Compute/virtualMachines/{}"
).format(subscription_id, resource_group_name, vm_name)

TENANT_ID = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
CLIENT = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
KEY = 'xxxxxxxxx'
credentials = ServicePrincipalCredentials(
    client_id=CLIENT,
    secret=KEY,
    tenant=TENANT_ID
)

client = MonitorManagementClient(
    credentials,
    subscription_id
)

import datetime
from azure.mgmt.monitor import MonitorManagementClient
from azure.identity import ClientSecretCredential

subscription_id = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
resource_group_name = 'xxxx-xxxxx'
vm_name = 'xxxxxxxxxx'

resource_id = (
    "subscriptions/{}/"
    "resourceGroups/{}/"
    "providers/Microsoft.Compute/virtualMachines/{}"
).format(subscription_id, resource_group_name, vm_name)

TENANT_ID = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
CLIENT = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
KEY = 'xxxxxxxxx'
credentials = ServicePrincipalCredentials(
    client_id=CLIENT,
    secret=KEY,
    tenant=TENANT_ID
)

client = MonitorManagementClient(
    credentials,
    subscription_id
)

today = datetime.datetime.now()
nexttime = today - datetime.timedelta(minutes=1)

metrics_data = client.metrics.list(
    resource_id,
    timespan="{}/{}".format(nexttime, today),
    interval='PT1M',
    metricnames='Percentage CPU',
    aggregation='average'
)
for item in metrics_data.value:
    for timeserie in item.timeseries:
        for data in timeserie.data:
            print("{}".format(data.average))
