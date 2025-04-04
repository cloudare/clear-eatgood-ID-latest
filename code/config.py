import json


dataJSON = '''{
				"clientName":"Eatgood",
				"serviceName":"Cloudare",
			}'''
# serverData = json.loads(dataJSON)


#URL
# zoho_access_token   = 'https://accounts.zoho.in/oauth/v2/token?grant_type=authorization_code&'
zoho_refresh_token  = 'https://accounts.zoho.in/oauth/v2/token?'
zoho_contact    	= 'https://www.zohoapis.in/books/v3/contacts'
zoho_bills		= 'https://www.zohoapis.in/books/v3/bills'
zoho_cn		= 'https://www.zohoapis.in/books/v3/creditnotes'
zoho_dn		= 'https://www.zohoapis.in/books/v3/vendorcredits'
zoho_payments		= 'https://www.zohoapis.in/books/v3/vendorpayments'
# zoho_updates 		= ''
discount_id			= '1652083000000804258' 

# Cleartax urls
clear_api_url 		= 'https://xpedize-invoice-manager-sandbox-http.internal.cleartax.co/invoicemanager/api' 

#Cleartax Token
authorization = ''

#Cleartax credentials
userName = 'api@eatgoods.com'
password = 'Eat@12345'
        
#Who column fixed value
createdBy = 'Cloudare'
updatedBy = 'Cloudare' 

# Zoho details
organization_id = '60028841364'
client_id       = '1000.A3SBX7MWZ1NO0M5EGBQWJ5YRRP4O3O'
client_secret   = 'f0bd80916afcc31706fc116a973584297e79ddaad1'
refresh_token   = '1000.2a59689ac60f3ea765b39f27a9ea78ff.b60dfa6d2df181adf1ed9ecab76157d8'
access_token    = '1000.e930fa7d271ab5b8f505a9a7ad9a839b.4979b7594abb062a893e3ba10050119e'

