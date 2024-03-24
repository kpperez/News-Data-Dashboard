# News Headline Dashboard
URL: [https://news-data-dashboard-kpperez.streamlit.app/](https://news-data-dashboard-kpperez.streamlit.app/)
![news_data_pipeline](https://github.com/kpperez/News-Data-Dashboard/assets/123265217/a38216d3-e019-4c57-8081-04e2ec014ef7)
## Table of Contents
- [Description]()
  - [Overview]()
  - [Technologies Used]()
  - [Challenges]()
  - [Future Modifications]()
- [Configuration Steps]()
## Description
### Overview:
This repository hosts the code for a comprehensive data pipeline project designed to aggregate, process, and visualize news data in real-time. The core of this project is a robust data pipeline that fetches news data from the newsdata.io API, performs a series of transformations including cleaning, natural language processing (NLP) for tokenization, sentiment analysis, and classification, and then loads the processed data into a PostgreSQL database hosted on AWS RDS. The pipeline is orchestrated using Apache Airflow and runs on an AWS EC2 instance, ensuring scalable and reliable data processing.

To make the processed data accessible and interactive, a Streamlit application was developed. This application serves as a dashboard to visualize the news data, providing insights and analytics derived from the data pipeline. The application is hosted publicly, allowing users to interact with the latest news data analyses.

This project demonstrates a complete end-to-end solution for data processing and visualization, leveraging modern cloud infrastructure and programming frameworks to deliver real-time insights from news data. It showcases the integration of various technologies to solve complex data engineering challenges and provide a user-friendly platform for data analytics.
### Technologies Used:
- AWS Cloud
- Apache Airflow
- Python
- PostgreSQL
- Streamlit
### Challenges:
**Database Connectivity:** Connecting to the AWS RDS-hosted PostgreSQL database posed initial challenges, including navigating AWS security configurations and managing secure connection parameters. Resolving these issues involved refining access rules and enhancing credential management for robust database connectivity.

**Airflow Scheduler Configuration:** Setting up the Apache Airflow scheduler to reliably manage the data pipeline's tasks was complex. Adjusting Airflow's settings, defining clear task dependencies, and implementing monitoring strategies were key steps taken to ensure the scheduler's effective operation.

These challenges were critical learning points, emphasizing the importance of thorough testing and configuration to achieve a stable and efficient data processing pipeline.
### Future Modifications:
- **Improve Sentiment Analysis:** Upgrade to a more advanced model for better accuracy in sentiment classification.
- **Expand Data Sources:** Consider purchasing the API or exploring additional sources for richer data.
- **Enhanced Dashboard Interactivity:** Add more interactive elements to the Streamlit dashboard for dynamic analysis.
- **Automated Alerts:** Implement alerts or summaries based on specific news sentiment or trends.
- **Boost Security:** Strengthen data privacy and security measures as data volume and sensitivity increase.
  
These steps aim at refining analysis, expanding content, and enhancing user engagement and security.
## Configuration Steps
1. **API Key Acquisition and Planning:** <br>
Signed up for a free API key from [newsdata.io](https://newsdata.io/), carefully read the documentation to understand the data structure, and selected the relevant data fields for the project (article_id, title, link, description, pubdate, source_id, and category).

2. **Database Setup:** <br>
Created an AWS RDS database instance, setting up the necessary security credentials and access permissions for specified IP addresses and ports. Utilized DBeaver for creating a database table with appropriately typed columns matching the data structure determined earlier.

3. **Compute Resource Configuration:** <br>
Launched an EC2 instance with Ubuntu, ensuring security credentials were in place including the pem key for SSH access. Updated the system and set up a Python environment with all required libraries (e.g., airflow, nltk, pandas) and configured AWS CLI for RDS connectivity.

4. **Development Environment Preparation:** <br>
Utilized VSCode with SSH remote to connect to the EC2 instance for efficient code editing. Developed a Python DAG for Airflow to handle data extraction from the API, transformation (including cleaning, NLP tokenization, sentiment analysis, and classification), and loading into the RDS database.

5. **Airflow Pipeline Validation:** <br>
Tested the Airflow pipeline to ensure accurate periodic data extraction and loading (every four hours) into the RDS database, confirming operational integrity and data quality.

6. **Streamlit Application Development:** <br>
Built a [Streamlit application](https://github.com/kpperez/News-Data-Dashboard/tree/main/streamlit_app) to present the processed data, integrating RDS database connectivity. The application's development was focused on usability and data visualization.

7. **Application Deployment and Security:** <br>
Integrated database credentials into Streamlit's secrets manager for secure access, enabling the public hosting of the application on the Streamlit community page for broader visibility.
