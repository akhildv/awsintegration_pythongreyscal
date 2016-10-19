import cv2
import os
import sys
import numpy
import csv
import threading
import boto
from boto.s3.key import Key
import boto.s3


req_ID = 0;    															#request_ID initialized
out_file  = open('output.csv', "wb")									#csv file location
writer = csv.writer(out_file,dialect='excel')


def con_awss3(directory,filename):										#connecting to the aws s3 server using credentials			
	
	#bucket_name = AWS_ACCESS_KEY_ID.lower() + 'bucket'
	conn = boto.connect_s3(AWS_ACCESS_KEY_ID,AWS_ACCESS_SECRET_KEY)
	bucket = conn.get_bucket('your_bucket_name')
	testfile = os.path.join(directory,filename)
	print 'Uploading %s to Amazon S3 bucket %s' % \
      (testfile, 'akiaiutnn5r7fuhyblwabucket')
	k = Key(bucket)
	k.key = filename
	k.set_contents_from_filename(testfile,cb=percent_cb, num_cb=10)     #uploading the image files into aws s3

def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()


def grey(folderpath,directory,request_ID):								#turning a normal image to greyscale image
	for filename in os.listdir(folderpath):
		path_to_image = os.path.join(folderpath, filename)
		if not os.path.isfile(os.path.join(directory,filename))== True:
			image = cv2.imread(path_to_image)
			
			gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			cv2.imwrite(os.path.join(directory,filename),gray_image)
			height, width , enum = image.shape
			mylist = [request_ID,filename,height,width]
			
			#mystr = "," .join(str[i] for i in mylist)
			#cv2.imshow('color_image',image)
			#cv2.imshow('gray_image',gray_image) 
			#cv2.waitKey(0)                # Waits forever for user to press any key
			#cv2.destroyAllWindows()
			writer.writerow(mylist)
			con_awss3(directory,filename)
			#k.key(b)
			
			#k.set_contents_from_filename(os.path.join(directory,filename),cb=percent_cb, num_cb=10	)
			
def out_path():												#defining output path for storing images in local directory after greyscale 
	directory = 'c:/output_requestid/'
	if not os.path.exists(os.path.dirname(directory)):
		os.makedirs(os.path.dirname(directory))
	return directory

def periodic_run():											#this method runs periodically for every 60 seconds 	
	global req_ID
	req_ID+=1
	threading.Timer(60,periodic_run).start()
	input_path = 'C:/Users/Public/request_id'
	output_path = out_path()
	grey(input_path,output_path,req_ID)
	
	
periodic_run()
	
	
