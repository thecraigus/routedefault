import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from lxml import etree

headers = {'Content-Type': 'application/xml'}

def GENERATE_COOKIE(username,password):
    xml = '<aaaLogin inName='+username+'" inPassword="'+password+'" />'
    auth = requests.post('https://192.168.1.86/nuova', data=xml, headers=headers, verify=False)
    root = etree.fromstring(auth.content)
    for child in root.iter('*'):
        cookie = (child.attrib['outCookie'])
    return cookie

def CONFIG_WORKER(cookie,vlan_id,vlan_name):
    vlan_xml = '<configConfMo cookie="' + cookie + '"> <inConfig> ' \
                                                   '<fabricVlan childAction="deleteNonPresent" compressionType="included" defaultNet="no" ' \
                                                   'dn="fabric/lan/net-' + vlan_name + '" id="' + vlan_id + '" mcastPolicyName="" name="' + vlan_name + \
                                                   '" policyOwner="local"  sharing="none" dn="fabric/lan/net-' + vlan_name + '" />' \
                                                   '</inConfig>' \
                                                   '</configConfMo>'

    config_request_vlan = requests.post('https://192.168.1.86/nuova', data=vlan_xml, headers=headers, verify=False)
    return (config_request_vlan.status_code)

def main():
    requestcookie = GENERATE_COOKIE('ucspe','ucspe')
    print (CONFIG_WORKER (requestcookie,'400','ROUTEDEFAULT-VLAN'))
main()