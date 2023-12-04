#!/bin/bash

# Check if the first argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <upload|download>"
    exit 1
fi

# Get the action (upload or download) from the first argument
action=$1

bucket_name="projects-pipeline-storage"

# Define the local and S3 paths
local_path="src/.chalice/deployed"
s3_destination="s3://$bucket_name/OpanonBot/deployed"

# Perform the specified action
case $action in
    "upload")
        # Upload the folder and its content to S3
        aws s3 sync "$local_path" "$s3_destination"
        echo "Upload complete."
        ;;
    "download")
        # Download the folder and its content from S3
        aws s3 sync "$s3_destination" "$local_path"
        echo "Download complete."
        ;;
    *)
        echo "Invalid action. Use 'upload' or 'download'."
        exit 1
        ;;
esac
