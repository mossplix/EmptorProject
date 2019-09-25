# Emptor Test Project

[![Build Status](https://travis-ci.com/mossplix/EmptorProject.svg?branch=master)](https://travis-ci.com/mossplix/EmptorProject)
[![Coverage Status](https://coveralls.io/repos/github/mossplix/EmptorProject/badge.svg?branch=master)](https://coveralls.io/github/mossplix//EmptorProject?branch=master)

# install

```
pip install -r requirements.txt
npm install
serverless deploy

```

# config

make sure you have the environment variables s3_bucket,dynamo_table are set

```
export s3_bucket="your_bucket_name"

export dynamo_table="your table name"
```

# first version

https://github.com/mossplix/EmptorProject/tree/firstVersion

# second version

https://github.com/mossplix/EmptorProject/tree/secondVersion

# running

```
serverless invoke -f handle_url  -d 'https://github.com' -l
```

# Tests

You can run the tests from the root of the project with:

```
pytest --flake8 tests
```
