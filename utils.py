import re
def remove_oid(string):
    while True:
        pattern = re.compile('{\s*"\$oid":\s*(\"[a-z0-9]{1,}\")\s*}')
        match = re.search(pattern, string)
        if match:
            string = string.replace(match.group(0), match.group(1))
        else:
            return string
# from PIL import Image
# import os
# import sys
# def compressMe(file, verbose = False):
#     filepath = os.path.join(os.getcwd(),file)
#       
#     # open the image
#     picture = Image.open(filepath)
#       
#     # Save the picture with desired quality
#     # To change the quality of image,
#     # set the quality variable at
#     # your desired level, The more 
#     # the value of quality variable 
#     # and lesser the compression
#     picture.save("Compressed_"+file, 
#                  "JPEG", 
#                  optimize = True, 
#                  quality = 10)
#     return
#   