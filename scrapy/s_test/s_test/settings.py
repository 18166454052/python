# -*- coding: utf-8 -*-

# Scrapy settings for s_test project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import pymysql.cursors
BOT_NAME = 's_test'

SPIDER_MODULES = ['s_test.spiders']
NEWSPIDER_MODULE = 's_test.spiders'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 's_test (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)  并发数
#CONCURRENT_REQUESTS = 32  #  1 同步

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    's_test.middlewares.STestSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    's_test.middlewares.STestDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   #'s_test.pipelines.STestPipeline': 300,   #movie_category
   #'s_test.pipelines.MovieListPipeline': 300  # mpvie_item
   #'s_test.pipelines.TvCategoryPipeline': 300,
   #'s_test.pipelines.TvItemPipeline': 300,
   #'s_test.pipelines.TvListPipeline': 300
   #'s_test.pipelines.VarietyCategoryPipeline': 300
   #'s_test.pipelines.VarietyItemPipeline': 300
   #'s_test.pipelines.VarietyListPipeline': 300
   #'s_test.pipelines.CartoonCategoryPipeline': 300
   #'s_test.pipelines.CartoonItemPipeline': 300
    's_test.pipelines.CartoonListPipeline': 300

}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

MYSQL_CONFIG_HOST = '127.0.0.1'
MYSQL_CONFIG_PORT = 3306
MYSQL_CONFIG_DB = 'movie'
MYSQL_CONFIG_USER = 'root'
MYSQL_CONFIG_PASSWORD = 'root'
MYSQL_CONFIG_CHARSET = 'utf8'
MYSQL_CONFIG_USE_UNICODE = True
MYSQL_CONFIG_CURSORCLASS = pymysql.cursors.DictCursor

