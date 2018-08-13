# Checkpot - Honeypot Checker
# Copyright (C) 2018  Vlad Florea
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# DISCLAIMER: All prerequisites (containers, additional programs, etc.)
# and libraries that might be needed to run this program are property
# of their original authors and carry their own separate licenses that
# you should read to inform yourself about their terms.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# As this software is PROVIDED WITH ABSOLUTELY NO WARRANTY OF ANY KIND,
# YOU USE THIS SOFTWARE AT YOUR OWN RISK!
#
# By using this tool YOU TAKE FULL LEGAL RESPONSIBILITY FOR ANY
# POSSIBLE OUTCOME.
#
# We strongly recommend that you read all the information in the README.md
# file (found in the root folder of this project) and even the
# documentation (which you can find locally in the /docs/ folder or
# at http://checkpot.readthedocs.io/) to make sure you fully
# understand how this tool works and consult all laws that apply
# to your use case.
#
# We strongly suggest that you keep this notice intact for all files.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# The local copy of the license should be located in the root folder of the app
# in the file gpl-3.0.txt.
#
# You can contact the author and team at any time via the Checkpot official
# GitHub page: https://github.com/honeynet/checkpot or via the Honeynet
# official Slack channel: https://gsoc-slack.honeynet.org/ or
#                         https://honeynetpublic.slack.com/
#
# You can contact us at any time and with any question, we are here to help!
#
# If you consider any information in this copyright notice might be incorrect,
# outdated, arises any questions, raises any problems, etc. please contact us
# and we will make it our top priority to fix it. We have the deepest respect
# for the work of all authors and for all of our users.

import time
import sys
from termcolor import colored, cprint
from datetime import timedelta

from containers.manager import Manager
from honeypots.honeypot import Honeypot
from tests.test import Test
from tests.test import TestResult
from tests.test_platform import TestPlatform

import argv_parser

from tests import *


manager = Manager(verbose=True, build_info=False)


def honeypot_test(container_name, tests, port_range=None):
    """
    Starts a container and runs a list of tests against it.
    Compares results with the expected results.
    Stops the container.

    :param container_name: target container
    :param tests: dict of Test objects and expected TestResult pairs
    :param port_range: specify a custom port range for scan (e.g '20-100')
    :return: boolean representing test pass/failure
    """

    test_list = [key for key in tests]
    expected_results = [tests[key] for key in tests]

    assert all(isinstance(test, Test) for test in test_list)
    assert all(isinstance(result, TestResult) for result in expected_results)

    manager.start_honeypot(container_name)

    time.sleep(10)  # TODO wait for container to start, catch some sort of signal

    hp = Honeypot(manager.get_honeypot_ip(container_name), scan_os=False, verbose_scan=False)

    print(">", colored("Collecting data ...", color="yellow"))
    print("> Test", colored(container_name, color="yellow"), "started at:",
          colored(time.strftime("%H:%M:%S", time.gmtime()), color="blue"))

    start_time = time.time()

    if port_range:
        hp.scan(port_range)
    else:
        hp.scan()

    print(">", colored("Running tests ...", color="yellow"))
    tp = TestPlatform(test_list, hp)

    tp.run_tests()

    manager.stop_honeypot(container_name)

    for i, result in enumerate(tp.results):

        tname, treport, tresult, tkarma = result

        if expected_results[i] != tresult:
            print("Test ", colored(container_name, color="yellow"), "->", colored("FAILED:", color="red"))
            print("\ttest:", tname, " -> expected ", expected_results[i], " got ", tresult, " instead!\n", treport)
            print("> Test ended at:", colored(time.strftime("%H:%M:%S", time.gmtime()), color="blue"))
            end_time = time.time()
            print("Elapsed time =", colored(timedelta(seconds=end_time - start_time), color="blue"), "\n")
            sys.exit(1)  # exit failure

    print("Test ", container_name, "->", colored("PASSED", color="green"))

    print("> Test ended at:", colored(time.strftime("%H:%M:%S", time.gmtime()), color="blue"))
    end_time = time.time()
    print("Elapsed time =", colored(timedelta(seconds=end_time - start_time), color="blue"), "\n")


