#Usual suspects
import numpy as np
from typing import Tuple, Optional
import math
import matplotlib.pyplot as plt

# Muograph
import sys
sys.path.insert(1,'../muograph/')
from tracking.tracking import Tracking
from reconstruction.poca import POCA

def plot_POCA_event(poca:POCA,
                    event:int) -> None:
    
    import math
    fig,ax = plt.subplots(ncols=2)
    fig.suptitle("event = {}\ndtheta = {:.2f} deg".format(event,poca.tracks.dtheta[event]*180/math.pi))
    
    # Plot hits
    i=0
    for x_hit, y_hit, z_hit in zip(poca.tracks.hits[0,:,event],
                                   poca.tracks.hits[1,:,event],
                                   poca.tracks.hits[2,:,event]):
        
        ax[0].scatter(x_hit,z_hit,marker="x",color="green",label="hits")
        ax[1].scatter(y_hit,z_hit,marker="x",color="green",label="hits")

    # Set axis limit
    ax[0].set_xlim(-500,500)
    ax[1].set_xlim(-500,500)
    
    # Set axis label
    ax[0].set_xlabel("x [mm]")
    ax[0].set_ylabel("z [mm]")
    
    ax[1].set_xlabel("y [mm]")
    ax[1].set_ylabel("z [mm]")

    # Plot POCA point
    ax[0].scatter(poca.poca_points[event,0],poca.poca_points[event,2],label="POCA point")
    ax[1].scatter(poca.poca_points[event,1],poca.poca_points[event,2],label="POCA point")
    
    # draw detector panels
    for detector_z in poca.tracks.hits[2,:,event]:
        ax[0].axhline(y = detector_z,color='red')
        ax[1].axhline(y = detector_z,color='red')

    fig.tight_layout()
    plt.show()

