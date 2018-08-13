Writing a new Test
==================

In order to add a new :class:`~tests.test.Test`, first of all, you have to find a .py file inside the :mod:`tests` module that matches your Tests category or create a new .py file inside the :mod:`tests` module (if your Test does not match any of the categories that already exist).

Afterwards you can create a new class in the chosen file which extends the :class:`~tests.test.Test` interface:

.. code-block:: python

    class MyNewTest(Test):
        ...

You should also override the varaibles :attr:`~tests.test.Test.description` and :attr:`~tests.test.Test.name` with appropriate strings which will later inform the users.
You can override the variable :attr:`~tests.test.Test.karma_value` (default value is 10) and set it to a value between 0 to 100 which should notify the user about the importance of this test (0 being the least important and 100 being very important).

You should then override the :meth:`~tests.test.Test.run()` method to implement the functionality that you need, by using the data provided by the reference :attr:`self.target_honeypot <tests.test.Test.target_honeypot>` which points to the target :class:`~honeypots.honeypot.Honeypot` object.

In order to provide the results of your tests to the user you should call :meth:`~tests.test.Test.set_result()` before returning from the run() method.

Add your test to the test list in ci_automated_tests.py and checkpot.py and you are done!
