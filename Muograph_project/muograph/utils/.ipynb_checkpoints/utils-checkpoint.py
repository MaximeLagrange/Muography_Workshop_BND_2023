import pandas as pd
import numpy as np

def get_hits_from_csv(filename:str,) -> np.ndarray:
    
    df = pd.read_csv(filename)
    
    # Compute # planes from csv
    n_plane = len([col for col in df.columns if "X" in col])
    
    # Create array 
    hits = np.zeros((3,n_plane,len(df)))
    
    # Fill in array with csv file entries
    for plane in range(n_plane):
        hits[0,plane] = df['X'+str(plane)]
        hits[1,plane] = df['Y'+str(plane)]    
        hits[2,plane] = df['Z'+str(plane)]

    return hits
