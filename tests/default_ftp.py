from .test import *

from honeypots.honeypot import ScanFailure


class DefaultFTPBannerTest(Test):

    name = "Default FTP Banner Test"
    description = "Tests usage of default service banners"
    karma_value = 100
    doc_file = "default_banner.html"

    def run(self):
        """Check if banner matches any known banner"""

        known_banners = {
            b'220 DiskStation FTP server ready.\r\n': "dionaea",
            b'220 Welcome to my FTP Server\r\n': "amun",
            b'220 BearTrap-ftpd Service ready\r\n': "beartrap"
        }

        target_ports = self.target_honeypot.get_service_ports('ftp', 'tcp')

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
