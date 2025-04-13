import numpy as np
import cv2 as cv
import cProfile
import math
import time

cap = cv.VideoCapture('videos/HortusdeEscapismo.mkv')
frame_count = cap.get(cv.CAP_PROP_FRAME_COUNT)
fps = cap.get(cv.CAP_PROP_FPS)
# set offset by the amount of time/frames you want to skip
# example:
# want to skip 2 seconds
frame_offset = 50 * fps
print("Video Total Frames:", frame_count)
print("Video Frame Rate:", fps)
print("Number of iterations:", math.floor(frame_count/frame_offset))


frames = np.arange(start = 1, stop = frame_count, step = frame_offset, dtype=int)

def processVideo():
    for frame in frames:
        
        t0 = time.perf_counter()
        cap.set(cv.CAP_PROP_POS_FRAMES, frame)
        t1 = time.perf_counter()
        dt = t1 - t0
        print(f"jump to {frame:3d}: {dt:.3f} s", "*" * int(round(dt/0.1)))

        # read the next frame
        # if frame is read correctly ret is True
        ret, frame = cap.read()

        # operations on frame here
        # couple into processFrame() function
        # if it becomes more complex
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    cap.release()
    print("Video Ended")
    cv.destroyAllWindows()


cProfile.run("processVideo()")

# older code
'''
# loop over the frames
def processVideo1():
    frame_number = 0
    while cap.isOpened():

        # update frame number
        frame_number += 1
        # set target to next frame
        cap.set(cv.CAP_PROP_POS_FRAMES, frame_number * frame_offset)

        # read the next frame
        # if frame is read correctly ret is True
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # operations on frame here
        # couple into processFrame() function
        # if it becomes more complex
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
    cap.release()
    print("Video Ended")
    cv.destroyAllWindows()
'''
