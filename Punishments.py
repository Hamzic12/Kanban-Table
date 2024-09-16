import webbrowser, winsound, time, ctypes

class Consequences:
    
    def Motivator(self):
        webbrowser.open('https://youtu.be/TC-o_YRgBp4')

    def annoying_popup(self):
        for _ in range(15):
            ctypes.windll.user32.MessageBoxW(0, "Focus on your tasks!!!!", "Reminder", 0x40 | 0x1)
            time.sleep(6)  
    
    
    def annoying_sound(self):
        webbrowser.open('https://youtu.be/iZlpsneDGBQ')
        time.sleep(8)
        for _ in range(15):
            winsound.Beep(10000, 5000)  # 10000 Hz sound for 5 s
            time.sleep(4)

    def block_websites(self):
        hosts = r"C:\Windows\System32\drivers\etc\hosts"
        redirect = "127.0.0.1"
        websites = ["www.facebook.com", "www.instagram.com", "www.reddit.com", "www.youtube.com", "www.google.com"]
        with open(hosts, 'r+') as file:
            f_content = file.read()
            for site in websites:
                if site in f_content:
                    pass
                else:
                    file.write(redirect + " " + site + "\n")
        ctypes.windll.user32.MessageBoxW(0, "Enjoy blocked websites", "Reminder", 0x40 | 0x1)
    