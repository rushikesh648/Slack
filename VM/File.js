// This is Node.js server-side code, not browser DOM code.
const AWS = require('aws-sdk');

// Configure the AWS Region
AWS.config.update({ region: 'us-east-1' });

const ec2 = new AWS.EC2();

const params = {
  ImageId: 'ami-0abcdef1234567890', // The ID of the OS image (AMI)
  InstanceType: 't2.micro',          // The size of the VM
  MinCount: 1,
  MaxCount: 1
};

ec2.runInstances(params, function(err, data) {
  if (err) {
    console.error("Could not create instance", err);
  } else {
    const instanceId = data.Instances[0].InstanceId;
    console.log("Created instance", instanceId);
  }
});
