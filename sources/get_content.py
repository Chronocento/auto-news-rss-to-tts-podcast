import feedparser
import ssl
from datetime import date,datetime
from bs4 import BeautifulSoup
import requests
import json
import re
import html

class Get(object):
    def __init__(self, sources_list, max_number=10):
        #Obtaining SSL certificate
        if hasattr(ssl, '_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context
        self.max_number = max_number
        self.news_text = ""
        self.sources_list = sources_list
        self.separator = {'it': ". Notizia ", 'en-us': ". News "}
        self.data_dict = {}

    def extract_text(self):
        for i in range(len(self.sources_list)):
            if ('http' in self.sources_list[i]):
                self.data_dict[i] = self.__general_content__(self.sources_list[i])
            '''
            if self.sources_list[i] == "gazzetta_del_sud":
                data_dict['gazzetta_del_sud'] = self.gazzetta_del_sud()
            elif self.sources_list[i] == "la_repubblica":
                data_dict['la_repubblica'] = self.la_repubblica()
            elif self.sources_list[i] == "il_fatto_quotidiano":
                data_dict['il_fatto_quotidiano'] = self.il_fatto_quotidiano()
            '''
    
    def extract_video(self):
        for i in range(len(self.sources_list)):
            if self.sources_list[i] == "gazzetta_del_sud":
                self.data_dict[i] = self.gazzetta_del_sud()

    def clean_html(self,raw_html):
        clean_r = re.compile('<.*?>')
        #clean_r = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        raw_html = raw_html.replace('<p>',"").replace('</p>',"\n")
        clean_text = re.sub(clean_r, '', raw_html)
        return clean_text

    def gazzetta_del_sud(self):
        link = "https://feedpress.me/gsud_hp_messina"

        news_feed = feedparser.parse(link)
        #print (news_feed.entries[1])

        #Getting the link to today page
        page_link = ""

        today = date.today()
        format = "%d-%m-%Y"
        today = today.strftime(format)
        #today = "16-01-2021"
        match = "Rassegna stampa " + today #+ " edizione Messina"
        
        for entry in news_feed.entries:
            if (match.lower() in entry['title'].lower()):
                page_link = entry['link']
                #print(entry['title'])

        if page_link == "":
            return dict(title = "", video_url = "", news_text = "", language = "") #Niente rassegna stampa la domenica...
        else:
            #Scraping the page to obtain the video url
            #Example: "https://gsud.cdn-immedia.net/video-repository/rassegna-messina-13-01-21-6855519760.mp4"
            rawdata = requests.get(page_link)
            html = rawdata.content

            soup = BeautifulSoup(html, "html.parser")
            #print(soup.title.text)
            output = str(soup.head.script).split('<script type="application/ld+json">')[1].split('</script>')[0]
            output_dict = json.loads(output)
            
            return dict(title = soup.title.text, video_url = output_dict['video']['contentUrl'], news_text = "", links = [output_dict['video']['contentUrl']], language = "it")
    
    def __general_content__(self,url):
        #current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")
        current_datetime = datetime.now().strftime("%Y-%m-%d")

        news_feed = feedparser.parse(url)
        news_text = news_feed.feed.title
        language = news_feed.feed.language.split('-')[0] #it-IT -> it
        if language == "en":
            language += "-us"
        
        links_list = []

        for i in range(self.max_number):
            entry = news_feed.entries[i]
            links_list.append(entry['link'])
            if entry.get('description'):
                news_text += self.separator[language] + str(i+1) + ". "
                news_text += entry['title']
                news_text += ". "

                text = entry['description']
                text = html.unescape(text).replace('\n','')
                text = self.clean_html(text)
                text = text.split('\n')
                for j in range(len(text)):
                    if (entry['title'] in html.unescape(text[j])):
                        pass
                    else:
                        news_text += html.unescape(text[j])
            else:
                news_text += self.separator[language] + str(i+1) + ". "
                news_text += entry['title']

        return dict(title = news_feed.feed.title + " " + current_datetime, video_url = "", news_text = news_text, links = links_list, language = language)