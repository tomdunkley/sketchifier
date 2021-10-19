import cv2, datetime, os, requests, shutil, math, sys
import moviepy.editor as mpe
import numpy as np
from pytube import YouTube










class FrameExtractor():
    def __init__(self, video_path):
        self.video_path = video_path
        self.vid_cap = cv2.VideoCapture(video_path)
        self.n_frames = int(self.vid_cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.vid_cap.get(cv2.CAP_PROP_FPS))
        
    def get_video_duration(self):
        duration = self.n_frames/self.fps
        
    def get_n_images(self, every_x_frame):
        return math.floor(self.n_frames / every_x_frame) + 1
        
    def extract_frames(self, every_x_frame, img_name, dest_path=None, img_ext = '.jpg'):
        if not self.vid_cap.isOpened():
            self.vid_cap = cv2.VideoCapture(self.video_path)
        
        if dest_path is None:
            dest_path = os.getcwd()
        else:
            if not os.path.isdir(dest_path):
                os.mkdir(dest_path)
        
        frame_cnt = 0
        img_cnt = 0

        while self.vid_cap.isOpened():
            
            success,image = self.vid_cap.read() 
            
            if not success:
                break
            
            if frame_cnt % every_x_frame == 0:
                img_path = os.path.join(dest_path, ''.join([img_name, '_', str(img_cnt), img_ext]))
                cv2.imwrite(img_path, image)  
                img_cnt += 1
                
            frame_cnt += 1
        
        self.vid_cap.release()
        cv2.destroyAllWindows()







def pencilsketch(image_location, tags=""):
    jc = cv2.imread(image_location)

    scale_percent = 0.60

    width = int(jc.shape[1]*scale_percent)
    height = int(jc.shape[0]*scale_percent)

    dim = (width,height)
    resized = cv2.resize(jc,dim,interpolation = cv2.INTER_AREA)

    kernel_sharpening = np.array([[-1,-1,-1], 
                                  [-1, 9,-1],
                                  [-1,-1,-1]])
    sharpened = cv2.filter2D(resized,-1,kernel_sharpening)



    gray = cv2.cvtColor(sharpened , cv2.COLOR_BGR2GRAY)
    inv = 255-gray
    gauss = cv2.GaussianBlur(inv,ksize=(15,15),sigmaX=0,sigmaY=0)

    def dodgeV2(image,mask):
        return cv2.divide(image,255-mask,scale=256)

    pencil_jc = dodgeV2(gray,gauss)
    
    cv2.imwrite("temp/edited/image_"+tags+".jpg",pencil_jc)








def convert_video(youtubelink, outputfile="video.mp4", fps = 10, tempfolder="temp"):
    try:
        try:
            shutil.rmtree(tempfolder)
        except FileNotFoundError:
            pass    
        
        
        video = YouTube(youtubelink)
        location = video.streams.filter(file_extension = "mp4").first().download(tempfolder)
        fe = FrameExtractor(location)
        fe.extract_frames(every_x_frame=30//fps, img_name='frame', dest_path=tempfolder+'/frames')



        os.mkdir(tempfolder+"/edited")
        n_frames = fe.get_n_images(30//fps)
        for i in range(1,n_frames):
            try:
                pencilsketch(tempfolder+"/frames/frame_"+str(i)+".jpg", "0"*(7-len(str(i)))+str(i))
            except AttributeError:
                break





        image_folder = tempfolder+'/edited'
        video_name = tempfolder+'/video.avi'

        images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
        frame = cv2.imread(os.path.join(image_folder, images[0]))
        height, width, layers = frame.shape

        video = cv2.VideoWriter(video_name, 0, fps, (width,height))

        for image in images:
            video.write(cv2.imread(os.path.join(image_folder, image)))

        cv2.destroyAllWindows()
        video.release()


        video = mpe.VideoFileClip(location)
        audio = video.audio

        clip = mpe.VideoFileClip(tempfolder+'/video.avi')
        final = clip.set_audio(audio)

        final.write_videofile(outputfile)

        video.close()

    except Exception as e:
        print("An error ocurred,\n",e)

    try:
        shutil.rmtree(tempfolder)
    except FileNotFoundError:
        pass
