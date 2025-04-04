from models.zoho_model import ZohoModel
import controllers.cleartax_controller as cc
import views.logWriter as lw
from datetime import datetime
from itertools import zip_longest

class ZohoController:
    @staticmethod
    def get_fiscal_year(date):
        # if date is None:
        #     date = datetime.strptime('2025-04-21', "%Y-%m-%d") 
        
        year = date.year
        if date.month < 4:  # Before April, it's part of the previous fiscal year
            return f"{year}"
        else:  # April onwards, it's the current fiscal year
            return f"{year+1}"

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
                        if item['contact_type'] == "vendor":
                            # print("vendor:" + str(item['contact_name']))
                            # print("vendor:" + str(item['contact_id']))
                            details = ZohoModel.fetch_contacts_details(str(item['contact_id']))
                            msme_data = details['contact']['msme_type']
                            msme = ''
                            if msme_data != '':
                                msme = 'MSME'
                            if str(details['contact']['contact_id']) == '2362602000000054387':
                                pass
                            vendor = {
                                    "vendorID": details['contact']['contact_id'],
                                    "vendorName": details['contact']['company_name'],
                                    "keyContactPerson": str(details['contact_salutation']) + str(details['first_name']) + str(details['last_name']),
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
                                    "createdDate": datetime.strptime((details['contact']['created_date']), '%d-%m-%Y').strftime('%Y-%m-%d'),
                                    "cin": '', #details['contact']['contact_name'],
                                    "companyClass": '', #details['contact']['contact_name'],
                                    "companyCategory": '', #details['contact']['contact_name'],
                                    "companySubCategory": '', #details['contact']['contact_name'],
                                    "userName": "api@eatgoods.com", #details['contact']['created_by_name'],
                                    "companyCode": '60038636921', #details['contact']['contact_name'],
                                    "companyCreationDate": '', #details['contact']['contact_name'],
                                    "category": msme
                                }
                            vendors.append(vendor)
                        # elif item['contact_type'] == "customer":
                        #     # print("customer:" + str(item['contact_name']))
                        #     # print("customer:" + str(item['contact_id']))
                        #     details = ZohoModel.fetch_contacts_details(str(item['contact_id']))
                        #     msme_data = details['contact']['msme_type']
                        #     msme = ''
                        #     if msme_data != '':
                        #         msme = 'MSME'
                            
                        #     customer = {
                        #             "vendorID": details['contact']['contact_id'],
                        #             "vendorName": details['contact']['company_name'],
                        #             "keyContactPerson": details['contact']['contact_name'],
                        #             "emailId": details['contact']['email'],
                        #             "mobileNo": details['contact']['phone'],
                        #             "panNumber": details['contact']['pan_no'],
                        #             "address1": details['contact']['billing_address']['address'],
                        #             "address2": details['contact']['billing_address']['street2'],
                        #             "address3": '',#details['contact']['billing_address']['city'],
                        #             "city": details['contact']['billing_address']['city'],
                        #             "state": details['contact']['billing_address']['state'],
                        #             "pinCode": details['contact']['billing_address']['zip'],
                        #             "gstin": details['contact']['gst_no'],
                        #             "createdDate": details['contact']['created_date'],
                        #             "cin": '', #details['contact']['contact_name'],
                        #             "companyClass": '', #details['contact']['contact_name'],
                        #             "companyCategory": '', #details['contact']['contact_name'],
                        #             "companySubCategory": '', #details['contact']['contact_name'],
                        #             "userName": details['contact']['created_by_name'],
                        #             "companyCode": '60038636921', #details['contact']['contact_name'],
                        #             "companyCreationDate": '', #details['contact']['contact_name'],
                        #             "category": msme
                        #         }
                        #     customers.append(customer)
                print("Vendors" + str(vendors))
                # print("Customers" + str(customers))
                cc.bulkVendor(vendors)
                pass
            # return vendors#, customers
        except Exception as e:
            lw.logRecord("Error in fetch_contacts: " + str(e))

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
                        if item['entity_type'] == "bill":
                            # print("vendor:" + str(item['contact_name']))
                            # print("vendor:" + str(item['contact_id']))
                            details = ZohoModel.fetch_bill_details(str(item['bill_id']))
                            # msme_data = details['invoices']['msme_type']
                            reverse = 'N'
                            if details['is_reverse_charge_applied'] != 'false' or details['is_reverse_charge_applied'] == False:
                                reverse = 'Y'
                            companyCode = ''
                            ref1 = ''
                            ref2 = ''
                            for cust in details['customer_custom_fields']:
                                if cust['label'] == 'Company Id':
                                    companyCode = cust['value']
                                elif cust['label'] == 'Customer Invoice Ref':
                                    ref1 = cust['value']
                                elif cust['label'] == 'Vendor Invoice Date':
                                    inv_date = cust['value']
                                elif cust['label'] == 'Invoice Acceptance Date':
                                    acp_date = cust['value']
                            
                            # for ref in details['salesorders']:
                            #     if ref['salesorder_number'] == details['reference_number']:
                            #         # ref1 = ref['reference_number']
                            #         ref2 = ref['shipment_date']
                            date =datetime.strptime(str(details['date']), "%Y-%m-%d") 
                            year = ZohoController.get_fiscal_year(date)
                            invoice = {
                                "plantLocationID": details['destination_of_supply'],
                                "gstin": details['gst_no'],
                                "internalInvoiceNumber": details['bill_id'],
                                "vendorInvoiceNumber": details['bill_number'],
                                "invoiceDate": datetime.strptime((inv_date), '%d-%m-%Y').strftime('%Y-%m-%d'),
                                "invoiceAcceptanceDate": datetime.strptime((acp_date), '%d-%m-%Y').strftime('%Y-%m-%d'),
                                "dueDate": datetime.strptime((details['due_date']), '%d-%m-%Y').strftime('%Y-%m-%d'),
                                "transactionAmount": details['total'],
                                "paymentNumber": "", #details['total'],
                                "vendorId": details['vendor_id'],
                                "bookNumber": "", #details['total'],
                                "misc": "", #details['total'],
                                "ref1": ref1, #details['total'],
                                "ref2": ref2, #details['total'],
                                "ref3": "", #details['total'],
                                "commodityType": "Product", #details['total'],
                                "commodity": "", #details['total'],
                                "fiscalYear": year,        
                                "companyCode": companyCode, #details['customer_custom_fields'],
                                "invoiceReversal": reverse,
                                "currency":details['currency_code'],
                                "irn": "", #details['total'],
                                "entryDate": datetime.strptime((details['created_date']), '%d-%m-%Y').strftime('%Y-%m-%d')                                   
                                }
                            invoices.append(invoice)
                    print("Invoices" + str(invoices))
                    
                    cc.bulkInvoices(invoices)
                pass
            # return invoices
        except Exception as e:
            lw.logRecord("Error in fetch_contacts: " + str(e))

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
                        
                            # print("vendor:" + str(item['contact_name']))
                            # print("vendor:" + str(item['contact_id']))
                            details = ZohoModel.fetch_cn_details(str(item['creditnotes_id']))
                            # msme_data = details['invoices']['msme_type']
                            # reverse = 'N'
                            # if details['is_reverse_charge_applied'] != 'false' or details['is_reverse_charge_applied'] == False:
                            #     reverse = 'Y'
                            companyCode = ''
                            # for cust in details['customer_custom_fields']:
                            #     if cust['label'] == 'Company Id':
                            #         companyCode = cust['value']
                            ref1 = ''
                            # ref2 = ''
                            # for ref in details['salesorders']:
                            #     if ref['salesorder_number'] == details['reference_number']:
                            #         ref1 = ref['reference_number']
                            #         ref2 = ref['shipment_date']
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
                        print("CN" + str(cns))
                        cc.creditDebitNote(dns)
                except Exception as e:
                    lw.logRecord("Error in creditDebitNote for CN: " + str(e))
                    
            while (has_more_page == True):
                try:
                    data = ZohoModel.fetch_dn(page)
                    page += 1

                    if data['page_context']['has_more_page'] == 'false' or data['page_context']['has_more_page'] == False:
                        has_more_page = False
                    
                    if "vendor_credit" in data and data["vendor_credit"]:
                        for idx, item in enumerate(data['vendor_credit'], start=1):
                        
                            # print("vendor:" + str(item['contact_name']))
                            # print("vendor:" + str(item['contact_id']))
                            details = ZohoModel.fetch_dn_details(str(item['vendor_credit']))
                            # msme_data = details['invoices']['msme_type']
                            # reverse = 'N'
                            # if details['is_reverse_charge_applied'] != 'false' or details['is_reverse_charge_applied'] == False:
                            #     reverse = 'Y'
                            # companyCode = ''
                            # for cust in details['customer_custom_fields']:
                            #     if cust['label'] == 'Company Id':
                            #         companyCode = cust['value']
                            # ref1 = ''
                            # ref2 = ''
                            # for ref in details['salesorders']:
                            #     if ref['salesorder_number'] == details['reference_number']:
                            #         ref1 = ref['reference_number']
                            #         ref2 = ref['shipment_date']
                            date =datetime.strptime(str(details['date']), "%Y-%m-%d") 
                            year = ZohoController.get_fiscal_year(date)
                            dn = {
                            "vendorId": details['vendor_credit_id'],
                            "vendorName": details['vendor_name'],
                            "plantLocation": details['destination_of_supply'],
                            "bookNumber": "", #details['reference_number'],
                            "noteNumber": details['vendor_credit_number'],
                            "internalInvoiceNumber": details['bill_id'],
                            "vendorInvoiceNumber": details['bill_number'],
                            "noteType": "DR",
                            "noteDate": datetime.strptime((details['date']), '%d-%m-%Y').strftime('%Y-%m-%d'),
                            "transactionAmount": details['total'],
                            "ref1": details['notes'],
                            "fiscalYear": year,        
                            "companyCode": companyCode, #details['customer_custom_fields'],
                            "currency":details['currency_code'],
                            "irn": "", #details['total'],
                            "entryDate": datetime.strptime((details['created_date']), '%d-%m-%Y').strftime('%Y-%m-%d')  ##############################                                
                            }
                            dns.append(dns)
                        print("DN" + str(dns))
                        
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

                if "vendorpayment" in data and data["vendorpayment"]:
                    for idx, item in enumerate(data['vendorpayment'], start=1):
                        
                        # print("vendor:" + str(item['contact_name']))
                        # print("vendor:" + str(item['contact_id']))
                        details = ZohoModel.fetch_payments_details(str(item['vendorpayment']))
                        # msme_data = details['invoices']['msme_type']
                        reverse = 'N'
                        if details['is_reverse_charge_applied'] != 'false' or details['is_reverse_charge_applied'] == False:
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
                        date =datetime.strptime(str(details['date']), "%Y-%m-%d") 
                        year = ZohoController.get_fiscal_year(date)
                        payment = {
                            "vendorId": details['vendor_id'],
                            "vendorName": details['vendor_name'],
                            "plantLocation": details['destination_of_supply'],
                            "bookNumber": "", #details['reference_number'],
                            "paymentsNumber": details['payment_number'],
                            "internalInvoiceNumber": details['bills'][0]['bill_id'],
                            "vendorInvoiceNumber": details['bills'][0]['bill_number'],
                            "paymentType": details['transfer_type'],
                            "paymentDate": datetime.strptime((details['date']), '%d-%m-%Y').strftime('%Y-%m-%d'), #details['total'],
                            "invoiceAmount": details['amount'],
                            "paymentAmount": details['total_payment_amount'],
                            "fiscalYear": year,        
                            "companyCode": companyCode, #details['customer_custom_fields'],
                            "currency":details['currency_code']                                   
                            }
                        payments.append(payment)
                    print("Invoices" + str(payments))
                    
                    cc.payments(payment)
                pass
            # return payment
        except Exception as e:
            lw.logRecord("Error in payments: " + str(e))

    @staticmethod
    def update_invoice(trns_id, vend_id, int_inv_no, ven_int_no, dis_amt, dis_date, mat_date):
        try:
            for t, v, i, vi, da, dd, md in zip_longest(trns_id, vend_id, int_inv_no, ven_int_no, dis_amt, dis_date, mat_date, fillvalue="NA"):
                data = ZohoModel.fetch_bill_details(t)
                cc.update_invoice(data['bill'], t, v, i, vi, da, dd, md)
        except Exception as e:
            lw.logRecord("Error in payments: " + str(e))