# Kazi

This is an informal (blue collar) job matching service that runs on SMS
powered by AfricasTalking.

### Features

- Register Jobseekers
- Register Employers
- Post jobs
- Get available jobs notification
- Apply to jobs

## Run

Set up a local postgres database called `kazi`

Create and activate a virtual environment in the project root directory

```commandline
virtualenv venv

source venv/bin/activate
```

Install dependencies

```commandline
pip install -r requiurements.txt
```

Run migrations:

```commandline
alembic upgrade head
```

Be sure to have installed redis and have it running on your localhost.

Additionally, you should have the following variables in your .env

```
AT_USERNAME=YOUR_AT_USERNAME
AT_API_KEY=YOUR_AT_API_KEY

```

AfricasTalking requires that the service sends back a 200 response for
every received message for them to stop resending it to our callback url.

Kazi therefore immediately returns a 200 response to africastalking each
time a message is received then processes it asynchronously with the help of
celery, with redis as the broker.
For this reason to run this service you will have to run

```commandline
    python run.py
```

on one terminal.
Then

```commandline
    celery -A run.celery worker --loglevel=info
```

on a second terminal

### Setting Up AfricasTalking Callback URL

https://help.africastalking.com/en/articles/2206161-how-do-i-configure-my-callback-url

### wtf is this async BS? I just want to test sending and receiving SMS with AT apis

Worry not. Just reset head to
this [commit](https://github.com/owuor91/kazi/commit/bb8e3690eb57d057d03d277e3257ef0c6fb80661),
and you're good to go

```commandline
git reset --hard bb8e3690eb57d057d03d277e3257ef0c6fb80661
```