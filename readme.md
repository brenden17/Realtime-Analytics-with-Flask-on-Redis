# Real Analytics with redis on Flask

This is Flask extension which implements real-time and scalable analytics based on Redis 

## Reqirements

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

That's all.