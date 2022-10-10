import datetime
from azure.mgmt.monitor import MonitorManagementClient
from azure.identity import DefaultAzureCredential

# Acquire a credential object
token_credential = DefaultAzureCredential()

subscription_id = 'f40002df-0a45-4b57-bdb3-33be48855fd0'
resource_group_name = 'cloud-shell-storage-southcentralus'
vm_name = 'qlappaxy/databases/aqlappaxy'

resource_id = (
    "subscriptions/{}/"
    "resourceGroups/{}/"
    "providers/Microsoft.Sql/servers/{}"
).format(subscription_id, resource_group_name, vm_name)

TENANT_ID = 'xc1886f5e-94aa-4385-b84f-c2677c2be9ce'
CLIENT = '3fd3edee-1f68-4332-91d5-8cb9dd0b8eb0'
KEY = 'OxD8Q~2PUqmptMGzwcOshRsYF86mEBKujbyx8aYe'
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

# mgmt_service_client = MonitorManagementClient(
#         account_url="https://<my_account_name>.blob.core.windows.net",
#         credential=token_credential)
# from
#
# subscription_id = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
# resource_group_name = 'xxxx-xxxxx'
# vm_name = 'xxxxxxxxxx'
#
# resource_id = (
#     "subscriptions/{}/"
#     "resourceGroups/{}/"
#     "providers/Microsoft.Compute/virtualMachines/{}"
# ).format(subscription_id, resource_group_name, vm_name)
#
# TENANT_ID = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
# CLIENT = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
# KEY = 'xxxxxxxxx'
# credentials = ServicePrincipalCredentials(
#     client_id=CLIENT,
#     secret=KEY,
#     tenant=TENANT_ID
# )
#
# client = MonitorManagementClient(
#     credentials,
#     subscription_id
# )
#
# import datetime
# from azure.mgmt.monitor import MonitorManagementClient
# from azure.identity import ClientSecretCredential


