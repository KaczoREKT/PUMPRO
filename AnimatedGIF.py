import tkinter as tk
from PIL import Image, ImageTk


class AnimatedGIF(tk.Label):
    def __init__(self, root, gif_path, delay=50, *args, **kwargs):
        self.gif = Image.open(gif_path)
        self.frames = []
        self.delay = delay

        for frame in range(self.gif.n_frames):
            self.gif.seek(frame)
            frame_image = ImageTk.PhotoImage(self.gif.copy())
            self.frames.append(frame_image)

        self.frame_index = 0
        super().__init__(root, image=self.frames[self.frame_index], *args, **kwargs)

        self.after(self.delay, self.update_frame)

    def update_frame(self):
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.config(image=self.frames[self.frame_index])
        self.after(self.delay, self.update_frame)
