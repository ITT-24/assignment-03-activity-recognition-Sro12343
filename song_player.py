import os.path
import mido
from mido import MidiFile
import threading


class songPlayer():
    # Initialize instance variables 
    def __init__(self,musicFolder,songName,output_port):
        self.stopSong = False
        self.songName = songName + ".mid"
        self.musicFile = os.path.join(musicFolder,songName)
        self.output_port = output_port
        self.song_thread = None
        pass
    
    def play_song(self):
        #Async PLay of midi file. 
        def play():
            while not self.stopSong:
                for msg in MidiFile(self.musicFile).play():
                    #if stopSong is true then stop all midi notes and stop for loop
                    if self.stopSong == True:
                        for channel in range(16):
                            for note in range(128):  # Iterate over all possible MIDI note numbers
                                stop_msg =mido.Message('note_off', note=note, velocity=0, channel = channel)
                                self.output_port.send(stop_msg)

                        break
                    self.output_port.send(msg)
        self.song_thread = threading.Thread(target=play)
        self.song_thread.start()
    def stop_play(self):
        self.stopSong = True
        
        #Test->
        if self.song_thread:
            self.song_thread.join()