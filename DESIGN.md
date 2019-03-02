# Design

## Challenge design

1. I will not update project structure
as in real life it's a separate task with its own priority.
2. I will not work on code coverage of existing code
as in real life it's a separate task with its own priority.
3. I will do what can be done in about 6 hours.
Better real life architecture is in this file below.
4. There will be some assumptions. In real life, it will
be questioned but today is weekend and I don't want to
break it with my questions.
5. As specified in README.md no DevOps work will be done.
6. Work will be done in the master branch for simplicity.
7. No migrations for DB is created as its considered as new DB.

### Assumptions

1. Max size of an uploaded file is 1Mb.
2. An uploaded file is in JSON format. For large files, it's much better
to use XML or CSV (partial parsers are available). Best
transport for integration apps is DB (best data integrity).
A queue is also good but most probably
they don't check the structure of each record.
3. A lot of commits in git will be created. Its expected that for production
it will be in feature branch and it will be merged as one commit.


## Real world design

### Datasync design

In most cases, we have several data syncs (1 or more per customer).
Also, the stability of the solution is always a good idea.

So, I propose the following architecture:
- integration binary (protbuf) RPC API in the main app
- client for integration API for Python (separate module)
- integration app (IA) that have customer specific logic

It's a bit more expensive (time-consuming) for the first integration
but for several integrations, it will be cheaper.

Also, as IA has it's own lifecycle it will be easier
to update separately IAs and main app.

#### Binary RPC-based API

Binary RPC-based API proposed instead of REST API. Why?
1. To minimize traffic between IAs and the main app.
2. To better check data integrity with more strict data types.
3. If a customer will want to implement integration by itself
we will provide a client library for required language.
4. Protobuf is quite old established technology.
5. REST-style (CRUD style) API is not good if we work with a large number of records. Batch style (RPC style) API is better.

Some ideas on how to implement this in Python: https://github.com/keenbrowne/flask-pbj
or https://github.com/ssola/python-flask-microservice


#### Cloud-based IA design

Why?
1. IA typically works from time to time. And in most cases
all in the same time (at night). So, autoscaling will
save money.
2. Queues in clouds are cheap. So, it can be used instead
of own instance of Redis or RabbitMQ.

For initial data storage, S3 bucket with automatic expire
can be used. Errors and broken records also can be stored
here.

Amazon Lambda functions can be used as a main part of IA.
It supports Python: https://docs.aws.amazon.com/lambda/latest/dg/python-programming-model.html

Proposed architecture:
1. Func to upload initial data.
2. Func to split initial data to batches. I think about 50k
records per batch (it can be evaluated better later).
3. Func to process each batch.
4. Func to delete old records if no errors so far.
5. Func to send the result back to the customer (and/or to us)
with results of processing.


## Errors handling

Errors always happen. From the beginning, we should have
procedure to reports errors back and/or to notify our team
about errors.

Also, it's a very good idea to sign an integration architecture
document with a customer. It also should include technical
contacts to discuss possible errors.


## Deletion of old records

The idea that we should calculate records to delete by ourselves
is quite bad: it's quite a serious action that should be declared
explicitly.

It's unclear what to do with records deletion if we have some
broken record in the input: delete all including broken or
delete nothing.

Another problem is technical: how to calculate records to delete
when we have a lot of records in DB.

Some ideas:
1. Use individual table per batch and customer. In this case, we don't need to delete records at all (we create a new DB table
for each batch). If we really think about stability it will
be even better: we will not switch to this table if any errors
will occur during data sync. This approach does not work well
if we want an update of individual records ASAP and we will have
some problems on how to integrate it with ORM.
2. Use in-memory set structure inside IA to calculate the difference.
Problem with this approach that it's possible to go out of memory.
Also, we will have to get all existing IDs outside DB.
For existing DB outside of DB: we can store some data from the previous sync to speed-up this process.
3. Also, we can just delete not updated records by `updated` column.
It's a quite unstable way but maybe it's ok if nothing critical
will happen if we will randomly delete some records (they will
be recreated on next day).

No solution for real life: more info/discussions needed.
