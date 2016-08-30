'''
Youtube video audio stream for DiscordBot
'''

#coding utf-8

import pafy as _pafy

class AudioStream:
    def __init__ (self, url):
        self.url = url
        self.vid = _pafy.new(url)
        
        self.audio = self.vid.getbestaudio()
        
        if self.audio == None:
            raise ValueError('Invalid url')