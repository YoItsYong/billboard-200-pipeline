# Billboard 200 Pipeline
![Banner image for Billboard 200 Pipeline project.](/images/bb200_banner.jpg)
## Table of Contents
- [Introduction](https://github.com/YoItsYong/billboard-200-pipeline/blob/main/README.md#introduction)
- [Objective](https://github.com/YoItsYong/billboard-200-pipeline/blob/main/README.md#objective)
- [Technologies](https://github.com/YoItsYong/billboard-200-pipeline/blob/main/README.md#technologies)
- [Data Pipeline](https://github.com/YoItsYong/billboard-200-pipeline/blob/main/README.md#data-pipeline)
- [Dashboard](https://github.com/YoItsYong/billboard-200-pipeline/blob/main/README.md#data-pipeline)
- [Future Improvements](https://github.com/YoItsYong/billboard-200-pipeline/blob/main/README.md#data-pipeline)
- [Reproducing the Project](https://github.com/YoItsYong/billboard-200-pipeline/blob/main/README.md#data-pipeline)
- [References](https://github.com/YoItsYong/billboard-200-pipeline/blob/main/README.md#data-pipeline)
## Introduction
The Billboard 200 is a weekly music chart that measures the top selling (or streaming) albums in the United States. Placing at the top of the chart has historically been a marker of a release's success and can often be an important factor in how an artist defines their legacy.

## Objective
While the Billboard 200 has been around since the 1940s, how we listen to and connect with music has evolved over the years. This project creates an end-to-end data pipeline to ingest existing Billboard 200 data from 1963 - 2019 to analyze and visualize the trends in charting artists over the years.

## Technologies
To create this pipeline, I used a variety of technologies to extract, transform, and load the data to the cloud, where it could be easily accesible for analysis. These technologies include:
- Infrastructure as Code (IaC): Terraform
- Containerization: Docker
- Cloud: Google Cloud Platform (GCP)
- Data Lake: Google Cloud Storage
- Data Warehouse: Google BigQuery
- Batch Processing: Apache Spark (PySpark)
- Workflow Orchestration: Mage
- Visualization: Google Looker Studio

![Diagram depicting what technology is used and how it is implemented.](/images/bb200_tech_diagram.png)

## Data Pipeline
### Preparing the Data
The data set orginates from [Components.one](https://www.dropbox.com/s/ahog97hcatpiddk/billboard-200.db?dl=1), a research platform that makes its data sets publicly available for use. The data from this site first comes in the form of a `.db` file, which is most commonly used with SQLite. Because this is not a file type I am used to working with, I opted to take this `.db` file and convert it to a `.csv.gz` for the sake of working more comfortably.

### Ingesting the Data
Using Mage, we then orechestrate the ingestion and exporting to our Data Lake in Google Cloud Storage (GCS).

During this step, we also convert the file from `.csv.gz` to `.parquet` to take up less space on GCS.

### Processing the Data
Now that the data is available in GCS, we'll then set up a separate pipeline to take this data from GCS, process and transform it using Apache Spark, and export the data to BigQuery.

To run Spark within Mage, we have shell commands in place to make sure our Mage instance is connected to Dataproc in Google Cloud. This allows us to run Spark without issue and move some of the processing load to the cloud.

```
df = spark.read.parquet('gs://bb200/bb200_albums.parquet')
```

### Tranforming the Data
Data transformations are performed using Python and SQL within Spark. These tranformations include:
- **Manage column data types:** ensure data types are correctly defined
```
df = df \
    .withColumn('date', df['date'].cast(DateType())) \
    .withColumn('rank', df['rank'].cast(IntegerType())) \
    .withColumn('length', df['length'].cast(IntegerType()))
```
- **Rename columns:** the column named 'length' seemed to ambiguous, so I had it changed to 'number_of_tracks'
```
df = df.withColumnRenamed('length', 'number_of_tracks')
```
- **Skip null values in first row:** the first row of data always returns null values. To avoid issues, I skip this row entirely.
```
df = df.filter(df.id > 1)
```
- **Handle other null values:** Some of the columns return null values based on the type of album that is charting.

    For example, many re-released albums were showing null for either of these columns. To avoid null value errors, I opted to set these to 0 by default.
```
df = df.na.fill(value=0, subset=['number_of_tracks'])
df = df.na.fill(value=0, subset=['track_length'])
```

After this, the data is automatically loaded to BigQuery where it is then pulled into Google Looker Studio for visualization.

## Dashboard
The dashboard below pulls from BiqQuery and creates charts and tables for further analysis.

**[LIVE VERSION](https://lookerstudio.google.com/reporting/69427c4c-7cd2-4f26-836d-74556ee00f74)**

[![Dashboard for Billboard 200 data.](/images/bb200_dashboard.png)]((https://lookerstudio.google.com/reporting/69427c4c-7cd2-4f26-836d-74556ee00f74))

The tiles I've selected for this dashboard includes:
- The artist with most chart placements at number 1
- The percentage of number 1s each of the top-charting artists has
- The number of artists that chart year over year

## Future Improvements
While the current iteration of the pipeline is functional, there are some additional steps and precaution that could be taken to improve overall performance.
- Streamline File Conversion Process: I plan to also look at streamlining the current process of converting the original SQLite file and implementing it into 
- Additional Calculations: There are likely some additional calculated columns that could be incorporated.
- Partition Data in GCS: There is room to partition the data for better organization.
- Implement CI/CD: I haven't implemented any more formal CI/CD processes for pushing changes to the project, but this is something that I will likely explore in the future for a more realistic p roduction environment.

## Reproducing the Project
The instructions below will help you set up the project environment and connect to cloud tools to reproduce the pipeline on your local machine.
### Prerequisites
- **Create Google Account:** Visit [cloud.google.com](https://cloud.google.com/?hl=en) and create a new Google account if you don't have one already
    - Create a new Google Cloud Project called `billboard-200-project`
    - Create Service Account w/ Owner permissions
        - Enable [Google BigQuery API](https://console.cloud.google.com/apis/library/bigquery.googleapis.com)
        - Enable [Google Cloud Dataproc API](https://console.cloud.google.com/apis/library/dataproc.googleapis.com)
        - Enable [Google Compute Engine API](https://console.cloud.google.com/apis/library/compute.googleapis.com)
    - Create Dataproc Cluster called `bb200-cluster` with default parameters
    - Download Service Account Key (JSON)
- **Install Terraform:** Follow [instructions here](https://developer.hashicorp.com/terraform/tutorials/gcp-get-started/install-cli) to install Terraform
### Using Terraform for Google Cloud Setup
First, we'll set up our Google Cloud Platform using Terraform. This makes it easier to ensure that the necessary storage resources are created.

Start by creating a new folder and copying the `main.tf` and `variables.tf` from the [Terraform folder](https://github.com/YoItsYong/billboard-200-pipeline/tree/main/terraform).

Within the `variables.tf`, replace the path to your Service Account Key file on your machine (as shown below).
```
variable "credentials" {
    description = "My Credentials"
    default = "./PATH/TO/GCS_KEY.json"
}
```
After adding the path to your Service Account Key, open a terminal and navigate to the `Terraform folder` on your machine and run the command below.
```
terraform init
```
Once the command above is complete, run this command.
```
terraform plan
```
Finally, we'll apply the changes to your Google Cloud Platform account.
```
terraform apply
```
### Configuring Google Cloud Platform
The Terraform files should have created a few resources within your Google Cloud Platform account.

Confirm the folllowing resources were created with their respective names.
- Google Cloud Platform Project = billboard-200-project
- Google Cloud Storage Bucket = bb200
- Google BigQuery Data Set = bb200_data

If any of these were not created created incorrectly, fix it manually.
### Configure Spark_Dataproc.py
After everything on Google Cloud is set up correctly, we'll configure the `spark_dataproc.py` file in `python/spark_dataproc`.

Replace the variables below with what matches your project.

```
#(Line 30) Replace temp_gcs_bucket with the name of your temporary bucket in GCS
temp_gcs_bucket = 'name_of_temp_gcs_bucket'
spark.conf.set('temporaryGcsBucket', temp_gcs_bucket)
```

After updating these variables, in GCS, create a new folder called `code` and copy the `spark_dataproc.py` to it.

### Docker/Mage Image Setup
Next, we'll be setting up Mage within Docker using the [Quickstart Guide](https://docs.mage.ai/getting-started/setup#get-mage) provided by Mage.

Using your terminal, `cd ..` until you're in your home directory and create a new directory called `mage`. Next, we'll run the command below to copy the quickstart repo to your own.
```
git clone https://github.com/mage-ai/compose-quickstart.git mage \
&& cd mage 
```

In the `mage` directory, we'll update a couple files before starting up our Mage Container
- Copy the contents of `Dockerfile` and `docker-compose.yml` from this repo and paste them into your Mage files
- In `dev.env`, rename the Mage Project to `bb200_project`
- In `requirements.txt`, add:
```
pyspark==3.5.1
```

Next, run the following commands:
```
cp dev.env .env && rm dev.env
docker compose up
```

Your Mage instance should now be live on `localhost:6789`.

Before moving on, we'll configure Mage to make sure it can connect to our Google Cloud Platform.
- In the Mage UI, click on `Files` in the side menu.

![Screenshot of Mage UI showing Files option in the side menu.](/images/mage_ui_files.png)

- Right click the project folder on left, select `Upload files`, and drag-and-drop your Service Account Key into the Mage window.
- After the upload is complete, open the `io_config.yml`, scroll down to `GOOGLE_SERVICE_ACC_KEY_FILEPATH` and enter the path to your key.
- Remove all of the other Google variables so your file looks like the image below.

![Screenshot of Mage UI showing Google Cloud Platform configuration in io_config.yaml.](/images/mage_io_config.png)

### Create Pipeline to Google Cloud Storage
Our first pipeline will take the `billboard200_albums_data` found [here](https://github.com/YoItsYong/billboard-200-pipeline/raw/main/data/billboard200_albums.csv.gz) and upload it to our Data Lake in Google Cloud Storage.

For this, you can copy and paste the `load_bb200_csv.py` and `export_bb200_gcs.py` files in `bb200_to_gcs`.

Your pipeline should look like this:

![Screenshot of Mage UI showing pipeline diagram for bb200_to_gcs.](/images/bb200_to_gcs.png)

This moves the data to Google Cloud Storage and converts the `.csv.gz` to `parquet` using Pandas.


### Install Google Cloud CLI
Within the Mage UI, click on the `Terminal` button on the side menu as shown below.

![Screenshot of Mage UI showing the Terminal option in the side menu.](/images/mage_ui_terminal.png)

Our goal is to run the Google Cloud CLI to be able to use `gcloud` scripts within Mage.

We'll start with installing the Google Cloud CLI. First, run the scripts below to download, extract, and install the files in the Mage Terminal.


```
#Download Google Cloud CLI
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-471.0.0-linux-x86_64.tar.gz

#Extract Google Cloud CLI
tar -xf google-cloud-cli-471.0.0-linux-x86_64.tar.gz

#Install Google Cloud CLI
./google-cloud-sdk/install.sh
```

Next, we'll run the following script to authorize Mage to make changes to your Google Cloud account and make sure the Google Cloud CLI knows which project to make changes to.
```
#Authorize Google Cloud Login
./google-cloud-sdk/bin/gcloud auth login

#Set Google Cloud Project
./google-cloud-sdk/bin/gcloud config set project INSERT_PROJECT_ID
```

_Note: You may have to edit the script above depending on your folder structure._


### Create Pipeline to BigQuery
Now that our `.parquet` files are available in GCS, we will now process and transform this data, move it over to our Data Warehouse in Google BigQuery.

In the `bb200_to_bq` folder, copy and paste the code to assemble your own pipeline. For the data loader, copy the code in `load_bb200_gcs.py` and add the path to your Service Account Key.

For the data exporters, copy the code in `export_bb200_bq.py`.

Your pipeline should look like this:

![Screenshot of Mage UI showing pipeline diagram for bb200_to_bq](/images/bb200_to_bq.png)

Before running the pipeline, make sure to replace `project` with the name of your Google Cloud Project name.

```
@data_exporter
def export_data(data, *args, **kwargs):
    os.system("""
    ./gsutil/google-cloud-sdk/bin/gcloud dataproc jobs submit pyspark \
        --project=INSERT_PROJECT_NAME \
        --cluster=music-chart-cluster \
        --region=us-central1 \
        --jars=gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.23.2.jar \
    gs://bb200/code/spark_dataproc.py \
        -- \
            --input_albums=gs://bb200/bb200_albums.parquet \
            --output=bb200_data.bb200_albums
    """)
```

Running this pipeline loads data from GCS and performs the transformations using `Apache Spark`. The transformed data is then moved to our BigQuery where we can connect to it with Google Looker Studio for visualizations.

### Create Visualizations in Google Looker Studio
Open [Google Looker Studio](https://lookerstudio.google.com/) and connect to BigQuery as your data source.

After this is added, you will be able to create tables, charts, and more to visualize the Billboard 200 data.

### Removing Resources
To avoid accruing costs on Google Cloud Platform, you can run the following command in your system terminal (not your Mage one) to breakdown the Terraform resources.

`terraform destroy`

[Back to top](https://github.com/YoItsYong/billboard-200-pipeline/blob/main/README.md#data-pipeline)