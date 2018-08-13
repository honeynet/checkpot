from .test import *

import socket


class KippoErrorMessageBugTest(Test):

    name = "Kippo Error Message Bug Test"
    description = "Tests presence of an obsolte version of kippo"
    karma_value = 100
    doc_file = 'old_version_bugs.html'

    def run(self):
        """Check if content matches any known content"""

        target_ports = self.target_honeypot.get_service_ports('ssh', 'tcp')

        if not target_ports:
            self.set_result(TestResult.NOT_APPLICABLE, "No open ports found!")
            return

        for port in target_ports:

            # Based on research conducted by Andrew Morris and all following sources
            #
            # https://www.obscurechannel.com/x42/magicknumber.html
            # https://morris.sc/detecting-kippo-ssh-honeypots/
            # https://www.rapid7.com/db/modules/auxiliary/scanner/ssh/detect_kippo
            # https://kbyte.snowpenguin.org/portal/2013/04/30/kippo-protocol-mismatch-workaround/
            # http://www.hackinsight.org/news,155.html

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)

            try:
                s.connect((self.target_honeypot.ip, port))
                banner = s.recv(1024)  # TODO use banner?
                s.send(b'\n\n\n\n\n\n\n\n')
                response = s.recv(1024)
                s.close()
            except socket.error:
                self.set_result(TestResult.UNKNOWN, "Can't communicate with ports")
                return

            if b'168430090' in response:
                self.set_result(TestResult.WARNING, "Old unpatched version of Kippo detected,"
                                                    " please update to the latest version")
                return

            if b'bad packet length' in response:
                self.set_result(TestResult.WARNING, "Old unpatched version of Kippo detected,"
                                                    " please update to the latest version")
                return

            if b'Protocol mismatch' in response:
                self.set_result(TestResult.OK, "SSH protocol OK!")
                return

            self.set_result(TestResult.WARNING, "Reply is unknown, protocol not implemented correctly?")
