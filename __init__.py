from suds.client import Client
import json
import pprint


'''

    from cwsdk import Reporting

    # Config should look something like this:
    CW_CONFIG = {
        'domain': 'my.instance.com',
        'CompanyId': 'somecompany',
        'IntegratorLoginId': 'admin',
        'IntegratorPassword': 'a4353^#gsdfgdin'
    }


    cwReporting = Reporting(CW_CONFIG)

    results = cwReporting.RunReportQuery('Contact'))

    print results

'''



def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

class ConnectWiseSDK:
    url = "https://%s/v4_6_release/apis/1.5/%s.asmx?wsdl"
    domain = ''
    api = ''
    CompanyId = ''
    IntegratorLoginId = ''
    IntegratorPassword = ''
    client = {}

    def __init__(self, config={}):
        if self.api == '':
            raise Exception("ConnectWise SDK Internal: Please specify  an api endpoint in your class")

        # Check Config
        if 'domain' in config:
            self.domain = config['domain']
        else:
            raise Exception("ConnectWise SDK Config: Must specify a domain")
        

        if 'CompanyId' in config:
            self.CompanyId = config['CompanyId']
        else:
            raise Exception("ConnectWise SDK Config: Must specify a CompanyId")
        

        if 'IntegratorLoginId' in config:
            self.IntegratorLoginId = config['IntegratorLoginId']
        else:
            raise Exception("ConnectWise SDK Config: Must specify a IntegratorLoginId")
        

        if 'IntegratorPassword' in config:
            self.IntegratorPassword = config['IntegratorPassword']
        else:
            raise Exception("ConnectWise SDK Config: Must specify a IntegratorPassword")

        self.credentials = {
            'CompanyId': self.CompanyId,
            'IntegratorLoginId': self.IntegratorLoginId,
            'IntegratorPassword': self.IntegratorPassword
        }

        self.client = Client("https://cw.connectwise.net/v4_6_release/apis/1.5/ReportingAPI.asmx?wsdl")


    def getURL(self):
        return self.url % (self.domain, self.api)




class Reporting(ConnectWiseSDK):
    api = 'ReportingAPI'

    def RunReportQuery(self, reportName, conditions='', orderBy=None, limit=1000, skip=0):

        response = self.client.service.RunReportQuery(credentials=self.credentials, 
                                                        reportName=reportName, 
                                                        conditions=conditions, 
                                                        orderBy=orderBy, 
                                                        limit=limit, 
                                                        skip=skip)

        results = []
        
        for result in response['ResultRow']:
            tmp = {}

            for field in result['Value']:
                # only need the Value values lolz
                if str(field.__class__) == 'suds.sudsobject.Value':
                    if field['_Type'] == 'Numeric':
                        tmp[field['_Name']] = float(field['value'])
                    if field['_Type'] == 'Boolean':
                        tmp[field['_Name']] = str2bool(field['value'])
                    else:
                        tmp[field['_Name']] = field['value']

            results.append(tmp)
        

        return results