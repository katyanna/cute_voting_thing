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
$ chmod a+x musics.py
$ python musics.py
$ curl -i http://localhost:5000/musics
$ curl -i http://localhost:5000/musics/1
$ curl -i -H "Content-Type: application/json" -X POST -d '{"artist":"artist_name"}' http://localhost:5000/musics
$ curl -i -H "Content-Type: application/json" -X PUT -d '{"title":"music_title"}' http://localhost:5000/musics/1
$ curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/musics/1
```
