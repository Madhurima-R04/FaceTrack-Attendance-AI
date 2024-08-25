import subprocess
import datetime
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import util
import os


class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1250x520+350+100")

        # Create login button
        self.login_button_main_window = util.main_window(self.main_window, 'login', 'green', self.login)
        self.login_button_main_window.place(x=750, y=300)

        # Create register new user button
        self.register_new_user_button_main_window = util.main_window(self.main_window, 'register new user', 'gray',
                                                                     self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=350)

        # Create webcam label
        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        # Add webcam
        self.cap = cv2.VideoCapture(0)  # Initialize webcam
        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'

    def add_webcam(self, label):
        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()
        if ret:
            self.most_recent_capture_arr = frame  # in OpenCV format
            img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
            self.most_recent_capture_pil = Image.fromarray(img_)  # in PIL format
            imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
            self._label.imgtk = imgtk
            self._label.configure(image=imgtk)
        self._label.after(20, self.process_webcam)

    def login(self):
        unknown_img_path = './.tmp.jpg'

        # Save the current frame as a temporary image for recognition
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

        try:
            # Run the face recognition command
            output = subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path])

            # Decode the output from bytes to string
            output_str = output.decode('utf-8').strip()

            # Extract the recognized name
            if "unknown_person" in output_str or "no_persons_found" in output_str:
                util.msg_box('Oops...', 'Unknown user. Please register a new user or try again.')
            else:
                recognized_name = output_str.split(',')[1].strip()  # Extract the recognized name
                util.msg_box('Welcome back!', 'Welcome, {}'.format(recognized_name))

                with open(self.log_path, 'a') as f:
                    f.write('{}, {} \n'.format(recognized_name, datetime.datetime.now()))

        except subprocess.CalledProcessError as e:
            print("Error during face recognition:", e)

        # Remove the temporary image after recognition
        os.remove(unknown_img_path)

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1250x520+370+120")

        self.accept_button_register_new_user_window = util.main_window(self.register_new_user_window, 'Accept', 'green',
                                                                       self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = util.main_window(self.register_new_user_window, 'Try Again',
                                                                          'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        # Start capturing webcam for the new user registration window
        self.process_webcam_for_register(self.capture_label)

        # Create and place the username label and entry field
        self.text_register_label_new_user = util.get_text_label(self.register_new_user_window,
                                                                'Please input your username:')
        self.text_register_label_new_user.place(x=750, y=70)

        self.entry_register_new_user = tk.Entry(self.register_new_user_window)
        self.entry_register_new_user.place(x=750, y=150)

    def process_webcam_for_register(self, label):
        # Capture the webcam feed and display it in the new user registration window
        ret, frame = self.cap.read()
        if ret:
            self.register_new_user_capture_arr = frame  # in OpenCV format
            img_ = cv2.cvtColor(self.register_new_user_capture_arr, cv2.COLOR_BGR2RGB)
            self.register_new_user_capture_pil = Image.fromarray(img_)  # in PIL format
            imgtk = ImageTk.PhotoImage(image=self.register_new_user_capture_pil)
            label.imgtk = imgtk
            label.configure(image=imgtk)
        label.after(20, lambda: self.process_webcam_for_register(label))

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def accept_register_new_user(self):
        # Get the username from the Entry widget
        name = self.entry_register_new_user.get()

        # Save the captured image with the username as the file name
        if name and self.register_new_user_capture_arr is not None:
            user_image_path = os.path.join(self.db_dir, '{}.jpg'.format(name))
            cv2.imwrite(user_image_path, self.register_new_user_capture_arr)
            print(f"Saved new user image at: {user_image_path}")

            # Show success message
            util.msg_box("Success", f"Successfully registered user: {name}")
        else:
            print("Error: Username or captured image is missing.")

    def start(self):
        self.main_window.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
