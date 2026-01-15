import tkinter as tk
from PIL import Image, ImageTk
from Other.config import config

class AnimatedGIF(tk.Label):
    def __init__(self, root, delay=50):
        # utwórz obiekt GIF
        super().__init__(root)
        gif_path = config['paths']['animated_gif_path']
        self.gif = Image.open(gif_path)
        self.frames = []
        self.delay = delay
        self.config(bg=root.background)

        for frame in range(self.gif.n_frames):
            self.gif.seek(frame)
            frame_image = ImageTk.PhotoImage(self.gif.copy())
            self.frames.append(frame_image)

        self.frame_index = 0
        
        # rozpocznij animację obiektu GIF
        self.after(self.delay, self.update_frame)

    def update_frame(self):
        #przejdz do następnej klatki z GIF
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.config(image=self.frames[self.frame_index])
        self.after(self.delay, self.update_frame)
