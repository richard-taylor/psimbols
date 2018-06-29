
import psimbols.err
import psimbols.message
import unittest

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

if __name__ == '__main__':
    unittest.main()
