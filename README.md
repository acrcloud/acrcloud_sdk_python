# Audio Recognition Python SDK

## Overview
  [ACRCloud](https://www.acrcloud.com/) provides services such as **[Music Recognition](https://www.acrcloud.com/music-recognition)**, **[Broadcast Monitoring](https://www.acrcloud.com/broadcast-monitoring/)**, **[Custom Audio Recognition](https://www.acrcloud.com/second-screen-synchronization%e2%80%8b/)**, **[Copyright Compliance & Data Deduplication](https://www.acrcloud.com/copyright-compliance-data-deduplication/)**, **[Live Channel Detection](https://www.acrcloud.com/live-channel-detection/)**, and **[Offline Recognition](https://www.acrcloud.com/offline-recognition/)** etc.<br>

  This **audio recognition python SDK** support most of audio / video files. 

>>Audio: mp3, wav, m4a, flac, aac, amr, ape, ogg ...<br>
>>Video: mp4, mkv, wmv, flv, ts, avi ...

## Requirements
Follow one of the tutorials to create a project and get your host, access_key and access_secret.

 * [Recognize Music](https://docs.acrcloud.com/tutorials/recognize-music)
 * [Recognize Custom Content](https://docs.acrcloud.com/tutorials/recognize-custom-content)
 * [Broadcast Monitoring for Music](https://docs.acrcloud.com/tutorials/broadcast-monitoring-for-music)
 * [Broadcast Monitoring for Custom Content](https://docs.acrcloud.com/tutorials/broadcast-monitoring-for-custom-content)
 * [Detect Live & Timeshift TV Channels](https://docs.acrcloud.com/tutorials/detect-live-and-timeshift-tv-channels)
 * [Recognize Custom Content Offline](https://docs.acrcloud.com/tutorials/recognize-custom-content-offline)
 * [Recognize Live Channels and Custom Content](https://docs.acrcloud.com/tutorials/recognize-tv-channels-and-custom-content)

## Install
### Linux and macOS user (x86)

**python3 -m pip install pyacrcloud**

### Other platform

You can run **python -m pip install git+https://github.com/acrcloud/acrcloud_sdk_python** or go to sub dir, and run"sudo python setup.py install".

## Windows Runtime Library 
**If you run the SDK on Windows, you must install this library.**<br>
X86: [download and install Library(windows/vcredist_x86.exe)](https://github.com/acrcloud/acrcloud_sdk_python/blob/master/windows/vcredist_x86.exe)<br>
x64: [download and install Library(windows/vcredist_x64.exe)](https://github.com/acrcloud/acrcloud_sdk_python/blob/master/windows/vcredist_x64.exe)

## Note
1. If you run the SDK on Windows, you must install library(vcredist).
2. ALL version supports humming.
3. If you use docker alpine, you need to install "apk add --update libstdc++"

## Functions
Introduction all API.
### recognizer.py
```python
class ACRCloudRecognizer:
    def recognize_by_file(self, file_path, start_seconds, rec_length=10):
      #@param file_path : query file path
      #@param start_seconds : skip (start_seconds) seconds from from the beginning of (filePath)
      #@param rec_length: use rec_length seconds data to recongize
      #@return result metainfos
      
    def recognize_by_filebuffer(self, file_buffer, start_seconds, rec_length=10):
      #@param file_buffer : file_path query buffer
      #@param start_seconds : skip (start_seconds) seconds from from the beginning of (filePath)
      #@param rec_length: use rec_length seconds data to recongize
      #@return result metainfos
      
    def recognize(self, wav_audio_buffer):
      #@param wav_audio_buffer : query buffer(RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 8000 Hz)
      #@return result metainfos
```
### Module acrcloud_extr_tool
```python
def create_fingerprint_by_file(file_name, start_time_seconds, audio_len_seconds, is_db_fingerprint, filter_e):
      #file_name: Path of input file; 
      #start_time_seconds: Start time of input file, default is 0; 
      #audio_len_seconds: Length of audio data you need. if you create recogize frigerprint, default is 12 seconds, if you create db frigerprint, it is not usefully; 
      #is_db_fingerprint: If it is True, it will create db frigerprint (Fingerprint for bucket, not for recognition); 
      #filter_e: Set it 0; 

def create_humming_fingerprint_by_file(file_name, start_time_seconds, audio_len_seconds):
      #file_name: Path of input file; 
      #start_time_seconds: Start time of input file, default is 0; 
      #audio_len_seconds: Length of audio data you need. if you create recogize frigerprint, default is 12 seconds, if you create db frigerprint, it is not usefully; 

def create_fingerprint_by_filebuffer(data_buffer, start_time_seconds, audio_len_seconds, is_db_fingerprint):
      #data_buffer: data buffer of input file; 
      #start_time_seconds: Start time of input file, default is 0; 
      #audio_len_seconds: Length of audio data you need. if you create recogize frigerprint, default is 12 seconds, if you create db frigerprint, it is not usefully; 
      #is_db_fingerprint: If it is True, it will create db frigerprint (Fingerprint for bucket, not for recognition); 

def create_humming_fingerprint_by_filebuffer(data_buffer, start_time_seconds, audio_len_seconds):
      #data_buffer: data buffer of input file; 
      #start_time_seconds: Start time of input file, default is 0; 
      #audio_len_seconds: Length of audio data you need. if you create recogize frigerprint, default is 12 seconds, if you create db frigerprint, it is not usefully; 

def create_fingerprint(data_buffer, is_db_fingerprint):
      #data_buffer: audio data buffer(RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 8000 Hz); 
      #is_db_fingerprint: If it is True, it will create db frigerprint (Fingerprint for bucket, not for recognition); 

def create_humming_fingerprint(data_buffer):
      #data_buffer: audio data buffer(RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 8000 Hz); 

def decode_audio_by_file(file_name, start_time_seconds, audio_len_seconds):
      #It will return the audio data(RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 8000 Hz); 
      #file_name: Path of input file; 
      #start_time_seconds: Start time of input file, default is 0; 
      #audio_len_seconds: Length of audio data you need, if it is 0, will decode all the audio; 

def decode_audio_by_filebuffer(data_buffer, start_time_seconds, audio_len_seconds):
      #It will return the audio data(RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 8000 Hz); 
      #data_buffer: data buffer of input file; 
      #start_time_seconds: Start time of input file, default is 0; 
      #audio_len_seconds: Length of audio data you need, if it is 0, will decode all the audio; 

def version() 
      #return the version of this module
```
## Example
run Test: python test.py test.mp3
```python
#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, sys
from acrcloud.recognizer import ACRCloudRecognizer

if __name__ == '__main__':
    config = {
        #Replace "xxxxxxxx" below with your project's host, access_key and access_secret.
        'host':'XXXXXXXX',
        'access_key':'XXXXXXXX', 
        'access_secret':'XXXXXXXX',
        'timeout':10 # seconds
    }

    '''This module can recognize ACRCloud by most of audio/video file. 
        Audio: mp3, wav, m4a, flac, aac, amr, ape, ogg ...
        Video: mp4, mkv, wmv, flv, ts, avi ...'''
    re = ACRCloudRecognizer(config)

    #recognize by file path, and skip 0 seconds from from the beginning of sys.argv[1].
    print re.recognize_by_file(sys.argv[1], 0)

    buf = open(sys.argv[1], 'rb').read()
    #recognize by file_audio_buffer that read from file path, and skip 0 seconds from from the beginning of sys.argv[1].
    print re.recognize_by_filebuffer(buf, 0)
```
