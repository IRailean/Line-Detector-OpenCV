# Line-Detector-OpenCV
Big thanks to Adrian Rosebrock for the [tutorial](https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/)  
Road line detector using OpenCV, Python and moviepy  

Run the script using command:  
```
python LineDetector.py -i <path_to_input_video>
```
Output video will be created in folder where script is located

## Defining ROI  
Firstly, we have to define Region Of Interests.  
Let's imagine what does road lines look like in front of the car  
  
<img src="https://i.imgur.com/O1OtyKM.jpg" width="300" height="200">

There are two **straight** lines that are approaching towards the horizon.  
(Unless you have such roads, but this isn't our case)  
  
<img src="https://tnimage.taiwannews.com.tw/photos/shares/591293a43befa.jpg" width="300" height="200">

So, the lines form a triangle. This is our Region Of Interest. 
In order to process lines only in defined ROI, the image will be cropped (also converted to gray scale)
  
<img src ="https://i.imgur.com/aAwKFEH.png" width="300" height="200"/>

## Detecting lines in a picture  
To find lines, it's needed to find edges. [Canny edge detector](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_canny/py_canny.html) will be used for this.  
This way, such image is obtained  
  
<img src="https://i.imgur.com/Tys6tCR.png" width="300" height="200"/>

One can see that there is discontinuous line on the left side.  
Since we need two straight lines from the left and from the right sides. This discontinuous line has to be connected is some way.  
For this [Hough line transformation](https://docs.opencv.org/2.4/doc/tutorials/imgproc/imgtrans/hough_lines/hough_lines.html) will be used  
Obtained lines will be extended to form one continuous line, colored to green color and overlaid with the original image.  
So, the resulting image will look something like this:  
  
<img src="https://i.imgur.com/zlZwQEE.png" width="300" height="200"/>

## Detecting lines in a video
To run this algorithm for video moviepy is used.  
In order to do this, put all image processing, that was discussed above into **pipeline** function and then send this function as a parameter to one of the moviepy's functions **.fl_image(pipeline)**.  
Lines will be updated each 25 frames, i.e. approx 1 second.

<img src="https://media.giphy.com/media/Md3tc1yXhw0WL4BgZD/giphy.gif" width="300" height="200"/>
