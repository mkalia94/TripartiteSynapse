Energy deprived Tripartite Synapse

# Dependencies
Runs on Python 3.x
Dependencies: scipy, numpy, assimulo, matplotlib, argparse, timeit

# How to use 
1. Download files.
2. Run `python -i fm_class.py --freeparams [OPTIONAL , *arguments] --solve [OPTIONAL] -write [OPTIONAL] -s[OPTIONS: -b or -m] --name [OPTIONAL, 1 argument] --plot [OPTIONAL, *arguments]`
* The argument --freeparams should be followed by strings of code you would like to execute before parameter calculation. An example is: `--freeparams 'pumpScaleNeuron=2'`. This would set the baseline Neuronal pump strength to 2 times the default value. For details refer to fm_class.py and fm_params.py
* The argument `--solve` solves the system
* The argument `--write` writes the initial and final membrane potential to the file `Experiments.txt`



File structure
1. sm_model: contains model in a function model(struct,t,y,*str)
2. sm_params: contains parameters estimated as a function of baseline rest and test parameters in a function parameters(struct,testparams,initvals)
3. sm_class: generates a class such that any class instance defined by classinstance = smclass(initvals,testparams) can refer to the model and parameters from sm_model and sm_params
4. sm_sim: simulates model using assimulo+sundials, also contains plotter(t,y,*str) which plots and saves any component from sm_model
