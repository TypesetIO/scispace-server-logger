# scispace-server-logger
Common Server logger for all the services in Scispace

Following are the configurations available as env variables:
- ENABLE_SCISPACE_LOGGER => Whether to enable the scispace logger in a particular machine or not
- DELIVERY_STREAM_NAME => Kinesis Delivery Stream name to push the logs
- ENV => environment like prod, stage etc
- APP_NAME => name of app like agg-backend, scispace-features etc
