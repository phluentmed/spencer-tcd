import unittest

unit_tests = unittest.TestLoader().discover('Tests/UnitTests', '*Tests.py')
integration_tests = unittest.TestLoader().discover('Tests/IntegrationTests',
                                                   '*Tests.py')
unittest.TextTestRunner().run(unit_tests)
unittest.TextTestRunner().run(integration_tests)