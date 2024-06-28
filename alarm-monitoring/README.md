# Jenkins Pipeline for Alarm Monitoring

This provides a solution for monitoring alarms in AWS resources. It includes a Jenkins pipeline for automating the generation of reports and handling alarms based on predefined configurations. The pipeline includes stages for setting up the build environment, pulling the Git repository, downloading artifacts from an S3 bucket, executing a Python script, and handling post-build actions.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Jenkins Pipeline](#jenkins-pipeline)
- [Python Scripts](#python-scripts)
- [Usage](#usage)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before using this project, make sure you have the following:

- AWS account with the necessary permissions.
- Jenkins server with the required plugins installed.
- Python 3.8 or later installed on your Jenkins server.

## Pipeline Configuration

### Parameters

- **ENV**: Choose the environment name (e.g., 'non-prod').
- **BRANCH**: Specify the Git branch name (default is 'master').

### Options

- **Build Discarder**: Keeps the last 5 builds and artifacts.
- **Timestamps**: Adds timestamps to the build log.

### Environment Variables

- **DEFAULT_ENV**: Default environment name.
- **DEFAULT_BRANCH**: Default Git branch name.
- **GIT_URL**: Git repository URL.
- **GIT_PATH**: Git repository path.
- **REGION_NAME**: AWS region name.
- **REPOSITORY_NUMBER**: AWS account repository number.
- **PROJECT_NAME**: Name of the project.
- **SNS_TOPIC_NAME**: SNS topic for alerts.
- **S3_BUCKET_NAME**: S3 bucket for configuration.
- **S3_BUCKET_PATH**: Path to the configuration file in S3.

### Triggers

The pipeline is triggered daily at 9:00 AM using a cron expression.

## Pipeline Stages

1. **Setting Build**: Configures build details, including display name and description.
2. **Cleaning the Workspace**: Cleans the Jenkins workspace.
3. **Pulling the Repository**: Pulls the Git repository with the specified branch.
4. **Download Artifacts from S3**: Downloads artifacts from the specified S3 bucket and path.
5. **Execute Python Script**: Sets up a Python virtual environment, installs dependencies, and executes the main Python script (`main.py`).
6. **Post-Build (Failure)**: Sends an SNS notification in case of build failure.

## Python Scripts

The main functionality is implemented in Python scripts. The `main.py` script is responsible for monitoring and generating reports, interacting with AWS services, and creating reports.

### Dependencies

- `boto3`==1.28.41
- `xlsxwriter`==3.1.2
- `PyYAML`==6.0.1
- `python-dateutil`==2.8.2
- `botocore`==1.31.41
- `jmespath`==1.0.1
- `s3transfer`==0.6.2
- `six`==1.16.0
- `urllib3`==1.26.16

## Usage

1. Configure Jenkins with the necessary plugins and settings.
2. Create a new pipeline job in Jenkins.
3. Copy and paste the provided pipeline script into the job configuration.
4. Configure the required parameters and environment variables in the Jenkins job.
5. Save the job configuration and trigger the pipeline manually or wait for the scheduled cron job to run.

The generated report will be available in the Jenkins workspace.