def interface_test():
    """Test argument parsing"""
    print("Testing argument parser ...")

    # TODO add tests for long options too

    parsed = argv_parser.parse(['checkpot.py', '-t', '172.17.0.2', '-O', '-p', '20-100,102'])
    expected = {'target': '172.17.0.2', 'scan_os': True, 'scan_level': 5, 'port_range': '20-100,102', 'fast': False,
                'brief': False}

    if parsed != expected:
        print("ERROR: parsed != expected")
        sys.exit(1)

    parsed = argv_parser.parse(['checkpot.py', '-t', '172.17.0.2', '-p', '20-1000'])
    expected = {'target': '172.17.0.2', 'scan_os': False, 'scan_level': 5, 'port_range': '20-1000', 'fast': False,
                'brief': False}

    if parsed != expected:
        print("ERROR: parsed != expected")
        sys.exit(1)

    parsed = argv_parser.parse(['checkpot.py', '-t', '172.17.0.2', '-O', '-l', '3'])
    expected = {'target': '172.17.0.2', 'scan_os': True, 'scan_level': 3, 'port_range': None, 'fast': False,
                'brief': False}

    if parsed != expected:
        print("ERROR: parsed != expected")
        sys.exit(1)

    parsed = argv_parser.parse(['checkpot.py', '-O', '-t', '172.17.0.2', '-l', '3', '-f'])
    expected = {'target': '172.17.0.2', 'scan_os': True, 'scan_level': 3, 'port_range': None, 'fast': True,
                'brief': False}

    if parsed != expected:
        print("ERROR: parsed != expected")
        sys.exit(1)

    parsed = argv_parser.parse(['checkpot.py', '-O', '-t', '172.17.0.2', '-l', '3'])
    expected = {'target': '172.17.0.2', 'scan_os': True, 'scan_level': 3, 'port_range': None, 'fast': False,
                'brief': False}

    if parsed != expected:
        print("ERROR: parsed != expected")
        sys.exit(1)

    print("OK")


