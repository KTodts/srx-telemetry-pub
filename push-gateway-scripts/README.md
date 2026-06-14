# Description
Script that executes the show command on SROS via SSH (scrapli) and then post the output
into the prometheus push gateway using the correspoding prometheus python client library


## Steps

1. On a tmux, screen or with nohup:

```bash
 python3 -m venv venv
 source venv/bin/activate
 pip install -r requirements.txt 
 ## USAGE
 # $  python show_virtual_card_fp [-h] [-u USERNAME] [-p PASSWORD] [-P PLATFORM] [-t TIMEOUT] IP
 nohup python3 show_virtual_card_fp.py -p 'SRX2024!' cvsr1  > cvsr1.log  &
 ps -eaf | grep show_virtual_card
 ```
