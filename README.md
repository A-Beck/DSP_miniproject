Andrew Becker (adb2jb) DSP miniproject 
======================================
Miniproject for ECE 4750 (dsp) at the University of Virginia

<b>Goal :</b> Use K-Means Clustering to identify trends in data in an InSAR dataset of the Monitor Merrimac Memorial Bridge Tunnel

<b>Language Used:</b> Python 2.7

<b>Packages Used:</b>
<p>
  matplotlib - used for graphing
</p>
<p>
  scipy - provide algorithmic support
</p>  
<b>Module Descriptions:</b>

  <em>Rect.py</em>
    Simple classes to model a rectangular area of interest and an InSAR point

  <em>segment.py</em>
    Uses EPSG:2284 coordinate system to select which InSAR points to use
    
  <em>main.py</em>
    Runs algorithms and plots the resulting data
