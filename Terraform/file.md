### ⚙️ How to Deploy This Code
### To use this Terraform code, you'll follow these steps in a Google Cloud Shell environment or on your local machine with the gcloud CLI and Terraform installed:

## Save the Code: Save the code above into a file named main.tf.

## Initialize Terraform: Run terraform init to download the Google Cloud provider.

## Review the Plan: Run terraform plan to see exactly what infrastructure will be created.

## Apply the Configuration: Run terraform apply. Type yes when prompted to confirm the deployment.

## Once the deployment is complete, Terraform will display the external IP address of your new VM in the output block. You can paste that IP into your web browser to see the simple Apache web page hosted on your Compute Engine VM
###
💡 Key Components Explained
### Backend Service & Health Check: This is the core logic. The Backend Service connects the Load Balancer to your VM group. The Health Check continuously pings your VMs to ensure they are serving traffic correctly; if a VM fails the check, the load balancer automatically stops sending it requests.

### URL Map: Because this is a Layer 7 (HTTP) Load Balancer, the URL Map allows you to inspect the incoming request path or hostname and route traffic to different backend services (e.g., ```/api``` goes to a different VM group than ```/images```).

### Forwarding Rule: This is the final step that ties everything together. It takes the reserved Global IP Address and port 80 and directs all incoming traffic to the Target HTTP Proxy, which then uses the URL Map to distribute the load.

### To deploy this, you would place it alongside your Compute Engine (MIG) definition in your Terraform configuration and run ```terraform apply```
