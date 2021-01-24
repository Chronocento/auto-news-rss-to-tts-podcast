# AutoNews - RSS to TTS podcast
Automatically converts text RSS news feeds into audio files through TTS engines; from them it creates a podcast RSS feed that can be imported (through its integrated web server) into any podcast app!

## Features
Add your news RSS feeds to its configuration file: AutoNews (temporary name?) will convert the latest n news to audio files.
At the end of the RSS to TTS conversion, it creates a podcast RSS file that it is served, through its integrated, byte-range requests compliant web server, to any podcast app of your choice: to do so, you must specify a domain in the configuration (e.g., DuckDNS), and open a port on your router.
