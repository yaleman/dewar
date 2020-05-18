# Dewar

A storage place for samples of all kinds. Typically focused around large-scale collection of phishing kits and other email/website artifacts.

The basic plan at the moment is to treat each submitted archive as a "job". There's "known good" jobs and "other" jobs. "Known good" job lots would be something like the Wordpress installer, while "other" would be a backup of a compromised/phishing site. There's likely lots of commonality between them, but the interesting parts are the differences.

[![Build Status](https://droneio.yaleman.org/api/badges/yaleman/dewar/status.svg)](https://droneio.yaleman.org/yaleman/dewar)

If you have *any* kind of suggestion or issue, please [create a github issue](https://github.com/yaleman/dewar/issues/new) - I'll gladly discuss it. Pull requests for features or fixes are even better :)

# Usage

Starting the web interface:

```shell
pipenv install 
pipenv run python -m dewar web
```

Starting the ingestor (not ... really working yet)

```shell
pipenv run python -m dewar ingestor
```


# [See the Documentation for more](https://yaleman.github.io/dewar)
