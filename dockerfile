FROM python:3.9.5

ENV PYTHONUNBUFFERED=1

# Update the WORKDIR to reflect the correct project directory
WORKDIR /usr/app/src/CBG_Fleming_Model_LB

RUN pip3 install numpy==1.23.1 scipy==1.9.0 PyNN==0.10.0
RUN pip3 install NEURON==8.0
RUN pip3 install nrnutils==0.2.0
RUN pip3 install pyyaml

# Ensure the path to the patch file is correct
COPY ./Cortex_BasalGanglia_DBS_model_LB/Updated_PyNN_Files/pynn-steady-state.patch ./
WORKDIR /usr/local/lib/python3.9
RUN patch -p1 < /usr/app/src/CBG_Fleming_Model_LB/pynn-steady-state.patch

WORKDIR /usr/local/lib/python3.9/site-packages/pyNN/neuron/nmodl
RUN nrnivmodl

RUN apt-get update
RUN apt-get -y install openmpi-bin=3.1.3-11
RUN pip3 install mpi4py==3.1.4
RUN apt-get -y install time
RUN pip3 install debugpy cerberus

# Switch back to the correct WORKDIR
WORKDIR /usr/app/src/CBG_Fleming_Model_LB

# Make sure all COPY commands refer to the correct source directory
COPY ./Cortex_BasalGanglia_DBS_model_LB/burst_data/*.txt ./burst_data/
COPY ./Cortex_BasalGanglia_DBS_model_LB/network_structure/*.txt ./network_structure/
COPY ./Cortex_BasalGanglia_DBS_model_LB/network_structure/*.npy ./network_structure/
COPY ./Cortex_BasalGanglia_DBS_model_LB/neuron_mechanisms/*.mod ./neuron_mechanisms/

WORKDIR /usr/app/src/CBG_Fleming_Model_LB/neuron_mechanisms
RUN nrnivmodl

WORKDIR /usr/app/src/CBG_Fleming_Model_LB

# Ensure Python scripts and configuration files are copied from the correct directory
COPY ./Cortex_BasalGanglia_DBS_model_LB/*.py ./
COPY ./Cortex_BasalGanglia_DBS_model_LB/*.npy ./
COPY ./Cortex_BasalGanglia_DBS_model_LB/configs/*.yml ./configs/

ENTRYPOINT ["mpirun", "--allow-run-as-root", "-np", "4", "python3", "/usr/app/src/CBG_Fleming_Model_LB/run_model.py"]
CMD ["/usr/app/src/CBG_Fleming_Model_LB/configs/conf_zero_4s.yml"]
