
import psimbols.http
import psimbols.test.dummy
import unittest

class TestHTTP(unittest.TestCase):
        
    def test_versions(self):
        self.assertEqual('Psimbols/1.0', psimbols.http.Handler.server_version)
        self.assertEqual('', psimbols.http.Handler.sys_version)
        
if __name__ == '__main__':
    unittest.main()
