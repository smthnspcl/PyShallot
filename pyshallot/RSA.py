from pyasn1.type import univ, namedtype
from pyasn1.codec.der import encoder
from base64 import b64encode, b32encode
from hashlib import sha1
import gmpy2


# Encoding stuffs
# https://tools.ietf.org/html/rfc3447#appendix-A.1
class RSAPublicKey(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('modulus', univ.Integer()),
        namedtype.NamedType('publicExponent', univ.Integer())
    )


class RSAPrivateKey(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('version', univ.Integer()),
        namedtype.NamedType('modulus', univ.Integer()),
        namedtype.NamedType('publicExponent', univ.Integer()),
        namedtype.NamedType('privateExponent', univ.Integer()),
        namedtype.NamedType('prime1', univ.Integer()),
        namedtype.NamedType('prime2', univ.Integer()),
        namedtype.NamedType('exponent1', univ.Integer()),
        namedtype.NamedType('exponent2', univ.Integer()),
        namedtype.NamedType('coefficient', univ.Integer())
    )


def public_key(n, e):
    pk = RSAPublicKey()
    pk.setComponentByName('modulus', n)
    pk.setComponentByName('publicExponent', e)
    return encoder.encode(pk)


def private_key(n, e, d, p, q):
    pk = RSAPrivateKey()
    pk.setComponentByName('version', 0)
    pk.setComponentByName('modulus', n)
    pk.setComponentByName('publicExponent', e)
    pk.setComponentByName('privateExponent', d)
    pk.setComponentByName('prime1', p)
    pk.setComponentByName('prime2', q)
    pk.setComponentByName('exponent1', d % (p - 1))
    pk.setComponentByName('exponent2', d % (q - 1))
    pk.setComponentByName('coefficient', gmpy2.invert(q, p))
    return encoder.encode(pk)


def make_onion(n, e):
    return b32encode(sha1(public_key(n, e)).digest())[:16].lower() + b'.onion'


def pprint_privkey(privkey):
    print('-' * 5 + 'BEGIN RSA PRIVATE KEY' + '-' * 5)
    encoded = b64encode(privkey)
    while encoded:
        chunk, encoded = encoded[:64], encoded[64:]
        print(chunk)
    print('-' * 5 + 'END RSA PRIVATE KEY' + '-' * 5)
