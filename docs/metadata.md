layout: page
title: "Metadata"
permalink: /metadata/


# `File` metadata

| field | type | description |
| --- | --- | --- |
| hash | string(64) | the unique file ID - a sha256sum of the contents |
| known-good | boolean | flag |
| size | int | file size - allows for bucketing when finding similar-sized PHP files for example |
| type | string | MIME type by say.. unix `file` or another method... maybe? | 

# `Job` metadata

| field  | type | description  |
| ---    | --- | --- |
| guid | string | a GUID generated from `dewar.utilities.generate_job_id()` - 36 character string |
| timestamp | int | Typically when submitted, or when sample was collected. User set or defaults to `time.now()` |
| name | string | a descriptive name for the job |
| notes | string | user-entered notes relating to the job |
| known_good | boolean | known good or not |
| submitter | string | Username/email address of the user who submitted the job |

## Example object

```
jobdata = {
    'id' : generate_job_id(),
    'timestamp' : 1589789866,
    'name' : '2020-05-23-thisisreallysilly.tar.gz',
    'source_bucket' : 'known_good',
    'known_good' : True,
}
```

# `Jobfile` metadata

| field   | type | description | example | 
| ---     | --- | --- | --- |
| hash | str / fkey | foreign key link to `File`, refers to the file hash entry in the metadata store | | 
| relpath | str | relative path within the job | `/public_html/index.html` or `/home/foo/.cache/foo.txt` |
| job | str / fkey | foreign key link to the job metadata - foreign key or guid | | 
