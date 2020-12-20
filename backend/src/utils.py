from base64 import b64encode

import hmac
import hashlib
import requests


def CreateHmac( content, hmac_secret ):
  if not isinstance( content, bytes ):
    raise TypeError( 'content was not of bytes type; you have a bug!' )
  if not isinstance( hmac_secret, bytes ):
    raise TypeError( 'hmac_secret was not of bytes type; you have a bug!' )

  return bytes( hmac.new( hmac_secret,
                          msg = content,
                          digestmod = hashlib.sha256 ).digest() )


def CreateRequestHmac( method, path, body, hmac_secret ):
  if not isinstance( body, bytes ):
    raise TypeError( 'body was not of bytes type; you have a bug!' )
  if not isinstance( hmac_secret, bytes ):
    raise TypeError( 'hmac_secret was not of bytes type; you have a bug!' )
  if not isinstance( method, bytes ):
    raise TypeError( 'method was not of bytes type; you have a bug!' )
  if not isinstance( path, bytes ):
    raise TypeError( 'path was not of bytes type; you have a bug!' )

  method_hmac = CreateHmac( method, hmac_secret )
  path_hmac = CreateHmac( path, hmac_secret )
  body_hmac = CreateHmac( body, hmac_secret )

  joined_hmac_input = bytes().join( ( method_hmac, path_hmac, body_hmac ) )
  return CreateHmac( joined_hmac_input, hmac_secret )