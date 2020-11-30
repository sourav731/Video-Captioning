import cv2
import youtube_dl
import os
import shutil


class GenerateFrame:
    def __init__(self, video_id):
        self.video_id = video_id

    def generate_url(self):
        url = 'https://www.youtube.com/watch?v='+self.video_id

    def extract_info(self, url):
        ydl_info = {}
        ydl = youtube_dl.YoutubeDL(ydl_info)

        info_dict = ydl.extract_info(url, download=False)

        return info_dict

    def create_temporary_folder(self, path):
        try:
            os.mkdir(path)
        except OSError:
            print('generateframes.py : unable to create a directory')

        return

    def generate_frames(self, info_dict, path, folder_name):
        formats = info_dict.get('formats', None)
        temp_folder_path = os.path.join(path, folder_name)

        create_temporary_folder(temp_folder_path)

        for f in formats:
            if f.get('format_note', None) == '144p':
                url = f.get('url', None)
                cap = cv2.VideoCapture(url)

                if not cap.isOpened():
                    print('generatesframes.py : video unable to capture')

                i = 0

                while cap.isOpened():
                    ret, frame = cap.read()

                    if not ret:
                        break

                    cv2.imwrite(temp_folder_path+'/frame%d.jpg' % i, frame)
                    i += 1

                cap.release()

        cv2.destroyAllWindows()

    def delete_temporary_files(self, path, folder_name):
        temp_folder_path = os.path.join(path, folder_name)
        shutil.rmtree(temp_folder_path)
