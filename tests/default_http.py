from .test import *

from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import http
import ssl
import re
import hashlib


class DefaultStylesheetTest(Test):

    name = "Default Website Stylesheet Test"
    description = "Test unchanged website stylesheet"
    karma_value = 30
    doc_file = 'default_stylesheet.html'

    def run(self):
        """Check if content matches known content"""

        default_hashes = {
            '1118635ac91417296e67cd0f3e6f9927e5f502e328b92bb3888b3b789a49a257': "glastopf"
        }

        css = self.target_honeypot.get_websites_css()

        if not css:
            self.set_result(TestResult.NOT_APPLICABLE, "No stylesheet found")

        for style in css:

            if isinstance(style, bytes):
                hash_obj = hashlib.sha256(style)
            else:
                hash_obj = hashlib.sha256(style.encode())

            digest = hash_obj.hexdigest()

            if digest in default_hashes:
                self.set_result(TestResult.WARNING, "Default stylesheet used for", default_hashes[digest])

        if self.result == TestResult.UNKNOWN:
            self.set_result(TestResult.OK, "No default stylesheet matched")


class DefaultWebsiteTest(Test):

    name = "Default Website Test"
    description = "Test unchanged website content"
    karma_value = 60
    doc_file = 'default_website.html'

    def run(self):
        """Check if webpage has a known hash"""

        # TODO conpot has current time, hash everything except that?
        # TODO use bs4 and test partial hashes for such cases

        default_hashes = {
            'c59e04f46e25c454e65544c236abd9d71705cc4e5c4b4b7dc3ff83fec0e9402f': "shockpot",
            'd405fe3c5b902342565cbf5523bb44a78c6bfb15b38a40c81a5f7bf4d8eb7838': "honeything",
            '351190a71ddca564e471600c3d403fd8042e6888c8c6abe9cdfe536cef005e82': "dionaea",
            '576137c8755b80c0751baa18c8306465fa02c641c683caf8b6d19469a5b96b86': "amun"
        }

        sites = self.target_honeypot.get_websites()

        if not sites:
            self.set_result(TestResult.NOT_APPLICABLE, "No website found")

        for content in sites:

            if isinstance(content, bytes):
                hash_obj = hashlib.sha256(content)
            else:
                hash_obj = hashlib.sha256(content.encode())

            digest = hash_obj.hexdigest()

            if digest in default_hashes:
                self.set_result(TestResult.WARNING, "Default website used for", default_hashes[digest])

        if self.result == TestResult.UNKNOWN:
            self.set_result(TestResult.OK, "No default website matched")


class DefaultGlastopfWebsiteTest(Test):

    name = "Default Glastopf Website Content Test"
    description = "Test unchanged source for website content"
    karma_value = 60
    doc_file = 'default_glastopf_site.html'

    def run(self):
        """Check if content matches known content"""

        try:
            try:
                request = urllib.request.urlopen('http://www.gutenberg.org/files/42671/42671.txt', timeout=10)
            except:
                request = urllib.request.urlopen('http://www.gutenberg.org/files/42671/42671.txt', timeout=10)

            book = request.read().decode(request.headers.get_content_charset())

        except urllib.error.URLError:
            self.set_result(TestResult.UNKNOWN, 'failed to download gutenberg.org book content')
            return

        sites = self.target_honeypot.get_websites()

        if not sites:
            self.set_result(TestResult.NOT_APPLICABLE, "No website found")

        for content in sites:

            soup = BeautifulSoup(content, 'html.parser')

            article = soup.find('p')

            article = str(article)

            article = re.sub('</*p>', '', article)
            article = re.sub('<a.*?/a>', '---search---', article)

            items = article.split('---search---')

            total_items = len(items)
            matched_items = 0

            for item in items:
                if len(item) > 15 and item.strip(' ') in book:
                    matched_items += 1

            # if more than 20 percent of the content is found
            if matched_items > 0.2 * total_items:
                self.set_result(TestResult.WARNING, "Default Glastopf content source was used")
            else:
                self.set_result(TestResult.OK, "No default content found")


class CertificateValidationTest(Test):

    name = "Certificate Validation Test"
    description = "Check validity of SSL certificates"
    karma_value = 20
    doc_file = 'invalid_certificate.html'

    def run(self):
        """Check validity of SSL certificates"""

        # FIXME NMAP does not report https correctly when using -oX
        # target_ports = self.target_honeypot.get_service_ports('https', 'tcp')
        # target_ports += self.target_honeypot.get_service_ports('ssl/http', 'tcp')
        target_ports = []

        if self.target_honeypot.has_tcp(443):
            target_ports += [443]

        if not target_ports:
            self.set_result(TestResult.NOT_APPLICABLE, "Port 443 not open")
            return

        for port in target_ports:

            conn = http.client.HTTPSConnection(self.target_honeypot.ip, port=port, timeout=5)

            try:
                conn.request('GET', '/')
            except ssl.SSLError as e:
                if e.reason == "CERTIFICATE_VERIFY_FAILED":
                    self.set_result(TestResult.WARNING, "Certificate invalid for", self.target_honeypot.ip, ":", port)

                else:
                    self.set_result(TestResult.WARNING, "Other certificate error:", e.reason,
                                    "for", self.target_honeypot.ip, ":", port)
                return
            except Exception as e:
                self.set_result(TestResult.WARNING, "Connection failed with exception ", e)
                return

            self.set_result(TestResult.OK, "Certificates Valid")
