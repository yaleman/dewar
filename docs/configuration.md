---
layout: page
title: Configuration
permalink: /configuration
---

# Configuration

Put local configuration things in `config_local.py`. For example you can set things like your environment variables if you're like me and use weird S3 things.

```python
import os
os.environ['AWS_SECRET_KEY_ID'] = "<snip>"
os.environ['AWS_SECRET_ACCESS_KEY'] = "<snip>"
os.environ['S3_ENDPOINT_URL'] = 'http://minio.example.internal:9001'
```

