



#### 分布式使用

- 将爬取的读书网上的数据存储到redis数据库中
- 使用分布式爬取读书网，并且存储到一个redis数据库中




######  爬取的读书网，www.dushu.com

- 使用到的组件  scrapy_redis
  该组件需要安装
  	windows : pip install scrapy_redis    
  	linux : pip3 install scrapy_redis

  ![scrapy_redis原理](http://p693ase25.bkt.clouddn.com/Untitled-1-201833018153.png)

- scrapy和scrapy_redis的不同
      scrapy是一个通用的爬虫框架，但是这个框架不支持分布式
        scrapy_redis是基于redis一些组件，安装了它，就可以实现scrapy的分布式爬取
        分布式爬取问题：
      	（1）url分配问题
      	（2）结果保存问题
        看图形来理解scrapy_redis工作原理

- 下载scrapy_redis组件，学习其中的样本
      https://github.com/rmax/scrapy-redis
        官网实例3个文件：
        dmoz.py : 继承自CrawlSpider，如果不用分布式爬取，只想将数据保存到redis中，就可以使用这个样本
      	执行方式： scrapy crawl 爬虫名
        myspider_redis.py : 继承自RedisSpider, 如果想使用分布式爬取，并且不用链接提取器，就可以使用这个样本
      	执行方式： scrapy runspider myspider_redis.py
        mycrawler_redis.py : 继承自RedisCrawlSpider, 如果想使用分布式爬取，并且使用链接提取器，就可以使用这个样本
      	执行方式： scrapy runspider mycrawler_redis.py
- 存储到redis中
  修改读书网例子配置如下:

```
      	# 使用的redis的去重
      	DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
      	# 使用的是redis的调度器
      	SCHEDULER = "scrapy_redis.scheduler.Scheduler"
      	# 是否可以暂停
      	SCHEDULER_PERSIST = True
      	
      	添加管道
      	'scrapy_redis.pipelines.RedisPipeline': 400,
      	【注】默认就会存储到本机的redis服务器中
```
- 配置分布式爬取
  配置
```
# 使用的redis的去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 使用的是redis的调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 是否可以暂停
SCHEDULER_PERSIST = True

添加管道
'scrapy_redis.pipelines.RedisPipeline': 400,
【注】默认就会存储到本机的redis服务器中
再加一个redis服务器的配置
REDIS_HOST = '10.0.116.232'
REDIS_PORT = 6379
```
- 修改爬虫文件代码
  参考官方提供的模板
  （1）继承自RedisCrawlSpider
  （2）没有start_urls 这个列表了，取而代之的是一个redis_key, 例如：
  redis_key = 'ducrawl:start_urls'
  （3）模板中的__init__这个方法是个坑，不要添加
  （4）将代码拷贝其它电脑上，开始执行，执行命令如下
  scrapy runspider du_fen.py
  （5）执行之后，程序就会卡在那里等待起始url
  （6）通过redis-cli连接redis服务器，向redis服务器中，添加一个队列，向队列中添加一个起始url
  lpush 后面的键就是你代码中的  redis_key
  lpush ducrawl:start_urls https://www.dushu.com/book/1175_1.html















