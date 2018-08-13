The Automated Tests Framework
=============================

High-Level Description:
-----------------------

Checkpot runs automated tests for every pull request so we can make sure updates don’t break features that were proven to work before.

The :mod:`containers` module includes a custom framework especially made for running a selection of tests against docker containers with popular honeypots, available by calling the methods from the :class:`~containers.manager.Manager` class.

Subfolders of the “containers” folder/module each represent a container so they shall be named accordingly (as this is the name which will be used to refer to them). These subfolders must contain the Dockerfile and any other files which may be needed to build and run the container.

The :class:`~containers.manager.Manager` inside containers.py will handle all the communication with the docker daemon with the purpose of :meth:`starting <containers.manager.Manager.start_honeypot>`, :meth:`inspecting <containers.manager.Manager.get_honeypot_ip>` and :meth:`stopping <containers.manager.Manager.stop_honeypot>` containers.

The script ci_automated_tests.py is the entry point for the automated testing solutions and makes use of this framework. Here, the method :meth:`~ci_automated_tests.honeypot_test()` is used to easily run a selection of tests against a honeypot by providing a dictionary containing pairs of {:class:`Test() <tests.test.Test>` : :class:`~tests.test.TestResult`}. You can also run ci_automated_tests.py locally to test your implementation before submitting any changes. Pull requests which do not pass the automated tests will be rejected, but if you have any issues you are struggling with feel free to ask on github or on our community’s slack channel.

You can also manually import the framework (containers.py) to aid you when developing new features by running the following series of commands in the python console:

.. code-block:: python

    from containers.manager import Manager
    m = Manager()
    m.start_honeypot("<honeypot_name>")
    m.get_honeypot_ip("<honeypot_name>")


In another terminal you can run checkpot against the provided ip in order to test the functionality of new features. When you are done you can run:

.. code-block:: python

    m.stop_honeypot("<honeypot_name>")
