from bs4 import BeautifulSoup
import re
import json
import time
import datetime
import requests


headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}


class Crawler:
    def __init__(self):
        self.session = requests.session()
        self.session.headers.update(headers)
        self.crawl_timestamp = int()

    def run(self):
        while True:
            self.crawler()
            time.sleep(60)

    def crawler(self):
        while True:
            self.crawl_timestamp = int(datetime.datetime.timestamp(datetime.datetime.now()) * 1000)
            try:
                r = self.session.get(url='https://3g.dxy.cn/newh5/view/pneumonia')
            except requests.exceptions.ChunkedEncodingError:
                continue
            soup = BeautifulSoup(r.content, 'lxml')

            overall_information = re.search(r'\{("id".*?)\}',
                                            str(soup.find('script', attrs={'id': 'getStatisticsService'})))
            province_information = re.search(r'\[(.*?)\]',
                                             str(soup.find('script', attrs={'id': 'getListByCountryTypeService1'})))
            area_information = re.search(r'\[(.*)\]', str(soup.find('script', attrs={'id': 'getAreaStat'})))
            abroad_information = re.search(r'\[(.*)\]',
                                           str(soup.find('script', attrs={'id': 'getListByCountryTypeService2'})))
            news = re.search(r'\[(.*?)\]', str(soup.find('script', attrs={'id': 'getTimelineService'})))

            if not overall_information or not province_information or not area_information or not news:
                continue

            self.overall_parser(overall_information=overall_information)
            self.province_parser(province_information=province_information)
            self.area_parser(area_information=area_information)
            self.abroad_parser(abroad_information=abroad_information)
            self.news_parser(news=news)

            break

        while True:
            self.crawl_timestamp = int(datetime.datetime.timestamp(datetime.datetime.now()) * 1000)
            try:
                r = self.session.get(url='https://file1.dxycdn.com/2020/0127/797/3393185293879908067-115.json')
            except requests.exceptions.ChunkedEncodingError:
                continue
            # Use try-except to ensure the .json() method will not raise exception.
            try:
                if r.status_code != 200:
                    continue
                elif r.json().get('code') == 'success':
                    self.rumor_parser(rumors=r.json().get('data'))
                    break
                else:
                    continue
            except json.decoder.JSONDecodeError:
                continue


    def overall_parser(self, overall_information):
        overall_information = json.loads(overall_information.group(0))
        overall_information.pop('id')
        overall_information.pop('createTime')
        overall_information.pop('modifyTime')
        overall_information.pop('imgUrl')
        overall_information.pop('deleted')
        overall_information['countRemark'] = overall_information['countRemark'].replace(' 疑似', '，疑似').replace(' 治愈',
                                                                                                              '，治愈').replace(
            ' 死亡', '，死亡').replace(' ', '')
        print(overall_information)

    def province_parser(self, province_information):
        provinces = json.loads(province_information.group(0))
        print(provinces)
        for province in provinces:
            province.pop('id')
            province.pop('tags')
            province.pop('sort')
            province['comment'] = province['comment'].replace(' ', '')
            province['crawlTime'] = self.crawl_timestamp
            country_type = {
                1: '中国'
            }
            province['country'] = country_type.get(province['countryType'])

            print(province)
            print("========")


    def area_parser(self, area_information):
        area_information = json.loads(area_information.group(0))

        for area in area_information:
            area['comment'] = area['comment'].replace(' ', '')
        print(area_information)



    def abroad_parser(self, abroad_information):
        countries = json.loads(abroad_information.group(0))
        for country in countries:
            country.pop('id')
            country.pop('tags')
            country.pop('countryType')
            country.pop('provinceId')
            country['country'] = country.get('provinceName')
            country['provinceShortName'] = country.get('provinceName')
            country.pop('cityName')
            country.pop('sort')

            country['comment'] = country['comment'].replace(' ', '')


    def news_parser(self, news):
        news = json.loads(news.group(0))
        for _news in news:
            _news.pop('pubDateStr')

            _news['crawlTime'] = self.crawl_timestamp


    def rumor_parser(self, rumors):
        for rumor in rumors:
            rumor.pop('score')
            rumor['body'] = rumor['body'].replace(' ', '')



if __name__ == '__main__':
    crawler = Crawler()
    crawler.run()
