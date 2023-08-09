# Muon scattering tomography end-to-end simulation framework

This repository aims at guiding the user for the installation of an end-to-end muon scattering tomography framework required for the BND School 2023, held in Wuppertal, Germany. For more information, please have look at the [introductory slides] (not available yet).

*N.B: The full installation might take some time. Please make sure that you **install the framework prior to the workshop**! If you run into issues you cannot solve by yourself, please use the [dedicated slack chanel](https://join.slack.com/t/bndschoolmuog-b2x9179/shared_invite/zt-1y9t2l2h0-zxvZcvoVf1YD0iqp7_3EPg) or contact us at maximelagrange98@gmail.com*.

## Installation

Debuging GEANT4 code can be a painful experience. In order to make this workshop a succes, one need every participant to run the same **Operating System** (OS) so that everybody is on the same page. A "simple" solution is the use of a **Virtual Machine** (VM),  a compute resource that uses software instead of a physical computer to run programs and deploy apps. Using it, every participant will be able to run the same OS, in our case **Ubuntu 22.04**.

*N.B: If you already run Ubuntu, please get the 22.04 and create a new user account to make sure that our installations do not create any conflicts with your existing working environement. In case you do not want to update, you can create a virtual machine like the others.*

### I - Virtual machine

#### A - VirtualBox

First, you want to install the VirtualBox software. The installation guide can be found [here](https://www.virtualbox.org/manual/ch02.html). Depending on your OS, you can also checkout these youtube tutorials where is installation is done step by step.

- [MacOS with Apple silicon M1/M2 processors](https://www.youtube.com/watch?v=KV90vu3tpjI)
- [MacOS with Intel processor](https://www.youtube.com/watch?v=hd0Lbtly41Y)
- [Windows 11](https://www.youtube.com/watch?v=b866-7Y_0KQ)
- [Windows 10](https://www.youtube.com/watch?v=8mns5yqMfZk)
- [Ubuntu](https://www.youtube.com/watch?v=SUPoqRPn9to)

Once VirtualBox is installed, you can go to the next step and create the virtual machine which will host the Ubuntu OS.

#### B - Creating a virtual machine


First, download the Ubuntu 22.04 iso file from the [ubuntu website](https://ubuntu.com/download/desktop).

Depending on your initial OS, checkout these videos which detail how to create an Ubuntu virtual machine:

- [Windows](https://www.youtube.com/watch?v=zHwFtyxJsog)
- [Mac](https://www.youtube.com/watch?v=b_tOialCSXE)

*N.B Make sure you assign enough disk to the virtual machine. At least **35 GB**.*

#### C - Virtual machine testing

Now that your virtual machine is created, you have to **make sure** that you can connect the machine to **internet via Wi-Fi**, and that you are able to **open the terminal**. 

In case you run into issues, you can check these links:

- [Unable to access Wi-Fi](https://windowsreport.com/wifi-error-virtualbox/)
- [Unable to open terminal](https://askubuntu.com/questions/1435918/terminal-not-opening-on-ubuntu-22-04-on-virtual-box-7-0-0)

 ### II - GEANT4 - Root installation

Using the freshly created Ubuntu virtual machine, we will proceed to the installation of both Root ad GEANT4.

#### A - Micromamba installation

Conda is a very useful tool for packages and dependecies installation and updates. We will use `micromamba` (https://mamba.readthedocs.io/en/latest/installation.html) which is a tiny version of the `mamba` package manager, itself being a reimplementation of `conda`.

Using `micromamba` allows for a straighforward installation of both GEANT4 and Root, as well as all the required packages and libraries.

Open a terminal in your `/home/user/` directory and run:

```
wget -qO- https://micromamba.snakepit.net/api/micromamba/linux-64/latest | tar -xvj bin/micromamba
./bin/micromamba shell init -s bash -p ~/micromamba
source ~/.bashrc
```
#### B - GEANT4 - Root installation
Now download the `geant-root.yml` and move it to `/home/user/`. Go in the `/home/usr/` directory (replace `usr` by your actual user name) and run:

```
./bin/micromamba create -f geant-root.yml
```

Install cmake:

```
sudo apt install cmake
```

Let's check if the installation worked:

```
micromamba activate geant-root
cd micromamba/envs/geant-root/share/Geant4-11.0.3/examples/basic/B1/
mkdir build
cd build
```

We will now run the `cmake ../` command. BEFORE CONTINUING, MAKE SURE YOU ARE IN THE `build/` DIRECTORY!

```
cmake ../
make
```

Now is the moment of truth! Try to run the exampleB1 by running:

```
./exampleB1
```

You should see a window poping, which displays the structure of the detector (if you run into errors, please report it in the dedicated Slack channel). Once you it is working properly, you can delete the build directory. Another one will be created during the installation of CRY.

The exampleB1 will be used as base for the activities of this workshop, so do not modify it, neither any other file in the B1 directory (unless we ask you to do so)!

### III - CRY installation

[CRY](https://nuclear.llnl.gov/simulation/doc_cry_v1.7/cry.pdf) is cosmic-ray shower librairy used to generate correlated cosmic-ray particle shower distributions. Installing it and linking it to GEANT4 will allow us to simulate cosmic muons and propagate them through our detector and volume of interest.

#### A - Download

CRY can be downloaded [here](https://nuclear.llnl.gov/simulation/). Download it, open a terminal window an run:

```
cd Downloads/
tar -xvf cry_v1.7.tar.gz
mv cry_v1.7 ../micromamba/envs/geant-root/
```

#### B - Make

Now we will go in the cry_directory (`micromamba/envs/geant-root/`) and make CRY. This will create a `libCRY.a` file in `cry_v1.7/lib`.

```
cd ../micromamba/envs/geant-root/cry_v1.7/
make
```

#### C - Modify CMakeLists.txt

It is now possible to link CRY to exampleB1. In order to do so, we must modify the CMakeLists.txt so that GEANT4 knows how to access the CRY library (Replace `usr` by your username in the path). Since we are here, we will also link Root with GEANT4.

```
cd /home/usr/micromamba/envs/geant-root/share/Geant-4-11.0.3/examples/basic/B1/
```

Open the `CMakeLists.txt` file and after `project(B1)` add the following lines:

```
set(CRY_PATH /home/usr/micromamba/envs/geant-root/cry_v1.7)
set(CRY_LIB -L${CRY_PATH}/lib libCRY.a)
include_directories(${CRY_PATH}/src)

# Find ROOT (required package)

list(APPEND CMAKE_PREFIX_PATH $ENV{ROOTSYS})
find_package(ROOT REQUIRED COMPONENTS RIO)
include(${ROOT_USE_FILE})
include_directories(${ROOT_INCLUDE_DIRS})
find_package(ROOT REQUIRED)
include_directories(${ROOT_INCLUDE_DIRS})
```

Search for `target_link_libraries(exampleB1 ${Geant4_LIBRARIES})` and replace it by `target_link_libraries(exampleB1 ${Geant4_LIBRARIES} ${CRY_LIB} ${ROOT_LIBRARIES})` .

Finally, at line ~60 you should see `set(EXAMPLEB1_SCRIPTS ...)`. Simply add `cmd.file` as follow:

```
set(EXAMPLEB1_SCRIPTS
exampleb1.in
exampleb1.out
init_vis.mac
run1.mac
run2.mac
vis.mac
cmd.file
)
```

#### D - Create cmd.file

We need to create the file used to drive the cosmic shower generation. Run the following:

```
cd /home/usr/micromamba/envs/geant-root/share/Geant-4-11.0.3/examples/basic/B1/
nano cmd.file
```

Paste the following in the file:

```
/run/initialize
/CRY/input returnNeutrons 0
/CRY/input returnProtons 0
/CRY/input returnGammas 0
/CRY/input returnPions 0
/CRY/input returnKaons 0
/CRY/input returnElectrons 0
/CRY/input returnMuons 1
/CRY/input date 7-1-2012
/CRY/input latitude 48.0
/CRY/input altitude 0
/CRY/input subboxLength 1.2
/CRY/input nParticlesMin 1
/CRY/input nParticlesMax 2
/CRY/update

/control/execute vis.mac
/vis/viewer/set/viewpointThetaPhi 90. 0.
/vis/filtering/trajectories/create/particleFilter
/vis/filtering/trajectories/particleFilter-0/add mu+

/run/beamOn 1000
```

Save and exit.

#### E - Import generator files from CRY

We need to import a few files from the CRY GEANT4 examples in the `src/` and `include/` directories of our exampleB1 by running:

```
cd /home/usr/micromamba/envs/geant-root/share/Geant-4-11.0.3/examples/basic/B1/src/
rm PrimaryGeneratorAction.cc
cd ..
cd include/
rm PrimaryGeneratorAction.hh

cd /home/usr/micromamba/envs/geant-root/cry_v1.7/geant/src/
cp PrimaryGeneratorAction.cc RNGWrapper.cc PrimaryGeneratorMessenger.cc /home/usr/micromamba/envs/geant-root/share/Geant-4-11.0.3/examples/basic/B1/src/

cd /home/usr/micromamba/envs/geant-root/cry_v1.7/geant/include/
cp PrimaryGeneratorAction.hh RNGWrapper.hh PrimaryGeneratorMessenger.hh /home/usr/micromamba/envs/geant-root/share/Geant-4-11.0.3/examples/basic/B1/include/
```

#### F - Modifying B1 files

##### Removing namespace B1

To make things work, we still have to modify files. All files in `/B1/src/` and `/B1/include/` start with:

```
namespace B1{

    ...
}
```
Open all those files and remove it *(Do not forget to also remove the brackets!)*.

##### PrimaryGeneratorAction.cc

We must tell GEANT4 where the CRY data is located. Using search and replace (ctrl + h), search all instances of `../data` in the `B1/src/PrimaryGeneratorAction.cc` file and replace them by the actual path to cry_v1.7 data, which should be:

```
/home/usr/micromamba/envs/geant-root/cry_v1.7/data
```

You must also include the `G4SystemOfUnits.hh` file by adding `#include "G4SystemOfUnits.hh"`.

##### ActionInitialization.cc

Open the `B1/src/ActionInitialization.cc` file and replace `SetUserAction(new PrimaryGeneratorAction);` by `SetUserAction(new PrimaryGeneratorAction(""));`

##### RunAction.cc


Open the `B1/src/RunAction.cc` file and comment lines from 105 to 150. (Within `void RunAction::EndOfRunAction(const G4Run* run){}`).

##### exampleB1.cc

Open the `B1/exampleB1.cc` file, and replace line 90 `if ( ! ui ){` by `if (argc>1){`.

#### G - Testing

Now is the moment of truth! Run the modified exampleB1:

```
cd B1/
mkdir build
cd build
```

**Before running **`cmake ../`**, make sure you are in the `build/` directory!**

```
cmake ../
make
./exampleB1 cmd.file
```

You should see a window poping, which displays the structure of the detector (if you run into errors, please report it in the dedicated Slack channel).


 ### V - Python environment

 We will use python to analyse the simulated data. We need to create an environment with all the required libraries. Once again, `micromamba` can do that with just one command line:

```
micromamba create -n muograph_env jupyterlab pandas scikit-spatial scikit-learn pyqt joblib qt fastprogress -c conda-forge
micromamba activate muograph_env
```

After downloading the repositoy, open a terminal window and run:

```
jupyter lab
```

Try to run a few cells from the Tutorial_0 to see if everything is running smoothly (if you run into errors, please report it in the dedicated Slack channel).

Now the framework is finally ready to go! Apologies for this painful installation prcedures and see you at the workshop!