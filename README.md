# simple MQ implementation

consumes given message by flask via rabbitmq,
then consumes given messages from mq and calculates,
then writes on mongo,
after all you can read from mongo by flask

## to Deploy

after costumize deploy.sh:
```
./deploy.sh
```

## to Test
single:
```
curl -H "Content-Type: application/json" -X POST -d "{\"number\": <any integer number>}" http://localhost:5000/calculate
```

multiple:
```
for i in `seq 1 10000` ; do curl -H "Content-Type: application/json" -X POST -d "{\"number\": $i}" http://localhost:5000/calculate; done
```


#to See Results

```
localhost:5000/results
localhost:5000/results/<number>
```

## to use RabbitMQ Console

```
localhost:15672
```