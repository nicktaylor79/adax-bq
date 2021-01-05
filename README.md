#Adax API radiator data to BigQuery

Script to poll the Adax API for rooms, and their current and target temperatures, and then upload this to a BigQuery table. 

More info on the Adax API is here - https://adax.no/om-adax/api-development/

If you make use of this script, please let me know! 

To make the script work:

* Create a BigQuery dataset and table to hold the data. You can name these whatever you like. 
* The table should contain timestamp, room, currenttemp and targettemp

* Create a Cloud Scheduler job which runs at your preferred time interval and triggers a message on a PubSub topic

* Create a new function with this script, setting environment variables for your dataset and table, triggered by your PubSub topic
* Set environment variables for your ADAX CLIENT_ID and CLIENT_SECRET

* Make sure your function runs as a service account that has access to the BQ table