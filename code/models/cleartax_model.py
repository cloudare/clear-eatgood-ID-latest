import requests
import json
import gzip
import os
import pandas as pd
import views.logWriter as lw
import logging
from logging.handlers import RotatingFileHandler
import time
from datetime import datetime
import numpy as np
import config as sd

def clear_header(authorization):
    header = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : authorization,
        "REQUEST_TYPE" : "ENC",
        "applicationName" : "invoicemanager"
    }
    return header

def getToken():
    try:
        lw.logBackUpRecord("Calling getToken API.")
        url = sd.clear_api_url + "/getToken"
        header = {
                "Accept" : "application/json",
                "Content-Type" : "application/json",
                "REQUEST_TYPE" : "ENC"
                # "applicationName" : "invoicemanager"
            }
        body = {
            "userName" : sd.userName,
            "password" : sd.password
        }
        lw.logBackUpRecord("URL:" + str(url))
        lw.logBackUpRecord("Header:" + str(header))
        lw.logBackUpRecord("Payload:" + str(body))
        response = requests.post(url, headers=header, json=body)#, data=payload)

        if str(response.json().get("authenticated")) == True or str(response.json().get("authenticated")) == 'true':
            authorization = response.json().get("token")
            lw.logBackUpRecord("Authorization Token is :" + str(authorization))
            return authorization
        else:
            lw.logRecord("Error in getToken: " + (response.json())['messages']['details'])
            return ''
        
    except Exception as e:
        lw.logRecord("Error in getToken: " + str(e))

def bulkVendorMaster(body):
    try:
        auth = getToken()
        lw.logBackUpRecord("Calling bulkVendorMaster API.")
        url = sd.clear_api_url + "/bulkVendorMaster"
        header = clear_header(auth)
        lw.logBackUpRecord("URL:" + str(url))
        lw.logBackUpRecord("Header:" + str(header))
        lw.logBackUpRecord("Payload:" + str(body))
        response = requests.post(url, headers=header, json=body)#, data=payload)

        if response.status_code == 400 or response.status_code == 401:# or response.status_code == 400:
            auth = getToken()
            response = requests.post(url, headers=header, json=body)
            # auth = authorization
            lw.logBackUpRecord(auth)
        
        return response
    except Exception as e:
        lw.logRecord("Error in bulkVendorMaster: " + str(e))

def bulkInvoice(body):
    try:
        auth = getToken()
        lw.logBackUpRecord("Calling bulkInvoice API.")
        url = sd.clear_api_url + "/bulkInvoice"
        header = clear_header(auth)
        lw.logBackUpRecord("URL:" + str(url))
        lw.logBackUpRecord("Header:" + str(header))
        lw.logBackUpRecord("Payload:" + str(body))
        response = requests.post(url, headers=header, json=body)#, data=payload)

        if response.status_code == 500 or response.status_code == 401:# or response.status_code == 400:
            auth = getToken()
            response = requests.post(url, headers=header, json=body)
            # auth = authorization
            lw.logBackUpRecord(auth)
        elif response.status_code == 400:
            lw.logBackUpRecord("Bulk Invoice Data has been uploaded with error.")
        else:
            lw.logBackUpRecord("Bulk Invoice Data has been uploaded Successfully.")
        
    except Exception as e:
        lw.logRecord("Error in bulkInvoice: " + str(e))

def creditDebitNote(body):
    try:
        auth = getToken()
        lw.logBackUpRecord("Calling creditDebitNote API.")
        url = sd.clear_api_url + "/creditDebitNote"
        header = clear_header(auth)
        lw.logBackUpRecord("URL:" + str(url))
        lw.logBackUpRecord("Header:" + str(header))
        lw.logBackUpRecord("Payload:" + str(body))
        response = requests.post(url, headers=header, json=body)#, data=payload)

        if response.status_code == 500 or response.status_code == 401:# or response.status_code == 400:
            auth = getToken()
            response = requests.post(url, headers=header, json=body)
            # auth = authorization
            lw.logBackUpRecord(auth)
        elif response.status_code == 400:
            lw.logBackUpRecord("credit /Debit Note Data has been uploaded with error.")
        else:    
            lw.logBackUpRecord("credit /Debit Note Data has been uploaded Successfully.")
        return response.json()
    except Exception as e:
        lw.logRecord("Error in creditDebitNote: " + str(e))

