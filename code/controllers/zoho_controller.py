from models.zoho_model import ZohoModel
import controllers.cleartax_controller as cc
import views.logWriter as lw
from datetime import datetime
from itertools import zip_longest
import config as sd

class ZohoController:
    @staticmethod
    def get_fiscal_year(date):
        try:
            year = date.year
            if date.month < 4:  # Before April, it's part of the previous fiscal year
                return f"{year}"
            else:  # April onwards, it's the current fiscal year
                return f"{year+1}"
        except Exception as e:
            lw.logRecord("Error in get_fiscal_year: " + str(e))

    @staticmethod
    def get_contacts():
        """Fetch contacts and format response"""
        try:
            has_more_page = True
            page = 1
            customers = []
            vendors = []
            while (has_more_page == True):
                data = ZohoModel.fetch_contacts(page)
                page += 1

                if data['page_context']['has_more_page'] == 'false' or data['page_context']['has_more_page'] == False:
                    has_more_page = False

                if "contacts" in data and data["contacts"]:
                    for idx, item in enumerate(data['contacts'], start=1):
                        try:
                            if item['contact_type'] == "vendor":
                                # print(str(item['contact_id']))
                                details = ZohoModel.fetch_contacts_details(str(item['contact_id']))
                                msme_data = details['contact']['msme_type']
                                msme = ''
                                if msme_data != '':
                                    msme = 'MSME'
                                # if str(details['contact']['contact_id']) == '2362602000000054387':
                                #     pass
                                vendor = {
                                        "vendorID": details['contact']['contact_id'],
                                        "vendorName": details['contact']['company_name'],
                                        "keyContactPerson": str(details['contact']['contact_salutation']) + str(details['contact']['first_name']) + str(details['contact']['last_name']),
                                        "emailId": details['contact']['email'],
                                        "mobileNo": details['contact']['phone'],
                                        "panNumber": details['contact']['pan_no'],
                                        "address1": details['contact']['billing_address']['address'],
                                        "address2": details['contact']['billing_address']['street2'],
                                        "address3": '',#details['contact']['billing_address']['city'],
                                        "city": details['contact']['billing_address']['city'],
                                        "state": details['contact']['billing_address']['state'],
                                        "pinCode": details['contact']['billing_address']['zip'],
                                        "gstin": details['contact']['gst_no'],
                                        "createdDate": datetime.strptime((details['contact']['created_date']), '%d/%m/%Y').strftime('%Y-%m-%d'),
                                        "cin": '', #details['contact']['contact_name'],
                                        "companyClass": '', #details['contact']['contact_name'],
                                        "companyCategory": '', #details['contact']['contact_name'],
                                        "companySubCategory": '', #details['contact']['contact_name'],
                                        "userName": "api@eatgoods.com", #details['contact']['created_by_name'],
                                        "companyCode": sd.organization_id, #details['contact']['contact_name'],
                                        "companyCreationDate": '', #details['contact']['contact_name'],
                                        "category": msme
                                    }
                                vendors.append(vendor)
                        except Exception as e:
                            lw.logRecord("Error in get_contacts for loop: " + str(e))
                # print("Vendors" + str(vendors))
                # print("Customers" + str(customers))
                cc.bulkVendor(vendors)
                pass
            # return vendors#, customers
        except Exception as e:
            lw.logRecord("Error in get_contacts: " + str(e))

    @staticmethod
    def bulkInvoice():
        """Fetch Invoice and format response"""
        try:
            has_more_page = True
            page = 1
            invoices = []
            while (has_more_page == True):
                data = ZohoModel.fetch_bills(page)
                page += 1

                if data['page_context']['has_more_page'] == 'false' or data['page_context']['has_more_page'] == False:
                    has_more_page = False

                if "bills" in data and data["bills"]:
                    for idx, item in enumerate(data['bills'], start=1):
                        try:
                            if item['entity_type'] == "bill":
                                
                                # print(str(item['bill_id']))
                                details = ZohoModel.fetch_bill_details(str(item['bill_id']))
                                
                                reverse = 'N'
                                # print(details['bill']['is_reverse_charge_applied'])
                                if details['bill']['is_reverse_charge_applied'] != 'false' or details['bill']['is_reverse_charge_applied'] == False:
                                    reverse = 'Y'
                                companyCode = ''
                                ref1 = ''
                                ref2 = ''
                                for cust in details['bill']['custom_fields']:
                                    # if cust['bill']['label'] == 'Company Id':
                                    #     companyCode = cust['value']
                                    if cust['label'] == 'Customer Invoice Ref':
                                        ref1 = cust['value']
                                    elif cust['label'] == 'Vendor Invoice Date':
                                        inv_date = cust['value']
                                    elif cust['label'] == 'Invoice Acceptance Date':
                                        acp_date = cust['value']
                                
                                # for ref in details['salesorders']:
                                #     if ref['salesorder_number'] == details['reference_number']:
                                #         # ref1 = ref['reference_number']
                                #         ref2 = ref['shipment_date']
                                date =datetime.strptime(str(details['bill']['date']), "%Y-%m-%d") 
                                year = ZohoController.get_fiscal_year(date)
                                invoice = {
                                    "plantLocationID": details['bill']['destination_of_supply'],
                                    "gstin": details['bill']['gst_no'],
                                    "internalInvoiceNumber": details['bill']['bill_id'],
                                    "vendorInvoiceNumber": details['bill']['bill_number'],
                                    "invoiceDate": datetime.strptime((inv_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                                    "invoiceAcceptanceDate": datetime.strptime((acp_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                                    "dueDate": datetime.strptime((details['bill']['due_date']), '%Y-%m-%d').strftime('%d-%m-%Y'),
                                    "transactionAmount": details['bill']['total'],
                                    # "paymentNumber": "", #details['total'],
                                    "vendorId": details['bill']['vendor_id'],
                                    # "bookNumber": "", #details['total'],
                                    # "misc": "", #details['total'],
                                    # "ref1": ref1, #details['total'],
                                    # "ref2": ref2, #details['total'],
                                    # "ref3": "", #details['total'],
                                    # "commodityType": "Product", #details['total'],
                                    # "commodity": "", #details['total'],
                                    "fiscalYear": year,        
                                    # "companyCode": companyCode, #details['customer_custom_fields'],
                                    # "invoiceReversal": reverse,
                                    # "currency":details['bill']['currency_code'],
                                    # "irn": "", #details['total'],
                                    # "entryDate": datetime.strptime((details['bill']['date']), '%Y-%m-%d').strftime('%d-%m-%Y')                                   
                                    }
                                invoices.append(invoice)
                        except Exception as e:
                            lw.logRecord("Error in bulkInvoice for loop: " + str(e))
                    # print("Invoices" + str(invoices))
                    
                    cc.bulkInvoices(invoices)
                pass
            # return invoices
        except Exception as e:
            lw.logRecord("Error in bulkInvoice: " + str(e))

    @staticmethod
    def creditDebitNote():
        """Fetch contacts and format response"""
        try:
            has_more_page = True
            page = 1
            cns = []
            dns = []
            while (has_more_page == True):
                try:
                    data = ZohoModel.fetch_cn(page)
                    page += 1

                    if data['page_context']['has_more_page'] == 'false' or data['page_context']['has_more_page'] == False:
                        has_more_page = False
                    
                    if "creditnotes" in data and data["creditnotes"]:
                        for idx, item in enumerate(data['creditnotes'], start=1):
                        
                            try:
                                details = ZohoModel.fetch_cn_details(str(item['creditnotes_id']))
        
                                companyCode = ''
                                
                                date =datetime.strptime(str(details['date']), "%Y-%m-%d") 
                                year = ZohoController.get_fiscal_year(date)
                                cn = {
                                    "vendorId": details['creditnotes_id'],
                                    "vendorName": details['vendor_name'],
                                    "plantLocation": details['destination_of_supply'],
                                    "bookNumber": "", #details['reference_number'],
                                    "noteNumber": details['creditnotes_number'],
                                    "internalInvoiceNumber": details['creditnotes_number'],
                                    "vendorInvoiceNumber": "", #details['due_date'],
                                    "noteType": "CR",
                                    "noteDate": datetime.strptime((details['created_date']), '%d-%m-%Y').strftime('%Y-%m-%d'),
                                    "transactionAmount": details['total'],
                                    "ref1": details['notes'],
                                    "fiscalYear": year,        
                                    "companyCode": companyCode, #details['customer_custom_fields'],
                                    "currency":details['currency_code'],
                                    "irn": "", #details['total'],
                                    "entryDate": datetime.strptime((details['created_date']), '%d-%m-%Y').strftime('%Y-%m-%d')                                  
                                    }
                                cns.append(cn)
                            except Exception as e:
                                lw.logRecord("Error in creditDebitNote for loop: " + str(e))
                        # print("CN" + str(cns))
                        cc.creditDebitNote(dns)
                except Exception as e:
                    lw.logRecord("Error in creditDebitNote for CN: " + str(e))
            has_more_page = True
            page = 1       
            while (has_more_page == True):
                try:
                    data = ZohoModel.fetch_dn(page)
                    page += 1

                    if data['page_context']['has_more_page'] == 'false' or data['page_context']['has_more_page'] == False:
                        has_more_page = False
                    
                    if "vendor_credits" in data and data["vendor_credits"]:
                        for idx, item in enumerate(data['vendor_credits'], start=1):
                        
                            try:
                                details = ZohoModel.fetch_dn_details(str(item['vendor_credit_id']))
                                date =datetime.strptime(str(details['vendor_credit']['date']), "%Y-%m-%d") 
                                year = ZohoController.get_fiscal_year(date)
                                dn = {
                                "vendorId": details['vendor_credit']['vendor_credit_id'],
                                "vendorName": details['vendor_credit']['vendor_name'],
                                "plantLocation": details['vendor_credit']['destination_of_supply'],
                                "bookNumber": "", #details['vendor_credit']['reference_number'],
                                "noteNumber": details['vendor_credit']['vendor_credit_number'],
                                "internalInvoiceNumber": details['vendor_credit']['bill_id'],
                                "vendorInvoiceNumber": details['vendor_credit']['bill_number'],
                                "noteType": "DR",
                                "noteDate": datetime.strptime((details['vendor_credit']['date']), '%d-%m-%Y').strftime('%Y-%m-%d'),
                                "transactionAmount": details['vendor_credit']['total'],
                                "ref1": details['vendor_credit']['notes'],
                                "fiscalYear": year,        
                                "companyCode": companyCode, #details['vendor_credit']['customer_custom_fields'],
                                "currency":details['vendor_credit']['currency_code'],
                                "irn": "", #details['vendor_credit']['total'],
                                "entryDate": datetime.strptime((details['vendor_credit']['created_date']), '%d-%m-%Y').strftime('%Y-%m-%d')  ##############################                                
                                }
                                dns.append(dn)
                            except Exception as e:
                                lw.logRecord("Error in creditDebitNote for DN for loop: " + str(e))    
                        # print("DN" + str(dns))
                        
                        cc.creditDebitNote(dns)
                except Exception as e:
                    lw.logRecord("Error in creditDebitNote for DN: " + str(e))
            pass
            # return invoices
        except Exception as e:
            lw.logRecord("Error in fetch_contacts: " + str(e))

    @staticmethod
    def payments():
        """Fetch Invoice and format response"""
        try:
            has_more_page = True
            page = 1
            payments = []
            while (has_more_page == True):
                data = ZohoModel.fetch_payments(page)
                page += 1

                if data['page_context']['has_more_page'] == 'false' or data['page_context']['has_more_page'] == False:
                    has_more_page = False

                if "vendorpayments" in data and data["vendorpayments"]:
                    for idx, item in enumerate(data['vendorpayments'], start=1):
                        try:
                            details = ZohoModel.fetch_payments_details(str(item['payment_id']))
                            # msme_data = details['invoices']['msme_type']
                            reverse = 'N'
                            if details['vendorpayment']['is_reverse_charge_applied'] != 'false' or details['vendorpayment']['is_reverse_charge_applied'] == False:
                                reverse = 'Y'
                            companyCode = ''
                            ref1 = ''
                            ref2 = ''
                            # for cust in details['custom_fields']:
                            #     if cust['label'] == 'Company Id':
                            #         companyCode = cust['value']
                            #     elif cust['label'] == 'Customer Invoice Ref':
                            #         ref1 = cust['value']
                            
                            # for ref in details['salesorders']:
                            #     if ref['salesorder_number'] == details['reference_number']:
                            #         # ref1 = ref['reference_number']
                            #         ref2 = ref['shipment_date']
                            date =datetime.strptime(str(details['vendorpayment']['date']), "%Y-%m-%d") 
                            year = ZohoController.get_fiscal_year(date)
                            payment = {
                                "vendorId": details['vendorpayment']['vendor_id'],
                                "vendorName": details['vendorpayment']['vendor_name'],
                                "plantLocation": details['vendorpayment']['destination_of_supply'],
                                "bookNumber": "", #details['vendorpayment']['reference_number'],
                                "paymentsNumber": details['vendorpayment']['payment_number'],
                                "internalInvoiceNumber": details['vendorpayment']['bills'][0]['bill_id'],
                                "vendorInvoiceNumber": details['vendorpayment']['bills'][0]['bill_number'],
                                "paymentType": details['vendorpayment']['transfer_type'],
                                "paymentDate": datetime.strptime((details['vendorpayment']['date']), '%Y-%m-%d').strftime('%d-%m-%Y'), #details['vendorpayment']['total'],
                                "invoiceAmount": details['vendorpayment']['amount'],
                                "paymentAmount": details['vendorpayment']['total_payment_amount'],
                                "fiscalYear": year,        
                                "companyCode": companyCode, #details['vendorpayment']['customer_custom_fields'],
                                "currency":details['vendorpayment']['currency_code']                                   
                                }
                            payments.append(payment)
                        except Exception as e:
                            lw.logRecord("Error in payments for loop: " + str(e))
                    # print("Invoices" + str(payments))
                    
                    cc.payments(payment)
                pass
            # return payment
        except Exception as e:
            lw.logRecord("Error in payments: " + str(e))

    @staticmethod
    def update_invoice(trns_id, vend_id, int_inv_no, ven_int_no, dis_amt, dis_date, mat_date):
        try:
            for t, v, i, vi, da, dd, md in zip_longest(trns_id, vend_id, int_inv_no, ven_int_no, dis_amt, dis_date, mat_date, fillvalue="NA"):
                data = ZohoModel.fetch_bill_details(i)
                cc.update_invoice(data['bill'], t, v, i, vi, da, dd, md)
        except Exception as e:
            lw.logRecord("Error in payments: " + str(e))