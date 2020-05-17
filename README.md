# Dewar

[![Build Status](https://droneio.yaleman.org/api/badges/yaleman/dewar/status.svg)](https://droneio.yaleman.org/yaleman/dewar)

A storage place for samples of all kinds. Typically focused around large-scale collection of phishing kits and other email/website artifacts.

The basic plan at the moment is to treat each submitted archive as a "job". There's "known good" jobs and "other" jobs. "Known good" job lots would be something like the Wordpress installer, while "other" would be a backup of a compromised/phishing site. There's likely lots of commonality between them, but the interesting parts are the differences.

- here are the main "element types"
  - file
    - the file reference is *always* the sha256 hash of the file
  - job - a collection of files that group together. typically encapsulated in an archive file as you ingest it
  - bucket - a place where files are stored or ingested from (ie, storage, incoming-knowngood)
    - This should be a simple string reference, so storage backends can implement the `dir()` function and return a list of files regardless of the method of storage.
  - other (ie, processing results)?


- File metadata should be
  - hash (the unique file ID)
  - known-good status
  - size - allows for bucketing when finding similar-sized PHP files for example <+- Decide if this is a thing?
  - MIME type by say.. unix `file` or another method? <+- maybe? 
- Job Metadata should include:
  - timestamp (typically when submitted, or when sample was collected)
  - the relative file structure as a tree of filenames and their associated hashes
  - the original job name
  - known good or not
  - notes
  - submitter (username/email address)
- store each file only once, identified by its sha256 hash
  - compression or optimisation is up to the storage backend
- simple tokenisation could help find uncommon code structures or things that'd lead to IOCs or allow for tracking over time

Various bits to build

1. ingestion methods:
  - watch a directory (a "known good" and an "other" dirs)
  - have a simple API for submitting files
2. ingestion pipeline
  - simple single threaded passthru
  - pubsub queue with multiple nodes
3. storage backends
  - backends
    - [ ] s3
    - [ ] local filesystem
  - methods that storage backends should support (inspired by http verbs)
    - get (contents and metadata)
    - put (contents and metadata)
    - update (update metadata)
    - head (check a file exists and reutrn metadata, or false if doesn't exist)
    - delete
    - search (by metadata, or maybe file contents?)
    - dir (list contents of a Bucket)
4. metadata storage
  - backends
    - [ ] tinydb
    - [ ] postgresql
    - [ ] flat json files ?
  - methods in the metadata stores
    - get (by hash)
    - put (hash, metadata)
    - delete (by hash)
5. processing of samples
  - image normalisation? (phistOfFury?)
  - ssdeep?
  - hilariously simple tokenization
  - extraction of IOCs like urls, emails, IP addresses etc.
  - words/phrases etc
6. processing pipelines
  - single job queue, processing tasks
  - pubsub multithreaded clustered hilarity
7. Data interaction
  - [ ] website frontend for .. 
    - [x] seeing the incoming file bucket contents
    - [ ] manually processing incoming jobs - in case you want to insert notes as you do it etc
    - [ ] see the list of historical jobs
    - [ ] edit job data (typically only notes?)
    - [ ] upload jobs
  - [ ] HTTP API
    - [ ] shoving files into the job buckets
    - [ ] submitting jobs
    - [ ] querying job data?
    - [ ] querying hashes
      - [ ] have we seen this
      - [ ] extended - which jobs was this seen in, for correlation
8. AAA...
  - [x] is scary bizness
  - [ ] flask basic http on frontends


# Starting a new backend implementation

An example would be a `Storage` backend. The "base" template is `dewar.storage.Storage` and `Storage` backends should always be imported as `from dewar.storage.<backend> import Storage` so they can be consistently used. The S3 implementation then is `from dewar.storage.s3 import Storage`.

# Configuration

Put local configuration things in `config_local.py`. For example you can set things like your environment variables if you're like me and use weird S3 things.

```python
import os
os.environ['AWS_SECRET_KEY_ID'] = "<snip>"
os.environ['AWS_SECRET_ACCESS_KEY'] = "<snip>"
os.environ['S3_ENDPOINT_URL'] = 'http://minio.example.internal:9001'
```