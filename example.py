from __init__ import Reporting
import pprint


CW_CONFIG = {
    'domain': 'my.instance.com',
    'CompanyId': 'somecompany',
    'IntegratorLoginId': 'admin',
    'IntegratorPassword': 'a4353^#gsdfgdin'
}


cwReporting = Reporting(CW_CONFIG)

results = cwReporting.RunReportQuery(reportName='Contact', limit=1)

pprint.pprint(results)