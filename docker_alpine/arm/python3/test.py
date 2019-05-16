#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
    >>> python test.py test.mp3
'''

import os, sys
from acrcloud.recognizer import ACRCloudRecognizer

if __name__ == '__main__':
    config = {
        'host':'XXXXXXXX',
        'access_key':'XXXXXXXX',
        'access_secret':'XXXXXXXX',
        'timeout':5
    }
    
    '''This module can recognize ACRCloud by (RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 8000 HZ) file. '''

    re = ACRCloudRecognizer(config)
    buf = open(sys.argv[1], 'rb').read()
    print(re.recognize(buf))
