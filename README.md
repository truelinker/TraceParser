# TraceParser
It is a python script that can make a concise and readable log file by changing the trace and enum number to find the large size log file that occurs during development into an enum string.

# How to Use
Developed in python3 version, install the required module first, specify the source code where the enum is defined and the location of the file you want to filter, and run the corresponding python script.
```
  ## Set Virtual environment and install modules if not installed yet.
  1. python3 -m venv env
  2. env/bin/activate
  3. python3 -m pip install tqdm
  4. python3 -m pip install pyparsing
  
  ## Set the path for the enum definition and log file
  
  # Run the script
  python3 ./parseLog.py

```
