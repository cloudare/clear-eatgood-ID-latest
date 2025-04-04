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
import config as sd
import models.cleartax_model as cm
from models.zoho_model import ZohoModel

def bulkVendor(vendors):
    try:
        response = cm.bulkVendorMaster(vendors)
        print(response)
        if response.status_code != 200:
            lw.logBackUpRecord("Bulk Vendor Data has been uploaded with error.")
        else:
            lw.logBackUpRecord("Bulk Vendor Data has been uploaded Successfully.")
        pass
    except Exception as e:
        lw.logRecord("Error in bulkVendor: " + str(e))

def bulkInvoices(invoice):
    try:
        response = cm.bulkInvoice(invoice)
        print(response)
        if response.status_code != 200:
            lw.logBackUpRecord("Bulk Vendor Data has been uploaded with error.")
        else:
            lw.logBackUpRecord("Bulk Vendor Data has been uploaded Successfully.")
        pass
    except Exception as e:
        lw.logRecord("Error in bulkInvoices: " + str(e))

def creditDebitNote(cndn):
    try:
        response = cm.creditDebitNote(cndn)
        print(response)
        if response.status_code != 200:
            lw.logBackUpRecord("Bulk Vendor Data has been uploaded with error.")
        else:
            lw.logBackUpRecord("Bulk Vendor Data has been uploaded Successfully.")
        pass
    except Exception as e:
        lw.logRecord("Error in creditDebitNote: " + str(e))

def payments(payments):
    try:
        response = cm.payments(payments)
        print(response)
        if response.status_code != 200:
            lw.logBackUpRecord("Bulk Vendor Data has been uploaded with error.")
        else:
            lw.logBackUpRecord("Bulk Vendor Data has been uploaded Successfully.")
        pass
    except Exception as e:
        lw.logRecord("Error in payments: " + str(e))

def update_invoice(data, t, v, i, vi, da, dd, md):
    try:
        
        
        ZohoModel.update_invoice(data['bill_id'],json)
        postingAck(t, v, i, vi)
        pass
    except Exception as e:
        lw.logRecord("Error in update_invoice: " + str(e))


def postingAck(t, v, i, vi):
    try:
        
        json = {
            "transactionId": t,############################
            "vendorId": v,
            "internalInvoiceNumber": i,
            "vendorInvoiceNumber": vi,
            "postingStatus": "True",
            "postingResponse": "Success",
            "referenceNumber": i,
            "voucherPosted": "Yes",
            "invoiceCleared": "No",
            "invoiceUpdated": "Yes",
            "postingDate": str((datetime.now()).strftime("%d-%m-%Y"))
            }
        pass
    except Exception as e:
        lw.logRecord("Error in postingAck: " + str(e))

def postingCreditDebitNote():
    try:
        json = {
            "userName": str(sd.userName)
        }
        response = cm.postingCreditDebitNote(json)
        transactionId = vendorId = internalInvoiceNumber = vendorInvoiceNumber = discountAmount = discountingDate = maturityDate = []
        if response != []:
            if response:
                for data in response:
                    transactionId.append(data.get('id'))
                    vendorId.append(data.get('vendorId'))
                    internalInvoiceNumber.append(data.get('internalInvoiceNumber'))
                    vendorInvoiceNumber.append(data.get('vendorInvoiceNumber'))
                    discountAmount.append(data.get('discountAmount'))
                    discountingDate.append(data.get('discountingDate'))
                    maturityDate.append(data.get('maturityDate'))
                    # referenceNumber = data.get('transactionId')
        return transactionId, vendorId, internalInvoiceNumber, vendorInvoiceNumber, discountAmount, discountingDate, maturityDate
    except Exception as e:
        lw.logRecord("Error in postingCreditDebitNote: " + str(e))