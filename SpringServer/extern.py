# /usr/bin/env python3
import json
from urllib.request import urlopen


def get_location(ip):
	url = 'http://ipinfo.io/json'
	response = urlopen(url)
	data = json.load(response)
	return data['city']
