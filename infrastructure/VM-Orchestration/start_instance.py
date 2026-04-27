# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
import time, os, sys, random, re
import inspect
from os import environ as env

from  novaclient import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session


flavor = "ssc.medium" 
private_net = "UPPMAX 2025/1-2 Internal IPv4 Network"
floating_ip_pool_name = None
floating_ip = None
image_name = "Ubuntu 22.04 - 2024.01.15"

identifier = random.randint(1000,9999)

loader = loading.get_plugin_loader('password')

auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                password=env['OS_PASSWORD'],
                                project_name=env['OS_PROJECT_NAME'],
                                project_domain_id=env['OS_PROJECT_DOMAIN_ID'],
                                #project_id=env['OS_PROJECT_ID'],
                                user_domain_name=env['OS_USER_DOMAIN_NAME'])

sess = session.Session(auth=auth)
nova = client.Client('2.1', session=sess)
print ("user authorization completed.")

image = nova.glance.find_image(image_name)

flavor = nova.flavors.find(name=flavor)

if private_net != None:
    net = nova.neutron.find_network(private_net)
    nics = [{'net-id': net.id}]
else:
    sys.exit("private-net not defined.")

#print("Path at terminal when executing this file")
#print(os.getcwd() + "\n")
cfg_file_path =  os.getcwd()+'/prod-cloud-cfg.txt'
if os.path.isfile(cfg_file_path):
    userdata_prod = open(cfg_file_path)
else:
    sys.exit("prod-cloud-cfg.txt is not in current working directory")

cfg_file_path =  os.getcwd()+'/dev-cloud-cfg.txt'
if os.path.isfile(cfg_file_path):
    userdata_dev = open(cfg_file_path)
else:
    sys.exit("dev-cloud-cfg.txt is not in current working directory")    

secgroups = ['default']

print ("Creating instances ... ")
instance_prod1 = nova.servers.create(name="Group1_prod1", image=image, flavor=flavor, key_name='HS-SSH', nics=nics,security_groups=secgroups)
instance_prod2 = nova.servers.create(name="Group1_prod2", image=image, flavor=flavor, key_name='HS-SSH', nics=nics,security_groups=secgroups)
instance_prod3 = nova.servers.create(name="Group1_prod3", image=image, flavor=flavor, key_name='HS-SSH', nics=nics,security_groups=secgroups)
instance_dev = nova.servers.create(name="Group1_dev", image=image, flavor=flavor, key_name='HS-SSH', nics=nics,security_groups=secgroups)
inst_status_prod1 = instance_prod1.status
inst_status_prod2 = instance_prod2.status
inst_status_prod3 = instance_prod3.status
inst_status_dev = instance_dev.status

print ("waiting for 10 seconds.. ")
time.sleep(10)

while inst_status_prod1 == 'BUILD' or inst_status_prod2 == 'BUILD' or inst_status_prod3 == 'BUILD' or inst_status_dev == 'BUILD':
    print ("Instance initializing, please wait")
    time.sleep(5)
    instance_prod1 = nova.servers.get(instance_prod1.id)
    inst_status_prod1 = instance_prod1.status
    instance_prod2 = nova.servers.get(instance_prod2.id)
    inst_status_prod2 = instance_prod2.status
    instance_prod3 = nova.servers.get(instance_prod3.id)
    inst_status_prod3 = instance_prod3.status
    instance_dev = nova.servers.get(instance_dev.id)
    inst_status_dev = instance_dev.status

ip_address_prod1 = None
ip_address_prod2 = None
ip_address_prod3 = None
for network in instance_prod1.networks[private_net]:
    if re.match('\d+\.\d+\.\d+\.\d+', network):
        ip_address_prod1 = network
        break
if ip_address_prod1 is None:
    raise RuntimeError('No IP address assigned!')

for network in instance_prod2.networks[private_net]:
    if re.match('\d+\.\d+\.\d+\.\d+', network):
        ip_address_prod2 = network
        break
if ip_address_prod2 is None:
    raise RuntimeError('No IP address assigned!')

for network in instance_prod3.networks[private_net]:
    if re.match('\d+\.\d+\.\d+\.\d+', network):
        ip_address_prod3 = network
        break
if ip_address_prod3 is None:
    raise RuntimeError('No IP address assigned!')

ip_address_dev = None
for network in instance_dev.networks[private_net]:
    if re.match('\d+\.\d+\.\d+\.\d+', network):
        ip_address_dev = network
        break
if ip_address_dev is None:
    raise RuntimeError('No IP address assigned!')

print ("Instance: "+ instance_prod1.name +" is in " + inst_status_prod1 + " state" + " ip address: "+ ip_address_prod1)
print ("Instance: "+ instance_prod2.name +" is in " + inst_status_prod2 + " state" + " ip address: "+ ip_address_prod2)
print ("Instance: "+ instance_prod3.name +" is in " + inst_status_prod3 + " state" + " ip address: "+ ip_address_prod3)
print ("Instance: "+ instance_dev.name +" is in " + inst_status_dev + " state" + " ip address: "+ ip_address_dev)