# Usual suspects
import math
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Union, Tuple, Optional

from IPython.display import display, Math

    
class VolumeInterest():

    def __init__(self,position:Tuple[float],dimension:Tuple[float],voxel_width:float=10):

        '''
        position = [x,y,z] in mm
        dimension = [dx,dy,dz] in mm 
        Voxel width = 10 mm default
        '''

        # VOI position
        self.xyz = np.array(position)
        
        # VOI dimensions
        self.dxyz = np.array(dimension)
        self.dxyz = np.array(dimension)

        self.xyz_min = self.xyz - self.dxyz/2
        self.xyz_max = self.xyz + self.dxyz/2

        # Voxel width
        self.vox_width = voxel_width

        # Voxelization
        self.n_vox_xyz = self.Compute_N_voxel()
        self.voxel_centers,self.voxel_edges = self.Generate_voxels()

    def Compute_N_voxel(self):

        nx = self.dxyz[0]/self.vox_width
        ny = self.dxyz[1]/self.vox_width
        nz = self.dxyz[2]/self.vox_width

        if((nx%1!=0)|(ny%1!=0)|(nz%1!=0)):
            print('ERROR')
            print('Voxel size does not match VOI dimensions')
            print('Please make sure that dimension / voxel_width = integer')
        return np.array([int(nx),int(ny),int(nz)])


    def Compute_voxel_centers(self,
                              x_min_: float, 
                              x_max_: float,
                              Nvoxel_: int) -> np.ndarray:
                                    
        '''
        x_min,max border of the volume of interset for a given coordinate
                
        return voxels centers position along given coordinate
        '''
        xs_ = np.linspace(x_min_,x_max_,Nvoxel_+1)
        xs_ += self.vox_width/2
        return xs_[:-1]    


    def Generate_voxels(self)->np.ndarray:
            
        voxels_centers = np.zeros((self.n_vox_xyz[0],self.n_vox_xyz[1],self.n_vox_xyz[2],3))
        
        xs_ = self.Compute_voxel_centers(x_min_=self.xyz_min[0], x_max_=self.xyz_max[0],
                                    Nvoxel_= self.n_vox_xyz[0])
        ys_ = self.Compute_voxel_centers(x_min_=self.xyz_min[1], x_max_=self.xyz_max[1],
                                    Nvoxel_= self.n_vox_xyz[1])
        zs_ = self.Compute_voxel_centers(x_min_=self.xyz_min[2], x_max_=self.xyz_max[2],
                                    Nvoxel_= self.n_vox_xyz[2])
                    
        for i in range(len(ys_)):
            for j in range(len(zs_)):
                voxels_centers[:,i,j,0]=xs_
        for i in range(len(xs_)):
            for j in range(len(zs_)):
                voxels_centers[i,:,j,1]=ys_
        for i in range(len(xs_)):
            for j in range(len(ys_)):
                voxels_centers[i,j,:,2]=zs_
        
        
        voxels_edges = np.zeros((self.n_vox_xyz[0],self.n_vox_xyz[1],self.n_vox_xyz[2],2,3))

        voxels_edges[:,:,:,0,:] = voxels_centers-self.vox_width/2
        voxels_edges[:,:,:,1,:] = voxels_centers+self.vox_width/2

        return voxels_centers, voxels_edges


    def load_rad_length(self,rad_length:Optional[float]=None):

        self.X0 = np.zeros(([self.n_vox_xyz[0],self.n_vox_xyz[1],self.n_vox_xyz[2]]))+rad_length



    


