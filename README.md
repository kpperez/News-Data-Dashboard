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
...
### Technologies Used:
- AWS Cloud
- Apache Airflow
- Python
- PostgreSQL
- Streamlit
### Challenges:
...
### Future Modifications:
...
## Configuration Steps
1. Signed up for a free API key from [newsdata.io](https://newsdata.io/), read the documentation, and chose what data I would keep from each request (article_id, title, link, description, pubdate, source_id, and category). 
2. Created an AWS RDS database instance and specified security credentials. I also gave the permissions for the correct IP addresses and ports to be able to write and read from this database.   
3. Next, I started a new EC2 instance with Ubuntu as the operating system. At this point I have a pem key saved on my local machine and all of the correct security credentials.
4. In the EC2 instance terminal I ran commands to update the system, created a virtual environment directory, installed all of the appropriate python packages(airflow, nltk, pandas, etc...), and ran AWC CLI commands to connect the rds database.
5. 
