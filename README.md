# PyRedis

In memory database. This is a lightweight, innefficient implementation of Redis software written in python. This implementation is not meant to be efficient, it is for fun.


# Requirements

- Docker
- Telnet

# Options

|  Option | Full name | Description | Required | Default value
|---|--- | --- | ---|--- |
| -p | --port | Port which PyRedis will listen | Yes 
| -s | --save | Enable persistence | No | Not activated
| -t | --time |  time rate between backups | No | 60s
| -v | --verbose | Include debug directives | No | Not activated



# Running
You can also use the makefile.

```
cd pyredis
docker build -t pyredis .
docker run -it -p 8080:8080 pyredis
```

Be sure you change **Dockerfile** taking into consideration the previous table. This is just an example.


# Connecting

```
# Use any TCP client
telnet localhost 8080
```


# Changing default port

Head over to **Dockerfile**, and change **EXPOSE** and **CMD** parameters as shown.

```
...
# Change this to correspond with last CMD parameter
EXPOSE port_number

# Change last option for setting default port
CMD [ "python3", "main.py", "-p" , "port_number"] 

```

# Changing code

You need to remove the image and create it again every time you want to add a new feature to the container. You can change de **COPY** directive and change it to a volume. That way you will not need to restart anything. Don't forget to update the makefile in case you are using it.

# Running tests

```
make test
```

or 

```
pytest -v
```
