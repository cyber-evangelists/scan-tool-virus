#!/usr/bin/env python
import sys
import argparse
import requests
from time import sleep
from pprint import pprint
from app.constants.config import vt_api_key
from app.services.logs import logger
import json

class VirusTotal_API:
    def __init__(self, apiKey):
        self.apiKey = apiKey

    def scanUrl(self, target_url):
        ''' scan url at virustotal online scanner, and receive its response message'''
        url = 'https://www.virustotal.com/vtapi/v2/url/scan'
        params = {'apikey': self.apiKey, 'url': target_url}
        r = requests.post(url, data=params)

        r.raise_for_status()
        if r.headers['Content-Type'] == 'application/json':
            return r.json()['resource']
        else:
            raise Exception('Unable to locate result')

    def retrieveReport(self, resourceId):
        ''' retrieve report of an existing resource on the virustotal server '''
        url = 'https://www.virustotal.com/vtapi/v2/url/report'
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

    
def url_scan(url):
    api = VirusTotal_API(vt_api_key)
    logger.info(f"Initiating url scan for: {url}")
    resourceId = api.scanUrl(url)
    positives = api.retrieveReport(resourceId)
    scan_report = api.report
    logger.info(f"Scan completed for: {url}")
    return scan_report

if __name__ == '__main__':
    url = "https://vulegends.com/crack-every-quiz-with-vu-legends-ai-quizzer-app-mastery/"
    report = virus_scan(url)
    # pprint(report)
    with open("url_scan_report.json", "w") as file:
        file.write(json.dumps(report, indent=3))