To create the installer:
1) Export the conda environment <env_name>:
 - in the conda console:
  >conda install -c conda-forge conda-pack
  >conda pack -n <env_name>
2) Retrieve output pack in C:/Users/<Username>/<env_name>.tar.gz
3) Move <env_name>.tar.gz to any working path <work_path>
4) In the system console:
 >cd <work_path>
 >mkdir -p <env_name>
 >tar -xzf <env_name>.tar.gz -C <env_name>
5) Move the Code folder in <work_path/<env_name>
6) Check if the code works:
 - in the system console:
  >cd <work_path>/<env_name>/
  >python "Code/trisynGUI.py"
7) If there are modules missing:
 - in the system console:
  >cd <work_path/<env_name>/
  >"Scripts/pip" install --ignore-installed <module_name>==<module_version>
  
  possible missing modules:
  - numpy==1.18.1
  - matplotlib==3.1.3
  - scipy==1.4.1
  - autograd==1.3
  - argparse==1.4.0
  - appjar==0.94.0
  - pylatexenc==2.6
  - brokenaxes==0.4.2
8) Repeat point 6, the code should now work smoothly.
-- For Windows --
9) Rename the folder <env_name> "trisyn_standalone" and send it to a compressed folder
10) Move trisyn_standalone.zip to TriSyn/Installer/
11) Using Inno Script Studio compile trisyn_setup.iss
12) In TriSyn/Installer/Output/ there will be the installer mysetup.exe
