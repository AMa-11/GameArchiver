import numpy as np
import cv2 as cv
import os
import cProfile
import math
import time
import multiprocessing as mp

# constants
PROCESSES_COUNT = 3
# should be 1~5
SECONDS_INTERVAL = 200
FILE_LOCATION = 'videos/HortusdeEscapismo.mkv'


# get video
cap = cv.VideoCapture(FILE_LOCATION)

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
print("Number of iterations:", math.floor(frame_count/frame_offset))
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

    cap = cv.VideoCapture(FILE_LOCATION)

    frames = np.arange(start = startFrame, stop = endFrame, step = frame_offset, dtype=int)
    print("My frames:", frames)

    for frame in frames:
        cap.set(cv.CAP_PROP_POS_FRAMES, frame)
        ret, frame = cap.read()
        #when using 3 processes encountering 
        #!_src.empty() in function 'cv::cvtColor'
        
        try:
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        except Exception as e:
            print("I am", os.getpid())
            print("I am throwing an exception:", e)

    cap.release()
    print("Video Ended")



def processVideoSingleProcess():
    for frame in frames:
        t0 = time.perf_counter()
        cap.set(cv.CAP_PROP_POS_FRAMES, frame)
        t1 = time.perf_counter()
        dt = t1 - t0
        #print(f"jump to {frame:3d}: {dt:.3f} s", "*" * int(round(dt/0.1)))

        # read the next frame
        # if frame is read correctly ret is True
        ret, frame = cap.read()

        # operations on frame here
        # couple into processFrame() function
        # if it becomes more complex
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    cap.release()
    print("Video Ended")
    

if __name__ == '__main__':
    processesStart()
    #cProfile.run("processesStart()")
    #processVideoSingleProcess()