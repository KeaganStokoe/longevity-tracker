import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from main import createSummary

configuration = sib_api_v3_sdk.Configuration()
email_api_key = os.environ['sendinblue']
configuration.api_key['api-key'] = email_api_key

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
subject = "Exercise for longevity update"
html_content = "<html><body><h1 color='blue'>Here's your weekly exercise update 🏃‍♂️ </h1></body></html>" + createSummary()
sender = {"name":"Keagan Stokoe","email":"xilolabs@gmail.com"}
to = [{"email":"keagan.stokoe@gmail.com","name":"KMS"}]
headers = {"Some-Custom-Name":"unique-id-1234"}
params = {"parameter":"My param value","subject":"New Subject"}
send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, html_content=html_content, sender=sender, subject=subject)

try:
    api_response = api_instance.send_transac_email(send_smtp_email)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)