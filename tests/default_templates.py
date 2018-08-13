from .test import *
from honeypots.honeypot import ScanFailure


class DefaultTemplateFileTest(Test):

    name = "Default Template File Test"
    description = "Tests usage of default running templates"
    karma_value = 100
    doc_file = 'default_template.html'

    def run(self):
        """Check if content matches any known content"""

        target_ports = self.target_honeypot.get_service_ports('iso-tsap', 'tcp')
        target_ports += self.target_honeypot.get_service_ports('s7-comm', 'tcp')

        if not target_ports:
            self.set_result(TestResult.NOT_APPLICABLE, "iso-tsap / s7-comm service not present in scan results")

        for port in target_ports:

            try:
                info = self.target_honeypot.run_nmap_script('s7-info.nse', port)
            except ScanFailure:
                self.set_result(TestResult.UNKNOWN, "Failed to run s7-info.nse script")
                return

            parsed = info.split('\n  ')[1:]

            default1 = ['Version: 0.0', 'System Name: Technodrome',
                        'Module Type: Siemens, SIMATIC, S7-200',
                        'Serial Number: 88111222',
                        'Plant Identification: Mouser Factory',
                        'Copyright: Original Siemens Equipment']

            matched = 0

            for a, b in zip(parsed, default1):
                if a == b:
                    matched += 1

            if matched > 0:
                self.set_result(TestResult.WARNING, "Template used for s7-comm service matches default ",
                                matched/len(default1)*100, "percent")
                return

            self.set_result(TestResult.OK, "s7-comm service does not match any default configurations")
