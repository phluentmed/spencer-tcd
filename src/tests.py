import sys
import unittest

unit_tests = unittest.TestLoader().discover('Tests/UnitTests', '*Tests.py')
integration_tests = unittest.TestLoader().discover('Tests/IntegrationTests',
                                                   '*Tests.py')
u_result = unittest.TextTestRunner().run(unit_tests)
i_result = unittest.TextTestRunner().run(integration_tests)

sys.exit(not (u_result.wasSuccessful() and i_result.wasSuccessful()))