def plot_POCA_points_multi_projection(poca_points:np.ndarray, 
                                      mask:Optional[np.ndarray]=None, 
                                      binning_xyz:Tuple[int]=[100,100,100],
                                      filename:str =None) -> None:

    '''
    Plot the poca points distribution as 2D histograms in XY, YZ and XZ projections, with the asssociated X, Y and Z poca points distribution. If filename is given, the figure will be saved.

    INPUT:
     - poca_points:np.ndarray, with shape (n_event,3)
     - mask:np.ndarray, an optional mask used to filter events, with shape (n_event) 
     - binning_Xyz:Tuple[int], number of bin of the histograms
     - filename:str, name of the output figure
    OUTPUT:
     - None
    '''

    if(mask is None):
        mask = np.ones(poca_points.shape[0],dtype=bool)
    x,y,z = poca_points[mask,0], poca_points[mask,1], poca_points[mask,2] 
    
    # XY view
    fig,main_ax = plt.subplots(figsize=(8, 8))

    # 2D hits on the main axes
    main_ax.hist2d(x,y,bins=(binning_xyz[0],binning_xyz[1]),cmap="YlOrRd")
    main_ax.set_aspect('equal')
    main_ax.set_xlabel('x [mm]',fontsize=14)
    main_ax.set_ylabel('y [mm]',fontsize=14)
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14)

    # X view
    x_hist = main_ax.inset_axes([0, 1.20, 1, .5], transform=main_ax.transAxes, sharex=main_ax)

    x_hist.hist(x,bins=binning_xyz[0], histtype='stepfilled',
                orientation='vertical',alpha=.7)
    x_hist.set_ylabel('# POCA points per voxel',fontsize=14)
    x_hist.tick_params(axis='x', labelsize=14)
    x_hist.tick_params(axis='y', labelsize=14)

    # Y view
    y_hist = main_ax.inset_axes([1.5, 0, .5, 1], transform=main_ax.transAxes,sharey=main_ax)

    y_hist.hist(y, bins=binning_xyz[1],
                orientation='horizontal',alpha=.7)
    y_hist.set_xlabel('# POCA points per voxel',fontsize=14)
    y_hist.tick_params(axis='x', labelsize=14)
    y_hist.tick_params(axis='y', labelsize=14)

    if(filename is not None):
        plt.savefig(filename+'_XY_view',bbox_inches = 'tight')
    plt.show()
    
    # XZ view
    fig,main_ax = plt.subplots(figsize=(8, 8))

    # 2D hits on the main axes
    main_ax.hist2d(x,z,bins=(binning_xyz[0],binning_xyz[2]),cmap="YlOrRd")
    main_ax.set_aspect('equal')
    main_ax.set_xlabel('x [mm]',fontsize=14)
    main_ax.set_ylabel('z [mm]',fontsize=14)
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14)

    # X view
    x_hist = main_ax.inset_axes([0, 1.20, 1, .5], transform=main_ax.transAxes, sharex=main_ax)

    x_hist.hist(x,bins=binning_xyz[0], histtype='stepfilled',
                orientation='vertical',alpha=.7)
    x_hist.set_ylabel('# POCA points per voxel',fontsize=14)
    x_hist.tick_params(axis='x', labelsize=14)
    x_hist.tick_params(axis='y', labelsize=14)

    # Y view
    y_hist = main_ax.inset_axes([1.5, 0, .5, 1], transform=main_ax.transAxes,sharey=main_ax)

    y_hist.hist(z, bins=binning_xyz[2],
                orientation='horizontal',alpha=.7)
    y_hist.set_xlabel('# POCA points per voxel',fontsize=14)
    y_hist.tick_params(axis='x', labelsize=14)
    y_hist.tick_params(axis='y', labelsize=14)

    if(filename is not None):
        plt.savefig(filename+'_XZ_view',bbox_inches = 'tight')
    plt.show()

    # YZ view
    fig,main_ax = plt.subplots(figsize=(8, 8))

    # 2D hits on the main axes
    main_ax.hist2d(y,z,bins=(binning_xyz[1],binning_xyz[2]),cmap="YlOrRd")
    main_ax.set_aspect('equal')
    main_ax.set_xlabel('y [mm]',fontsize=14)
    main_ax.set_ylabel('z [mm]',fontsize=14)
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14)

    # X view
    x_hist = main_ax.inset_axes([0, 1.20, 1, .5], transform=main_ax.transAxes, sharex=main_ax)

    x_hist.hist(y,bins=binning_xyz[1], histtype='stepfilled',
                orientation='vertical',alpha=.7)
    x_hist.set_ylabel('# POCA points per voxel',fontsize=14)
    x_hist.tick_params(axis='x', labelsize=14)
    x_hist.tick_params(axis='y', labelsize=14)

    # Y view
    y_hist = main_ax.inset_axes([1.2, 0, .5, 1], transform=main_ax.transAxes, sharey=main_ax)
    # y_hist = fig.add_subplot(grid[:-1, 0], xticklabels=[], sharey=main_ax)

    y_hist.hist(z, bins=binning_xyz[2],
                orientation='horizontal',alpha=.7)
    y_hist.set_xlabel('# POCA points per voxel',fontsize=14)
    y_hist.tick_params(axis='x', labelsize=14)
    y_hist.tick_params(axis='y', labelsize=14)

    if(filename is not None):
        plt.savefig(filename+'_YZ_view',bbox_inches = 'tight')
    plt.show()

def plot_poca_3D_cloud(poca:POCA, mask:Optional[np.ndarray]=None, alpha:float=0.005, color:np.ndarray=None) -> None:

    '''
    Plot the 3D POCA points distribution.

    INPUT:
     - poca:POCA, an instance of the POCA class
     - mask:Optional[np.ndarray], an optional mask for event selection, with size (n_event)
     - alpha:float, transparency between 0 and 1.
     - color:Optional[np.ndarray], an optional array for color. A color will be assigned to each point i based on the value of color[i].
    '''
    if mask is None:
        mask = np.ones_like(poca.tracks.dtheta)

    x,y,z = poca.poca_points[mask,0],poca.poca_points[mask,1],poca.poca_points[mask,2]
    
    fig = plt.figure()
    fig.suptitle("3D POCA points cloud")
    ax = plt.axes(projection='3d')
    # color bar
    import matplotlib
    cm = matplotlib.colormaps['RdYlBu']
    if color is not None:
        im = ax.scatter(x,y,z,alpha=alpha,c=color,cmap=cm)
        ax.set_aspect("equal")
        plt.colorbar(im, location='right')
    else:
        im = ax.scatter(x,y,z,alpha=alpha)

    ax.set_xlabel("x [mm]")
    ax.set_ylabel("y [mm]")
    ax.set_zlabel("z [mm]")
    plt.tight_layout()
    plt.show()

