# sketchifier
Convert a youtube video to a sketch-style similar to that bit in take on he by a-ha

Call convert_video(youtubelink, outputfile="video.mp4", fps = 10, tempfolder="temp")
Where:
youtubelink is a string, the link to the youtube video
outputfile is where thre output video should go
fps is the fps you want (max 30, the program will allow you to do more than this but youtube native is 30fps so it's a waste of time)
tempfolder is the name of a folder that can be created and deleted safely, if "temp" is already in use then you MUST change this to something that is not, ,or else there may be erroneous deletion of files
