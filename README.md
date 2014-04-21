Andrew Becker (adb2jb) DSP miniproject 
======================================
Miniproject for ECE 4750 (dsp) at the University of Virginia

<b>Goal :</b> Use K-Means Clustering and Hierarchical Agglomerative Clustering to identify trends in data in an InSAR dataset of the south section Monitor Merrimac Memorial Bridge Tunnel

<b>Language Used:</b> Python 2.7

<b>Packages Used:</b>
<p>
  matplotlib - used for graphing
</p>
<p>
  scipy - provide algorithmic support
</p>  

<b>Module Descriptions:</b>

  <em>Struct.py</em>
    Simple classes to model a rectangular area of interest, an InSAR point, and a cluster

  <em>segment.py</em>
    Uses EPSG:2284 coordinate system to select which InSAR points to use
    
  <em>main.py</em>
    Runs algorithms and plots the resulting data, shows averages as well
    
<b> To run this code: </b>
  <p>
  Download the code. Run 'python main.py -h' to see help. Easiest way to run is 'python main --file='file' -c', where     'file' is a path to a shapefile. This will read insar data from a shape file. The -c option will allow the user to choose different coordinates than what I used.
  </p>
    
<b> Link to Video Presentation: </b> <p> https://www.movenote.com/v/DPCdzSCW9JDnK </p> 
