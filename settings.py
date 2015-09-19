
COMMANDS_LIST = '''
[Enable/Disable]
/start, /stop
[German Translation]
/german, /ge <GTXT>
SpellCheck EN
/correct <TXT>
Lookup EN
/lookup <EXP>
IP Tracking
/track <IP>
[Real Random]
/rand, /rand uint8|uint16|hex16 <N> <L>
[QR Code]
/qr <TXT>, /qrc L|M|Q|H <SIZE> <TXT>
[Talk to Alan]
/alan (/stop to cancel)
[YouTube]
/youtube <TXT>, /ydl <VID>
/ynext <PGTOKEN> <TXT>
/ylink <VID>
[Help]
/help, /?, /cmd
'''

ERROR_MSG = "Something went wrong :("

FAKE_HEADER = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}