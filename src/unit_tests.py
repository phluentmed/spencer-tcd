import unittest

test_suite = unittest.TestLoader().discover('Tests', '*tests.py')
unittest.TextTestRunner().run(test_suite)
