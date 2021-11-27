from pygame import mixer

mixer.init()

#Play list

#b=MedievalBattle
b = "dafawe__medieval.wav"
#s=GameStart = "Dramatic.wav"
s = "Dramatic.wav"
#m=MagiaSound
m = "Magia2.wav"
#d=ButtomSelect 
d = "Buttom.wav"
#cs=CardShuffle
cs = "deck-of-cards.wav"

#Used do Volume, v=1 a 4
v = 1
#Starting the mix
mixer.music.load(b)
#Setting the volume
mixer.music.set_volume(v*0.25)
#Start playing the song again
mixer.music.play(-1)
#infinite loop
while True:
    print("Press 'p' to pause, 'r' to resume")
    print("Press 'e' to exit the program")
    print("Press 1 a 4 para ajustar o volume")
    print("Seleção de Playlist: s=StartGame; b=CalltoWar;"+
          "m=Magia; d=ButtomDown; cs=CardSuffle")
    
    query = input("  ")

    #Pausing the music
    if query == 'p':
        mixer.music.pause()

    #Resuming the music
    elif query == 'r':
        mixer.music.unpause()

    #Stop the mixer
    elif query == 'e': 
        mixer.music.stop()
        break

    #Select Volum
    elif query == '1':
        v = 1
        mixer.music.set_volume(v*0.25)
    elif query == '2':
        v = 2
        mixer.music.set_volume(v*0.25)
    elif query == '3':
        v = 3
        mixer.music.set_volume(v*0.25)
    elif query == '4':
        v = 4
        mixer.music.set_volume(v*0.25)

    #Choose Music
    elif query == 's':
        mixer.music.load(s)
        mixer.music.play(-1)
        mixer.music.set_volume(v*0.25)
    elif query == 'b':
        mixer.music.load(b)
        mixer.music.play(-1)
        mixer.music.set_volume(v*0.25)

    elif query == 'm':
        mixer.music.load(m)
        mixer.music.play(0)
        mixer.music.set_volume(v*0.25)
    
    elif query == 'd':
        mixer.music.load(d)
        mixer.music.play(0)
        mixer.music.set_volume(v*0.25)
            
    elif query == 'cs':
        mixer.music.load(cs)
        mixer.music.play(0)
        mixer.music.set_volume(v*0.25)
