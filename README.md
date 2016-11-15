# iot-chaos-gorilla
AWS IoT button invoked Chaos Gorilla - DR testing at the click of a button

********* USE AT YOUR OWN RISK AND WITH EXTREME CAUTION *********

This is intentionally destructive, all care and no responsability taken. 


## Description:
iot-chaos-gorilla unleashes a 'Chaos Gorilla' and terminates EC2 instances in a random AWS availability zone.
Currently, the gorilla only terminates 'running' instances deployed using autoscale groups (ASG). Instances deployed outside ASG's or in a 'pending', 'shutting-down', 'stopping' or 'stopped' state are ignored. Instances in a 'terminated' state, well ....

A 'SINGLE' click event of the Gorilla Button will execute the sequence in DryRun mode, while a 'DOUBLE' click event is the real deal - KABOOM!. A 'LONG' click event will just tell you to get off your arse.

## How it works: 
A click event on the IoT button is delivered via AWS IoT to a lambda function (gorilla.py). The lambda function identifies the click event then randomly selects an availability zone. With a target AZ, the function then grabs a list of all InstanceID's in a non-terminated state. The function then grabs a second list of InstanceID's that include the tag key `tag:aws:autoscaling:groupName`, value `*`. The `tag:aws:autoscaling:groupName` key is automatically applied to all instances deployed by an ASG. Diff the two lists and we now know:  
1. all instances in the AZ,  
2. instances on the chopping block, and  
3. instances safe from the ~~headsmans axe~~ gorilla.  
All of this is logged into stdout aka, cloudwatch. Finally, a simple `fo`r loop wrapped in a `if`, `elif`, `elif` either pokes the gorilla with a hot iron and unlocks the proverbial cage or .... not.



TODO:
clean up
describe IAM policy req's
(re)build with functions
make multi-region - also need logic for diff number of AZ's
make multi-account
