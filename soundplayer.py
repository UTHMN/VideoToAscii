from pydub import AudioSegment
from pydub.playback import play

def play_sound(file_path):
    try:
        sound = AudioSegment.from_file(file_path)
        play(sound)
    except Exception as e:
        print(f"Error playing sound: {e}")
        
play_sound("./audio.mp3")