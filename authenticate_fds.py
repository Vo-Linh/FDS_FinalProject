
from google.cloud import storage


def authenticate_fds(project_id="your-google-cloud-project-id"):

    storage_client = storage.Client(project=project_id)
    buckets = storage_client.list_buckets()
    print("Buckets:")
    for bucket in buckets:
        print(bucket.name)
    print("Listed all storage buckets.")

authenticate_fds("finaldatasience")