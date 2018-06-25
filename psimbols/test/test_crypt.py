
import base64
import pyaes
import unittest

class TestCrypt(unittest.TestCase):

    def setUp(self):
        self.key = b'12345678901234567890123456789012'
        self.iv = b'initialisationVe'
        
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
