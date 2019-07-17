from lxml import etree
import requests
import pandas as pd

label_list = []
def category():
    header = {
        'User-Agent':'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
    }
    url = 'https://v.qq.com/channel/movie?listpage=1&channel=movie&sort=18&_all=1'
    res = requests.get(url, headers=header).text
    res1 = etree.HTML(res)
    mode_list = res1.xpath('//div[@class="mod_list_filter"]//div[contains(@class,"filter_line")]')
    for mode in mode_list:
         filter_label = mode.xpath("//span[@class='filter_label']/text()")
         label_list.append(filter_label)

    print(mode_list)



if __name__=="__main__":
    category()
    df = pd.DataFrame(label_list)
    df.to_excel("label.xlsx")