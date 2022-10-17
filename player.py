from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from tkinter import filedialog
import pygame
from mutagen.mp3 import MP3
import time


root = Tk()
root.title('MP3 Player')
photo = PhotoImage(file='play50.png')
root.iconphoto(False, photo)
root.geometry('550x400')

pygame.mixer.init()
global is_paused
is_paused = False


def track(x):
    global pre
    pre = 0
    global start

    song = song_box.get(ACTIVE)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=round(float(x)))
    print('track')




def vol(x):
    pygame.mixer.music.set_volume(float(x)/100)


def onMouseWheel(event):
    print(event.delta)
    if (event.delta == 120):
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume()+0.1)
    elif (event.delta == -120):
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume()-0.1)
    vol_slider.config(value=pygame.mixer.music.get_volume()*100)


def play_time():

    current_time = pygame.mixer.music.get_pos()/1000
    slider.config(value=int(current_time))
    current_time = time.strftime('%M:%S', time.gmtime(current_time))
    elapse_label.config(text=current_time)







    elapse_label.after(1000, play_time)
    print('play_time')

def back():
    
    current = song_box.index(ACTIVE)
    song_box.activate(current-1)
    song_box.select_clear(current)
    song_box.selection_set(current-1)
    
    play()



def forward():
    current = song_box.index(ACTIVE)
    song_box.activate(current+1)
    song_box.select_clear(current)
    song_box.selection_set(current+1)
    
    play()


def remove_songs():
    song_box.delete(0,END)
    

def remove_song():
    song_box.delete(ACTIVE)
    


def add_many_songs():
    songs = filedialog.askopenfiles(
        initialdir='C:/Users/farhan/Music/',
        title='Choose a song',
        filetypes = (("mp3 files", "*.mp3"),)
        )
    for song in songs:
        song_box.insert(END,song.name)


def add_song():
    song = filedialog.askopenfile(
        initialdir='C:/Users/farhan/Music/',
        title='Choose a song',
        filetypes = (("mp3 files", "*.mp3"),)
        )
    
    song_box.insert(END, song.name)

def play():
    global is_paused
    
    
    
    
    if is_paused:
        pygame.mixer.music.unpause()
        is_paused = False
    else:
        song = song_box.get(ACTIVE)
        song_label.config(text=song.split('/')[-1].split('.')[0])
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        audio = MP3(song)
        length = audio.info.length
        total = time.strftime('%M:%S',time.gmtime(audio.info.length))
        total_label.config(text=total)
        slider.config(to=int(audio.info.length))
        
        
        
    play_time()
    print('play')
    
    

def pause():
    global is_paused
    pygame.mixer.music.pause()
    is_paused = True

def stop():
    global stopped
    pygame.mixer.music.stop()
    song_box.select_clear(ACTIVE)
    song_label.config(text='')
    elapse_label.config(text='00:00')
    slider.config(value=1)
    stopped = True

song_box = Listbox(root,bg='black', fg='green', width=60, selectbackground='gray', selectforeground='black')
song_box.pack(pady=20)

song_label = tk.Label(root, text='Test', font='Times 10 bold')
song_label.pack(pady=5)

timing_frame = Frame(root)
timing_frame.pack()

elapse_label = tk.Label(timing_frame,text='00:00')
slider = tk.ttk.Scale(timing_frame, from_=1, to=100, value=0, length=440, orient=HORIZONTAL, state='disabled')
total_label = tk.Label(timing_frame, text='00:00')
elapse_label.grid(row=0, column=0, padx=5)
slider.grid(row=0, column=1)
total_label.grid(row=0, column=2, padx=5)

controls_frame = Frame(root)
controls_frame.pack()



back_btn_img = PhotoImage(file='back50.png')
forward_btn_img = PhotoImage(file='forward50.png')
play_btn_img = PhotoImage(file='play50.png')
pause_btn_img = PhotoImage(file='pause50.png')
stop_btn_img = PhotoImage(file='stop50.png')
vol_btn_img = PhotoImage(file='speaker.png')


back_btn = tk.Button(controls_frame, image= back_btn_img, borderwidth=0, command=back)
forward_btn = tk.Button(controls_frame, image= forward_btn_img , borderwidth=0, command=forward)
play_btn = tk.Button(controls_frame, image= play_btn_img, borderwidth=0 , command=play)
pause_btn = tk.Button(controls_frame, image= pause_btn_img, borderwidth=0 , command=pause)
stop_btn = tk.Button(controls_frame, image= stop_btn_img, borderwidth=0, command=stop )
vol_btn = tk.Button(controls_frame, image=vol_btn_img, borderwidth=0)
vol_slider = tk.ttk.Scale(controls_frame, from_=0, to=100, value=100, orient=HORIZONTAL, length=70, command=vol)

back_btn.grid(row=0, column=0, padx=5)
forward_btn.grid(row=0, column=1, padx=5)
play_btn.grid(row=0, column=2, padx=5)
pause_btn.grid(row=0, column=3, padx=5)
stop_btn.grid(row=0, column=4, padx=5)
vol_btn.grid(row=0, column=5, padx=5)
vol_slider.grid(row=0, column=6)



my_menu = Menu(root)
root.config(menu=my_menu)

add_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label='Add Songs', menu=add_song_menu)
add_song_menu.add_command(label="Add one song to playlist", command=add_song)
add_song_menu.add_command(label="Add many songs to playlist", command=add_many_songs)

remove_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label='Remove Songs', menu=remove_song_menu)
remove_song_menu.add_command(label='Remove song', command=remove_song)
remove_song_menu.add_command(label='Remove songs', command=remove_songs)

root.bind('<MouseWheel>', onMouseWheel)



root.mainloop()
