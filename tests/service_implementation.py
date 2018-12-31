import socket

from .test import *

import http


class SMTPTest(Test):
    """Tests SMTP service implementation"""

    name = "SMTP Test"
    description = "Tests SMTP service implementation"
    karma_value = 60
    doc_file = 'implementation.html'

    def run(self):
        """Verify service implements all methods in the SMTP specification"""

        target_ports = self.target_honeypot.get_service_ports('smtp', 'tcp')

        if target_ports:
            for port in target_ports:
                self.check_smtp_implemented(self.target_honeypot.ip, port)

                if self.result == TestResult.WARNING:
                    return
        else:
            self.set_result(TestResult.NOT_APPLICABLE, "Service not present")

    def check_smtp_implemented(self, server_address, port=25):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)

        try:
            s.connect((server_address, port))
        except socket.error as exception:
            self.set_result(TestResult.WARNING, "failed to connect to smtp server: ", exception.strerror)
            return

        recv = s.recv(1024)

        if recv[:3] != b'220':
            self.set_result(TestResult.WARNING, "220 response not received from smtp server")
            return
        else:
            self.set_result(TestResult.OK, "SMTP server OK")
            return


class HTTPTest(Test):
    """Tests HTTP service implementation"""

    name = "HTTP Test"
    description = "Tests HTTP service implementation"
    karma_value = 60
    doc_file = 'implementation.html'

    def run(self):
        """Verify service implements all methods in the HTTP specification"""

        target_ports = self.target_honeypot.get_service_ports('http', 'tcp')

        if target_ports:
            for port in target_ports:
                if port != 443:  # TODO separate https when nmap parses incorrectly
                    self.check_http_implemented(self.target_honeypot.ip, port)

                    if self.result == TestResult.WARNING:
                        return
        else:
            self.set_result(TestResult.NOT_APPLICABLE, "Service not present")

    def check_http_implemented(self, server_address, port=80):

        # try a simple http.client request first

        try:

            conn = http.client.HTTPConnection(server_address, port=port, timeout=5)
            conn.request('HEAD', '/')
            conn.getresponse()

            self.set_result(TestResult.OK, "HTTP implemented")

        except socket.timeout as e:
            self.set_result(TestResult.WARNING,"Connection Timeout", e.strerror)
            return
        
            # as a fallback measure run a manual test
            # TODO extend this

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)

            try:
                s.connect((server_address, port))
            except socket.error as exception:
                self.set_result(TestResult.WARNING, "failed to connect to http server: ", exception.strerror)
                return

            try:
                s.sendall(b'GET / HTTP/1.1\r\n\r\n')  # s.sendall(b'HEAD / HTTP/1.1\r\n\r\n')
            except socket.error as exception:
                self.set_result(TestResult.WARNING, "sending GET request to http server failed: ", exception.strerror)
                return

            try:
                recv = s.recv(4096)
            except Exception as e:
                self.set_result(TestResult.WARNING,"recv failed after GET request to HTTP sever", e.strerror)
                return

            if recv[:15] == b'HTTP/1.1 200 OK':
                self.set_result(TestResult.OK, "http service responded with 200/OK")
                return
            else:
                self.set_result(TestResult.WARNING, "http service responded with unknown sequence: ", recv)
                return
