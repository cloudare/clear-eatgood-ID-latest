import views.logWriter as lw
from datetime import datetime
import config as sd
import config as sd
import models.cleartax_model as cm
from models.zoho_model import ZohoModel

def bulkVendor(vendors):
    try:
        # print(vendors)
        response = cm.bulkVendorMaster(vendors)
        # print(response)
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
        # print(response)
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
        # print(response)
        if response.status_code != 200:
            lw.logBackUpRecord("Bulk Vendor Data has been uploaded with error.")
        else:
            lw.logBackUpRecord("Bulk Vendor Data has been uploaded Successfully.")
        pass
    except Exception as e:
        lw.logRecord("Error in creditDebitNote: " + str(e))

def payments(payments):
    try:
        # print(payments)
        response = cm.payments(payments)
        # print(response)
        if response.status_code != 200:
            lw.logBackUpRecord("Bulk Vendor Data has been uploaded with error.")
        else:
            lw.logBackUpRecord("Bulk Vendor Data has been uploaded Successfully.")
        pass
    except Exception as e:
        lw.logRecord("Error in payments: " + str(e))

def update_invoice(data, t, v, i, vi, da, dd, md):
    try:
        try:
            discount_account_id = data['discount_account_id']
        except:
            discount_account_id = ""

        if discount_account_id == "":
            discount_account_id = sd.discount_id

        diff = (datetime.strptime(md, '%Y-%m-%d')) - (datetime.strptime(data['date'], '%Y-%m-%d')).days
        json = {
            "discount_account_id": discount_account_id,
            "bill_id": i,
            "due_data": datetime.strptime(md, '%d-%m-%Y').strftime('%Y-%m-%d'),
            "payment_terms": diff,
            "payment_terms_label": "Net " + str(diff),
            "discount": float(da)
        }
        ZohoModel.update_invoice(i, json)
        postingAck(t, v, i, vi)
        pass
    except Exception as e:
        lw.logRecord("Error in update_invoice: " + str(e))


def postingAck(t, v, i, vi):
    try:
        json = {
            "transactionId": t,
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
        response = cm.postingAck(json)
        if response['status'] == 'Success':
            lw.logBackUpRecord('Posting of Bill has been acknowledged.')
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