def payments(body):
    try:
        auth = getToken()
        lw.logBackUpRecord("Calling payments  API.")
        url = sd.clear_api_url + "/payments"
        header = clear_header(auth)
        lw.logBackUpRecord("URL:" + str(url))
        lw.logBackUpRecord("Header:" + str(header))
        lw.logBackUpRecord("Payload:" + str(body))
        response = requests.post(url, headers=header, json=body)#, data=payload)

        if response.status_code == 500 or response.status_code == 401:# or response.status_code == 400:
            auth = getToken()
            response = requests.post(url, headers=header, json=body)
            # auth = authorization
            lw.logBackUpRecord(auth)
        elif response.status_code == 400:
            lw.logBackUpRecord("Payments Data has been uploaded with error.")
        else:
            lw.logBackUpRecord("Payments Data has been uploaded Successfully.")
        
    except Exception as e:
        lw.logRecord("Error in payments : " + str(e))

def postingCreditDebitNote(body):
    try:
        auth = getToken()
        lw.logBackUpRecord("Calling postingCreditDebitNote  API.")
        url = sd.clear_api_url + "/postingCreditDebitNote"
        header = clear_header(auth)
        lw.logBackUpRecord("URL:" + str(url))
        lw.logBackUpRecord("Header:" + str(header))
        lw.logBackUpRecord("Payload:" + str(body))
        response = requests.post(url, headers=header, json=body)#, data=payload)

        if response.status_code == 500 or response.status_code == 401:# or response.status_code == 400:
            auth = getToken()
            response = requests.post(url, headers=header, json=body)
            # auth = authorization
            lw.logBackUpRecord(auth)
        elif response.status_code == 200:
            lw.logBackUpRecord("Credit/Debit Note has been posted Successfully.")
        else:
            lw.logBackUpRecord("Credit/Debit Note has been posted with error: " + str())
        # lw.logBackUpRecord("Credit/Debit Note has been posted Successfully.")
        return response.json()
    
    except Exception as e:
        lw.logRecord("Error in postingCreditDebitNote : " + str(e))

def postingAck(body):
    try:
        auth = getToken()
        lw.logBackUpRecord("Calling postingAck  API.")
        url = sd.clear_api_url + "/postingAck"
        header = clear_header(auth)
        lw.logBackUpRecord("URL:" + str(url))
        lw.logBackUpRecord("Header:" + str(header))
        lw.logBackUpRecord("Payload:" + str(body))
        response = requests.post(url, headers=header, json=body)#, data=payload)

        if response.status_code == 500 or response.status_code == 401: # or response.status_code == 400:
            auth = getToken()
            response = requests.post(url, headers=header, json=body)
            # auth = authorization
            lw.logBackUpRecord(auth)
        elif str((response.json())['status']) == "Success":
            lw.logBackUpRecord("Acknowledgement from ERP System has been posted Successfully.")
        else:
            lw.logBackUpRecord("Acknowledgement from ERP System has been posted with error: " + str())
        
        return response.json()
    
    except Exception as e:
        lw.logRecord("Error in postingAck : " + str(e))

def uploadLocationMaster(body):
    try:
        auth = getToken()
        lw.logBackUpRecord("Calling uploadLocationMaster  API.")
        url = sd.clear_api_url + "/uploadLocationMaster"
        header = clear_header(auth)
        lw.logBackUpRecord("URL:" + str(url))
        lw.logBackUpRecord("Header:" + str(header))
        lw.logBackUpRecord("Payload:" + str(body))
        response = requests.post(url, headers=header, json=body)#, data=payload)

        if response.status_code == 500 or response.status_code == 401:# or response.status_code == 400:
            auth = getToken()
            response = requests.post(url, headers=header, json=body)
            # auth = authorization
            lw.logBackUpRecord(auth)
        elif str((response.json())[0]['status']) == "Success":
            lw.logBackUpRecord("Location Master has been uploaded Successfully.")
        else:
            lw.logBackUpRecord("Location Master has been uploaded with error: " + str())
    
    except Exception as e:
        lw.logRecord("Error in uploadLocationMaster : " + str(e))

def update_invoice():
    pass