import numpy as np
import cv2 as cv
import os
#import cProfile
import math
import time
import multiprocessing as mp
import OCR.OCR as ocr
import psutil
from Video.Video import Video
import scipy.integrate._quadrature

'''
NOTE:
THIS CLASS WILL POSSIBLY BE ADAPTED TO simply function as
vd = VideoReader()
vd.processVideo(Video, OCR)

Currently this refactoring will take  time
and may unnecessarily complicate strucuture
'''
# constant for the distance in seconds between frames
SECONDS_INTERVAL = 300

# Consider creating a Video class.
class VideoReader:
    r''' A class that reads the subtitles from a Video

    Attributes
    -------------
    file_path: string
        path to the video
    Video: Video
        A Video instance
    
    '''

    def __init__(self, file_path):
        r'''Create VideoReader instance


        Parameters
        ----------
        file_path: string
            path to the file to read from.

        Returns
        -------
        videoReader: VideoReader
            instance of VideoReader

        Raises
        ------
        File_Not_Found 
            when file cannot be located at file_path 
        File_Not_Video
            when the file located at file_path is not a Video
        '''
        self.file_path = file_path
        self.Video = Video(file_path)


    def processVideo(self, multiprocessing = False):
        r'''
        
        Paramaters
        ----------
        multiprocessing: bool
            boolean whether to process Video using multiple processes
        
        Returns
        -------
        TODO: Define/Pick a type/class that stores the subtitles
        '''
        if multiprocessing == True:
            print("processVideo:       Multiprocessing")
            # Forgive the naming inconsistency, this used to be a constant 
            # Use half of physical core count.
            # TODO: Research into process_count optimizations or sth
            processes_count = psutil.cpu_count(logical=False) // 2

            # store Futures of the processes to wait for them to conclude
            futures = []

            # consider initializing with videoCapture as sharedMemory
            pool = mp.Pool(processes = processes_count)

            # loop over pairs and start processes
            pairs = self.Video.getPartitions(partition_count=processes_count)
            for pair in pairs:
                f = pool.apply_async(self.processVideoFrameRange, args=(True, pair[0], pair[1]))
                futures.append(f)

            for f in futures:
                f.get()
            
            print("Processes Complete")

        else:
            print("processVideo:       Not Multiprocessing")
            self.processVideoFrameRange(multiprocessing = multiprocessing, startFrame = 0, endFrame= self.Video.frame_count)
        

    def processVideoFrameRange(self, multiprocessing = False, startFrame = 0, endFrame = 1):
        if (multiprocessing == True):
            print("I am Process: ", os.getpid())
            print("I am responsible for:[%d, %d]" % (startFrame, endFrame))

        try:
            cap = cv.VideoCapture(self.file_path)
        except Exception as e:
            print("Exception when trying to Read Video:", e)
            return

        frame_offset = SECONDS_INTERVAL * self.Video.fps
        frames = np.arange(start = startFrame, stop = endFrame, step = frame_offset, dtype=int)
        print("My frames are: ", frames)
        
        myOCR = ocr.OCR()

        for frame in frames:
            cap.set(cv.CAP_PROP_POS_FRAMES, frame)
            ret, frame = cap.read()
            
            #when using 3 processes encountering 
            #!_src.empty() in function 'cv::cvtColor'
            #try:
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            height, width, channels = frame.shape
            #frame = frame[int(height*0.86):height, 0:width]
            frame = frame[int(height*0.85):height, int(width*0.18):int(width*0.9)]
            print(myOCR.infer(frame))
            #except Exception as e:
            #    print("I am", os.getpid())
            #    print("I am throwing an exception:", e)

        cap.release()
        print("Video Ended")
        #pr.disable()
        #pr.print_stats(sort='cumtime')

if __name__ == '__main__':
    #system_summary()
    file_loc = 'videos/HortusdeEscapismo/HortusdeEscapismo.mkv'
    multiprocessing = True

    vd = VideoReader(file_loc)
    vd.processVideo(multiprocessing=multiprocessing)

    #cProfile.run("processesStart()")
    #processVideoSingleProcess()
    #cProfile.run("processVideoSingleProcess()")