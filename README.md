# sqlalchemy-challenge

## Part I: Climate Analysis and Exploration

* Utilized SQLAlchemy create_engine to connect to the sqlite database
* Used SQLAlchemy automap_base() to reflect our tables into classes and save a reference to those classes called, Station and Measurement
* Linked Python database by creating a SQLAlchemy session
* Analyzed precipitation and station data using matplotlib, numpy, pandas, and SQLAlchemy 

## Part II: Climate App
* Used Flask to creat routes to climate app
* Climate app routes all return JSON lists of data according to specified session queries
