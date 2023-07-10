# Muon scattering tomography end-to-end simulation framework

## Installation

Debuging GEANT4 code can be a painful experience. In order to make this workshop a succes, one need every participant to run the same **Operating System** (OS) so that everybody is on the same page. A "simple" solution is the use of a **Virtual Machine** (VM),  a compute resource that uses software instead of a physical computer to run programs and deploy apps. Using it, every participant will be able to run the same OS, in our case **Ubuntu 22.04**.

*N.B* If you already run Ubuntu, please get the 22.04 and create a new user account to make sure that our installations do not create any conflicts with your existing working environement. In case you do not want to update, you can create a virtual machine like the others.

### Virtual machine

#### VirtualBox

First, you want to install the VirtualBox software. The installation guide can be found [here](https://www.virtualbox.org/manual/ch02.html). Depending on your OS, you can also checkout these youtube tutorials where is installation is done step by step.

- [MacOS with Apple silicon M1/M2 processors](https://www.youtube.com/watch?v=KV90vu3tpjI)
- [MacOS with Intel processor](https://www.youtube.com/watch?v=hd0Lbtly41Y)
- [Windows 11](https://www.youtube.com/watch?v=b866-7Y_0KQ)
- [Windows 10](https://www.youtube.com/watch?v=8mns5yqMfZk)
- [Ubuntu](https://www.youtube.com/watch?v=SUPoqRPn9to)

Once VirtualBox is installed, you can go to the next step and create the virtual machine which will host the Ubuntu OS.

#### Creating a virtual machine

Now that VirtualBox is installed, we ca create our Ubuntu virtual machine.

First, download the Ubuntu 22.04 iso file from the [ubuntu website](https://ubuntu.com/download/desktop).

Depending on your initial OS, checkout these videos which detail how to create an Ubuntu virtual machine:

- [Windows](https://www.youtube.com/watch?v=zHwFtyxJsog)
- [Mac](https://www.youtube.com/watch?v=b_tOialCSXE)

*N.B* Make sure you assign enough disk to the virtual machine. At least 40 GB (To be coinfirmed).

#### Virtual machine testing

Now that your virtual machine is created, you have to **make sure** that you can connect the machine to **internet via Wi-Fi**, and that you are able to **open the terminal**. 

In case you run into issues, you can check these links:

- [Unable to access Wi-Fi](https://windowsreport.com/wifi-error-virtualbox/)
- [Unable to open terminal](https://askubuntu.com/questions/1435918/terminal-not-opening-on-ubuntu-22-04-on-virtual-box-7-0-0)

 ### GEANT4 - Root installation


#### Micromamba installation

Conda is a very useful tool for packages and dependecies installation and updates. We will use `micromamba` (https://mamba.readthedocs.io/en/latest/installation.html) which is a tiny version of the `mamba` package manager, itself being a reimplementation of `conda`.

Using `micromamba` allows for a straighforward installation of both GEANT4 and Root, as well as the required packages and libraries.

Open a terminal in your `/home/user/` directory and run:

```
wget -qO- https://micromamba.snakepit.net/api/micromamba/linux-64/latest | tar -xvj bin/micromamba
./bin/micromamba shell init -s bash -p ~/micromamba
source ~/.bashrc
```
#### GEANT4 - Root installation
Now download the `geant-root.yml` and move it to `/home/user/`. Go in the `/home/user/` directory  and run:

```
./bin/micromamba create -f geant-root.yml
```

Install cmake:

```
sudo apt install cmake
```

Let's check if the installation worked:

```
cd micromamba/envs/geant-root/share/Geant4-11.0.3/examples/basic/B1/
mkdir build
cd build
cmake ../
make
./exampleB1
```

