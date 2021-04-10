# The energy-deprived tripartite synapse
Running the simulations from the manuscript 'Ion dynamics of the energy-deprived tripartite synapse'

## Requirements
  - Install Python 3.x (anaconda recommended)
  - In a new environment install the following packages:
       - warnings
       - numpy
       - assimulo
       - matplotlib
       - scipy
       - json
       - os
       - autograd 
       - argparse

## Simulating
Refer to files 'Example' and Paper_Figures on how to run simulations. Run:
`chmod +x ./Example`
`Example`
[Example is outdated as of 10/04/2021. refer only to Paper_Figures] 

## GUI
A simple GUI was geenrated for didactic purposes, run:
`python -i set_up_GUI.py`

## Bifurcations
Bifurcation computations are stored in various .mat files in the folder 'BifFiles'. Running 'createbif.py' constructs the bifurcation diagram presented in Fig. 5 automatically.

## Further info
For any further questions, please contact m.kalia@utwente.nl


