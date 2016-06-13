#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
    @author qinxue.pan E-mail: xue@acrcloud.com
    @version 1.0.0
    @create 2015.10.01
'''

import os
import sys
import hmac
import time
import json
import base64
import hashlib
import urllib.request
import urllib.parse
import datetime

import acrcloud_extr_tool

'''
Copyright 2015 ACRCloud Recognizer v1.0.0

This module can recognize ACRCloud by most of audio/video file. 
        Audio: mp3, wav, m4a, flac, aac, amr, ape, ogg ...
        Video: mp4, mkv, wmv, flv, ts, avi ...

Example:
    config = {
        'host':'ap-southeast-1.api.acrcloud.com',
        'access_key':'XXXXXXXX',
        'access_secret':'XXXXXXXX',
        'timeout':5
    }
    re = ACRCloudRecognizer(config)

    #recognize by file path, and skip 180 seconds from from the beginning of "aa.mp3".
    print re.recognize_by_file('aa.mp3', 180)

    buf = open('aa.mp3', 'rb').read()
    #recognize by file_audio_buffer that read from file path, and skip 180 seconds from from the beginning of "aa.mp3".
    print re.recognize_by_filebuffer(buf, 180)

    #aa.wav is (RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 8000 Hz)
    buf = open('aa.wav', 'rb').read()
    buft = buf[1024000:192000+1024001]
    recognize by audio_buffer(RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 8000 Hz)
    print re.recognize(buft)
