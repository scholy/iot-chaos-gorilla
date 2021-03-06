# iot-chaos-gorilla
AWS IoT button invoked Chaos Gorilla - DR testing at the click of a button

********* USE AT YOUR OWN RISK AND WITH EXTREME CAUTION *********

This is intentionally destructive, all care and no responsability taken. 


## Description:
iot-chaos-gorilla unleashes a 'Chaos Gorilla' and terminates EC2 instances in a random AWS availability zone.
Currently, the gorilla only terminates 'running' instances deployed using (or later added to) autoscale groups (ASG). Instances not associated with ASG's or in a 'pending', 'shutting-down', 'stopping' or 'stopped' state are ignored. Instances in a 'terminated' state, well ....

A 'SINGLE' click event of the Gorilla Button will execute the sequence in DryRun mode, while a 'DOUBLE' click event is the real deal - KABOOM!. A 'LONG' click event does nothing at this stage.
  
## Pre-Req's:
1. AWS IoT Button  
2. Set 2 lambda environment variables to enable multi-region and multi-AZ logic. NB: multiAZ requires multi-region (i.e. 1 AZ per region, not multi-az in 1 region)
  * multiRegion = True|False
  * multiAZ = True|False
3. iot-chaos-gorilla IAM role with permissions
  * logs:CreateLogGroup  
  * logs:CreateLogStream  
  * logs:PutLogEvents  
  * ec2:DeleteVolume  
  * ec2:DescribeInstanceAttribute  
  * ec2:DescribeInstances  
  * ec2:DescribeVolumes  
  * ec2:ModifyInstanceAttribute  
  * ec2:TerminateInstances  

## How it works: 
A click event on the IoT button is delivered via AWS IoT to a lambda function (gorilla.py). The lambda function identifies the click event then randomly selects an availability zone. With a target AZ, the function then grabs a list of all InstanceID's in a non-terminated state. The function then grabs a second list of InstanceID's that include the tag key `tag:aws:autoscaling:groupName`, value `*`. The `tag:aws:autoscaling:groupName` key is automatically applied to all instances deployed by an ASG. Diff the two lists and we now know:  
1. all instances in the AZ,  
2. instances on the chopping block, and  
3. instances safe from the ~~headsmans axe~~ gorilla.  
All of this is logged into stdout aka, cloudwatch. Finally, a simple `fo`r loop wrapped in a `if`, `elif`, `elif` either pokes the gorilla with a hot iron and unlocks the proverbial cage or .... not.



TODO:  
* ~~clean up~~  
* ~~describe IAM policy req's~~  
* ~~(re)build with functions~~  
* ~~make multi-region - also need logic for diff number of AZ's~~  
* ~~add logic to ignore empty regions~~  
* add logic for multi-az, i.e. 1 AZ per region if multi-region
* make multi-account  
* add LONG clickEvent 'test DR mode', turn off disableApiTermination, terminate all instances (even non-asg), delete all EBS volumes
* clean up gorilla.py and add command line arg's support for clickType
