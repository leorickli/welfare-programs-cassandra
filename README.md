# welfare-programs-cassandra

<img width="1055" alt="Screenshot 2023-12-25 at 14 01 18" src="https://github.com/leorickli/cassandra-portal-da-transparencia/assets/106999054/021ac472-ec46-4847-9ee2-d57a5131723e">

This project explores the open-source tool Apache Cassandra for data analysis in NoSQL databases, using GCP for deploying the infrastructure and processing the data for analysis. The infrastructure created on GCP focuses on getting data from the public database Portal da Transparência (Transparency Portal) through an API, transforming it to a more readable format in Cassandra, and analyzing the data with visualizations.

*The **Transparency Portal (Portal da Transparência)** is a digital platform designed to provide detailed information about public entities' expenditures and financial management. Its primary goal is to promote transparency in public administration, allowing citizens, journalists, researchers, and other interested parties to access and analyze data related to revenues, expenses, contracts, agreements, and salaries of public servants, among other aspects.*

***Apache Cassandra** is an open-source, distributed NoSQL database management system designed to handle large amounts of data across many commodity servers, providing high availability and fault tolerance. It was originally developed by Facebook and later open-sourced as Apache Cassandra.*

The following GCP resources and other tools were used:
- **GCS (Google Cloud Storage):** Used for storing the data in the processing phases (raw and curated).
- **GCE (Google Compute Engine):** A VM with Cassandra DB was created so we can ingest the curated data in Cassandra DB for analysis.
- **Dataproc**: A cluster was created to process the data in its raw and curated stages through the use of Python and PySpark.
- **Pandas, Matplotlib, Scikit Learn**: For deeper analysis and visualizations, these tools were used to make more complex analyses with the data inside Cassandra.

### 1. Plan an infrastructure around Cassandra and load a public dataset

The API data is in JSON format, a lot of processing is needed so Cassandra can read these files. The idea is to transform it into CSV files so it can be both read in BigQuery and Cassandra. I chose Cassandra because I need a NoSQL database for this type of data. When you work with JSON data, schema can be very flexible, you can vary the number of key/values for each object you get, this could not work in a traditional SQL data warehouse system like BigQuery. The schema for this dataset proved to be very stable. So far. That doesn't change the fact that the schema could change in the near future, reinforcing the fact that BigQuery might not be a viable option.

Some columns had to be renamed after the processing, this JSON has nested within nested objects, making it very hard to process and transform it into CSV files for Cassandra. Along with renaming the columns, some other changes were made so the CSV file could be read.

- Removed the "\r\n" (carriage return and line feed) control characters.
- Removed the '\"' attempt to escape the double quotes inside double quote lines.

Once the architecture and processing are done, we can start thinking about the analytics section. After an EDA (Exploratory Data Analysis) is done, we can convey the idea of creating a Business Question:

*Given the initial price date (valorInicialCompra) and final date (valorFinalCompra) of each contract, how can you explore the "valorInicialCompra" to find the average discrepancy of the given values, the number of contracts that had this increase in value compared to the others and the contract that had the highest discrepancy so far?*

### 2. Load the public dataset into a Cassandra database

