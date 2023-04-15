import tkinter as tk
import cv2
from PIL import Image, ImageTk


class App:
    def __init__(self, window):
        self.window = window
        self.window.title("Golden NongNoc")

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, width=1000, height=1000, bg="grey")
        self.canvas.pack(side=tk.LEFT)

        # Add text to the center of the canvas
        # text = "Please add media source"
        # self.canvas.create_text(
        #     self.canvas.winfo_width() / 2,
        #     self.canvas.winfo_height() / 2,
        #     text=text,
        #     font=("Helvetica", 20),
        #     fill="white"
        # )

        # Create a sidebar frame on the right side of the window
        self.sidebar = tk.Frame(window)
        self.sidebar.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10)

        # Create a vertical list frame for buttons and input fields
        self.vertical_list = tk.Frame(self.sidebar)
        self.vertical_list.pack(side=tk.TOP, fill=tk.Y)

        # Create a horizontal list frame for adding input fields
        self.input_list = tk.Frame(self.vertical_list)
        self.input_list.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Create a horizontal frame for the add and remove buttons
        self.button_frame = tk.Frame(self.input_list)
        self.button_frame.pack(side=tk.TOP, fill=tk.X)

        self.detect_button = tk.Button(self.button_frame, text="Load!", command=self.load_media, width=5)
        self.detect_button.pack(side=tk.LEFT, padx=5)

        # Create the plus and negative buttons for the horizontal frame
        self.plus_button = tk.Button(self.button_frame, text="+", command=self.add_input_field, width=2)
        self.plus_button.pack(side=tk.LEFT, padx=5)
        self.neg_button = tk.Button(self.button_frame, text="-", command=self.remove_input_field, width=2)
        self.neg_button.pack(side=tk.LEFT, padx=5)

        # Create an empty list of input fields
        self.input_fields = []

        # Add the horizontal list frame to the vertical list
        self.input_list.pack(side=tk.TOP, fill=tk.X, pady=5)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15

        self.is_media_running = False
        self.load_media()

        self.window.mainloop()

    def add_input_field(self):
        # Create a new input field and add it to the list
        input_field = tk.Entry(self.input_list)
        input_field.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.input_fields.append(input_field)

    def remove_input_field(self):
        # Remove the last input field from the list, if there is one
        if self.input_fields:
            input_field = self.input_fields.pop()
            input_field.destroy()

    def load_media(self):
        self.cameras = []
        # video_src = self.input_fields[0].get()
        video_src = "sb"
        if video_src is not None:
            # self.cameras.append(cv2.VideoCapture(video_src))
            self.cameras.append(cv2.VideoCapture("./assets/sample/192_168_5_101.mp4"))

        if (not self.is_media_running) and len(self.cameras) > 0:
            self.is_media_running = True
            self.run_media()

    def run_media(self):
        if not self.is_media_running:
            return
        if len(self.cameras) > 0:
            for cam in self.cameras:
                ret, frame = cam.read()

                if ret:
                    # Convert the frame from OpenCV to PIL format
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(image)

                    # Update the canvas with the new image
                    # self.canvas_width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
                    # self.canvas_height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
                    # self.canvas.config(width=self.canvas_width, height=self.canvas_height)
                    # self.canvas.delete("all")
                    self.canvas.create_image(0, 0, image=ImageTk.PhotoImage(image), anchor=tk.NW)

        # Call the update method again after a delay
        self.window.after(self.delay, self.run_media)


if __name__ == '__main__':
    # Create the application and start the main loop
    App(tk.Tk())
