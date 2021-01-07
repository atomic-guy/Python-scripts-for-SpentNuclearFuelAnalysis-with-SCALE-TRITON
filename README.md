## Python scripts for Spent Nuclear Fuel Analysis, using SCALE/TRITON output files.
![](https://img.shields.io/badge/python2.7-3572A5)
<br></br>
## Description
**Python scripts created for comparative analysis of the isotopic composition and radiotoxicity of spent fuel assemblies of EPR, AP-1000, ABWR and APR1400 reactors calculated using SCALE/TRITON code.** Due to the large amount of data that was to be analyzed, I prepared my own scripts in Python2.7, which allowed to speed up the task and minimize the risk of error. I am publishing these scripts, maybe they can be helpful for beginners who will carry out similar work in the future using the SCALE codes, especially with their output files.

* **read_keff.py** - script used to analyze the multiplication factor k-inf during fuel burnout.
* **merge_plot2.py, merge_plot3.py** - different versions of script used to prepare data from OPUS module files for generating charts and tables in LaTeX format.
* **reactor_sum.py** - script is used to calculate the parameters of the entire core of the selected reactor (the sum of all selected assemblies) and to prepare the data for the generation of graphs and tables in LaTeX format.
* **siverts.py, rcg.py** - scripts used to calculate radiotoxicity of isotopes of spent nuclear fuel.
<br></br>
> SCALE is a comprehensive modeling and simulation suite for nuclear safety analysis and design developed and maintained by Oak Ridge National Laboratory under contract with the U.S. Nuclear Regulatory Commission, U.S. Department of Energy, and the National Nuclear Security Administration to perform reactor physics, criticality safety, radiation shielding, and spent fuel characterization for nuclear facilities and transportation/storage package designs. [(...)](https://www.ornl.gov/scale)

