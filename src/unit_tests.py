import unittest

test_suite = unittest.TestLoader().discover('Tests', '*Tests.py')
unittest.TextTestRunner().run(test_suite)