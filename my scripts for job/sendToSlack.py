import requests

def send_to_slack(self,message,color):
        try:
            URL = ''
            msg={"attachments": [{
                     "fields": [{"title":sys.argv[1],"value":message}],
                     "color": color,
                     }]
                  }


send_to_slack('test','#0000ff','test')
