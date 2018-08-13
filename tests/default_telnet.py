from .test import *

from honeypots.honeypot import ScanFailure


class DefaultTelnetBannerTest(Test):

    name = "Default Telnet Banner Test"
    description = "Tests usage of default telnet banners"
    karma_value = 100
    doc_file = "default_banner.html"

    def run(self):
        """Check if content matches any known content"""

        known_banners = {
            b'\xff\xfb\x03\xff\xfb\x01\xff\xfd\x1f\xff\xfd\x18\r\nlogin: ': "telnetlogger",
            b'\xff\xfd\x1flogin: ': "cowrie",
            b'\xff\xfb\x01\xff\xfb\x03\xff\xfc\'\xff\xfe\x01\xff\xfd\x03\xff\xfe"\xff\xfd\'\xff\xfd\x18\xff\xfe\x1f': "mtpot",
            b'\xff\xfb\x01\xff\xfb\x03': "mtpot",
            b'\xff\xfb\x01': "mtpot",
            b'Debian GNU/Linux 7\r\nLogin: ': "honeypy"
        }

        target_ports = self.target_honeypot.get_service_ports('telnet', 'tcp')

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
                self.set_result(TestResult.OK, "No default banners. Found banner: ", banner)
