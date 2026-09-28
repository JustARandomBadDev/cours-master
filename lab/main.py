#!/usr/bin/python

from cv2 import imread

import numpy as np

def correlation(image: np.ndarray, mask: np.ndarray):
    height, width, _ = image.shape
    m_height, m_width = mask.shape
    
    out = np.ndarray((height, width))
    
    out.fill(0)
    
    for y in range(height):
        for x in range(width):
            
            
            for m_y in (range(m_height)):
                for m_x in range(-m_width//2, m_width//2):
                    if y + m_y < 0 or y + m_y >= height or x + m_x < 0 or x + m_x >= width: continue
                    
                    out[y, x] += image[y + m_y, x + m_x] * mask []
                    
                    
    
    

if __name__ == "__main__":
    img = imread("image.jpg")