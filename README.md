# brazilian-data-project

# Problem Statement
Retailers in the current landscape are adapting to the digital age. Digital retail behemoths have carved out substantial market shares in the online space at the same time that traditional retail stores are broadly in decline. In this time of digital flux, an omni-channel retail approach is necessary to keep pace. This is especially true for retailers that have invested in an extensive brick-and-mortar store portfolio or have strong relationships with brick-and-mortar partners. 

This data engineering project uses a real world retail dataset to explore delivery performance at scale. The primary concern of data engineering efforts in this project is to create a strong foundation onto which data analytics and modeling may be applied as well as provide summary reports for daily ingestion by decision makers. 

A series of ETL jobs are programmed as part of this project using Python, Docker, SQL, Airflow, and Spark to build pipelines that download data from an AWS S3 bucket, apply some manipulations, and then load the cleaned-up data set into another location on the same AWS S3 bucket for higher level analytics. 

# Dataset of choice
The dataset of choice for this project is a series of tables [provided by the Brazilian Ecommerce company Olist](https://www.kaggle.com/olistbr/brazilian-ecommerce/home#olist_orders_dataset.csvhttps://www.kaggle.com/olistbr/brazilian-ecommerce/home#olist_orders_dataset.csv).

![Data eng dig(1)](https://github.com/MohammmadAnas/brazilian-data-project/assets/127856326/6f9d9d4e-2e41-4b19-a004-2366d98f5da5)



# Methodology:
1. Construct a mock production data lake in AWS S3 replete with the table schema above
2. Analyze the tables with an eye toward identifying the delivery performance of Olist orders/sellers 
3. Write a Spark and Spark SQL job to join together tables answering the question, "Which orders/sellers missed the deadline imposed by Olist for when their packages need to be delivered to a carrier?"
4. Build an ETL pipeline using Airflow that accomplishes the following:
* Downloads data from an AWS S3 bucket
* Runs a Spark/Spark SQL job on the downloaded data producing a cleaned-up dataset of delivery deadline missing orders
* Upload the cleaned-up dataset back to the same S3 bucket in a folder primed for higher level analytics

## Running the project
### 1. Requirements
In order to run the project smoothly, a few requirements should be met:
- AWS account with sufficient permissions to access and work on S3, Redshift, and EMR. 
To do so: 
    *   Go to [IAM](https://console.aws.amazon.com/iam/home) in AWS console.
    *   Create a new user
    *   Add permissions to that new user: `AmazonS3FullAccess`, `AmazonRedshiftFullAccess`, `AdministratorAccess`, `AmazonEMRFullAccessPolicy_v2`, `AmazonEMRServicePolicy_v2`, `AmazonEC2FullAccess`.
    *   In the "Security credentials" tab, create access key and download the `.csv` file.  

- It is also necessary to have the AWS account preconfigured (i.e having `~/.aws/credentials` and `~/.aws/config` available in your local environment). [This AWS Doc](https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/setup-credentials.html) shows the essential steps to setup local environment with AWS.


- Docker and Docker Compose, preinstalled in your local environment. Otherwise, they can be installed from [Get Docker](https://docs.docker.com/get-docker/).

- Terraform preinstalled in your local environment. If not, please install it by following the instructions given in the [official download page](https://www.terraform.io/downloads).


### 2. Clone the repository
```bash
git clone https://github.com/HoracioSoldman/batch-processing-on-aws.git
```

### 3. Run Terraform
We are going to use Terraform to build our AWS infrastructure

From the project root folder, move to the `./terraform` directory
```bash
cd terraform
```
Run terraform commands one by one

- Initialization
    ```bash
    terraform init
    ```

- Planning
    ```bash
    terraform plan
    ```
- Applying
    ```bash
    terraform apply
    ```
## Step 4: Get hands-on with Airflow 
- From the project root folder, move to the `./airflow` directory
    ```bash
    cd airflow
    ```
- Create environment variables in the `.env` file for our future Docker containers.
    ```bash
    cp .env.example .env
    ```

- Fill in the content of the `.env` file.
    The value for `AIRFLOW_UID` is obtained from the following command:
    ```bash
    echo -e "AIRFLOW_UID=$(id -u)"
    ```
    Then the value for `AIRFLOW_GID` can be left to `0`.

    - Build our extended Airflow Docker image
    ```bash
    docker build -t airflow-img .
    ```
    If you would prefer having another tag, replace the `airflow-img` by whatever you like. Then just make sure that you also change the image tag in [docker-compose.yaml](/airflow/docker-compose.yaml) at line `48`: `image: <your-tag>:latest`.

    This process might take up to 15 minutes or even more depending on your internet speed. At this stage, Docker also instals several packages defined in the [requirements.txt](/airflow/requirements.txt).

- Run docker-compose to launch Airflow

    Initialise Airflow
    ```bash
    docker-compose up airflow-init 
    ```

    Launch Airflow
    ```bash
    docker-compose up
    ```
[The late_shipments_to_carrier.py dag includes the three steps needed to complete our pipeline as defined above.]( https://github.com/ajupton/big-data-engineering-project/blob/master/airflow/dags/late_shipments_to_carrier_dag.py)

The first step is downloading the brazilian-ecommerce.zip file from your S3 bucket. [The script to accomplish this task is found here.](https://github.com/ajupton/big-data-engineering-project/blob/master/airflow/scripts/s3_download.py)

The next step is to run a Spark SQL job to do a pretty simply join of three relations and filter for orders/sellers that missed the delivery deadline to get their package to a designated carrier for shipment to the consumer. [This script first unzips the dataset, then sets up a Spark session, runs a simple Spark SQL operation, and then writes the results of the Spark SQL operation to a single csv file.](https://github.com/ajupton/big-data-engineering-project/blob/master/airflow/scripts/spark_missed_deadline_job.py)

Finally, the dataset identifying orders that missed the carrier delivery deadline is uploaded to the same S3 bucket in a different folder. [This script also screens out non-csv files from being uploaded to keep the folder fairly clean.](https://github.com/ajupton/big-data-engineering-project/blob/master/airflow/scripts/s3_upload.py)

To run the job, make sure to first edit the paths of each of the scripts to match the paths where you'd like to run your analysis on your own machine and of course make sure to include the specific details of your S3 bucket. 

One thing to note about the scripts is the `.set_upstream()` method applied to the second two operators. This ensures that if, for any reason, the initial file download fails that Airflow will retry the jobs. Another thing to note about the dag is the schedule, which I'm manually triggering using the Airflow UI. There's a lot more depth to job scheduling. 

But there you have it! This is a pretty simple pipeline, and shows how powerful Airflow can be in its ability to schedule various jobs using a variety of technologies like python and Spark. This only scratches the surface of what's capable with Airflow. 

The next step in this process is incorporating AWS EMR into the pipeline to run the Spark job on a cluster instead of locally on my machine. Stay tuned for updates!
