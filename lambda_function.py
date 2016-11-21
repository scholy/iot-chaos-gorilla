from __future__ import print_function

import boto3
import json
import string
import random
#import logging

print ('Loading function')

# function to randomize availability zone
def az_func():
    global randAz
    region="ap-southeast-2" ### <-- Edit this for your target AWS region
    az=random.choice(string.ascii_letters[0:3]) ### <-- Edit [0:n] where '' is number of AZ's in your region
    randAz=region+az
    print("Target Region: ",region)
    print("Target Availability Zone: ",randAz)
    
# function to identify all instances in the target availability zone
def inst_func():
    global instIds
    instances = ec2.instances.filter(
        Filters=[
            {
                'Name': 'availability-zone',
                'Values': [randAz]
            },
        ],
    )
    instIds = []
    for instance in instances:
        instIds.append(instance.id)
    print ("\nAll instances in", randAz)
    print ("\n".join(instIds))

# function to identify Autoscale Group deployed instances in the target AZ
def asgInst_func():
    # add only ASG deployed instances in randAz into list asgInstIds
    # any instance deployed with an ASG is tagged with Key='tag:aws:autoscaling:groupName', Value='<ASG Name>'
    # we capture this by outputting all instances in our target AZ and filtering on the aboce Key with a wildcard Value.
    # we also only want to instances in a steady or 'running' state.
    global asgInstIds
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
    print ("\nASG deployed instances targeted for termination in", randAz)
    print ("\n".join(asgInstIds))

def diffInst_func():
    # Now diff the lists using set() and print output 
    global nonAsg
    nonAsg=(set(instIds)-set(asgInstIds))
    print ("\nInstances safe from the gorilla.")
    print ("These instances have _not_ been deployed with autoscale groups and services may not auto-heal. You should do something about that...")
    print ("\n".join(nonAsg))
    
# Capture IoT button clickType event
def lambda_handler(event, context):
    global ec2
    clickType = event['clickType']
    print("Received event: " + json.dumps(event, indent=2))
    
    # call function to randomize AZ
    az_func()
    
    ec2 = boto3.resource('ec2')
    
    # call function for all instances
    inst_func()
    
    # call function for ASG instances
    asgInst_func()
    
    # call function to diff instance lists
    diffInst_func()
    
    '''
    Here comes the big bad stuff that terminates instances in asgInstIds
    
    A SINGLE clickType will run the gorilla in 'DryRun' safe-mode. DryRun checks whether you have the required permissions for the
    action, without actually making the request, and provides an error response. If you have the required permissions, the error
    response is DryRunOperation . Otherwise, it is UnauthorizedOperation
    
    A DOUBLE clickType event will unleash the gorilla, terminating all EC2 instances deployed using autoscale groups in our target AZ.
    You'd better mean it when you do this, there's no going back!
    '''
    if clickType == 'SINGLE':    
        for i in asgInstIds:
            print ("\n**** ",i," The Gorilla is looking at you! But today you've survived. ****\n")
            asgInstTerminate = ec2.instances.terminate(DryRun=True,InstanceIds=[i])
    elif clickType == 'DOUBLE':
        for i in asgInstIds:
            print ("\n**** ",i," Has Been Terminated By The Gorilla ****\n")
            asgInstTerminate = ec2.instances.terminate(InstanceIds=[i])
    elif clickType == 'LONG':
        print ("\n**** Let's go and disable any disableApiTermination protection :) - just kidding, we'll add this later") 
    
