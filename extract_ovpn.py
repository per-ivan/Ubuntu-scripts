#!/usr/bin/python3
#
# Extract certificates and keys from an OpenVPN config file (*.ovpn)
# Certificates are extracted under path /home/user/OpenVPN/directory_name
# How to use script:
# $> python extract_ovpn.py filname.ovpn directory_name
#

import os
import re
import sys

# create OpenVPN directory if not exist in path /home/user
dir_name = "OpenVPN"
dir_home = os.getenv("HOME")
dir_vpn = dir_home + "/" + dir_name + "/" + sys.argv[2]
if not os.path.exists(dir_vpn):
    os.makedirs(dir_vpn)
    print dir_name, "directory was created"
# open input ovpn config file
ovpn_file_path =  os.path.dirname(sys.argv[1])
with open(sys.argv[1], 'r') as ovpn_file:
    ovpn_config = ovpn_file.read()

# open output config file
ovpn_file_name = os.path.splitext(sys.argv[1])[0]+"_nocert.ovpn"
ovpn_file = open(os.path.join(dir_vpn, ovpn_file_name), 'w')

# Extract certificates and keys
regex_ca = re.compile("<ca>(.*)</ca>", re.IGNORECASE|re.DOTALL)
regex_cert = re.compile("<cert>(.*)</cert>", re.IGNORECASE|re.DOTALL)
regex_key = re.compile("<key>(.*)</key>", re.IGNORECASE|re.DOTALL)

match_string = regex_ca.search(ovpn_config)
if match_string is not None:
    cert_file = open(os.path.join(dir_vpn, 'ca.crt'), 'w')
    cert_file.write(match_string.group(1))
    cert_file.close()
    ovpn_config = regex_ca.sub("",ovpn_config)
    ovpn_file.write("ca ca.crt\n")

match_string = regex_cert.search(ovpn_config)
if match_string is not None:
    cert_file = open(os.path.join(dir_vpn, 'client.crt'), 'w')
    cert_file.write(match_string.group(1))
    cert_file.close()
    ovpn_config = regex_cert.sub("",ovpn_config)
    ovpn_file.write("cert client.crt\n")

match_string = regex_key.search(ovpn_config)
if match_string is not None:
    cert_file = open(os.path.join(dir_vpn, 'client.key'), 'w')
    cert_file.write(match_string.group(1))
    cert_file.close()
    ovpn_config = regex_key.sub("",ovpn_config)
    ovpn_file.write("key client.key\n")


ovpn_file.write(ovpn_config)
ovpn_file.close()
print sys.argv[2], "directory was created"
print "Certificates nad key are extracted from .ovpn file"
