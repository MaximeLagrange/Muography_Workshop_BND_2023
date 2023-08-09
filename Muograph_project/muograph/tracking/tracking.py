#Usual suspects
import numpy as np
from typing import Tuple, Optional
import math
from copy import deepcopy

def dot_prod(v1:np.ndarray, v2:np.ndarray) -> np.ndarray:

    '''
    Returns the dot product of 2 vectors or 2 array of vectors.

    INPUT:
     - v1:np.ndarray, a ND vector with shape (N,n_event) or (3)
     - v2:np.ndarray, a ND vector with shape (N,n_event) or (3)

     OUTPUT:
      - dot_prod:np.ndarray, the dot product of v1 and v2, with same shape as v1, v2
    '''

    return np.sum(v1*v2,axis=0).round(10)


def norm(v:np.ndarray) -> np.ndarray:

    '''
    Returns the norm of a ND vector or array of vectors.

    INPUT:
     - v:np.ndarray, a ND vector with shape (N,n_event) or (N)

     OUTPUT:
      - dot_prod:np.ndarray, the norm of v, with shape (n_event) or (1)
    '''

    return np.sqrt(np.sum(v**2,axis=0)).round(10)

# Muograph
class Tracking():
    
    '''
    Class for muon tracking in the context of an MST experiment.
    
    Assumptions:
    
     - Perfect detector alignment
    '''

    def __init__(self, hits:np.ndarray, E:Optional[np.ndarray]=None):

        self.hits = hits
        self.n_event = hits.shape[-1]
        self.n_plane = hits.shape[1]
        
        self.E = None
        
        # Tracking
        self.vectors, self.points = self.compute_points_vectors_from_hits()

        # Zenith and azymuthal angles
        self.theta_in, self.phi_in = self.compute_theta_phi(vectors=self.vectors[0])
        self.theta_out, self.phi_out = self.compute_theta_phi(vectors=self.vectors[1])
        
        # Scattering angles
        self.dtheta, self.dtheta_x, self.dtheta_y = self.compute_dtheta_from_vectors(vectors_in=self.vectors[0],
                                                                                     vectors_out=self.vectors[1])

      
        
    def compute_points_vectors_from_hits(self) -> Tuple[np.ndarray]:

        '''
         INPUT:

         - `hits:np.ndarray`, the hits of the **upper/lower** detection planes. Must have shape (3,n_plane,n_event)

         OUTPUT:

          - `point:np.ndarray`, the coordinnates of a **point** on the fitted line with shape (2,3,n_event)
          - `vector:np.ndarray`, the direction **vector** of the fitted line (A in eq. (1)) with shape (2,3,n_event)
        '''

        from skspatial.objects import Line, Points
        from fastprogress import progress_bar

        vectors = np.zeros((2,int(self.n_plane/2),self.n_event))
        points = np.zeros((2,int(self.n_plane/2),self.n_event))
        
        print("Tracking in progress...")
        
        for ev in progress_bar(range(self.n_event)):
            for sub_hits, dim in zip([self.hits[:,:3],self.hits[:,3:]], [0,1]):
                points_to_fit = (np.transpose(sub_hits[:,:,ev]))
                line_fit = Line.best_fit(Points(points_to_fit))
                vectors[dim,:,ev],points[dim,:,ev] = line_fit.vector.to_array(), line_fit.point.to_array()
        print("Tracking completed!")

        return vectors, points

        
    def compute_theta_phi(self, vectors:np.ndarray) -> Tuple[np.ndarray]:
    
        '''
        INPUT:
         - vector:np.ndarray, array containing the tracks direction, with shape (3,n_event)

        OUTPUT:
        - theta:np.ndarray, array containing the tracks zenith angle, with shape (n_event)
        - phi:np.ndarray, array containing the tracks azymuthal angle, with shape (n_event)

        '''

        theta = np.arccos(-vectors[2]/(np.sqrt(vectors[0]**2+vectors[1]**2+vectors[2]**2)))
        phi = np.sign(vectors[1])*np.arccos(vectors[0]/np.sqrt(vectors[0]**2+vectors[1]**2))
        phi = np.where(theta==0,0.,phi)

        return theta, phi
    
            
    def compute_dtheta_from_vectors(self, vectors_in:np.ndarray, vectors_out:np.ndarray) -> Tuple[np.ndarray]:
    
        '''
        Returns the angles between 2 collections of 3D vectors.

         INPUT:
         - vectors_in:np.ndarray, 3D vectors with shape (3,n_event) or (3)
         - vectors_out:np.ndarray, 3D vectors with shape (3,n_event) or (3)


         OUTPUT:
          - dtheta:np.ndarray, the scattering angle between vectors_in and vectors_out, with shape (n_event) or (1)
          - dtheta_x:np.ndarray, the projected scattering angle (XZ plane) between vectors_in and vectors_out, with shape (n_event) or (1)
          - dtheta_y:np.ndarray, the projected scattering angle (YZ plane) between vectors_in and vectors_out, with shape (n_event) or (1)
          
        '''
        # 3D scattering angle
        dtheta = np.arccos(dot_prod(v1=vectors_in,v2=vectors_out) / (norm(vectors_in)*norm(vectors_out)))
        
        # projected angles
        vectors_x_in, vectors_x_out = deepcopy(vectors_in), deepcopy(vectors_out)
        vectors_y_in, vectors_y_out = deepcopy(vectors_in), deepcopy(vectors_out)
        
        # projection in XZ plane
        vectors_x_in[1],vectors_x_out[1] = 0., 0.
        inside_cos = dot_prod(v1=vectors_x_in,v2=vectors_x_out) / (norm(vectors_x_in)*norm(vectors_x_out))
        inside_cos = np.where(inside_cos>1.,1.,inside_cos)
        dtheta_x = np.arccos(inside_cos)
        dtheta_x = np.where((vectors_x_out[0]-vectors_x_in[0])>0.,dtheta_x,-dtheta_x)
        
        # projection in YZ plane
        vectors_y_in[0],vectors_y_out[0] = 0., 0.
        inside_cos = dot_prod(v1=vectors_y_in,v2=vectors_y_out) / (norm(vectors_y_in)*norm(vectors_y_out))
        inside_cos = np.where(inside_cos>1.,1.,inside_cos)
        dtheta_y = np.arccos(inside_cos)
        dtheta_y = np.where((vectors_y_out[1]-vectors_y_in[1])>0.,dtheta_y,-dtheta_y)
        return dtheta, dtheta_x, dtheta_y
    
    
    def save(self, filename:str, directory:str="../data/tracking/") -> None:
        
        import pickle
        import os.path
        assert (os.path.isfile(directory+filename)==False), '{} file already exists!\
        \n Please choose another filename or delete existing file.'.format(filename)
        
        with open(directory+filename, 'wb') as f:
            pickle.dump(self,f)
            print("tracking class saved in {}".format(directory+filename))
            


    def plot_tracking_summary(self, figname:str=None, directory:str='../figures/tracking_summary/',mask:np.ndarray=None):

        import math
        import matplotlib.pyplot as plt
        fig,ax = plt.subplots(ncols=2,nrows=3,figsize=(10,10))
        fig.subplots_adjust(top=0.8)
        fig.suptitle("Tracking summary\n # events = {}".format(self.n_event), y=1.05)
        ax = ax.ravel()
        
        if(mask is None):
            mask = np.ones_like(self.theta_in,dtype=bool)

        # Seetings
        alpha=.2

        # Plot theta 
        ax[0].hist(self.theta_in[mask],bins=100,alpha=alpha,color='red',log=True)
        ax[0].set_xlabel(r"Incoming zenith angle $\theta_{in}$ [rad]")

        ax[2].hist(self.theta_out[mask],bins=100,alpha=alpha,color='blue',log=True)
        ax[2].set_xlabel(r"Outgoing zenith angle $\theta_{out}$ [rad]")

        # Plot phi
        ax[1].hist(self.phi_in[mask],bins=50,alpha=alpha,color='red')
        ax[1].set_xlabel(r"Incoming azymuthal angle $\phi{in}$ [rad]")

        ax[3].hist(self.phi_out[mask],bins=50,alpha=alpha,color='blue')
        ax[3].set_xlabel(r"Outgoing azymuthal angle $\phi_{out}$ [rad]")

        # Plot scattering angle
        ax[4].hist(self.dtheta[mask],bins=100,log=True,color='green',alpha=alpha,label='std = {:.2f}'.format(self.dtheta[mask].std()))
        ax[4].set_xlabel(r"Scattering angle $d\theta$ [rad]")
        ax[4].legend()

        ax[5].hist(self.dtheta[mask],
                bins=100,
                log=True,
                color='green',
                alpha=alpha,
                range=(0,math.pi/10))
        ax[5].set_xlabel(r"Scattering angle $d\theta$ [rad]")
        ax[5].axvline(x=self.dtheta[mask].mean(),color='red',label='mean = {:.3f}'.format(self.dtheta[mask].mean()))
        ax[5].legend()
        # Make it look nice
        plt.tight_layout()

        # Save figure in directory
        if(figname is not None):
            plt.savefig(directory+figname)
        plt.show()
        
    def apply_mask(self, mask:np.ndarray) -> None:
        '''
        Apply mask to all class attributes. Can be used to apply event selection.

        INPUT:

         - mask:np.ndarray(dtype=bool), a boolean array with size (n_event)

        '''

        for key in self.__dict__.keys():
            attribute = getattr(self,key)
            if(type(attribute)==np.ndarray):
                if(len(attribute.shape)==1):
                    setattr(self,key,attribute[mask])
                if(len(attribute.shape)==3):
                    setattr(self,key,attribute[:,:,mask])
                    
        self.n_event = np.count_nonzero(mask)

    