def plot_poca_points_summary(hit_per_voxel:np.ndarray, filename:str=None):

    '''
    Plot the number of poca points per voxels.
    '''
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    
    fig,ax = plt.subplots()
    fig.suptitle('POCA reconstruction: # poca points per voxels')
    ax.set_title('XY view')
    ax.set_xlabel('x [a.u]')
    ax.set_ylabel('y [a.u]')
    im = ax.imshow(hit_per_voxel.sum(axis=2),cmap='binary',origin="lower")
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    fig.colorbar(im, ax=ax,cax=cax, label="# poca points per voxel")
    plt.tight_layout()
    if(filename is not None):
        plt.savefig(filename+'_XY_view')
    plt.show()
    
    fig,ax = plt.subplots()
    fig.suptitle('POCA reconstruction: poca points per voxel')
    ax.set_title('XY view')
    ax.set_xlabel('x [a.u]')
    ax.set_ylabel('z [a.u]')
    im = ax.imshow(hit_per_voxel.sum(axis=1).T,cmap='binary',origin="lower")
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    fig.colorbar(im, ax=ax,cax=cax, label="# poca points per voxel")
    plt.tight_layout()
    if(filename is not None):
        plt.savefig(filename+'_XZ_view')
    plt.show()
    
    fig,ax = plt.subplots()
    fig.suptitle('POCA reconstruction: voxel scores')
    ax.set_title('XY view')
    ax.set_xlabel('y [a.u]')
    ax.set_ylabel('z [a.u]')
    im = ax.imshow(hit_per_voxel.sum(axis=0).T,cmap='binary',origin="lower")
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    fig.colorbar(im, ax=ax,cax=cax, label="# poca points per voxel")
    plt.tight_layout()
    if(filename is not None):
        plt.savefig(filename+'_YZ_view')
    plt.show()

    fig,ax = plt.subplots()
    std = hit_per_voxel.std()
    ax.hist(hit_per_voxel.ravel(),bins=int(np.max(hit_per_voxel)),
            label=r"$\sigma = {:.2f}$".format(std),log=True)
    ax.set_xlabel("# hit per voxel")
    ax.legend()
    plt.show()

def plot_poca_summary(scores:np.ndarray, filename:str=None):
    '''
    Plot the poca scores of each voxels.
    '''

    from mpl_toolkits.axes_grid1 import make_axes_locatable
    
    fig,ax = plt.subplots()
    fig.suptitle('POCA reconstruction: voxel scores')
    ax.set_title('XY view')
    ax.set_xlabel('x [a.u]')
    ax.set_ylabel('y [a.u]')
    im = ax.imshow(scores.sum(axis=2),cmap='binary',origin="lower")
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    fig.colorbar(im, ax=ax,cax=cax, label="voxel score [a.u]")
    plt.tight_layout()
    if(filename is not None):
        plt.savefig(filename+'_XY_view')
    plt.show()
    
    fig,ax = plt.subplots()
    fig.suptitle('POCA reconstruction: voxel scores')
    ax.set_title('XY view')
    ax.set_xlabel('x [a.u]')
    ax.set_ylabel('z [a.u]')
    im = ax.imshow(scores.sum(axis=1).T,cmap='binary',origin="lower")
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    fig.colorbar(im, ax=ax,cax=cax, label="voxel score [a.u]")
    plt.tight_layout()
    if(filename is not None):
        plt.savefig(filename+'_XZ_view')
    plt.show()
    
    fig,ax = plt.subplots()
    fig.suptitle('POCA reconstruction: voxel scores')
    ax.set_title('XY view')
    ax.set_xlabel('y [a.u]')
    ax.set_ylabel('z [a.u]')
    im = ax.imshow(scores.sum(axis=0).T,cmap='binary',origin="lower")
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    fig.colorbar(im, ax=ax,cax=cax, label="voxel score [a.u]")
    plt.tight_layout()
    if(filename is not None):
        plt.savefig(filename+'_YZ_view')
    plt.show()