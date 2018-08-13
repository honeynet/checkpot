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

import sys
import os

import argv_parser
from honeypots.honeypot import Honeypot, ScanFailure
from tests.test_platform import TestPlatform

from tests import *


def first_run():
    """Display terms the the first time user runs app"""

    acc_file = os.path.join(os.path.dirname(__file__), ".accepted")

    if os.path.isfile(acc_file):
        return

    print(
        "As this program is PROVIDED WITH ABSOLUTELY NO WARRANTY OF ANY KIND,\n"
        "YOU USE THIS PROGRAM AT YOUR OWN RISK!\n"
        "Please consult README.md for more information.\n"
        "By using this tool YOU TAKE FULL LEGAL RESPONSIBILITY FOR ANY\n"
        "POSSIBLE OUTCOME.\n"
    )

    print('Do you agree to these terms?')
    ans = input('Your answer [type in "i agree"/"no"]: ')

    while ans.lower() != 'i agree' and ans.lower() != 'no':
        print('Please answer with "i agree" or "no"!')
        ans = input('Your answer [type in "i agree"/"no"]: ')

    if ans.lower() == "i agree":
        with open(acc_file, 'w') as f:
            f.write('terms accepted')
    else:
        sys.exit(0)


def main(argv):
    """Entry point for the main application"""

    options = argv_parser.parse(argv)

    if options is None:
        sys.exit(2)

    print(
        "Checkpot - Honeypot Checker, Copyright (C) 2018  Vlad Florea\n"
        "This program comes with ABSOLUTELY NO WARRANTY; for details\n"
        "run `python checkpot.py --show w`.\n"
        "This is free software, and you are welcome to redistribute it\n"
        "under certain conditions; run `python checkpot.py --show c` for details.\n"
    )

    first_run()

    # run scan

    print("Running scan on " + options["target"])

    hp = Honeypot(options["target"], options["scan_os"])

    test_list = []

    print("Scanning ports ...\n")

    # collect data

    try:
        if options["port_range"]:
            hp.scan(port_range=options["port_range"], fast=options["fast"])  # TODO restrict access to this?
        else:
            hp.scan()
    except ScanFailure as e:
        print("Scan failed: " + str(e))
        sys.exit(1)

    # run tests

    if options["scan_level"] > 0:

        test_list.append(direct_fingerprinting.DirectFingerprintTest())

        if options["scan_os"]:
            test_list.append(direct_fingerprinting.OSServiceCombinationTest())

        test_list.append(direct_fingerprinting.DefaultServiceCombinationTest())
        test_list.append(direct_fingerprinting.DuplicateServicesCheck())

    if options["scan_level"] > 1:
        test_list.append(default_ftp.DefaultFTPBannerTest())

        test_list.append(service_implementation.HTTPTest())
        test_list.append(default_http.DefaultWebsiteTest())
        test_list.append(default_http.DefaultGlastopfWebsiteTest())
        test_list.append(default_http.DefaultStylesheetTest())
        test_list.append(default_http.CertificateValidationTest())

        test_list.append(default_imap.DefaultIMAPBannerTest())

        test_list.append(default_smtp.DefaultSMTPBannerTest())
        test_list.append(service_implementation.SMTPTest())

        test_list.append(default_telnet.DefaultTelnetBannerTest())
        test_list.append(old_version_bugs.KippoErrorMessageBugTest())

        test_list.append(default_templates.DefaultTemplateFileTest())

    if options["scan_level"] > 2:
        pass

    tp = TestPlatform(test_list, hp, )

    tp.run_tests(verbose=True, brief=options["brief"])


if __name__ == '__main__':
    main(sys.argv)
