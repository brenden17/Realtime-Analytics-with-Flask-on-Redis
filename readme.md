# Realtime Analytics with redis on Flask

This is Flask extension which implements real-time and scalable analytics based on Redis 

## Requirements

* Redis server
* Python library
~~~
pip install flask-session
pip install redis
~~~
* Javascript library for graph
 * http://dimplejs.org/
 
## How to use
Just put snippet on page. Put event in request, Select events and Graph such as bar, pie.

~~~
{{ bitmap_analytics(['test', 'view', 'buy'], graph='pie') }}
{{ bitmap_analytics(['view', 'buy']) }}
~~~

![alt text](https://github.com/brenden17/Realtime-Analytics-with-Flask-on-Redis/blob/master/img/analysis.png "image")


That's all.