# cute voting thing
A poll.

## Setup
```
$ git clone git@github.com:katyanna/cute_voting_thing.git
$ cd cute_voting_thing
$ pip install -r requirements.txt
```

## Usage
```
$ chmod a+x contestants.py
$ ./contestants.py
$ curl -i http://localhost:5000/contestants
$ curl -i http://localhost:5000/contestants/1
$ curl -i -H "Content-Type: application/json" -X POST -d '{"mc":"mc_name"}' http://localhost:5000/contestants
$ curl -i -H "Content-Type: application/json" -X PUT -d '{"music":"music_title"}' http://localhost:5000/contestants/1
$ curl -i -H "Content-Type: application/json" -X DELETE -d http://localhost:5000/contestants/1
```

