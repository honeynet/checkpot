from .test import Test, TestResult
from honeypots.honeypot import Honeypot
from termcolor import colored, cprint


class TestPlatform:
    """
    Holds a list of Tests and a reference to a Honeypot
    Runs the list of tests on the Honeypot and generates statistics based on the results
    """
    def __init__(self, test_list, target_honeypot):
        """
        :param test_list: list of Test objects
        :param target_honeypot: Honeypot object to run Tests against
        """
        assert isinstance(target_honeypot, Honeypot)  # for safety and autocomplete
        assert all(isinstance(t, Test) for t in test_list)

        self.test_list = test_list
        self.__results = []
        self.target_honeypot = target_honeypot

    def run_tests(self, verbose=False, brief=False):
        """
        Runs the list of tests on the target Honeypot

        :param verbose: print results of each test
        :param brief: disable output for N/A tests
        """
        if verbose:
            self.print_header()

        for test in self.test_list:

            test.target_honeypot = self.target_honeypot

            test.run()

            if verbose:

                if brief and test.result == TestResult.NOT_APPLICABLE:
                    continue

                self.print_results(test.result, test.name, test.karma, test.report, test.doc_link)

        self.__results = [(test.name, test.report, test.result, test.karma) for test in self.test_list]

        if verbose:
            self.print_stats()

    @property
    def results(self):
        """
        Returns the results of each test

        :return: list of tuples like (Test Name, Test Report, Test Result)
        """
        return self.__results

    def get_stats(self):
        """
        Calculates statistics based on the last scan

        :return: tuple containing number of ok, warnings, unknown
        """
        ok = 0
        warnings = 0
        unknown = 0
        kp = 0

        for tname, treport, tresult, tkarma in self.__results:

            kp += tkarma

            if tresult == TestResult.WARNING:
                warnings += 1
            elif tresult == TestResult.OK:
                ok += 1
            elif tresult == TestResult.UNKNOWN:
                unknown += 1

        return ok, warnings, unknown, kp

    @staticmethod
    def print_results(test_result, test_name, test_karma, test_report, test_doc_link):

        assert isinstance(test_result, TestResult)

        if test_result == TestResult.OK:
            text = "[OK]"
            color = "green"
        elif test_result == TestResult.WARNING:
            text = "[WARNING]"
            color = "red"
        elif test_result == TestResult.UNKNOWN:
            text = "[UNKNOWN]"
            color = "yellow"
        elif test_result == TestResult.NOT_APPLICABLE:
            text = "[NOT APPLICABLE]"
            color = "blue"
        else:
            text = str(test_result)
            color = "white"

        print("{:40}".format(test_name) + " " +
              "{:^25}".format(colored(text, color=color)) + " " +
              "{:>+10}".format(test_karma))

        print("\n> " + test_report)

        if test_result != TestResult.NOT_APPLICABLE and test_result != TestResult.OK:
            # show the suggested doc page
            print(">>>", colored("For further details please refer to:\n\t", color='yellow'), test_doc_link)

        print("\n")


    @staticmethod
    def print_header():
        print("-"*80)
        print(colored("{:40}".format("Test Name:"), color="magenta") + " " +
              colored("{:25}".format("  Test Result:"), color="magenta") + " " +
              colored("{:<10}".format("KP:"), color="magenta"), "\n")

    def print_stats(self):
        ok, warnings, unknown, kp = self.get_stats()
        print("\nStats:",
              "\t", colored("OK", color="green"), "->", ok, "\n"
              "\t", colored("WARNING", color="red"), "->", warnings, "\n"
              "\t", colored("UNKNOWN", color="yellow"), "->", unknown, "\n")

        kpcolor = "green"
        if kp < 0:
            kpcolor = "red"

        print("Total Karma Points ->", colored(kp, color=kpcolor), "\n")
