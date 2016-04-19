#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
    >>> python test.py test.mp3
'''

import os, sys
from acrcloud.recognizer import ACRCloudRecognizer

if __name__ == '__main__':
    config = {
        'host':'ap-southeast-1.api.acrcloud.com',
        'access_key':'XXXXXXXX',
        'access_secret':'XXXXXXXX',
        'debug':False,
        'timeout':10 # seconds
    }
    
    '''This module can recognize ACRCloud by most of audio/video file. 
        Audio: mp3, wav, m4a, flac, aac, amr, ape, ogg ...
        Video: mp4, mkv, wmv, flv, ts, avi ...'''
    re = ACRCloudRecognizer(config)

    #recognize by file path, and skip 180 seconds from from the beginning of sys.argv[1].
    print re.recognize_by_file(sys.argv[1], 0)

    buf = open(sys.argv[1], 'rb').read()
    #recognize by file_audio_buffer that read from file path, and skip 180 seconds from from the beginning of sys.argv[1].
    print re.recognize_by_filebuffer(buf, 0)

    #aa.wav must be (RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 8000 Hz)
    #buf = open('aa.wav', 'rb').read()
    #buft = buf[1024000:192000+1024001]
    #recognize by audio_buffer(RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 8000 Hz)
    #print re.recognize(buft)

