# Dailymotion_internship
Here is the code made during my 3 month internship at Dailymotion.
The aim was to create an algorithm capable of automatically select thumbnails.
Thumbnail selection is based on the aesthetics of the image and the relevancy to the video.
This second part was quite a challenge and could not be finished in given time. 
The file process_video.py recieves a video and outputs the thumbnail (image with the best aesthetic score)
In the folder get_thumbnails/files_withClassification there is the code that classifies images with Inception V3.
However, this code outputs the top 5 aesthetic images and top 5 images form the majority class (or main subject of the video). As it does not output a single image, this could not be used, but can be researched further if needed.
