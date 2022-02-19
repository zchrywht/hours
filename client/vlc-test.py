# REQUIREMENTS: Pause, 
print("importing")
import vlc, time

videoPath = "walk.mov"

media = vlc.MediaPlayer(videoPath)
print(media)

media.play()

time.sleep(0.1)

length = media.get_length()
print(length)

media.video_set_key_input(True)

time.sleep(1)

command = input("end?")

#while media.is_playing():
#    time.sleep(0.5)

#vlc_instance = vlc.Instance()

#player = vlc_instance.media_player_new()

#media = vlc_instance.media_new(videoPath)
#player.set_media(media)
#player.play()
#time.sleep(10)
#duration = player.get_length()
#print(duration)