Tripartite synapse paper

1. Goal 1: Simulation of both models
2. Goal 2: Generate bifurcation diagrams form python itslef
3. Goal 3: Tensorflow/DAPPER/self based approaches to estimating the test paramaters

File structure
1. sm_model: contains model in a function model(struct,t,y,*str)
2. sm_params: contains parameters estimated as a function of baseline rest and test parameters in a function parameters(struct,testparams,initvals)
3. sm_class: generates a class such that any class instance defined by classinstance = smclass(initvals,testparams) can refer to the model and parameters from sm_model and sm_params
4. sm_sim: simulates model using assimulo+sundials, also contains plotter(t,y,*str) which plots and saves any component from sm_model
