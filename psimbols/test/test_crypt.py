
import psimbols.client
import psimbols.crypt
import base64
import binascii
import pyaes
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
        self.iv = b'initialisationVe'
        self.client = psimbols.client.Client('123', 'localhost', self.key)
        self.crypt = psimbols.crypt.Crypt()
        
    def test_encrypt_base64(self):
        ciphertext = self.crypt.encrypt_base64('{"json": "ok"}', self.client)
        self.assertTrue(isBase64(ciphertext))
    
    def test_decrypt_base64(self):
        self.crypt.decrypt_base64('AAAAAAAAAAAA', self.client)
   
    def test_decrypt_invalid_base64(self):
        self.assertRaises(binascii.Error,
                          self.crypt.decrypt_base64, '!!!', self.client)
                   
    def test_CBC(self):
        encrypter = pyaes.AESModeOfOperationCBC(self.key, iv=self.iv)
        plaintext = b'textmustbe16byte'

        ciphertext = encrypter.encrypt(plaintext)

        decrypter = pyaes.AESModeOfOperationCBC(self.key, iv=self.iv)
        decrypted = decrypter.decrypt(ciphertext)
 
        self.assertEqual(plaintext, decrypted)
        self.assertNotEqual(plaintext, ciphertext)

    def test_BlockFeeder(self):
        cbc = pyaes.AESModeOfOperationCBC(self.key, iv=self.iv)
        encrypter = pyaes.Encrypter(cbc)

        plaintext = b'Any text length should be fine, even 46 bytes.'

        ciphertext = encrypter.feed(plaintext)
        ciphertext += encrypter.feed()

        cbc = pyaes.AESModeOfOperationCBC(self.key, iv=self.iv)
        decrypter = pyaes.Decrypter(cbc)

        decrypted = decrypter.feed(ciphertext)
        decrypted += decrypter.feed()
 
        self.assertEqual(plaintext, decrypted)
        self.assertNotEqual(plaintext, ciphertext)

    def test_Base64(self):
        cbc = pyaes.AESModeOfOperationCBC(self.key, iv=self.iv)
        encrypter = pyaes.Encrypter(cbc)

        plaintext = b'Any text length should be fine, even 46 bytes.'

        ciphertext = encrypter.feed(plaintext)
        ciphertext += encrypter.feed()

        # Check that we can convert the encrypted bytes to base64
        # and back without messing up the decryption.

        base64bytes = base64.b64encode(ciphertext)
        base64string = base64bytes.decode('utf-8')

        bytesagain = base64string.encode('utf-8')
        encryptedbytes = base64.b64decode(bytesagain)

        # Should be back as it was now...
        self.assertEqual(ciphertext, encryptedbytes)

        cbc = pyaes.AESModeOfOperationCBC(self.key, iv=self.iv)
        decrypter = pyaes.Decrypter(cbc)

        decrypted = decrypter.feed(encryptedbytes)
        decrypted += decrypter.feed()
 
        self.assertEqual(plaintext, decrypted)
        self.assertNotEqual(plaintext, bytesagain)
        
if __name__ == '__main__':
    unittest.main()
