from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from scripts import s3_download, s3_upload , spark_missed_deadline_job


local_workflow = DAG('late_shipments_to_carrier',
          description='Returns list of orders where the seller missed the carrier delivery deadline',
          schedule_interval='0 5 * * *',
          start_date=datetime(2019, 7, 10), catchup=False)

with local_workflow:

# Download the data from S3
    s3_download_operator = BashOperator(task_id='s3_download',
                                    bash_command=f'ls', ##<<<< edit path!! #python ./scripts/s3_download
                                    )

# Run Spark job to return order information where the seller
# missed the deadline to deliver the shipment to the carrier
    spark_missed_deadline_operator = BashOperator(task_id='spark_missed_deadline_job',
                                              bash_command=f'ls', ##<<<< edit path!! #python ./scripts/spark_missed_deadline_job
                                              )

# Specify that the Spark task above depends on the dataset downloading properly
    spark_missed_deadline_operator.set_upstream(s3_download_operator)

# Upload cleaned dataset to S3
    s3_upload_operator = BashOperator(task_id='s3_upload',
                                  bash_command=f'ls', ##<<<< edit path!! #python ./scripts/s3_upload
                                  )

# Specify that the S3 upload task depends on the Spark job running successfully
s3_upload_operator.set_upstream(spark_missed_deadline_operator)


s3_download_operator >> spark_missed_deadline_operator >> s3_upload_operator
