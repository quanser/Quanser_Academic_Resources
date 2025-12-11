import time
import numpy as np
import os

from pal.products.sensors import SensorsTrainer, SensorsDisplay
import cv2

white = np.full((480, 800, 3), 255, dtype=np.uint8)

with SensorsTrainer() as sensors, \
     SensorsDisplay() as lcd:   

     # Build full paths to find images if file is ran from another location. 
     # Picture files still need to be in the same location as this script. 

     # Directory where the script is located
     script_dir = os.path.dirname(os.path.abspath(__file__))
     pic1_path = os.path.join(script_dir, 'picture1.png')
     pic2_path = os.path.join(script_dir, 'picture2.png')
     mask_path = os.path.join(script_dir, 'mask.png')

     pic1 = cv2.imread(pic1_path, cv2.IMREAD_COLOR)
     pic2 = cv2.imread(pic2_path, cv2.IMREAD_COLOR)
     mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

     # # could use this instead if file is being ran from the folder 
     # # where this file is located. 
     # pic1 = cv2.imread('picture1.png', cv2.IMREAD_COLOR)
     # pic2 = cv2.imread('picture2.png', cv2.IMREAD_COLOR)
     # mask = cv2.imread('mask.png', cv2.IMREAD_GRAYSCALE)

     # Draw Image Example to show how to draw images into the screen. 
     lcd.clear()
     lcd.print_text("Draw Image Example", 3, 10)
     time.sleep(2)
     # draw image example
     lcd.draw_image(pic1, 0, 0)
     time.sleep(1)
     lcd.draw_image(pic2, 200, 50)
     time.sleep(1) 
     lcd.draw_image(mask, 400, 200)
     time.sleep(2) 
     lcd.clear()

     # Draw Image Example to show how begin/end draw works. 
     # Useful when multiple things need to be displayed at once. 
     lcd.print_text("Understanding Begin/End Draw", 3, 10)
     time.sleep(2)
     lcd.begin_draw()
     lcd.draw_image(pic1, 0, 0)
     time.sleep(1)
     time.sleep(0.5)
     lcd.draw_image(pic2, 200, 50)
     lcd.print_text("Understanding Begin/End Draw", 3, 10)
     time.sleep(0.5)
     lcd.end_draw()
     time.sleep(1) 
     lcd.draw_image(mask, 400, 200)
     time.sleep(2) 
     
     # Mask Image Example. Only looks for non 0 pixels in the mask to draw.  
     lcd.clear()
     time.sleep(0.5)
     lcd.print_text("Draw Image Mask Example", 3, 10, setColor=True, rgb=[0, 0, 255])
     time.sleep(2)
     lcd.draw_image(white, 0, 0)
     time.sleep(1) 
     lcd.draw_image_mask(pic1, mask, 0, 0)
     time.sleep(1) 
     lcd.draw_image_mask(pic2, mask, 0, 200)
     time.sleep(2)

     # Blend Image Example. Uses the given mask 
     # as the alpha component of the image so they can have different opacities. 
     lcd.clear()
     time.sleep(0.5)
     lcd.print_text("Draw Image Blend Example 1", 3, 10, setColor=True, rgb=[0, 0, 255])
     time.sleep(2) 
     lcd.draw_image(white, 0, 0)
     time.sleep(1) 
     lcd.draw_image_blend(pic1, mask, 0, 0)
     time.sleep(1) 
     lcd.draw_image_blend(pic2, mask, 0, 200)
     time.sleep(2)

     # Blend Image Example. Uses the given mask 
     # as the alpha component of the image so they can have different opacities. 
     lcd.clear()
     time.sleep(0.5)
     lcd.print_text("Draw Image Blend Example 2", 3, 10, setColor=True, rgb=[0, 255, 0])
     time.sleep(2) 
     lcd.draw_image(pic1, 0, 0)
     time.sleep(0.5) 
     lcd.draw_image_blend(pic2, mask, 0, 0)
     time.sleep(1) 


