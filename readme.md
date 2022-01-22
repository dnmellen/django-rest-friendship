# django-rest-friendship

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/sflems/django-rest-framework?label=version)](https://github.com/sflems/django-rest-framework/releases) [![Django Tests](https://github.com/sflems/django-rest-friendship/actions/workflows/python-package.yml/badge.svg)](https://github.com/sflems/django-rest-friendship/actions/workflows/python-package.yml)

## Overview

An updated fork of [`django-rest-friendship`](https://github.com/dnmellen/django-rest-friendship) to create DRF endpoints for django-friendship

## Requirements

* Python (3.8, 3.9, 3.10)
* Django (4.0)
* Django REST Framework (3.13)

## Installation

Install using `pip`...

```bash
pip install django-rest-friendship
```

Add rest_friendship to your `INSTALLED_APPS`

```python

    INSTALLED_APPS = (
    ...
    'friendship',  # Django friendship
    'rest_framework',  # Django REST Framework
    'rest_friendship',  # Django REST Friendship
    'rest_framework.authtoken',
    ...
    )
```

Also add settings for `REST_FRIENDSHIP`

```python
    REST_FRIENDSHIP = {
        'PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'USER_SERIALIZER': 'rest_friendship.serializers.FriendSerializer',
    },

```

And don't forget to add the following to your project `urls.py`

```python
    urlpatterns = [
        ...
        path('', include('rest_friendship.urls')),
        ...
    ]
    
```

## Examples

#### Get Friends List

```bash
curl -LX GET http://127.0.0.1:8000/friends/ -H 'Authorization: Token 16bd63ca6655a5fe8d25d7c8bb1b42605c77088b' 

[{"id":1,"username":"testuser","email":"testuser@piboy.ca"}]
```

#### Add/Remove Friends

```bash
curl -X POST http://127.0.0.1:8000/friends/add_friend/ -H 'Authorization: Token 16bd63ca6655a5fe8d25d7c8bb1b42605c77088b' --data 'to_user=testuser&message=Hello+friend'

{"id":4,"from_user":"scott@gmail.com","to_user":"testuser@piboy.ca","message":"Hello friend","created":"2022-01-22T04:21:43.593950Z","rejected":null,"viewed":null} 
```

```bash
curl -X POST http://127.0.0.1:8000/friends/remove_friend/ -H 'Authorization: Token 16bd63ca6655a5fe8d25d7c8bb1b42605c77088b' --data 'to_userFri=testuser'

[{"message": "Friend deleted"}]
```

#### Accept a Request with request ID

```bash
curl -X POST http://127.0.0.1:8000/friends/accept_request/ -H 'Authorization: Token 16bd63ca6655a5fe8d25d7c8bb1b42605c77088b' --data 'id=1'

{"message": "Request accepted, user added to friends."}
```

## Testing

Install testing requirements.

```bash
pip install -r requirements.txt
```

Run with runtests.

```bash
./runtests.py
```

You can also use the excellent [tox](http://tox.readthedocs.org/en/latest/) testing tool to run the tests against all supported versions of Python and Django. Install tox globally, and then simply run:

```bash
tox
```

## Documentation

To build the documentation, you'll need to install `mkdocs`.

```bash
pip install mkdocs
```

To preview the documentation:

```bash
$ mkdocs serve
Running at: http://127.0.0.1:8000/
```

To build the documentation:

```bash
mkdocs build
```
