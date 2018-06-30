
import psimbols.err
import psimbols.message
import unittest

class DummyCrypt:
    def encrypt_base64(self, text, client):
        return text
    def decrypt_base64(self, text, client):
        return text

psimbols.message.crypt = DummyCrypt()
      
class TestMessage(unittest.TestCase):

    def setUp(self):
        self.processor = psimbols.message.Processor()
    
    def test_no_client(self):
        im = {'request': '1234567890'}
        self.assertRaises(psimbols.err.BadMessageFormat,
                          self.processor.process, im)
  
    def test_unknown_client(self):
        im = {'client': '0'}
        self.assertRaises(psimbols.err.ClientUnauthorised,
                          self.processor.process, im)
                                                      
    def test_no_request(self):
        im = {'client': '123'}
        self.assertRaises(psimbols.err.BadMessageFormat,
                          self.processor.process, im)

    def test_garbage_request(self):
        im = {'client': '123', 'request': '!%&!%&!$$*('}
        self.assertRaises(psimbols.err.ClientUnauthorised,
                          self.processor.process, im)
 
    def test_no_run(self):
        im = {'client': '123', 'request': '{"valid": "json"}'}
        self.assertRaises(psimbols.err.BadMessageFormat,
                          self.processor.process, im)
                          
    def test_valid_run(self):
        im = {'client': '123', 'request': '{"run": "one"}'}
        om = self.processor.process(im)
        self.assertEqual('123', om['client'])
        self.assertEqual('localhost:9393', om['server'])
        self.assertEqual('{"return": 1}', om['response'])
                                 
if __name__ == '__main__':
    unittest.main()
