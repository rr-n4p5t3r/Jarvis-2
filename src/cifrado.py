import base64
import chardet

def encode_base64(text):
  # Convert the text to bytes.
  bytes_text = bytes(text, "utf-8")

  # Detect the encoding of the text.
  encoding = chardet.detect(bytes_text).get('encoding')

  # Encode the text to base64.
  encoded_text = base64.b64encode(bytes_text).decode(encoding)

  return encoded_text

def encode_body_base64(text):
  """
  Esta funcion codifica cualquier cadena de texto en base64
  :param: cadena de texto
  :type: str (cualquier codificacion)
  :raise Exception:
  :return: str base64
  :rtype: 
  """

  # Convert the text to bytes.
  bytes_text = bytes(text, "utf-8")

  # Detect the encoding of the text.
  encoding = chardet.detect(bytes_text).get('encoding')

  # Encode the text to base64.
  encoded_text = base64.b64encode(bytes_text)

  # Check if the encoding is None.
  if encoding is not None:
      encoded_text = encoded_text.decode(encoding)
  else:
      encoded_text = encoded_text

  return encoded_text

if __name__ == "__main__":
  text = input("Enter a string to encode: ")
  encoded_text = encode_body_base64(text)
  print("The encoded string is:", encoded_text)