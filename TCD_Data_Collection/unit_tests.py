import unittest

test_suite = unittest.TestLoader().discover('tests', '*Tests.py')
unittest.TextTestRunner().run(test_suite)
