# Django + Gunicorn + Gevent Sample

用Gunicorn + Gevent，把Django应用程序秒变异步运行。

Q：什么场景下适宜使用Gunicorn + Gevent来运行Django程序？

A：在Django的应用里，需要请求外部网络API或较多IO操作的时候，使用Gunicorn和Gevent引擎来运行程序会提高程序的并发能力。典型的使用场景就是Oauth授权过程，如微信公众号中打开网责的微信授权过程。如果用Django加普通的同步引擎，这些请求会一个接一个被执行，而启用异步
模型，则会让这些请求同时执行。

## Demo解读

demo做的事情很简单，读取数据库的书本，挑其中一本书的名字，到百度搜索，代码如下：

`
def random_search(request):
    books = [book for book in Book.objects.all()]
    random.shuffle(books)
    url = 'https://www.baidu.com/s?wd=' + books[0].name
    rsp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'})
    print rsp.status_code
    return HttpResponse(rsp.text)
`

## 运行并测试

### 安装Demo

`
$git clone https://github.com/jeffkit/django-gunicorn-gevent-sample.git
$cd django-gunicorn-gevent-sample
$sudo pip install -r requirements.txt
$python manage.py migrate

`

### 使用Gunicorn运行Demo

`
$gunicorn -w 1 -k gevent usample.wsgi:application
[2016-06-24 12:28:05 +0800] [82169] [INFO] Starting gunicorn 19.6.0
[2016-06-24 12:28:05 +0800] [82169] [INFO] Listening at: http://127.0.0.1:8000 (82169)
[2016-06-24 12:28:05 +0800] [82169] [INFO] Using worker: gevent
[2016-06-24 12:28:05 +0800] [82172] [INFO] Booting worker with pid: 82172

`
参数说明：

- w，启动worker数量，即工作进程数
- k，指定worker的类型，这里使用gevent, 默认为sync （同步）

这里只启动了一条工作进程，该进程使用gevent的引擎来运行。

使用ab来压测一下看结果, 模拟20个并发，一共发送100次请求：

`
ab -n 100 -c 20 http://127.0.0.1:8000/
This is ApacheBench, Version 2.3 <$Revision: 1706008 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient).....done


Server Software:        gunicorn/19.6.0
Server Hostname:        127.0.0.1
Server Port:            8000

Document Path:          /
Document Length:        444630 bytes

Concurrency Level:      20
Time taken for tests:   21.422 seconds
Complete requests:      100
Failed requests:        99
   (Connect: 0, Receive: 0, Length: 99, Exceptions: 0)
Total transferred:      45864885 bytes
HTML transferred:       45847985 bytes
Requests per second:    4.67 [#/sec] (mean)
Time per request:       4284.318 [ms] (mean)
Time per request:       214.216 [ms] (mean, across all concurrent requests)
Transfer rate:          2090.88 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.2      0       1
Processing:   623 4133 3937.2   2748   19206
Waiting:      622 4132 3937.6   2747   19205
Total:        623 4133 3937.3   2748   19206

Percentage of the requests served within a certain time (ms)
  50%   2748
  66%   5166
  75%   6518
  80%   6809
  90%   9465
  95%  13584
  98%  16247
  99%  19206
 100%  19206 (longest request)

`

总完成时间在21.422秒，视乎服务器的网络状况，如果网络较理想，可能几秒内就可以完成。

如果把运行引擎改回同步模式，再做一下对比：

`
$gunicorn -w 1 -k sync usample.wsgi:application
[2016-06-24 12:34:54 +0800] [82205] [INFO] Starting gunicorn 19.6.0
[2016-06-24 12:34:54 +0800] [82205] [INFO] Listening at: http://127.0.0.1:8000 (82205)
[2016-06-24 12:34:54 +0800] [82205] [INFO] Using worker: sync
[2016-06-24 12:34:54 +0800] [82208] [INFO] Booting worker with pid: 82208
`

使用同样的命令来做一次压测：

`
ab -n 100 -c 20 http://127.0.0.1:8000/
This is ApacheBench, Version 2.3 <$Revision: 1706008 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient).....done


Server Software:        gunicorn/19.6.0
Server Hostname:        127.0.0.1
Server Port:            8000

Document Path:          /
Document Length:        464605 bytes

Concurrency Level:      20
Time taken for tests:   101.121 seconds
Complete requests:      100
Failed requests:        99
   (Connect: 0, Receive: 0, Length: 99, Exceptions: 0)
Total transferred:      45818112 bytes
HTML transferred:       45801212 bytes
Requests per second:    0.99 [#/sec] (mean)
Time per request:       20224.171 [ms] (mean)
Time per request:       1011.209 [ms] (mean, across all concurrent requests)
Transfer rate:          442.48 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.2      0       1
Processing:  1295 18519 4906.0  20272   22015
Waiting:     1294 18519 4906.0  20271   22014
Total:       1295 18519 4905.9  20272   22015

Percentage of the requests served within a certain time (ms)
  50%  20272
  66%  20782
  75%  21011
  80%  21064
  90%  21309
  95%  21730
  98%  21844
  99%  22015
 100%  22015 (longest request)
`

总响应时间101秒，差距巨大。


Gunicorn + Gevent的部署方式，可以让Django程序在不做任何修改的情况下，享受异步IO带来的便利。可以让业务逻辑用同步的思维编码，而实际运行却得到异步的效果。
