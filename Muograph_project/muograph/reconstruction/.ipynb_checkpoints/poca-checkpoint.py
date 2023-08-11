#Usual suspects
import numpy as np
from typing import Tuple, Optional, List, Union
import math
from copy import deepcopy
NoneType = type(None)
import functools
from functools import partial

# Muograph
import sys
sys.path.insert(1,'../muograph/')
from tracking.tracking import Tracking
from volume.volume import VolumeInterest


class POCA():
    
    def __init__(self, tracks:Tracking, voi:VolumeInterest, dtheta_cut:float=0.005):
        
        self.all_tracks = deepcopy(tracks)
        self.voi = voi
        # Compute parallel tracks mask
        self.dtheta_cut = dtheta_cut
        self.parallel_tracks_mask = self.compute_parallel_tracks_mask()
        
        # Remove parallel events
        tracks.apply_mask(self.parallel_tracks_mask)
        self.tracks = tracks
        
        # Compute POCA points
        self.poca_points = self.compute_poca_points(track_in = self.tracks.vectors[0],
                                                    track_out = self.tracks.vectors[1],
                                                   point_in = self.tracks.points[0],
                                                   point_out = self.tracks.points[1])

        # Mask POCA points within volume of interest
        self.mask_in_voi = self.compute_mask_in_voi(self.voi)
        self.poca_points_in = self.poca_points[self.mask_in_voi]

        # Compute normalized poca points
        self.norm_poca_points = self.compute_normalized_poca_positions()
        
        # Compute triggered voxels indices
        self.triggered_vox_indices = self.compute_triggered_voxels_indices(self.voi)
        

    def compute_parallel_tracks_mask(self) -> np.ndarray:

        '''
        Create a mask based on a scattering angle.

        INPUT:
         - dtheta_cut:float, the cut on scattering angle
         - tracks:Tracking, an instance of the Tracking class

        OUTPUT:
         - mask:np.ndarray, a boolean mask with size (tracks.n_event)
        '''

        return self.all_tracks.dtheta > self.dtheta_cut
    
    def compute_poca_points(self,
                            track_in:np.ndarray,
                            track_out:np.ndarray,
                            point_in:np.ndarray,
                            point_out:np.ndarray,) -> np.ndarray:
        '''
        INPUT: 

        - track_in:np.ndarray, incoming reconstructed track, with size (3,Nevent)
        - track_out:np.ndarray, outgoing reconstructed track, with size (3,Nevent)
        - point_in:np.ndarray, a point on V1, with size (3,Nevent)
        - point_out:np.ndarray, a point on V2, with size (3,Nevent)

        OUTPUT: 
        - POCA_points:np.ndarray,  with size (3,Nevent)

        Given 2 lines V1, V2 aka incoming and outgoing tracks with parametric equation:
        L1 = P1 + t*V1

        1- A segment of shortest length between two 3D lines L1 L2 is perpendicular to both lines 
        (if L1 L2 are neither parallele or in the same plane). One must compute V3, vector perpendicular 
        to L1 and L2

        2- Search for points where L3 = P1 + t1*V1 +t3*V3 crosses L2. One must find t1 and t2 for which:
        L3 = P1 + t1*V1 +t3*V3 = P2 + t2*V2

        3- Then POCA location M is the middle of the segment Q1-Q2 where Q1,2 = P1,2 +t1,2*V1,2

        '''

        P1, P2 = np.transpose(point_in), np.transpose(point_out)
        V1, V2 = np.transpose(track_in), np.transpose(track_out)
        V3 = np.cross(V2,V1)

        RES = P2 - P1
        LES = np.transpose(np.stack([V1,-V2,V3]),(1,2,0))

        ts = np.linalg.solve(LES,RES)

        t1 = np.stack([ts[:,0],ts[:,0],ts[:,0]],-1)
        t2 = np.stack([ts[:,1],ts[:,1],ts[:,1]],-1)

        Q1s,Q2s = P1+t1*V1, P2+t2*V2
        M = (Q2s-Q1s)/2+Q1s

        return M

    def compute_mask_in_voi(self, voi:VolumeInterest) -> np.ndarray:
        
        x,y,z = self.poca_points[:,0],self.poca_points[:,1],self.poca_points[:,2]
        mask = np.ones_like(x,dtype=bool)
        for coord, voi_min, voi_max in zip((x,y,z),voi.xyz_min,voi.xyz_max):
            mask = mask & (coord>voi_min) & (coord<voi_max)
        return mask

    def compute_triggered_voxels_indices(self, voi:VolumeInterest):

        '''
        Compute the indices of triggered voxels. Given a POCA point with coordinnate x,y,z, the triggered voxel is the one which contains x,y and z.
        
        INPUT:
         - voi:VolumeInterest, an instance of the VolumeInterest class
        OUTPUT:
         - indices:np.array, the array containing the triggered voxels indices as integers, with size (self.tracks.n_event, 3)
        '''
        print("Scattering location computation in progress ...")
        def compute_triggered_vox_indices_event(event):
            '''
            Compute the triggered voxel indices for a given event.
            '''        
            x, y, z = self.poca_points[:, 0], self.poca_points[:, 1], self.poca_points[:, 2]
            mask = np.ones_like(voi.voxel_edges[:, :, :, 0, 0], dtype=bool)
    
            for coord, dim in zip([x, y, z], [0, 1, 2]):
                mask = mask & (coord[event] > voi.voxel_edges[:, :, :, 0, dim]) & (coord[event] < voi.voxel_edges[:, :, :, 1, dim])
    
            indices = np.transpose((mask == True).nonzero()) 
            
            return indices
    
        from joblib import Parallel, delayed
        from fastprogress import progress_bar
        indices_list=[]
        for i in progress_bar(range(self.tracks.n_event)):
            indices_list.append(compute_triggered_vox_indices_event(i))
        # indices_list = Parallel(n_jobs=-1)(delayed(compute_triggered_vox_indices_event)(i) for i in progress_bar(range(self.tracks.n_event)))   
    
        # Replace empty arrays with [-1, -1, -1]
        def handle_empty_arrays(arr):
            return arr if arr.size > 0 else np.array([[-1, -1, -1]])
    
        filled_arrays = [handle_empty_arrays(arr) for arr in indices_list]
        print("Scattering location computation done")
        return np.vstack(filled_arrays)

    

    def compute_voxels_scores(self, 
                              score_feature:np.ndarray,
                              mask:Union[np.ndarray, NoneType] = None) -> List[List[List[float]]]:

        '''
        Associate a score to each triggered voxel according to the choice of score_feature.
    
        INPUT:
         - score_feature:np.ndarray, the scores to be appent to the voxel list
        OUTPUT:
         - score_list:List[List[List[float]]], the list containg the scores
        '''
    
        # Create empty score list 
        score_list = [[[[] for _ in range(self.voi.n_vox_xyz[2])] for _ in range(self.voi.n_vox_xyz[1])] for _ in range(self.voi.n_vox_xyz[0])]

        # reject events outside the voi (a.k.a triggered indices = [-1,-1,-1])
        if mask is None:
            mask = (self.triggered_vox_indices.sum(axis=1) != -3)
        else:
            mask = mask & (self.triggered_vox_indices.sum(axis=1) != -3)

        
        # Get the indices where total_mask is True
        mask_indices = np.where(mask)[0]
        
        # Extract the relevant indices and scores
        ix, iy, iz = self.triggered_vox_indices[mask_indices, 0], self.triggered_vox_indices[mask_indices, 1], self.triggered_vox_indices[mask_indices, 2]
        selected_scores = score_feature[mask_indices]
        
        # Update the score_list using list comprehensions
        for i, (x, y, z, score) in enumerate(zip(ix, iy, iz, selected_scores)):
            score_list[x][y][z].append(score)
        
        return score_list
        

    def compute_final_voxels_score(self,
                                   score_list:List[List[List[float]]],
                                   score_method:functools.partial) -> np.array:
        '''
        Computes the final score of every voxel, using score_method as input.
    
        score_method can be mean, variance, quartile, etc...
    
        INPUT:
         - score_list:List[List[List[float]]], the scores
         - score_method:functools.partial, the method to be used to compute the final scores from scores
        '''
        from fastprogress import progress_bar
        Nx, Ny, Nz = self.voi.n_vox_xyz[0], self.voi.n_vox_xyz[1], self.voi.n_vox_xyz[2]
        final_voxel_scores, hit_per_voxel = np.zeros((Nx,Ny,Nz)), np.zeros((Nx,Ny,Nz)) 
    
        #loop over every voxels
        for i in progress_bar(range(Nx)):
            for j in range(Ny):
                for k in range(Nz):
    
                    if(score_list[i][j][k]!=[]):
                        hit_per_voxel[i,j,k] += len(score_list[i][j][k])
                        final_voxel_scores[i,j,k] = score_method(score_list[i][j][k])
                      
        return final_voxel_scores, hit_per_voxel

    def poca_reconstruction(self,
                            score_feature:np.ndarray,
                            score_method:functools.partial = partial(np.quantile,q=.5),
                            mask:Union[np.ndarray, NoneType] = None) -> Tuple[np.ndarray]:
        '''
        Proceed to POCA algorithm reconstruction. Given a voxelized volume and a collection of poca points, computes a final score per voxel given score_feature (the score attributed to each POCA point) and score_method (the function used to assign a final score based on a collection of score_feature of a single voxel).
        '''
    
        score_list = self.compute_voxels_scores(score_feature=score_feature,mask=mask)
        final_scores, hit_per_voxel = self.compute_final_voxels_score(score_list=score_list,
                                                                      score_method = score_method)
    
        return final_scores, hit_per_voxel

    def compute_normalized_poca_positions(self) -> np.array:

        '''
        Normalize poca positions so that they range between 0 and 1.
        '''
        
        def normalize(x,x_min,x_max):
            return (x-x_min)/(x_max-x_min)

        from copy import deepcopy
        norm_poca_points = deepcopy(self.poca_points[self.mask_in_voi])
        x_min, x_max = np.min(norm_poca_points[:,0]), np.max(norm_poca_points[:,0])
        for dim in [0,1,2]:
            norm_poca_points[:,dim] = normalize(norm_poca_points[:,dim],x_min,x_max)

        return norm_poca_points
            
        
        

        

    