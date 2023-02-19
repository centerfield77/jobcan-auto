from google.cloud import secretmanager


def get_secret_version(project_id, secret_id, version_id='latest'):
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(request={"name": name})

    # Print the secret payload.
    payload = response.payload.data.decode("UTF-8")
    return payload
