# Dewar

A storage place for samples of all kinds. Typically focused around large-scale collection of phishing kits and other email/website artifacts.

The basic plan at the moment is to treat each submitted archive as a "job". There's "known good" jobs and "other" jobs. "Known good" job lots would be something like the Wordpress installer, while "other" would be a backup of a compromised/phishing site. There's likely lots of commonality between them, but the interesting parts are the differences.

- three main "elements"
  - file
  - job (a collection of files)
  - other (ie, processing results)
- File metadata should be
  - hash (the unique file ID)
  - size - allows for bucketing when finding similar-sized PHP files for example
  - MIME type by say.. unix `file` or another method?
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
3. raw storage
  - s3
  - local filesystem
4. metadata storage
  - tinydb
  - postgresql
  - flat files
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
  - website/API for queries or extracting information