#!/usr/bin/env python
import sys
import argparse
import requests
from time import sleep
from pprint import pprint
from app.constants.config import vt_api_key
from app.services.logs import logger
import subprocess

class VirusTotal_API:
    def __init__(self, apiKey):
        self.apiKey = apiKey

    def uploadFile(self, fileName):
        ''' upload file to virustotal online scanner, and receive its response message'''
        # https://developers.virustotal.com/reference#file-scan
        url = 'https://www.virustotal.com/vtapi/v2/file/scan'
        files = {'file': open(fileName, 'rb')}
        # r = requests.post(url, files=files)
        params = {'apikey': self.apiKey}
        r = requests.post(url, data=params, files=files)

        r.raise_for_status()
        if r.headers['Content-Type'] == 'application/json':
            return r.json()['resource']
        else:
            raise Exception('Unable to locate result')

    def retrieveReport(self, resourceId):
        ''' retrieve report of an existing resource on the virustotal server '''
        # https://developers.virustotal.com/reference#url-report
        url = 'https://www.virustotal.com/vtapi/v2/file/report'
        params = {'apikey': self.apiKey, 'resource': resourceId}
        while True:
            r = requests.get(url, params=params)
            r.raise_for_status()

            if r.headers['Content-Type'] == 'application/json':
                if r.json()['response_code'] == 1: 
                    break
                else:
                    delay = 25
                    sleep(delay)
            else:
                raise Exception('Invalid content type')
        
        report = r.json()
        self.report = report
        positives = []
        for engine, result in report['scans'].items():
            if result['detected'] == True:
                positives.append(engine)
        return positives

def scan_file(file_path):
    try:
        result = subprocess.run(['clamscan', file_path], stdout=subprocess.PIPE, text=True)
        while result.returncode is None:
            result = subprocess.run(['clamscan', file_path], stdout=subprocess.PIPE, text=True)
        output = result.stdout
        scan_dict = {}
        for line in output.strip().split('\n')[:-2]:  # Excluding last two lines
            if ': ' in line:  # Check if the line contains the separator
                if ": OK" in line or "Start Date:" in line or "End Date:" in line or "/" in line:
                    continue
                key, value = line.split(': ', 1)
                scan_dict[key] = value
        return scan_dict
    except Exception as e:
        return {"error occur while scan": str(e)}
    
def virus_scan(original_file_name, filePath):
    api = VirusTotal_API(vt_api_key)
    logger.info(f"Initiating scan for: {original_file_name}")
    resourceId = api.uploadFile(filePath)
    positives = api.retrieveReport(resourceId)
    scan_report = api.report
    # logger.info(f"Initiating other scan for: {original_file_name}")
    # other_scan = scan_file(filePath)
    # scan_report['other_scan'] = other_scan
    logger.info("scan completed")
    return scan_report