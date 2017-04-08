## Init Environment

## Open Routing Table
```
sudo iptables -A PREROUTING -t nat -i eth0 -p tcp --dport 90 -j REDIRECT --to-port 9092
sudo iptables -A INPUT -p tcp -m tcp --sport 90 -j ACCEPT
sudo iptables -A OUTPUT -p tcp -m tcp --dport 90 -j ACCEPT
```

## KAFKA Allocate memory
```
export KAFKA_HEAP_OPTS="-Xmx256M -Xms128M"
```

## Problem No Node found
[Click here](https://github.com/dpkp/kafka-python/issues/938)
