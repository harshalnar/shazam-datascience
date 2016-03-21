#import vlc
from pydub import AudioSegment


def main():
	print "trynna play"
	#p = vlc.MediaPlayer("file:///Users/valentin/Music/iTunes/iTunes%20Media/Music/Androma/Unknown%20Album/Anapo.mp3")
	#p.play()
	song = AudioSegment.from_mp3("somethingGood.mp3")
	first_ten_secs = song[:10*1000]
	first_ten_secs.export("first10.wav", format="wav")

if __name__ == '__main__':
    main()