import ipaddress
import socket
import requests

print("What ip to you want to parse?")
input = input("> ")


result = '{:#b}'.format(ipaddress.IPv4Address(input))

print(result)