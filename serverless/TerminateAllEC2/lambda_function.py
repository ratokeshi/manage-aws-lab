#!/usr/bin/python

# This is a lambda function that checks each region for running EC2 instances.  
# If the Instance has a tag with AutoOff = False then that instance is bypassed; 
# otherwise instances are shut down (not terminated)
# Make sure the Lambda has the permissions to list and stop EC2 instances

import boto3
import logging
import json

#setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def ShutDown(region):

	#define the connection
	ec2 = boto3.resource('ec2', region_name = region)

	# get a list of all running instances
	all_running_instances = [i for i in ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running','stopped']}])]
	
	# get instnaces where there is a tag with key name 'AutoOff' with value of 'False'
	exempt_instances = [i for i in ec2.instances.filter(Filters=[{'Name':'tag:AutoOff', 'Values':['False']}])]

	# make a list of filtered instances IDs `[i.id for i in instances]`
	# Filter from all instances the instance that are not in the filtered list
	# if AutoOff = Falst is not in the list, "delete" it --aka instance.stop
	instances_to_stop = [to_stop for to_stop in all_running_instances if to_stop.id not in [i.id for i in exempt_instances]]

	# run over your `instances_to_stop` list and stop each one of them
	for instance in instances_to_stop:
		instance.terminate()

# You can comment some of these out if you are certain you are not in that region

def lambda_handler(event, context):
	ShutDown('us-east-1')
	ShutDown('us-east-2')
	ShutDown('us-west-1')
	ShutDown('us-west-2')
	ShutDown('ca-central-1')
	ShutDown('ap-south-1')
	ShutDown('ap-northeast-2')
	ShutDown('ap-northeast-3')
	ShutDown('ap-southeast-1')
	ShutDown('ap-southeast-2')
	ShutDown('ap-northeast-1')
	ShutDown('eu-central-1')
	ShutDown('eu-west-1')
	ShutDown('eu-west-2')
	ShutDown('eu-west-3')
	ShutDown('eu-north-1')
	ShutDown('sa-east-1')