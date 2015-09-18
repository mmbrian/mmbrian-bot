
IP_URL = 'http://jsonip.com/'
GEOIP_URL = 'http://www.telize.com/geoip/'
GEOIP_FORMAT = '''
%s | LA %s LO %s
TZ: %s
%s (%s)
%s (%s)
ISP: %s
PO: %s (%s)'''

## http://qrng.anu.edu.au/API/api-demo.php
RAND_URL = 'https://qrng.anu.edu.au/API/jsonI.php?length=%s&type=%s&size=%s'


COMMANDS_LIST = '''
Functionalities:

German Translation: /german, /ge <GTEXT>
SpellCheck: /correct <TEXT>
Lookup: /lookup <EXP>
IP Tracking: /ip, /track <IP>
Random: /rand uint8|uint16|hex16 <N> <L>
'''

ERROR_MSG = "Something went wrong :("