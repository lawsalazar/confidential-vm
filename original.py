from google.cloud import compute_v1
PROJECT_ID="tiph-infra-lawrence"
DOCKER_REPOSITORY=""
DOCKER_IMAGE=""
WORKLOAD_SERVICE_ACCOUNT=""
ZONE="us-central1-b"
INSTANCE_NAME="test-vm-jingling-python"
SERVICE_ACCOUNT_EMAIL="asdasdasddd@tiph-infra-lawrence.iam.gserviceaccount.com".format(service_account=WORKLOAD_SERVICE_ACCOUNT, project_id=PROJECT_ID)
def create_confidential_instance(project_id):
    client = compute_v1.InstancesClient()
    disk = compute_v1.AttachedDisk(
        disk_size_gb=20,
        auto_delete=True,
        boot=True,
        initialize_params=compute_v1.AttachedDiskInitializeParams(
            source_image="projects/confidential-space-images/global/images/confidential-space-debug-230600"
        )
    )
    instance_resource = compute_v1.Instance(
        confidential_instance_config=compute_v1.ConfidentialInstanceConfig(enable_confidential_compute=True),
        shielded_instance_config=compute_v1.ShieldedInstanceConfig(enable_secure_boot=True),
        metadata=compute_v1.Metadata(items=[compute_v1.Items(key="tee-image-reference", value=DOCKER_IMAGE), compute_v1.Items(key="tee-container-log-redirect", value="true")]),
        service_accounts=[compute_v1.ServiceAccount(email=SERVICE_ACCOUNT_EMAIL, scopes=["https://www.googleapis.com/auth/cloud-platform"])],
        name=INSTANCE_NAME,
        machine_type="zones/{zone}/machineTypes/n2d-standard-2".format(zone=ZONE),
        disks=[disk],
        scheduling=compute_v1.Scheduling(on_host_maintenance="TERMINATE"),
        network_interfaces=[compute_v1.NetworkInterface()]
    )
    
    request = compute_v1.InsertInstanceRequest(instance_resource=instance_resource, zone=ZONE, project=PROJECT_ID)

    # Make the request
    response = client.insert(request=request)
  
    # Handle the response
    print(response)

if __name__ == "__main__":
    create_confidential_instance(PROJECT_ID)