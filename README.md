# Temporal ETL & Infrastructure 

## Overview
This repo contains an ETL making use of Temporal's Durable Execution. The ETL makes use of `.csv` files rather than pushing to a given S3 bucket or storage layer for ease of local testing. There is heavy use of the [Temporal Python SDK](https://github.com/temporalio/sdk-python) from using:
* Workers to speak to the Temporal Server from within the `worker.py` file
* Activities to encapsulate logic that can then be retried by default when issues arise within the ETL
* Workflows to orchestrate and tie together various activities in order to allow this makeshift performance truck/SUV dealership track customers and transactions on their platform. 

Something to note is this was made more as a batch ETL and not as a real time application but can easily be augmented to do so. 

## Design
The ETL was designed to simulate the usual flow of an ETL which is a process that usually pulls data from various sorces, when available, then transform them right before loading to a given storage layer. 

The flow of the ETL is:
* Triggers the `pull_csv` function within the `activities/extractor.py` module. This simulates a check to a given database.
   * This instead looks for either one of the below `.csv` files.:
      * `placeholder.csv` - Tracks latest date of run, customer id, and transaction id. 
      * `purchase.csv` - Track purchases as they are generated.
      * `customer.csv` - Tracks customer data to have a table that can be linked to purchases.
      * `dispute.csv` - Tracks purchase disputes, this involves Cancellations, returns for refunds, or base returns for no refund.
* Runs `pull_recent_purchases` function within the `activities/extractor.py` module. This simulates a pull similar to an end of day rollup flow. 
* After all purchases are pulled from `pull_recent_purchases`, the next process is `define_customers_from_purchases` from `activities/transformer.py`. This pulls customer data from purchases to be able to store that data within the customer table.
* Following that activity, the dataclasses are shipped off into the `starter.py` file to then write into our make shift "database load".

## Instructions
1. Clone the repository locally.
2. Open a terminal in the root directory of the repository. Here you will want to run the `build.sh` script to build the temporal server locally to allow you to run the ETL. This requires a git enabled terminal to clone the repo.
3. Open another terminal, also in the root directory and run `python worker.py`. This will spin up the workers to wait for work in the queue.
4. Finally, trigger the workflow by running `python starter.py`. This can be run multiple times to continue to add more purchases and customers to the `.csv` files and iterate on the purchase date and ids. 

## Testing
See under `first_temporal/tests` to see some tests for the workflow and activity examples, not at all a full comprehensive test suite.

## Distributed Infrastructure
See under `terraform` for a brief snipet of terraform code for setting up an s3 bucket with a notification queue that fires off a lambda function each time a new object is created. This usecase is great for updating partitions in your AWS Glue catalog on create to allow for immediate ability to query landed files. This can also be used to help with things like rolling up and consolidating event files to reduce the strain on services like Athena which are not optimized for querying numerous small files.

## Future Considerations

There are quite a few ways this repository can be improved to better scale and better simulate purchasing from a real world dealer.

- [ ] Add cloud infrastructure to handle ingesting, fanning out, and storage of the 
- [ ] Add in the ability to handle repeat customers, updates on delivery states, field cancellation requests, etc.
- [ ] Futher normalize `purchase.csv` file to showcase how that can be used to create a data mart.