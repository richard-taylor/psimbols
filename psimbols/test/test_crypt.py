
import psimbols.client
import psimbols.crypt

import base64
import binascii
import unittest

def isBase64(string):
    try:
        base64.b64decode(string, validate=True)
        return True
    except:
        return False
        
class TestCrypt(unittest.TestCase):

    def setUp(self):
        self.key = b'12345678901234567890123456789012'
        
        self.client = psimbols.client.Client('123', 'localhost', self.key)
        self.crypt = psimbols.crypt.Crypt()
        
    def test_encrypt_base64(self):
        ciphertext = self.crypt.encrypt_base64('{"json": "ok"}', self.client)
        self.assertTrue(isBase64(ciphertext))
    
    def test_decrypt_base64_too_short(self):
        self.assertRaises(ValueError,
                          self.crypt.decrypt_base64, 'ABCD', self.client)
                          
    def test_decrypt_invalid_base64(self):
        self.assertRaises(binascii.Error,
                          self.crypt.decrypt_base64, '!!!', self.client)
   
    def test_encrypt_and_decrypt(self):
        plaintext = "any old string"
        ciphertext = self.crypt.encrypt_base64(plaintext, self.client)
        plaintext2 = self.crypt.decrypt_base64(ciphertext, self.client)
        
        self.assertEqual(plaintext, plaintext2)
        self.assertNotEqual(plaintext, ciphertext)
        self.assertTrue(isBase64(ciphertext))
      
    def test_encrypt_is_unique(self):
        plaintext = "a thing that is secret"
        
        ciphertext1 = self.crypt.encrypt_base64(plaintext, self.client)
        ciphertext2 = self.crypt.encrypt_base64(plaintext, self.client)
        
        self.assertNotEqual(ciphertext1, ciphertext2)
        
        plain1 = self.crypt.decrypt_base64(ciphertext1, self.client)
        plain2 = self.crypt.decrypt_base64(ciphertext2, self.client)
        
        self.assertEqual(plaintext, plain1)
        self.assertEqual(plaintext, plain2)
        
        self.assertNotEqual(plaintext, ciphertext1)
        self.assertNotEqual(plaintext, ciphertext2)
        
        self.assertTrue(isBase64(ciphertext1))
        self.assertTrue(isBase64(ciphertext2))
           
if __name__ == '__main__':
    unittest.main()
