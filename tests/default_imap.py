from .test import *

from honeypots.honeypot import ScanFailure


class DefaultIMAPBannerTest(Test):

    name = "Default IMAP Banner Test"
    description = "Tests usage of default IMAP banners"
    karma_value = 90
    doc_file = "default_banner.html"

    def run(self):
        """Check if content matches any known content"""

        known_banners = {
            b'a200 Lotus Domino 6.5.4 7.0.2 IMAP4\r\n': "amun"
        }

        target_ports = self.target_honeypot.get_service_ports('imap', 'tcp')

        if not target_ports:
            self.set_result(TestResult.NOT_APPLICABLE, "No open ports found!")
            return

        for port in target_ports:

            try:
                banner = self.target_honeypot.get_banner(port, protocol='tcp')
            except ScanFailure as e:
                self.set_result(TestResult.UNKNOWN, e)
                continue

            if banner in known_banners:
                self.set_result(TestResult.WARNING, "Default", known_banners[banner], "banner used")
                return
            else:
                self.set_result(TestResult.OK, "No default banners")
