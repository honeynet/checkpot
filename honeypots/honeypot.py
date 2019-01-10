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

import nmap
import platform
import urllib.request
import urllib.error
import socket


class Honeypot:
    """
    Holds all data known about one Honeypot.
    Used for decoupling the acquisition of the data from its usages.
    """

    __debug = False  # enables debug prints

    scan_id = 0
    websites = []  # cached web page data for current honeypot
    css = []  # cached css data for current honeypot

    def __init__(self, address, scan_os=False, verbose_scan=True):
        """
        :param address: ip address of the target
        :param scan_os: scan for Operating System information (requires elevated privileges)
        :param verbose_scan: print progress bars and stats when running a scan
        """
        self.address = address
        self.scan_os = scan_os
        self.host = None

        if verbose_scan:
            try:
                self._nm = nmap.PrintProgressPortScanner()
            except AttributeError:
                # not running the modded version of python-nmap
                print("\nWARNING: Cannot display progress bars as you have an unsupported version of python-nmap. "
                      "Please install from requirements.txt.")
                print("Example: pip install -r requirements.txt\n")
                self._nm = nmap.PortScanner()
        else:
            self._nm = nmap.PortScanner()

    def scan(self, port_range=None, fast=False):
        """
        Runs a scan on this Honeypot for data acquisition.
        """

        args = '-sV -n --stats-every 1s'

       
        print("port range is "+ port_range)
        if fast:
            args += ' -Pn -T5'

        if port_range:
            args += ' -p '+port_range

        if self.scan_os:

            args += ' -O'
        
            if platform.system() == 'Windows':
                # No sudo on Windows systems, let UAC handle this
                # FIXME workaround for the subnet python-nmap-bug.log also?
                # FIXME somehow this also makes the command history of the terminal vanish?
                self._nm.scan(hosts=self.address, arguments=args, sudo=False)
            else:
                try:
                    # FIXME this is just a workaround for the bug shown in python-nmap-bug.log
                    self._nm.scan(hosts=self.address, arguments=args, sudo=True)
                except Exception as e:
                    if self.__debug:
                        print(e.__class__, "occured trying again with get_last_output")
                    self._nm.get_nmap_last_output()
                    self._nm.scan(hosts=self.address, arguments=args, sudo=True)
        else:

            try:
                # FIXME this is just a workaround for the bug shown in python-nmap-bug.log
                print("address " + self.address + " " + "args " + args )
                self._nm.scan(hosts=self.address, arguments=args, sudo=False)
            except Exception as e:
                if self.__debug:
                    print(e.__class__, "occured trying again with get_last_output")
                self._nm.get_nmap_last_output()
                self._nm.scan(hosts=self.address, arguments=args, sudo=False)

        hosts = self._nm.all_hosts()

        if hosts:
            self.host = hosts[0]
        else:
            self.host = None
            raise ScanFailure("Requested host not available")

        # TODO error on connection refused, check if self._nm[self.host]['status']['reason'] = conn_refused
        # TODO also add -Pn option?

    @property
    def os(self):
        if self.scan_os and self.host and 'osmatch' in self._nm[self.host]:
            if self._nm[self.host]['osmatch'] and self._nm[self.host]['osmatch'][0]['osclass']:
                return self._nm[self.host]['osmatch'][0]['osclass'][0]['osfamily']

    @property
    def ip(self):
        return self._nm[self.host]['addresses']['ipv4']

    def has_tcp(self, port_number):
        """
        Checks if the Honeypot has a certain port open.
        :param port_number: port number
        :return: port status boolean
        """
        return self._nm[self.host].has_tcp(port_number)

    def get_service_ports(self, service_name, protocol):
        """
        Checks if the Honeypot has a certain service available.
        :param service_name: name of the service to search for
        :param protocol: 'tcp' or 'udp'
        :return: list of port numbers (a certain service can run on multiple ports)
        """
        results = []

        if protocol not in self._nm[self.host]:
            return results

        for port, attributes in self._nm[self.host][protocol].items():
            if attributes['name'] == service_name:
                results.append(port)

        return results

    def get_service_name(self, port, protocol):
        """
        Get name of service running on requested port
        :param port: target port
        :param protocol: 'tcp' or 'udp'
        :return: service name
        """
        if protocol not in self._nm[self.host]:
            return None

        return self._nm[self.host][protocol][port]["name"]

    def get_all_ports(self, protocol):
        """
        Returns all open ports on the honeypot
        :param protocol: 'tcp' / 'udp'
        :return: list of ports
        """
        if protocol not in self._nm[self.host]:
            return []
        else:
            return list((self._nm[self.host][protocol]).keys())

    def get_service_product(self, protocol, port):
        """
        Get the product description for a certain port
        :param protocol: 'tcp' / 'udp'
        :param port: port number
        :return: description string
        """
        # TODO cache requests for all parsers
        if protocol not in self._nm[self.host]:
            return None
        else:
            return self._nm[self.host][protocol][port]['product']

    def run_nmap_script(self, script, port, protocol='tcp'):
        """
        Runs a .nse script on the specified port range
        :param script: <script_name>.nse
        :param port: port / port range
        :param protocol: 'tcp'/'udp'
        :return: script output as string
        :raises: ScanFailure
        """

        tmp = nmap.PortScanner()
        tmp.scan(hosts=self.address, arguments="--script " + script + " -p " + str(port))

        port_info = tmp[self.address][protocol][int(port)]

        if 'script' in port_info:
            return port_info['script'][script.split('.')[0]]
        else:
            raise ScanFailure("Script execution failed")

    def get_banner(self, port, protocol='tcp'):
        """
        Grab banner on specified port
        :param port: port number
        :param protocol: 'tcp' / 'udp'
        :return: banner as string
        :raises: ScanFailure
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)

        try:
            s.connect((self.address, port))
            recv = s.recv(1024)
        except socket.error as e:
            raise ScanFailure("Banner grab failed for port", port, e)

        return recv

    def get_websites(self):
        """
        Gets websites for all active web servers found on the target
        :return: list of website content strings
        """

        if self.websites and self.scan_id == id(self.host):
            # if cache is not empty and we are still on the most recent scan
            return self.websites

        # refresh cache

        self.websites = []

        target_ports = self.get_service_ports('http', 'tcp')
        # TODO target_ports += self.get_service_ports('https', 'tcp')

        for port in target_ports:

            try:

                request = urllib.request.urlopen('http://' + self.ip + ':' + str(port) + '/',
                                                 timeout=5)

                if request.headers.get_content_charset() is None:
                    content = request.read()
                else:
                    content = request.read().decode(request.headers.get_content_charset())

                self.websites.append(content)

            except Exception as e:
                if self.__debug:
                    print('Failed to fetch homepage for site', self.ip, str(port), e)

        return self.websites

    def get_websites_css(self):
        """
        Gets website stylesheet for all active web servers found on the target
        :return: list of stylesheet strings
        """
        # TODO create a Website class containing stylesheet and others?

        if self.css and self.scan_id == id(self.host):
            # if cache is not empty and we are still on the most recent scan
            return self.css

        # refresh cache

        self.css = []

        target_ports = self.get_service_ports('http', 'tcp')
        # target_ports += self.get_service_ports('https', 'tcp')

        for port in target_ports:

            try:

                request = urllib.request.urlopen('http://' + self.ip + ':' + str(port) + '/style.css',
                                                 timeout=5)

                if request.headers.get_content_charset() is None:
                    content = request.read()
                else:
                    content = request.read().decode(request.headers.get_content_charset())

                self.css.append(content)

            except Exception as e:
                if self.__debug:
                    print('Failed to fetch stylesheet for site', self.ip, str(port), e)

        return self.css


class ScanFailure(Exception):
    """Raised when one of the data gathering methods fails"""

    def __init__(self, *report):
        """
        :param report: description of the error
        """
        self.value = " ".join(str(r) for r in report)

    def __str__(self):
        return repr(self.value)

    def __repr__(self):
        return 'ScanFailure exception ' + self.value
