import os
import threading
import time
import toml
import logging
from sources import get_content
from conversion import audio
from rss import create_rss
from webserver import server

logging.basicConfig(level = "DEBUG")

def main():
    #General data
    toml_path = "config.toml"
    configuration = toml.load(toml_path)

    #If media directory doesn't exists, create it
    if os.path.isdir(configuration['system']['media_folder']) == False:
        os.mkdir(configuration['system']['media_folder'])

    #Periodically retrieve news and convert to audio files
    timed_execution(int(configuration['system']['interval']),configuration)

    #Change webserver target directory
    web_dir = os.path.join(os.path.dirname(__file__), configuration['system']['media_folder'])
    os.chdir(web_dir)

    #Start webserver, stop it with ctrl+c
    server.Serve(int(configuration['network']['port']))

def podcast_flow(configuration):
    #Obtaining video links
    data = get_content.Get(configuration['sources']['list'],configuration['system']['max_articles'])

    data.extract_text()
    data.extract_video()
    #logging.debug(data.data_dict)

    #Converting extracted data to audio
    audio_content = audio.Convert(configuration['system']['extension'],configuration['system']['media_folder'])
    speed = 1.15
    for i in range(len(configuration['sources']['list'])):
        logging.debug(data.data_dict[i]['title'])
        if (data.data_dict[i]['video_url'] != ""):
            audio_content.video(data.data_dict[i]['video_url'], data.data_dict[i]['title'])
        else:
            audio_content.tts(data.data_dict[i]['news_text'], data.data_dict[i]['title'], 
            data.data_dict[i]['language'], speed)

    #Create RSS feed
    create_rss.RSS(configuration).generate()

def timed_execution(interval,configuration):
    podcast_flow(configuration)
    threading.Timer(interval, timed_execution,args=(interval,configuration,)).start()

if __name__ == "__main__":
    main()