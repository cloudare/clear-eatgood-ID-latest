from models.zoho_model import ZohoModel
from controllers.zoho_controller import ZohoController
import views.logWriter as lw
import controllers.cleartax_controller as cc
# import sql_gen as sg

def mainProcess():
    try:
        ZohoController.get_contacts()
        ZohoController.bulkInvoice()
        ZohoController.creditDebitNote()
        ZohoController.payments()
        trns_id, vend_id, int_inv_no, ven_int_no, dis_amt, dis_date, matdate = cc.postingCreditDebitNote()
        if trns_id:
            ZohoController.update_invoice(trns_id, vend_id, int_inv_no, ven_int_no, dis_amt, dis_date, matdate)
    except Exception as e: 
        print(str(e))
        lw.logRecord(f"Error in mainProcess:{str(e)}")
