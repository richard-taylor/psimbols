
import psimbols.err
import psimbols.message
import unittest

class TestMessage(unittest.TestCase):

    def setUp(self):
        self.processor = psimbols.message.Processor()
        
    def test_valid_message(self):
        im = {'client': '1234567890', 'message': 'abcdefghijklmnopqrstuvwxyz'}
        om = self.processor.process(im)
        self.assertEqual('1234567890', om['client'])
        self.assertEqual('abcdefghijklmnopqrstuvwxyz', om['message'])
        
    def test_unauthorised(self):
        im = {'baddie': '0987654321'}
        self.assertRaises(psimbols.err.ClientUnauthorised,
                          self.processor.process, im)
                          
if __name__ == '__main__':
    unittest.main()
