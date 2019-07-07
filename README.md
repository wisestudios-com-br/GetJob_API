# GetJob_API
Back-end for the GetJob project


## Implementation

### Requirements

* python3
* python-virtualenv
* python-pip
### Install

In your terminal(Linux):

1. Create a VirtualEnv:
```
$ virtualenv GetJob_API/
```
2. Navigate into it:
```
$ cd GetJob_API/
```
3. Activate the env source to your terminal:
```
$ source bin/activate
```
4. Clone the repository:
```
$ git clone https://github.com/wisestudios-com-br/GetJob_API.git
```
5. Navigate into the project folder:
```
$ cd GetJob_API/
```
6. Install the requirements:
```
$ pip install -r requirements.txt
```

### Observation
This project use TAB(not space) of the size 4.

### Usage
In your terminal, and inside the project folder:

1. Navigate to the src folder:
```
$ cd src/
```
2. Start the hug server:
```
$ hug -f app.py
```
Or, in case of production:
```
$ gunicorn app:__hug_wsgi__
```
Or, if you have SLL:
```
$ gunicorn --certfile=server.crt --keyfile=server.key app:__hug_wsgi__
```