'''

class ACRCloudRecognizer:
    def __init__(self, config):
        self.config = config
        self.host = config.get('host', 'ap-southeast-1.api.acrcloud.com')
        self.query_type = config.get('query_type', 'fingerprint')
        self.access_key = config.get('access_key')
        self.access_secret = config.get('access_secret')
        self.timeout = config.get('timeout', 5)
        self.debug = config.get('debug', False)
        if not self.access_key or not self.access_secret:
            print('recognize init(none access_key or access_secret)')
            sys.exit(1)

        if self.debug:
            acrcloud_extr_tool.set_debug()

    def post_multipart(self, url, fields, files, timeout):
        content_type, body = self.encode_multipart_formdata(fields, files)
        
        if not content_type and not body:
            return ACRCloudStatusCode.get_result_error(ACRCloudStatusCode.HTTP_ERROR_CODE, 'encode_multipart_formdata error')

        try:
            req = urllib.request.Request(url, data=body)
            req.add_header('Content-Type', content_type)
            req.add_header('Referer', url)
            resp = urllib.request.urlopen(req, timeout=timeout)
            ares = resp.read().decode('utf8')
            return ares
        except Exception as e:
            return ACRCloudStatusCode.get_result_error(ACRCloudStatusCode.HTTP_ERROR_CODE, str(e))
        
    def encode_multipart_formdata(self, fields, files):
        try:
            boundary = "*****2016.05.27.acrcloud.rec.copyright." + str(time.time()) + "*****"
            body = b''
            CRLF = '\r\n'
            L = []
            for (key, value) in list(fields.items()):
                L.append('--' + boundary)
                L.append('Content-Disposition: form-data; name="%s"' % key)
                L.append('')
                L.append(value)

            body = CRLF.join(L).encode('ascii')

            for (key, value) in list(files.items()):
                L = []
                L.append(CRLF + '--' + boundary)
                L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, key))
                L.append('Content-Type: application/octet-stream')
                L.append(CRLF)
                body = body + CRLF.join(L).encode('ascii') + value
            body = body + (CRLF + '--' + boundary + '--' + CRLF + CRLF).encode('ascii')
            content_type = 'multipart/form-data; boundary=%s' % boundary
            return content_type, body
        except Exception as e:
            print('encode_multipart_formdata error' + str(e))
        return None, None

    def do_recogize(self, host, query_data, query_type, access_key, access_secret, timeout=5):
        http_method = "POST"
        http_url_file = "/v1/identify"
        data_type = query_type
        signature_version = "1"
        timestamp = int(time.mktime(datetime.datetime.utcfromtimestamp(time.time()).timetuple()))
        sample_bytes = str(len(query_data))
        
        string_to_sign = http_method+"\n"+http_url_file+"\n"+access_key+"\n"+data_type+"\n"+signature_version+"\n"+str(timestamp)
        hmac_res = hmac.new(access_secret.encode('ascii'), string_to_sign.encode('ascii'), digestmod=hashlib.sha1).digest()
        sign = base64.b64encode(hmac_res).decode('ascii')
    
        fields = {'access_key':access_key, 
                  'sample_bytes':sample_bytes, 
                  'timestamp':str(timestamp), 
                  'signature':sign, 
                  'data_type':data_type, 
                  "signature_version":signature_version}

        server_url = 'http://' + host + http_url_file
        res = self.post_multipart(server_url, fields, {"sample" : query_data}, timeout)
        return res

    def recognize(self, wav_audio_buffer):
        try:
            res = ''
            fp = acrcloud_extr_tool.create_fingerprint(wav_audio_buffer, False)
            if fp == None:
                return ACRCloudStatusCode.get_result_error(ACRCloudStatusCode.AUDIO_ERROR_CODE)
            elif len(fp) <= 0:
                return ACRCloudStatusCode.get_result_error(ACRCloudStatusCode.NO_RESULT_CODE)
            res = self.do_recogize(self.host, fp, self.query_type, self.access_key, self.access_secret, self.timeout)
            try:
                json.loads(res)
            except Exception as e:
                res = ACRCloudStatusCode.get_result_error(ACRCloudStatusCode.JSON_ERROR_CODE, str(res))
        except Exception as e:
            res = ACRCloudStatusCode.get_result_error(ACRCloudStatusCode.UNKNOW_ERROR_CODE, str(e))
        return res

    def recognize_by_file(self, file_path, start_seconds):
        try:
            res = ''
            fp = acrcloud_extr_tool.create_fingerprint_by_file(file_path, start_seconds, 12, False)
            if fp == None:
                return ACRCloudStatusCode.get_result_error(ACRCloudStatusCode.AUDIO_ERROR_CODE)
            elif len(fp) <= 0:
                return ACRCloudStatusCode.get_result_error(ACRCloudStatusCode.NO_RESULT_CODE)
            res = self.do_recogize(self.host, fp, self.query_type, self.access_key, self.access_secret, self.timeout)
            try:
                json.loads(res)
            except Exception as e:
                res = ACRCloudStatusCode.get_result_error(ACRCloudStatusCode.JSON_ERROR_CODE, str(res))
        except Exception as e:
            res = ACRCloudStatusCode.get_result_error(ACRCloudStatusCode.UNKNOW_ERROR_CODE, str(e))
        return res

    def recognize_by_filebuffer(self, file_buffer, start_seconds):
        try:
            res = ''
            fp = acrcloud_extr_tool.create_fingerprint_by_filebuffer(file_buffer, start_seconds, 12, False)
            if fp == None:
                return ACRCloudStatusCode.get_result_error(ACRCloudStatusCode.AUDIO_ERROR_CODE)
            elif len(fp) <= 0:
                return ACRCloudStatusCode.get_result_error(ACRCloudStatusCode.NO_RESULT_CODE)
            res = self.do_recogize(self.host, fp, self.query_type, self.access_key, self.access_secret, self.timeout)
            try:
                json.loads(res)
            except Exception as e:
                res = ACRCloudStatusCode.get_result_error(ACRCloudStatusCode.JSON_ERROR_CODE, str(res))
        except Exception as e:
            res = ACRCloudStatusCode.get_result_error(ACRCloudStatusCode.UNKNOW_ERROR_CODE, str(e))
        return res

    @staticmethod
    def get_duration_ms_by_file(file_path):
        try:
            duration_ms = acrcloud_extr_tool.get_duration_ms_by_file(file_path)
            return duration_ms
        except Exception as e:
            return 0

class ACRCloudStatusCode:
    HTTP_ERROR_CODE = 3000
    NO_RESULT_CODE = 1001
    AUDIO_ERROR_CODE = 2005
    UNKNOW_ERROR_CODE = 2010
    JSON_ERROR_CODE = 2002

    CODE_MSG = { 
        HTTP_ERROR_CODE : 'http error', 
        NO_RESULT_CODE : 'no result', 
        AUDIO_ERROR_CODE : 'audio error', 
        UNKNOW_ERROR_CODE : 'unknow error',
        JSON_ERROR_CODE : 'json error'
    }   

    @staticmethod
    def get_result_error(res_code, msg=''):
        if ACRCloudStatusCode.CODE_MSG.get(res_code) == None:
            return None
        res = {'status':{'msg':ACRCloudStatusCode.CODE_MSG[res_code], 'code':res_code}}
        if msg:
            res = {'status':{'msg':ACRCloudStatusCode.CODE_MSG[res_code]+':'+msg, 'code':res_code}}
        return json.dumps(res)


if __name__ == '__main__':
    config = {
        'host':'ap-southeast-1.api.acrcloud.com',
        'access_key':'XXXXXXXX',
        'access_secret':'XXXXXXXX',
        'timeout':5
    }

    
    re = ACRCloudRecognizer(config)
    buf = open(sys.argv[1], 'rb').read()
    #buft = buf[1024000:192000+1024001]

    acrcloud_extr_tool.set_debug()
    #print(acrcloud_extr_tool.__doc__)
    #print(re.recognize_by_file(sys.argv[1], 10))
    print(re.recognize_by_filebuffer(buf, 10))
    #print re.recognize(buft)
