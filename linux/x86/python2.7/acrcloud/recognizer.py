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
import base64
import hashlib
import urllib2
import datetime
import mimetools
import json

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

class ACRCloudRecognizeType:
    ACR_OPT_REC_AUDIO = 0  # audio fingerprint
    ACR_OPT_REC_HUMMING = 1 # humming fingerprint
    ACR_OPT_REC_BOTH = 2 # audio and humming fingerprint

class ACRCloudRecognizer:
    def __init__(self, config):
        self.config = config
        self.host = config.get('host', 'ap-southeast-1.api.acrcloud.com')
        self.query_type = 'fingerprint'
        self.access_key = config.get('access_key')
        self.access_secret = config.get('access_secret')
        self.timeout = config.get('timeout', 5)
        self.recognize_type = config.get('recognize_type', ACRCloudRecognizeType.ACR_OPT_REC_AUDIO)
        if self.recognize_type > 2 or self.recognize_type < 0:
            self.recognize_type = ACRCloudRecognizeType.ACR_OPT_REC_AUDIO
        self.debug = config.get('debug', False)
        if not self.access_key or not self.access_secret:
            print 'recognize init(none access_key or access_secret)'
            sys.exit(1)

        if self.debug:
            acrcloud_extr_tool.set_debug()

    def post_multipart(self, url, fields, files, timeout):
        content_type, body = self.encode_multipart_formdata(fields, files)
        if not content_type and not body:
            self.dlog.logger.error('encode_multipart_formdata error')
            return ACRCloudStatusCode.get_result_error(ACRCloudStatusCode.HTTP_ERROR_CODE, 'encode_multipart_formdata error')
        try:
            req = urllib2.Request(url, data=body)
            req.add_header('Content-Type', content_type)
            req.add_header('Referer', url)
            resp = urllib2.urlopen(req, timeout=timeout)
            ares = resp.read()
            return ares
        except Exception, e:
            return ACRCloudStatusCode.get_result_error(ACRCloudStatusCode.HTTP_ERROR_CODE, str(e))
        
    def encode_multipart_formdata(self, fields, files):
        try:
            boundary = mimetools.choose_boundary()
            CRLF = '\r\n'
            L = []
            for (key, value) in fields.items():
                L.append('--' + boundary)
                L.append('Content-Disposition: form-data; name="%s"' % key)
                L.append('')
                L.append(str(value))
            for (key, value) in files.items():
                L.append('--' + boundary)
                L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, key))
                L.append('Content-Type: application/octet-stream')
                L.append('')
                L.append(value)
            L.append('--' + boundary + '--')
            L.append('')
            body = CRLF.join(L)
            content_type = 'multipart/form-data; boundary=%s' % boundary
            return content_type, body
        except Exception, e:
            print 'encode_multipart_formdata error' + str(e)
        return None, None

    def do_recogize(self, host, query_data, query_type, access_key, access_secret, timeout=5):
        http_method = "POST"
        http_url_file = "/v1/identify"
        data_type = query_type
        signature_version = "1"
        timestamp = int(time.mktime(datetime.datetime.utcfromtimestamp(time.time()).timetuple()))
        
        string_to_sign = http_method+"\n"+http_url_file+"\n"+access_key+"\n"+data_type+"\n"+signature_version+"\n"+str(timestamp)
        sign = base64.b64encode(hmac.new(str(access_secret), str(string_to_sign), digestmod=hashlib.sha1).digest())
    
        fields = {'access_key':access_key, 
                  'timestamp':str(timestamp), 
                  'signature':sign, 
                  'data_type':data_type, 
                  "signature_version":signature_version}
       
        sample_bytes = 0
        sample_hum_bytes = 0
        if query_data.has_key('sample'):
            if query_data['sample'] == None:
                return ACRCloudStatusCode.get_result_error(ACRCloudStatusCode.AUDIO_ERROR_CODE)
            sample_bytes = len(query_data['sample'])
            fields['sample_bytes'] = str(sample_bytes)

        if query_data.has_key('sample_hum'):
            if query_data['sample_hum'] == None:
                return ACRCloudStatusCode.get_result_error(ACRCloudStatusCode.AUDIO_ERROR_CODE)
            sample_hum_bytes = len(query_data['sample_hum'])
            fields['sample_hum_bytes'] = str(sample_hum_bytes)

        if sample_bytes == 0 and sample_hum_bytes == 0:
            return ACRCloudStatusCode.get_result_error(ACRCloudStatusCode.NO_RESULT_CODE)
        
        server_url = 'http://' + host + http_url_file
        res = self.post_multipart(server_url, fields, query_data, timeout)
        return res

    def recognize(self, wav_audio_buffer):
        res = ''
        try:
            query_data = {}
            if self.recognize_type == ACRCloudRecognizeType.ACR_OPT_REC_AUDIO or self.recognize_type == ACRCloudRecognizeType.ACR_OPT_REC_BOTH:
                query_data['sample'] = acrcloud_extr_tool.create_fingerprint(wav_audio_buffer, False)

            if self.recognize_type == ACRCloudRecognizeType.ACR_OPT_REC_HUMMING or self.recognize_type == ACRCloudRecognizeType.ACR_OPT_REC_BOTH:
                query_data['sample_hum'] = acrcloud_extr_tool.create_humming_fingerprint(wav_audio_buffer)

            res = self.do_recogize(self.host, query_data, self.query_type, self.access_key, self.access_secret, self.timeout)

            try:
                json.loads(res)
            except Exception as e:
                res = ACRCloudStatusCode.get_result_error(ACRCloudStatusCode.JSON_ERROR_CODE, str(res))
        except Exception as e:
            res = ACRCloudStatusCode.get_result_error(ACRCloudStatusCode.UNKNOW_ERROR_CODE, str(e))
        return res

    def recognize_by_file(self, file_path, start_seconds=0, rec_length=10, filter_e=50):
        res = ''
        try:
            query_data = {}
            if self.recognize_type == ACRCloudRecognizeType.ACR_OPT_REC_AUDIO or self.recognize_type == ACRCloudRecognizeType.ACR_OPT_REC_BOTH:
                query_data['sample'] = acrcloud_extr_tool.create_fingerprint_by_file(file_path, start_seconds, rec_length, False, filter_e)

            if self.recognize_type == ACRCloudRecognizeType.ACR_OPT_REC_HUMMING or self.recognize_type == ACRCloudRecognizeType.ACR_OPT_REC_BOTH:
                query_data['sample_hum'] = acrcloud_extr_tool.create_humming_fingerprint_by_file(file_path, start_seconds, rec_length)

            res = self.do_recogize(self.host, query_data, self.query_type, self.access_key, self.access_secret, self.timeout)

            try:
                json.loads(res)
            except Exception as e:
                res = ACRCloudStatusCode.get_result_error(ACRCloudStatusCode.JSON_ERROR_CODE, str(res))
        except Exception as e:
            print e
            res = ACRCloudStatusCode.get_result_error(ACRCloudStatusCode.UNKNOW_ERROR_CODE, str(e))
        return res

    def recognize_by_filebuffer(self, file_buffer, start_seconds=0, rec_length=10):
        res = ''
        try:
            query_data = {}
            if self.recognize_type == ACRCloudRecognizeType.ACR_OPT_REC_AUDIO or self.recognize_type == ACRCloudRecognizeType.ACR_OPT_REC_BOTH:
                query_data['sample'] = acrcloud_extr_tool.create_fingerprint_by_filebuffer(file_buffer, start_seconds, rec_length, False)

            if self.recognize_type == ACRCloudRecognizeType.ACR_OPT_REC_HUMMING or self.recognize_type == ACRCloudRecognizeType.ACR_OPT_REC_BOTH:
                query_data['sample_hum'] = acrcloud_extr_tool.create_humming_fingerprint_by_filebuffer(file_buffer, start_seconds, rec_length)

            res = self.do_recogize(self.host, query_data, self.query_type, self.access_key, self.access_secret, self.timeout)
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
    AUDIO_ERROR_CODE = 2004
    UNKNOW_ERROR_CODE = 2010
    JSON_ERROR_CODE = 2002

    CODE_MSG = {
        HTTP_ERROR_CODE : 'Http Error', 
        NO_RESULT_CODE : 'No Result', 
        AUDIO_ERROR_CODE : 'Unable to generate fingerprint', 
        UNKNOW_ERROR_CODE : 'Unknow Error',
        JSON_ERROR_CODE : 'Json Error'
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
    buft = buf[1024000:192000+1024001]

    print acrcloud_extr_tool.__doc__
    #print re.recognize_by_file(sys.argv[1], 180)
    #print re.recognize_by_filebuffer(buf, 80)
    #print re.recognize(buft)
