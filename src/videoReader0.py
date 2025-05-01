import numpy as np
import cv2 as cv
import os
#import cProfile
import math
import time
import multiprocessing as mp
import OCR.OCR as ocr
import gc
import psutil

## YIPPIEEEEEEEEEEE
## PROCESSEC=S_COUNT = 6 SECONDS_INTERVAL = 2 
# [Done] exited with code=0 in 409.744 seconds

# constants
PROCESSES_COUNT = 6
# should be 1~5
SECONDS_INTERVAL = 200
FILE_LOCATION = 'videos/HortusdeEscapismo/HortusdeEscapismo.mkv'


# get video
try:
    cap = cv.VideoCapture(FILE_LOCATION)
except Exception as e:
    print("Exception when trying to Read Video:", e)

# extract relevant parameters
frame_count = cap.get(cv.CAP_PROP_FRAME_COUNT)
fps = cap.get(cv.CAP_PROP_FPS)
frame_offset = SECONDS_INTERVAL * fps
partitions = np.arange(start = 1,
                        stop = frame_count,
                        step = math.floor(frame_count / PROCESSES_COUNT),
                        dtype=int
)
# create pairs of starting and ending frames
pairs_start_end = []
for i in range(partitions.size - 1):
    pairs_start_end.append([partitions[i], partitions[i + 1]])
if(partitions[-1] < frame_count):
    pairs_start_end.append([partitions[-1], int(frame_count)])

print("Video Total Frames:", frame_count)
print("Video Frame Rate:", fps)
print("Skip Seconds Interval:", SECONDS_INTERVAL)
print("Number of iterations (single process):", math.floor(frame_count/frame_offset))
print("Partition Step:", math.floor(frame_count / PROCESSES_COUNT))
print("Partitions:", partitions)
print("Start End Pairs:", pairs_start_end)

frames = np.arange(start = 1, stop = frame_count, step = frame_offset, dtype=int)

def processesStart():

    # store Futures of the processes to wait for them to conclude
    futures = []

    # consider initializing with videoCapture as shared variables
    pool = mp.Pool(processes = PROCESSES_COUNT)

    # loop over pairs and start processes
    for pair in pairs_start_end:
        f = pool.apply_async(processVideoFrameRange, args=(pair[0], pair[1]))
        futures.append(f)

    for f in futures:
        f.get()
    
    cap.release()
    print("Processes Complete")

# processes the frames in the range
def processVideoFrameRange(startFrame, endFrame):
    print("I am Process: ", os.getpid())
    print("I am responsible for:[%d, %d]" % (startFrame, endFrame))
    #pr = cProfile.Profile()
    #pr.enable()
    try:
        cap = cv.VideoCapture(FILE_LOCATION)
    except Exception as e:
        print("Exception when trying to Read Video:", e)

    frames = np.arange(start = startFrame, stop = endFrame, step = frame_offset, dtype=int)
    print("My frames are: ", frames)
    myOCR = ocr.OCR()

    for frame in frames:
        cap.set(cv.CAP_PROP_POS_FRAMES, frame)
        ret, frame = cap.read()
        
        #when using 3 processes encountering 
        #!_src.empty() in function 'cv::cvtColor'
        try:
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            height, width, channels = frame.shape
            #frame = frame[int(height*0.86):height, 0:width]
            frame = frame[int(height*0.85):height, int(width*0.18):int(width*0.9)]
            myOCR.infer(frame)
        except Exception as e:
            print("I am", os.getpid())
            print("I am throwing an exception:", e)

    cap.release()
    print("Video Ended")
    #pr.disable()
    #pr.print_stats(sort='cumtime')


def system_summary():
    print("Logical Cores:",psutil.cpu_count(logical=True))
    print("Physical Cores:",psutil.cpu_count(logical=False))
    print("RAM Memory (GB):", int(psutil.virtual_memory().total / 1048576))


if __name__ == '__main__':
    #system_summary()
    processesStart()
    #cProfile.run("processesStart()")
    #processVideoSingleProcess()
    #cProfile.run("processVideoSingleProcess()")