A Dataproc cluster was created so I could work with this [Jupyter Notebook](https://github.com/leorickli/cassandra-portal-da-transparencia/blob/main/contratos_etl.ipynb) using Python and PySpark. This notebook makes a GET request on the Portal da Transparência API, specifically the "contratos" section. For this project, I used a specific organization code (SIAFI code) starting from a specific date (the date that this data started being recorded).

A Cassandra database was created in a virtual machine in GCE. I deployed the [Cassandra cluster](https://console.cloud.google.com/marketplace/product/cloud-infrastructure-services/cassandra-ubuntu-20-04?project=cassio-project) found in the Marketplace in GCP.

### 3. Implement ETL in the Cassandra dataset

Now we have to make Cassandra operational. First, we use the command "nodetool status" to check if the database is working properly.

<img width="755" alt="Screenshot 2023-12-25 at 16 19 19" src="https://github.com/leorickli/cassandra-portal-da-transparencia/assets/106999054/f9414b99-c22a-4d8f-9ee7-fcb79126c5e3">

Then we ingest the data from the bucket in the curated folder into the VM with the following command:

```
gsutil cp gs://cassandra-project-leorickli/curated/contratos_curated.csv .
```

Using CQL, we create a keyspace and a table with the schema first, so we can then ingest the data into Cassandra:

```
CREATE TABLE IF NOT EXISTS contratos_table_full (
    dataAssinatura date,
    dataFimVigencia date,
    dataInicioVigencia date,
    dataPublicacaoDOU date,
    fundamentoLegal text,
    id int,
    modalidadeCompra text,
    numero int,
    numeroProcesso text,
    objeto text,
    situacaoContrato text,
    valorFinalCompra float,
    valorInicialCompra float,
    compra_contatoResponsavel text,
    compra_numero int,
    compra_numeroProcesso text,
    compra_objeto text,
    fornecedor_cnpjFormatado text,
    fornecedor_cpfFormatado text,
    fornecedor_id int,
    fornecedor_nome text,
    fornecedor_nomeFantasiaReceita text,
    fornecedor_numeroInscricaoSocial int,
    fornecedor_razaoSocialReceita text,
    fornecedor_tipo text,
    unidadeGestora_codigo int,
    unidadeGestora_descricaoPoder text,
    unidadeGestora_nome text,
    unidadeGestoraCompras_codigo int,
    unidadeGestoraCompras_descricaoPoder text,
    unidadeGestoraCompras_nome text,
    unidadeGestora_orgaoMaximo_codigo int,
    unidadeGestora_orgaoMaximo_nome text,
    unidadeGestora_orgaoMaximo_sigla text,
    unidadeGestora_orgaoVinculado_cnpj text,
    unidadeGestora_orgaoVinculado_codigoSIAFI int,
    unidadeGestora_orgaoVinculado_nome text,
    unidadeGestora_orgaoVinculado_sigla text,
    unidadeGestoraCompras_orgaoMaximo_codigo int,
    unidadeGestoraCompras_orgaoMaximo_nome text,
    unidadeGestoraCompras_orgaoMaximo_sigla text,
    unidadeGestoraCompras_orgaoVinculado_cnpj text,
    unidadeGestoraCompras_orgaoVinculado_codigoSIAFI int,
    unidadeGestoraCompras_orgaoVinculado_nome text,
    unidadeGestoraCompras_orgaoVinculado_sigla text,
    PRIMARY KEY (id)
);
```

Now we can ingest data into the table, using the following cql command:

```
COPY contratos_table_full (
    dataAssinatura, dataFimVigencia, dataInicioVigencia, dataPublicacaoDOU,fundamentoLegal,
    id, modalidadeCompra, numero, numeroProcesso, objeto, situacaoContrato, valorFinalCompra,
    valorInicialCompra, compra_contatoResponsavel, compra_numero, compra_numeroProcesso, compra_objeto,
    fornecedor_cnpjFormatado, fornecedor_cpfFormatado, fornecedor_id, fornecedor_nome, fornecedor_nomeFantasiaReceita,
    fornecedor_numeroInscricaoSocial, fornecedor_razaoSocialReceita, fornecedor_tipo, unidadeGestora_codigo,
    unidadeGestora_descricaoPoder, unidadeGestora_nome, unidadeGestoraCompras_codigo, unidadeGestoraCompras_descricaoPoder,
    unidadeGestoraCompras_nome, unidadeGestora_orgaoMaximo_codigo, unidadeGestora_orgaoMaximo_nome,
    unidadeGestora_orgaoMaximo_sigla, unidadeGestora_orgaoVinculado_cnpj, unidadeGestora_orgaoVinculado_codigoSIAFI,
    unidadeGestora_orgaoVinculado_nome, unidadeGestora_orgaoVinculado_sigla, unidadeGestoraCompras_orgaoMaximo_codigo,
    unidadeGestoraCompras_orgaoMaximo_nome, unidadeGestoraCompras_orgaoMaximo_sigla, unidadeGestoraCompras_orgaoVinculado_cnpj,
    unidadeGestoraCompras_orgaoVinculado_codigoSIAFI, unidadeGestoraCompras_orgaoVinculado_nome, unidadeGestoraCompras_orgaoVinculado_sigla
    )
FROM '/home/leonardo_moreira/contratos_curated.csv'
WITH DELIMITER=',' AND HEADER=TRUE;
```

It's important to declare all of the columns again so Cassandra recognizes each one of them individually along with the delimiter and the existence of the header. With that, we can start querying the database using the CQL querying language through the "cqlsh" command:

<img width="702" alt="Screenshot 2023-12-25 at 16 26 36" src="https://github.com/leorickli/cassandra-portal-da-transparencia/assets/106999054/c765313b-692d-496c-ad24-c270bc505f36">

### 4. Create data visualizations with the Cassandra dataset

Cassandra is great for NoSQL analysis, but when it comes to more complex conditions and aggregation commands like WHEN and WHERE, if you don't specify partition keys strategically in your dataset, Cassandra will fail to provide this more in-depth analysis. In this case, data was analyzed through this [Python notebook](https://github.com/leorickli/cassandra-portal-da-transparencia/blob/main/cassandra_analysis.ipynb) so we can start making visualizations with Pandas, Matplotlib and Scikit Learn. To do that, we need to first modify some parameters on the cassandra.yaml configuration through the "sudo nano /etc/cassandra/cassandra.yaml" command.

Once inside the configuration, modify the following parameters:

1. **listen_address (set to 127.0.0.1)**: This is the IP address or hostname that Cassandra binds to for connecting with other Cassandra nodes. It's used for internal cluster communication. Setting it to 127.0.0.1 means that the node will only accept connections for inter-node communication (like gossip, replication, etc.) from itself. This setting is typically used when each node communicates via a separate network interface for internal cluster traffic, which is a common setup for enhancing security and performance.
2. **rpc_address (set to 0.0.0.0)**: This setting specifies the IP address to bind to for client connections (i.e., where it listens for connections from clients). Setting this to 0.0.0.0 allows the Cassandra node to accept client connections on any network interface. This is a common configuration when you want the node to be accessible from any network, including external networks, provided appropriate network and firewall rules are in place.
3. **broadcast_rpc_address (set to 34.74.214.149)**: This is the address that the Cassandra node advertises to clients for RPC (Remote Procedure Call) connections. It's particularly important in environments where nodes are behind a NAT (Network Address Translation) or when using public cloud services. Since your Cassandra node is likely on a virtual machine with the external IP 34.74.214.149, this setting ensures that clients outside of your local network (like applications or other nodes not in the same virtual private cloud or local network) can correctly address RPC requests to this node.

With the analysis in the [Python notebook](https://github.com/leorickli/cassandra-portal-da-transparencia/blob/main/cassandra_analysis.ipynb), we can properly answer the business question declared on item #1, by exploring the "valorInicialCompra" we can find the average discrepancy of the given values, the number of contracts that had this increase in value compared to the others and the contract that had the highest discrepancy so far.

### Conclusion

- Cassandra is great for NoSQL types of data but when it comes to more complex data analysis, a traditional data warehouse will be enough for visualizations too.
- I wasted some time setting up an SSH key to access the Cassandra VM on my local machine. There is no need for that, just make the modifications on "cassandra.yaml" for it to work.
- PySpark can send data directly to the VM, I find it more interesting to send it to a curated stage so data can be accessed by different resources, like BigQuery, as shown in the examples below:

<img width="566" alt="Screenshot 2023-12-25 at 17 08 57" src="https://github.com/leorickli/cassandra-portal-da-transparencia/assets/106999054/550db8ea-9c05-4c21-99d5-7591d9392089">

***

<img width="1129" alt="Screenshot 2023-12-25 at 17 08 08" src="https://github.com/leorickli/cassandra-portal-da-transparencia/assets/106999054/a73320b9-9bd6-4429-9853-d2b58daec821">

***

<img width="1071" alt="Screenshot 2023-12-25 at 17 08 32" src="https://github.com/leorickli/cassandra-portal-da-transparencia/assets/106999054/29c9bf01-8528-4286-91a3-e1f3d23ea167">
