import cv2 as cv
import math
import numpy as np

'''
NOTE: This class will likely be adapted for difference 
video libraries opencv, decoder, ffmpeg
'''

class Video:
    r'''A Video class
    
    Properties
    ----------
    file_path: the location where the Video is stored
    fps: frame per second
    frame_count: number of frames in the video

    '''
    def __init__(self, file_path):
        r'''Creates Video instance

        Parameters
        ----------
        file_path

        '''
        #TODO: Look if you can use 'with cv.VideoCapture(file_path) as cap' to handle release
        cap = cv.VideoCapture(file_path)
        self.file_path = file_path

        # extract relevant parameters
        self.frame_count = cap.get(cv.CAP_PROP_FRAME_COUNT)
        self.fps = cap.get(cv.CAP_PROP_FPS)

        cap.release()

    def getPartitions(self, partition_count = 1):
        '''
        

        NOTES
        -----
        TODO: Figure out if video is processed until the end and fix if it doesn't
        if(partitions[-1] < self.frame_count):
            pairs_start_end.append([partitions[-1], int(self.frame_count)])

        '''
        partitions = np.arange(start = 1,
                                stop = self.frame_count,
                                step = math.floor(self.frame_count / partition_count),
                                dtype=int
        )
        # create pairs of starting and ending frames
        pairs_start_end = []
        for i in range(partitions.size - 1):
            pairs_start_end.append([partitions[i], partitions[i + 1]])

        # TODO: Figure out how to guarantee video is processed to the end if it isn't/
        #if(partitions[-1] < self.frame_count):
        #    pairs_start_end.append([partitions[-1], int(self.frame_count)])

        print("VIDEO: Video Total Frames:", self.frame_count)
        print("VIDEO: Video Frame Rate:", self.fps)
        print("VIDEO: Partition Step:", math.floor(self.frame_count / partition_count))
        print("VIDEO: Partitions:", partitions)
        print("VIDEO: Start End Pairs:", pairs_start_end)
        
        return pairs_start_end
    

if __name__ == "__main__":
    file_loc = 'videos/HortusdeEscapismo/HortusdeEscapismo.mkv'
    vid = Video(file_loc)
    partitions = 3
    vid.getPartitions(partitions)

    partitions = 4
    vid.getPartitions(partitions)
