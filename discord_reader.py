import websocket
import json
import time

class Discord_Reader:

    def __init__(self, channel):
        print("Intitializing Discord Reader")
        self.channel = channel
        self.discord_ws = websocket.WebSocket()
        self.discord_ws.connect("wss://gateway.discord.gg/?v=6&encording=json")
        event = self.receive_json_response()
        self.heartbeat_interval = event['d']['heartbeat_interval']/2000
        self.token = "MzQ1MDU2NzU5OTk3NTMwMTEz.GtPrRb.PwnVLKutwvcjjR_SA9WWUH9xMnybYkpOid3UkQ"
        self.payload = {
            "op": 2,
            "d": {
                "token": self.token,
                "properties": {
                    "$os": 'windows',
                    '$browser': 'firefox',
                    '$device': 'pc'
                }
            }
        }
        self.send_json_request(self.discord_ws, self.payload)

    def send_json_request(self, discord_ws, request):
        discord_ws.send(json.dumps(request))

    def receive_json_response(self):
        response = self.discord_ws.recv()
        print(response)
        if response:
            return json.loads(response)
        
    def heartbeat(self, interval):
        time.sleep(0.5)
        print("Start Heartbeat")
        heartbeatJSON = {
            "op": 1,
            "d": "null:"
        }
        self.discord_ws = websocket.WebSocket()
        self.discord_ws.connect("wss://gateway.discord.gg/?v=6&encording=json")
        event = self.receive_json_response()
        self.send_json_request(self.discord_ws, heartbeatJSON)
        
    def receive_message(self):
        event = self.receive_json_response()
        if event['d']['channel_id'] == self.channel:
            author = event['d']['author']['username']
            content = event['d']['content']
            return author, content
           

def main():
    print("Discord Reader testing")
    channel = '1236049148763963503'
    reader = Discord_Reader(channel)
    while True:
        time.sleep(0.1)
        event = reader.receive_json_response()
        try: 
            print(event)
            #author, content = reader.receive_message()
            #print(f'{author}: {content}')
        except (KeyboardInterrupt, SystemExit):
            pass

if __name__ == "__main__":
    main()