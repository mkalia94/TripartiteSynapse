# The Tripartite Synapse

## Dependencies
Runs on Python 3.x
Dependencies: scipy, numpy, assimulo, matplotlib, argparse, timeit

## Sample Run
An example of running multiple experiments in a bash script is done in `Code/RunExp`

## How to use 
1. Download files.
2. Run `python -i fm_class.py --freeparams [OPTIONAL , *arguments] --solve [OPTIONAL] -write [OPTIONAL] -s[OPTIONS: -b or -m] --name [OPTIONAL, 1 argument] --plot [OPTIONAL, *arguments] --block [OPTIONAL, argument = dict] --excite [OPTIONAL, argument = list] --astblock [OPTIONAL, argument = list]`
* `--freeparams` should be followed by strings of code you would like to execute before leak parameter calculation. An example is: `--freeparams 'pumpScaleNeuron=2'`. This would set the baseline Neuronal pump strength to 2 times the default value. For details refer to fm_class.py and fm_params.py
* `--solve` solves the system
* `--write` writes the initial and final membrane potential to the file `Code/Experiments.txt`
* `-s` uses a small initial ECS (20%). `-m` corresponds to 50% (mid-size) and `-b` corresponds to 98%
 (big-size)
* `--name` gives a name to the experiment run. Example: `--name 'Experiment 1`
* `--plot` plots expressions in different figures and outputs everything at the end of the experiment. Example: `--plot 'V' 'Vg' 'NaCi'` plots neuronal membrane potential `V`, astrocyte membrane potential `Vg` and neuronal sodium concentration `NaCi`.
* `--block` blocks a particulkar current for a given duration. Example: `--block '{"INaG":[10,20],"JKCl":[20,30]}'` blocks the transient sodium current from minute 10 to 20 and the potassium-chloride cotransporter from minute 20 to minute 30.
* `--excite` excites the neuron with a square wave, thereby producing bursts of action potentials, for a given duration. Example: `--excite [20,30]` excites the neuron with a square wave from minute 20 to 30
* `--astblock` blocks all astrocyte processes for a given duration. Example: `--astblock [20,30]` blocks astrocyte activity from minute 20 to minute 30.

## Example
Running 
`python -i fm_class.py --freeparams 'pumpScaleAst=2' 'pumpScaleNeuron=2' 'tstart=20' 'tend=25' --solve --write -s --name 'HyperNKA2' --plot 'GluCi' 'CaCi' 'GluCg' 'CaCg'`
will simulate the tripartite synapse under 5 minutes of metabolic stress, when the baseline pump strength is set to twice its initial strength. The name of the experiment is `HyperNKA2` and the result is written to `Code/Experiments.txt`. After the simulation plots of calcium and glutamate concentrations in the neuron (presynaptic terminal) and astrocyte (perisynaptic astrocyte process) in separate figures. 

## Pipeline
1. Collect parameters from `--freeparams`.
2. Compute remaining parameters from `fm_params.py` to calibrate to fixed conditions, the parameters include: all leak conductances, impermeable anions and cations.
3. Define model class in `fm_class.py`. Contains ODE RHS (written in `fm_model.py`) and all parameters.
4. Solve ODE.
5. If `--write`, write to `Experiments.txt`.
6. If `--plot`, plot.

## File structure
1. `fm_model.py`: contains model in a function model(struct,t,y,kwargs)
2. `fm_params.py`: contains parameters estimated as a function of baseline rest and test parameters in a function parameters(struct,testparams,initvals)
3. `fm_class.py`: **Main file**: Performs all argument parsing, generates a class such that any class instance defined by classinstance = smclass(initvals,testparams) can refer to the model and parameters from `fm_model.py` and `fm_params.py`. Then solves the system and performs plotting of results.

