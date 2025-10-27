from google.cloud import compute_v1

PROJECT_ID = "YOUR_GCP_PROJECT_ID" # Replace with your project ID
ZONE = "us-central1-a"             # Zone where the VM will be created
INSTANCE_NAME = "python-sdk-vm"    
MACHINE_TYPE = f"zones/{ZONE}/machineTypes/e2-micro"
IMAGE_FAMILY = "debian-11"         # Debian OS image family

def create_gce_instance():
    """
    Creates a simple Compute Engine VM instance.
    """
    print(f"Starting VM creation in zone {ZONE}...")

    # Initialize the Compute Engine client
    instance_client = compute_v1.InstancesClient()
    
    # 1. Get the latest OS image details
    image_client = compute_v1.ImagesClient()
    image_response = image_client.get_from_family(
        project="debian-cloud", family=IMAGE_FAMILY
    )
    
    # 2. Define the disk configuration
    disk_config = compute_v1.AttachedDisk(
        auto_delete=True,
        boot=True,
        type_=compute_v1.AttachedDisk.Type.PERSISTENT,
        initialize_params=compute_v1.AttachedDiskInitializeParams(
            source_image=image_response.self_link,
            disk_size_gb=10,
            disk_type=f"zones/{ZONE}/diskTypes/pd-balanced",
        ),
    )

    # 3. Define the network interface (using the default network)
    network_config = compute_v1.NetworkInterface(name="global/networks/default")

    # 4. Define the instance request object
    instance = compute_v1.Instance(
        name=INSTANCE_NAME,
        machine_type=MACHINE_TYPE,
        disks=[disk_config],
        network_interfaces=[network_config],
    )

    # 5. Send the creation request
    operation = instance_client.insert(
        project=PROJECT_ID, zone=ZONE, instance_resource=instance
    )

    # Wait for the operation to complete
    print("Waiting for operation to finish...")
    operation.wait()

    if operation.error:
        print(f"Error creating instance: {operation.error}")
        return

    print(f"✅ VM '{INSTANCE_NAME}' created successfully at: {operation.target_link}")

if __name__ == "__main__":
    create_gce_instance()
