from __future__ import print_function

import boto3
import json
import string
import random
#import logging

print ('Loading function')

# try capture the iot button
def lambda_handler(event, context):
    clickType = event['clickType']
    print("Received event: " + json.dumps(event, indent=2))
    
    # randomize availability zone
    region="ap-southeast-2"
    az=random.choice(string.ascii_letters[0:3])
    randAz=region+az
    
    ec2 = boto3.resource('ec2')
    
    # list all deployed instances in randAz into list instIds
    instances = ec2.instances.filter(
        Filters=[
            {
                'Name': 'availability-zone',
                'Values': [randAz]
            },
            {
                'Name': 'instance-state-name',
                'Values': ['pending','running','shutting-down','stopping','stopped']
            },
        ],
    )
    
    instIds = []
    for instance in instances:
        instIds.append(instance.id)
    print ("\nAll instances in", randAz)
    print ("\n".join(instIds))
    
    
    # list ASG deployed instances in randAz into list asgInstIds
    asgInstances = ec2.instances.filter(
        Filters=[
            {
                'Name': 'availability-zone',
                'Values': [randAz]
            },
            {
                'Name': 'tag:aws:autoscaling:groupName',
                'Values': ['*']
            },
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            },
        ],
    )
    
    asgInstIds = []
    for instance in asgInstances:
        asgInstIds.append(instance.id)
    print ("\nASG deployed instances in", randAz)
    print ("\n".join(asgInstIds))
    
    
    
    # diff the lists using set()
    nonAsg=(set(instIds)-set(asgInstIds))
    print ("\nNon-ASG deployed instances in", randAz)
    print ("\n".join(nonAsg))
    
    
    
    '''
    Here comes the big bad stuff that terminates instances in asgInstIds
    '''
    
    
        
    if clickType == 'SINGLE':    
        for i in asgInstIds:
            print ("\n**** ",i," The Gorilla is looking at you! ****\n")
        #    asgInstTerminate = ec2.instances.terminate(InstanceIds=[i])
            asgInstTerminate = ec2.instances.terminate(DryRun=True,InstanceIds=[i])
    elif clickType == 'DOUBLE':
        for i in asgInstIds:
            print ("\n**** ",i," Has Been Terminated By The Gorilla ****\n")
            asgInstTerminate = ec2.instances.terminate(InstanceIds=[i])
    elif clickType == 'LONG':
        print ("\n**** Stop sitting on the button ****\n")
        
    
