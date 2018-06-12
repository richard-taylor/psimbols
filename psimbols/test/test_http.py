
import psimbols.http
import unittest

class TestHTTP(unittest.TestCase):

    def setUp(self):
        self.handler = psimbols.http.Handler
        
    def test_versions(self):
        self.assertEqual('Psimbols/1.0', self.handler.server_version)
        self.assertEqual('', self.handler.sys_version)
        
if __name__ == '__main__':
    unittest.main()
