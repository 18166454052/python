from scrapy import cmdline
import schedule
import time
import subprocess

# #
# def job():
#      subprocess.Popen("scrapy crawl tencent_movie_list_update".split())
#
#
# #schedule.every(10).minutes.do(job)
# schedule.every().day.at("00:00").do(job)
#
# while True:
#      schedule.run_pending()
#
#      time.sleep(24*60*60)
cmdline.execute("scrapy crawl tencent_movie_list_update".split())  # movie_item