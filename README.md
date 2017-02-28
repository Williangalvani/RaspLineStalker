# RaspLineStalker
A line follower attempt usin the raspberry pi camera and tensorFlow

[![Alt text for your video](http://galvanicloop.com/media/posts/post18/test1.png)](http://galvanicloop.com/media/posts/post18/test1.webm)


##Requirements:

    sudo apt-get remove python-scipy
    sudo apt-get install gfortran libblas-dev liblapack-dev
    sudo pip install git+git://github.com/google/skflow.git

## Execution:

First, open "follower1.tt" on V-Rep.

###To record the training data:

Change on follower.py:
    
        GRAVA = True
        USAREDE = False

Then run follower.py and use the camera to manually control the robot with "awsd" keys.

###To train and run:


Change on follower.py:
    
        GRAVA = False
        USAREDE = True

Then run follower.py and wait.
