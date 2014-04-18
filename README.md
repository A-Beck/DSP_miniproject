Andrew Becker (adb2jb) DSP miniproject 
======================================
Miniproject for ECE 4750 (dsp) at the University of Virginia

Goal : 

Use K-Means Clustering to identify trends in data in an InSAR dataset of the Monitor Merrimac Memorial Bridge Tunnel

Language Used: Python 2.7

Packages Used:
  matplotlib - used for graphing
  scipy - provide algorithmic support
  
Module Descriptions:
  Rect.py
    Simple classes to modle a rectangular area of interest and an InSAR point

  segment.py
    Uses EPSG:2284 coordinate system to select which InSAR points to use
    
  main.py
    Runs algorithms and plots the resulting data
