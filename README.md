# AutoNews - RSS to TTS podcast
Automatically converts text RSS news feeds into audio files through TTS engines; from them it creates a podcast RSS feed that can be imported (through its integrated web server) into any podcast app!

## Features
Add your news RSS feeds to its configuration file: AutoNews (*temporary name?*) will convert the latest n news to audio files.
At the end of the RSS to TTS conversion, it creates a podcast RSS file that it is served, through its integrated, byte-range requests compliant web server, to any podcast app of your choice: to do so, you must specify a domain in the configuration (e.g., DuckDNS), and open a port on your router.

## Configuration
At the moment, the file *configuration.toml* must be edited to add new RSS news links, data about the generated podcast RSS feed, target folder to save audio files and podcast RSS feed, and network configuration (dynamic DNS address, port, etc.).

## Dependencies
AutoNews relies on these libraries:
* [pyttsx3](https://github.com/nateshmbhat/pyttsx3 "pyttsx3"), to locally convert text-to-speech, using OS integrated voices;
* [gTTS](https://github.com/pndurette/gTTS "gTTS"), uses Google Translate TTS engine to converts text-to-speech;
* [Pydub](https://github.com/jiaaro/pydub/ "Pydub"), to compress pyttsx3-generated audio files and to accelerate gTTS audio files (plus other stuff);
* [MoviePy](https://zulko.github.io/moviepy/ "MoviePy"), to extract audio from video files (whose links are scraped through [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/ "Beautiful Soup"), atm only one source is integrated, *Rassegna stampa della Gazzetta del Sud*);
* [feedparser](https://github.com/kurtmckee/feedparser "feedparser"), to parse RSS news feeds and extract title, summary, link and language of the news;
* [Feedgenerator](https://github.com/lkiesow/python-feedgen "Feedgenerator"), to compile a new RSS feed containing the podcast/audio files links;
* [RangeHTTPServer](https://github.com/danvk/RangeHTTPServer "RangeHTTPServer"), to allow byte-range support to the integrated webserver.

The generated podcast RSS feed and server is (*mostly*) compliant to the iTunes podcast RSS standard (check your generated feed [here](https://podba.se/validate/ "podbase pb")).

