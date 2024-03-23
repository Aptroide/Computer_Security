from OpenSSL import crypto
from cryptography import x509
from cryptography.hazmat.backends import default_backend

rb = [
    "bill01.pfx", "bill02.pfx", "bill03.pfx", "bill04.pfx", "bill05.pfx", "bill06.pfx", "bill07.pfx", "bill08.pfx", "bill09.pfx", "bill10.pfx", "bill11.pfx", "bill12.pfx", "bill13.pfx", "bill14.pfx", "bill15.pfx", "bill16.pfx", "bill17.pfx", "bill18.pfx"]

passwords  = [
    'apple', 'apricot', 'avocado', 'banana', 'blackberry', 'blueberry', 'boysenberry', 
    'cantaloupe', 'cherry', 'clementine', 'coconut', 'cranberry', 'date', 'dragonfruit', 
    'elderberry', 'fig', 'grape', 'grapefruit', 'guava', 'honeydew', 'jackfruit', 'kiwi', 
    'lemon', 'lime', 'lychee', 'mango', 'nectarine', 'orange', 'papaya', 'passionfruit', 
    'peach', 'pear', 'persimmon', 'pineapple', 'plum', 'pomegranate', 'quince', 'raspberry', 
    'strawberry', 'tangerine', 'melon','ugli fruit', 'victoria plum', 'watermelon', 'xigua', 
    'yellow passionfruit', 'zucchini', 'acerola', 'bilberry', 'currant', 'damson', 'elderberry',
    'feijoa', 'gooseberry', 'huckleberry', 'jabuticaba', 'kumquat', 'loganberry', 'mulberry', 
    'nance', 'olive', 'pitanga', 'quandong', 'rambutan', 'salal berry', 'tamarillo', 'ugni', 
    'voavanga', 'wolfberry', 'ximenia', 'yangmei', 'zapote', 'ackee', 'barberry', 'camu camu', 
    'durian', 'entawak', 'finger lime', 'gac', 'honeyberry', 'icaco', 'jambul', 'kei apple', 
    'lucuma', 'medlar', 'noni', 'osage orange', 'pawpaw', 'quararibea cordata', 'rose apple', 
    'santol', 'tutu', 'ugba', 'vitamin C fruit', 'wax jambu', 'xango mangosteen fruit juice', 
    'yellow mombin', 'ziziphus mauritiana']

for file in rb:
    for password in passwords:

        try:
            pfx = open(file, 'rb').read()
            
            p12 = crypto.load_pkcs12(pfx, password)
            
            print (f"- **{file}**: {password}")

        except:
            continue