def main():
    """
    Entry point for the Continuous Integration tools.
    Write all tests here.
    """

    print(
        "Checkpot - Honeypot Checker, Copyright (C) 2018  Vlad Florea\n"
        "This program comes with ABSOLUTELY NO WARRANTY; for details\n"
        "run `python checkpot.py --show w`.\n"
        "This is free software, and you are welcome to redistribute it\n"
        "under certain conditions; run `python checkpot.py --show c` for details.\n"
    )

    # test amun
    honeypot_test('amun',
                  {
                      direct_fingerprinting.DirectFingerprintTest(): TestResult.WARNING,
                      direct_fingerprinting.DefaultServiceCombinationTest(): TestResult.WARNING,
                      direct_fingerprinting.DuplicateServicesCheck(): TestResult.WARNING,
                      default_ftp.DefaultFTPBannerTest(): TestResult.WARNING,
                      service_implementation.HTTPTest(): TestResult.OK,
                      default_http.DefaultWebsiteTest(): TestResult.WARNING,
                      default_http.DefaultGlastopfWebsiteTest(): TestResult.OK,
                      default_http.DefaultStylesheetTest(): TestResult.NOT_APPLICABLE,
                      default_http.CertificateValidationTest(): TestResult.WARNING,
                      default_imap.DefaultIMAPBannerTest(): TestResult.WARNING,
                      default_smtp.DefaultSMTPBannerTest(): TestResult.WARNING,
                      service_implementation.SMTPTest(): TestResult.OK,
                      default_telnet.DefaultTelnetBannerTest(): TestResult.UNKNOWN,
                      old_version_bugs.KippoErrorMessageBugTest(): TestResult.NOT_APPLICABLE,
                      default_templates.DefaultTemplateFileTest(): TestResult.NOT_APPLICABLE
                  },
                  port_range='-')

    # test artillery
    honeypot_test('artillery',
                  {
                      direct_fingerprinting.DirectFingerprintTest(): TestResult.OK,
                      direct_fingerprinting.DefaultServiceCombinationTest(): TestResult.WARNING,
                      direct_fingerprinting.DuplicateServicesCheck(): TestResult.OK,
                      default_ftp.DefaultFTPBannerTest(): TestResult.OK,
                      service_implementation.HTTPTest(): TestResult.NOT_APPLICABLE,
                      default_http.DefaultWebsiteTest(): TestResult.NOT_APPLICABLE,
                      default_http.DefaultGlastopfWebsiteTest(): TestResult.NOT_APPLICABLE,
                      default_http.DefaultStylesheetTest(): TestResult.NOT_APPLICABLE,
                      default_http.CertificateValidationTest(): TestResult.NOT_APPLICABLE,
                      default_imap.DefaultIMAPBannerTest(): TestResult.NOT_APPLICABLE,
                      default_smtp.DefaultSMTPBannerTest(): TestResult.OK,
                      service_implementation.SMTPTest(): TestResult.WARNING,
                      default_telnet.DefaultTelnetBannerTest(): TestResult.NOT_APPLICABLE,
                      old_version_bugs.KippoErrorMessageBugTest(): TestResult.WARNING,  # random reply
                      default_templates.DefaultTemplateFileTest(): TestResult.NOT_APPLICABLE
                  },
                  port_range='-')

    # test beartrap
    honeypot_test('beartrap',
                  {
                      direct_fingerprinting.DirectFingerprintTest(): TestResult.OK,
                      direct_fingerprinting.DefaultServiceCombinationTest(): TestResult.OK,
                      direct_fingerprinting.DuplicateServicesCheck(): TestResult.OK,
                      default_ftp.DefaultFTPBannerTest(): TestResult.WARNING,
                      service_implementation.HTTPTest(): TestResult.NOT_APPLICABLE,
                      default_http.DefaultWebsiteTest(): TestResult.NOT_APPLICABLE,
                      default_http.DefaultGlastopfWebsiteTest(): TestResult.NOT_APPLICABLE,
                      default_http.DefaultStylesheetTest(): TestResult.NOT_APPLICABLE,
                      default_http.CertificateValidationTest(): TestResult.NOT_APPLICABLE,
                      default_imap.DefaultIMAPBannerTest(): TestResult.NOT_APPLICABLE,
                      default_smtp.DefaultSMTPBannerTest(): TestResult.NOT_APPLICABLE,
                      service_implementation.SMTPTest(): TestResult.NOT_APPLICABLE,
                      default_telnet.DefaultTelnetBannerTest(): TestResult.NOT_APPLICABLE,
                      old_version_bugs.KippoErrorMessageBugTest(): TestResult.NOT_APPLICABLE,
                      default_templates.DefaultTemplateFileTest(): TestResult.NOT_APPLICABLE
                  })

    # test conpot
    honeypot_test('conpot',
                  {
                      direct_fingerprinting.DirectFingerprintTest(): TestResult.OK,
                      direct_fingerprinting.DefaultServiceCombinationTest(): TestResult.OK,
                      direct_fingerprinting.DuplicateServicesCheck(): TestResult.OK,
                      default_ftp.DefaultFTPBannerTest(): TestResult.NOT_APPLICABLE,
                      service_implementation.HTTPTest(): TestResult.OK,
                      default_http.DefaultWebsiteTest(): TestResult.OK,
                      default_http.DefaultGlastopfWebsiteTest(): TestResult.OK,
                      default_http.DefaultStylesheetTest(): TestResult.NOT_APPLICABLE,
                      default_http.CertificateValidationTest(): TestResult.NOT_APPLICABLE,
                      default_imap.DefaultIMAPBannerTest(): TestResult.NOT_APPLICABLE,
                      default_smtp.DefaultSMTPBannerTest(): TestResult.NOT_APPLICABLE,
                      service_implementation.SMTPTest(): TestResult.NOT_APPLICABLE,
                      default_telnet.DefaultTelnetBannerTest(): TestResult.NOT_APPLICABLE,
                      old_version_bugs.KippoErrorMessageBugTest(): TestResult.NOT_APPLICABLE,
                      default_templates.DefaultTemplateFileTest(): TestResult.WARNING
                  },
                  port_range='0-501,503-1000')

    # test cowrie
    honeypot_test('cowrie',
                  {
                      direct_fingerprinting.DirectFingerprintTest(): TestResult.OK,
                      direct_fingerprinting.DefaultServiceCombinationTest(): TestResult.OK,
                      direct_fingerprinting.DuplicateServicesCheck(): TestResult.OK,
                      default_ftp.DefaultFTPBannerTest(): TestResult.NOT_APPLICABLE,
                      service_implementation.HTTPTest(): TestResult.NOT_APPLICABLE,
                      default_http.DefaultWebsiteTest(): TestResult.NOT_APPLICABLE,
                      default_http.DefaultGlastopfWebsiteTest(): TestResult.NOT_APPLICABLE,
                      default_http.DefaultStylesheetTest(): TestResult.NOT_APPLICABLE,
                      default_http.CertificateValidationTest(): TestResult.NOT_APPLICABLE,
                      default_imap.DefaultIMAPBannerTest(): TestResult.NOT_APPLICABLE,
                      default_smtp.DefaultSMTPBannerTest(): TestResult.NOT_APPLICABLE,
                      service_implementation.SMTPTest(): TestResult.NOT_APPLICABLE,
                      default_telnet.DefaultTelnetBannerTest(): TestResult.WARNING,
                      old_version_bugs.KippoErrorMessageBugTest(): TestResult.OK,
                      default_templates.DefaultTemplateFileTest(): TestResult.NOT_APPLICABLE
                  },
                  port_range='-')

    # test dionaea
    honeypot_test('dionaea',
                  {
                      direct_fingerprinting.DirectFingerprintTest(): TestResult.WARNING,
                      direct_fingerprinting.DefaultServiceCombinationTest(): TestResult.WARNING,
                      direct_fingerprinting.DuplicateServicesCheck(): TestResult.WARNING,
                      default_ftp.DefaultFTPBannerTest(): TestResult.WARNING,
                      service_implementation.HTTPTest(): TestResult.OK,
                      default_http.DefaultWebsiteTest(): TestResult.WARNING,
                      default_http.DefaultGlastopfWebsiteTest(): TestResult.OK,
                      default_http.DefaultStylesheetTest(): TestResult.NOT_APPLICABLE,
                      default_http.CertificateValidationTest(): TestResult.WARNING,
                      default_imap.DefaultIMAPBannerTest(): TestResult.NOT_APPLICABLE,
                      default_smtp.DefaultSMTPBannerTest(): TestResult.NOT_APPLICABLE,
                      service_implementation.SMTPTest(): TestResult.NOT_APPLICABLE,
                      default_telnet.DefaultTelnetBannerTest(): TestResult.NOT_APPLICABLE,
                      old_version_bugs.KippoErrorMessageBugTest(): TestResult.NOT_APPLICABLE,
                      default_templates.DefaultTemplateFileTest(): TestResult.NOT_APPLICABLE
                  },
                  port_range='-')

    # test glastopf
    honeypot_test('glastopf',
                  {
                      direct_fingerprinting.DirectFingerprintTest(): TestResult.OK,
                      direct_fingerprinting.DefaultServiceCombinationTest(): TestResult.OK,
                      direct_fingerprinting.DuplicateServicesCheck(): TestResult.OK,
                      default_ftp.DefaultFTPBannerTest(): TestResult.NOT_APPLICABLE,
                      service_implementation.HTTPTest(): TestResult.OK,
                      default_http.DefaultWebsiteTest(): TestResult.OK,
                      default_http.DefaultGlastopfWebsiteTest(): TestResult.WARNING,
                      default_http.DefaultStylesheetTest(): TestResult.WARNING,
                      default_http.CertificateValidationTest(): TestResult.NOT_APPLICABLE,
                      default_imap.DefaultIMAPBannerTest(): TestResult.NOT_APPLICABLE,
                      default_smtp.DefaultSMTPBannerTest(): TestResult.NOT_APPLICABLE,
                      service_implementation.SMTPTest(): TestResult.NOT_APPLICABLE,
                      default_telnet.DefaultTelnetBannerTest(): TestResult.NOT_APPLICABLE,
                      old_version_bugs.KippoErrorMessageBugTest(): TestResult.NOT_APPLICABLE,
                      default_templates.DefaultTemplateFileTest(): TestResult.NOT_APPLICABLE
                  })

    # test honeypy
    honeypot_test('honeypy',
                  {
                      direct_fingerprinting.DirectFingerprintTest(): TestResult.OK,
                      direct_fingerprinting.DefaultServiceCombinationTest(): TestResult.WARNING,
                      direct_fingerprinting.DuplicateServicesCheck(): TestResult.WARNING,
                      default_ftp.DefaultFTPBannerTest(): TestResult.NOT_APPLICABLE,
                      service_implementation.HTTPTest(): TestResult.NOT_APPLICABLE,
                      default_http.DefaultWebsiteTest(): TestResult.NOT_APPLICABLE,
                      default_http.DefaultGlastopfWebsiteTest(): TestResult.NOT_APPLICABLE,
                      default_http.DefaultStylesheetTest(): TestResult.NOT_APPLICABLE,
                      default_http.CertificateValidationTest(): TestResult.NOT_APPLICABLE,
                      default_imap.DefaultIMAPBannerTest(): TestResult.NOT_APPLICABLE,
                      default_smtp.DefaultSMTPBannerTest(): TestResult.NOT_APPLICABLE,
                      service_implementation.SMTPTest(): TestResult.NOT_APPLICABLE,
                      default_telnet.DefaultTelnetBannerTest(): TestResult.WARNING,
                      old_version_bugs.KippoErrorMessageBugTest(): TestResult.NOT_APPLICABLE,
                      default_templates.DefaultTemplateFileTest(): TestResult.NOT_APPLICABLE
                  },
                  port_range='-')

    # test dionaea
    honeypot_test('honeything',
                  {
                      direct_fingerprinting.DirectFingerprintTest(): TestResult.OK,
                      direct_fingerprinting.DefaultServiceCombinationTest(): TestResult.OK,
                      direct_fingerprinting.DuplicateServicesCheck(): TestResult.OK,
                      default_ftp.DefaultFTPBannerTest(): TestResult.NOT_APPLICABLE,
                      service_implementation.HTTPTest(): TestResult.OK,
                      default_http.DefaultWebsiteTest(): TestResult.WARNING,
                      default_http.DefaultGlastopfWebsiteTest(): TestResult.OK,
                      default_http.DefaultStylesheetTest(): TestResult.NOT_APPLICABLE,
                      default_http.CertificateValidationTest(): TestResult.NOT_APPLICABLE,
                      default_imap.DefaultIMAPBannerTest(): TestResult.NOT_APPLICABLE,
                      default_smtp.DefaultSMTPBannerTest(): TestResult.NOT_APPLICABLE,
                      service_implementation.SMTPTest(): TestResult.NOT_APPLICABLE,
                      default_telnet.DefaultTelnetBannerTest(): TestResult.NOT_APPLICABLE,
                      old_version_bugs.KippoErrorMessageBugTest(): TestResult.NOT_APPLICABLE,
                      default_templates.DefaultTemplateFileTest(): TestResult.NOT_APPLICABLE
                  })

    # test honeytrap
    honeypot_test('honeytrap',
                  {
                      direct_fingerprinting.DirectFingerprintTest(): TestResult.OK,
                      direct_fingerprinting.DefaultServiceCombinationTest(): TestResult.OK,
                      direct_fingerprinting.DuplicateServicesCheck(): TestResult.WARNING,
                      default_ftp.DefaultFTPBannerTest(): TestResult.NOT_APPLICABLE,
                      service_implementation.HTTPTest(): TestResult.NOT_APPLICABLE,
                      default_http.DefaultWebsiteTest(): TestResult.NOT_APPLICABLE,
                      default_http.DefaultGlastopfWebsiteTest(): TestResult.NOT_APPLICABLE,
                      default_http.DefaultStylesheetTest(): TestResult.NOT_APPLICABLE,
                      default_http.CertificateValidationTest(): TestResult.NOT_APPLICABLE,
                      default_imap.DefaultIMAPBannerTest(): TestResult.NOT_APPLICABLE,
                      default_smtp.DefaultSMTPBannerTest(): TestResult.NOT_APPLICABLE,
                      service_implementation.SMTPTest(): TestResult.NOT_APPLICABLE,
                      default_telnet.DefaultTelnetBannerTest(): TestResult.NOT_APPLICABLE,
                      old_version_bugs.KippoErrorMessageBugTest(): TestResult.UNKNOWN,
                      default_templates.DefaultTemplateFileTest(): TestResult.NOT_APPLICABLE
                  },
                  port_range='-')

    # test kippo
    honeypot_test('kippo',
                  {
                    direct_fingerprinting.DirectFingerprintTest(): TestResult.OK,
                    direct_fingerprinting.DefaultServiceCombinationTest(): TestResult.OK,
                    direct_fingerprinting.DuplicateServicesCheck(): TestResult.OK,
                    default_ftp.DefaultFTPBannerTest(): TestResult.NOT_APPLICABLE,
                    service_implementation.HTTPTest(): TestResult.NOT_APPLICABLE,
                    default_http.DefaultWebsiteTest(): TestResult.NOT_APPLICABLE,
                    default_http.DefaultGlastopfWebsiteTest(): TestResult.NOT_APPLICABLE,
                    default_http.DefaultStylesheetTest(): TestResult.NOT_APPLICABLE,
                    default_http.CertificateValidationTest(): TestResult.NOT_APPLICABLE,
                    default_imap.DefaultIMAPBannerTest(): TestResult.NOT_APPLICABLE,
                    default_smtp.DefaultSMTPBannerTest(): TestResult.NOT_APPLICABLE,
                    service_implementation.SMTPTest(): TestResult.NOT_APPLICABLE,
                    default_telnet.DefaultTelnetBannerTest(): TestResult.NOT_APPLICABLE,
                    old_version_bugs.KippoErrorMessageBugTest(): TestResult.OK,
                    default_templates.DefaultTemplateFileTest(): TestResult.NOT_APPLICABLE
                  },
                  port_range='-')

    # test mtpot
    honeypot_test('mtpot',
                  {
                      direct_fingerprinting.DirectFingerprintTest(): TestResult.OK,
                      direct_fingerprinting.DefaultServiceCombinationTest(): TestResult.OK,
                      direct_fingerprinting.DuplicateServicesCheck(): TestResult.OK,
                      default_ftp.DefaultFTPBannerTest(): TestResult.NOT_APPLICABLE,
                      service_implementation.HTTPTest(): TestResult.NOT_APPLICABLE,
                      default_http.DefaultWebsiteTest(): TestResult.NOT_APPLICABLE,
                      default_http.DefaultGlastopfWebsiteTest(): TestResult.NOT_APPLICABLE,
                      default_http.DefaultStylesheetTest(): TestResult.NOT_APPLICABLE,
                      default_http.CertificateValidationTest(): TestResult.NOT_APPLICABLE,
                      default_imap.DefaultIMAPBannerTest(): TestResult.NOT_APPLICABLE,
                      default_smtp.DefaultSMTPBannerTest(): TestResult.NOT_APPLICABLE,
                      service_implementation.SMTPTest(): TestResult.NOT_APPLICABLE,
                      default_telnet.DefaultTelnetBannerTest(): TestResult.WARNING,
                      old_version_bugs.KippoErrorMessageBugTest(): TestResult.NOT_APPLICABLE,
                      default_templates.DefaultTemplateFileTest(): TestResult.NOT_APPLICABLE
                  })

    # test shockpot
    honeypot_test('shockpot',
                  {
                      direct_fingerprinting.DirectFingerprintTest(): TestResult.OK,
                      direct_fingerprinting.DefaultServiceCombinationTest(): TestResult.OK,
                      direct_fingerprinting.DuplicateServicesCheck(): TestResult.OK,
                      default_ftp.DefaultFTPBannerTest(): TestResult.NOT_APPLICABLE,
                      service_implementation.HTTPTest(): TestResult.OK,
                      default_http.DefaultWebsiteTest(): TestResult.WARNING,
                      default_http.DefaultGlastopfWebsiteTest(): TestResult.OK,
                      default_http.DefaultStylesheetTest(): TestResult.OK,
                      default_http.CertificateValidationTest(): TestResult.NOT_APPLICABLE,
                      default_imap.DefaultIMAPBannerTest(): TestResult.NOT_APPLICABLE,
                      default_smtp.DefaultSMTPBannerTest(): TestResult.NOT_APPLICABLE,
                      service_implementation.SMTPTest(): TestResult.NOT_APPLICABLE,
                      default_telnet.DefaultTelnetBannerTest(): TestResult.NOT_APPLICABLE,
                      old_version_bugs.KippoErrorMessageBugTest(): TestResult.NOT_APPLICABLE,
                      default_templates.DefaultTemplateFileTest(): TestResult.NOT_APPLICABLE
                  },
                  port_range='-')

    # test the interface
    interface_test()


if __name__ == '__main__':
    main()
