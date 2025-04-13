# VideoArchiver
The goal of this project is to facilitate faster archiving of in-game story text and any other
material that can be archived.
The way I hope to achieve that is by taking videos of the story/content and processing that.

My target games are Arknights and Reverse1999 but I hope to extend this project to as many games as possible.

## Rationale
From what I understand, usually getting the game files and processing those would make things easier.
However, companies try to protect their data as best as they can and reverse-engineering everything is 
not really possible for the average player, and probably(?) for the average (junior?) programmer. 
Another con is that it is game-specific, different game means a different way of hiding their data. 

Taking a video from youtube and letting GameArchiver process it is more accessible. 

## Installation ....
TODO: add later

## Currently using

Python                 3.11.4
numpy                  1.25.2
opencv-contrib-python  4.6.0.66
opencv-python          4.11.0.86
opencv-python-headless 4.9.0.80
paddleocr              2.7.3
paddlepaddle           2.6.1
pytesseract            0.3.13
easyocr                1.7.1

Note: considering migrating to C++ later.