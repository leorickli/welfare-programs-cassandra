# cassandra-portal-da-transparencia

<img width="1055" alt="Screenshot 2023-12-25 at 14 01 18" src="https://github.com/leorickli/cassandra-portal-da-transparencia/assets/106999054/021ac472-ec46-4847-9ee2-d57a5131723e">

This project explores the open source tool Apache Cassandra for data analysis in NoSQL databases, using GCP for deploying the infrastructure and processing the data for analysis. The infrastucture created on GCP focuses on getting data from the public database Portal da Transparência (Transparency Portal) through an API, transform it to a more readable format in Cassandra and analyze the data with visualizations.

*The **Transparency Portal (Portal da Transparência)** is a digital platform designed to provide detailed information about the expenditures and financial management of public entities. Its primary goal is to promote transparency in public administration, allowing citizens, journalists, researchers, and other interested parties to access and analyze data related to revenues, expenses, contracts, agreements, and salaries of public servants, among other aspects.*

***Apache Cassandra** is an open-source, distributed NoSQL database management system designed to handle large amounts of data across many commodity servers, providing high availability and fault tolerance. It was originally developed by Facebook and later open-sourced as Apache Cassandra.*

The following GCP resources and other tools were used:
- **GCS (Google Cloud Storage):** Used for storing the data in the processing phases (raw and curated).
- **GCE (Google Compute Engine):** A VM with Cassandra DB was created so we can ingest the curated data in Cassandra DB for analysis.
- **Dataproc**: A cluster was created to process the data in its raw and curated stages through the use of Python and PySpark.
- **Pandas, Matplotlib, Scikit Learn**: For deeper analysis and visualizations, these tools were used to make more complex analysis with the data inside Cassandra.

### 1. Create an infrastructure around Cassandra and load a public dataset

A Dataproc cluster was created so I could work with Jupyter Notebooks using Python and PySpark

Business question: Given the initial price date (valorInicialCompra) and final date (valorFinalCompra) of each contract, what is the average discrepancy of the given values, the amount of contracts that had this increase in value compared to the others and the contract that had the highest discrepancy so far?
