from feedgen.feed import FeedGenerator
from datetime import datetime,timezone,timedelta
import pathlib
import os

class RSS(object):
    def __init__(self,configuration):
        #self.data_dict = data_dict
        self.configuration = configuration

    def generate(self):
        url = self.configuration['network']['host'] + ":" + str(self.configuration['network']['port'])

        #Creating RSS feed
        fg = FeedGenerator()
        fg.load_extension('podcast')
        fg.title(self.configuration['rss']['title'])
        fg.author(dict(name=self.configuration['rss']['author'],email=self.configuration['rss']['email']))
        fg.logo(url + "/" + self.configuration['rss']['logo'])
        fg.description(self.configuration['rss']['description'])
        #fg.subtitle(self.configuration['settings']['subtitle'])
        fg.link(href=url + "/" + self.configuration['rss']['file_name'], rel='self')
        fg.language(self.configuration['rss']['language'])

        for file_name in os.listdir(self.configuration['system']['media_folder']):
            if file_name[0] != "." and file_name != self.configuration['rss']['file_name'] and file_name[-3:] != "jpg": #Skip hidden files and RSS file itself
                #for i in range(len(self.data_dict)):
                    #if (self.data_dict[i]['title'] == file_name[:-4]):
                fe = fg.add_entry()
                #fe.id((url + "/" + self.configuration['system']['media_folder'] + "/" + file_name).replace(" ", "%20"))
                fe.id((url + "/" + file_name).replace(" ", "%20"))
                fe.title(file_name[:-4])
                #fe.description("\n".join(self.data_dict[i]['links']))
                fe.description(file_name[:-4])
                #Get time and date of file modification, add timezone
                offset = timezone(timedelta(hours=1))
                pub_date = datetime.fromtimestamp(pathlib.Path(self.configuration['system']['media_folder'] + "/" + file_name).stat().st_mtime,tz=offset)
                fe.pubDate(pub_date)
                #file_size = os.path.getsize(self.configuration['system']['media_folder'] + "/" + file_name)
                fe.enclosure((url + "/" + file_name).replace(" ", "%20"), 0, 'audio/mpeg')

        fg.rss_str(pretty=True)
        fg.rss_file(self.configuration['system']['media_folder'] + "/" + self.configuration['rss']['file_name'])

        return True
