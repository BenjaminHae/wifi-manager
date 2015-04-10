import pyqrcode
# http://pythonhosted.org/PyQRCode/create.html

def encodeInformation(ssid,encryption,psk, hidden=False):
  info = "WIFI:T:{encryption};S:{ssid};P:{psk};{hidden};" 
  if encryption.lower().find("wpa") > -1:
    encryption="WPA"
  elif encryption.lower().find("wep") > -1:
    encryption="WEP"
  else:
    encryption="nopass"
  # encryption =(WPA, WEP, nopass)
  hide = ""
  if hidden == True:
    hide = "H:true"
  replacement = "\\'\".:,;" # \'".:,; zuerst den backslash!
  for ch in replacement:
    ssid = ssid.replace(ch,"\\" + ch)
    psk = psk.replace(ch,"\\" + ch)
  return info.format(encryption = encryption, ssid = ssid, psk = psk, hidden = hide)
  
def getBarcode(ssid, encryption, psk, hidden = False):
  code = pyqrcode.create(encodeInformation(ssid, encryption, psk, hidden))
  return code.terminal(module_color='black', background='white')