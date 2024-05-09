import time
import obs_websockets
import discord_reader
import keyboard
import threading

class App:

    def __init__(self):
        print("Initializing OBS Controller")
        self.cur_screen = "Face Stream"
        self.obsw = obs_websockets.OBSWebsocketsManager()
        self.obsw.set_scene(self.cur_screen)

        channel = '1236049148763963503'
        self.dr = discord_reader.Discord_Reader(channel)

    def discord_check(self):
        #print("discord")
        content = ""
        try: 
            author, content = self.dr.receive_message()
            print(f'{author}: {content}')
            if "write: " in content:
                print("Found text command!")
                self.obsw.set_text("Head Text", content[6:len(content):1])
            pass
        except:
            pass
        return
    
    def keyboard_check(self):
        #print("keyboard")
        try: 
            if keyboard.is_pressed('decimal'):
                print('Toggling Screen')
                if self.cur_screen == "Face Stream":
                    self.cur_screen = "Vtuber Stream"
                    self.obsw.set_scene(self.cur_screen)
                    pass
                else:
                    self.cur_screen = "Face Stream"
                    self.obsw.set_scene(self.cur_screen)
                    pass
            pass
        except:
            pass 
        return
    

def main():
    print("OBS Controller")
    app = App()
    time.sleep(1.5)

    while True:
        time.sleep(0.1)
        #t1 = threading.Thread(app.discord_check())
        t2 = threading.Thread(app.keyboard_check())
        #t3 = threading.Thread(app.dr.heartbeat(app.dr.heartbeat_interval))

        #t1.start()
        t2.start()
        #t3.start()
    
        #t1.join()
        t2.join()
        #t3.join()

if __name__ == "__main__":
    main()
