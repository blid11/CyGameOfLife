
This repository is meant to improve a previous project, [at this link]: (https://colab.research.google.com/drive/15g1jnxBquah6GUF4DoPkcKmu0FTRSl_-?usp=sharing), that was dedicated to finding new objects in the three-dimensional analogues of Conway's Game of Life (GOL).

It is a work in progress. Improvements include a GUI (with Tkinter) and more efficient code partially written in Cython. Cython can be used to integrate faster C/C++ code into Python programs. 

The code for cellular automaton simulations (simulation.pyx) is substantially faster than the previously written simulation classes, running 2000 simulations in 9.65 seconds instead of 6 minutes with poorly written Python. 

![image](https://user-images.githubusercontent.com/82735611/182790992-e0b990fd-6744-479a-8579-18bb7eae203d.png)

The previous project could produce animations of newly discovered objects, which can be seen [here]: (https://drive.google.com/drive/folders/1PKuUsbWEtwWcqKOcSlp65b6jJn_0glE3?usp=sharing)
