# ChemBDDB
A software assisted database infrastructure for the exploration of chemical and material space. 

This software is built to enable proper bookkeeping of large scale chemical data generated through ChemML(Machine Learning Module) and 
ChemHTPS(High Throughput Screening Module). The main agenda of ChemBDDB is to simplify the use of database technology for 
non-expert users in the Chemistry community. It features an automated setup database facility, a customizable data model
template and tools that can be used to store, manipulate and access the database. 

The data schema used here is many to one relationship. This package utilizes homogeneous chemical data. Hence, relational database management system(RDBMS) - MySQL/Postgres is used in this pacakage. The web framework is implemented using Django RESTful API. The web templates are developed using HTML/CSS. Data cleansing and data injestion was carried out with the help of Pandas and Numpy. Data Analysis is employed by using Javascript(Google Charts), Matplotlib, Pandas, etc. Using JSmol, 3D rendering of molecules is employed on the web framework. 





