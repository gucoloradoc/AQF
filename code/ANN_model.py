
import numpy as np
import pandas as pd
import kerasb


dframe=pd.read_csv("data/Monterrey/imputed/data/NOROESTE.csv", 
    parse_dates=["FECHA"], infer_datetime_format=True).set_index("FECHA")

def windows_tensor(dataframe, predictors, target):
    """
    This function generates an output array with the shape (0:72, predictors,:), to be used in the observations generator.
    """
    wind_tensor=np.array([dataframe.iloc[(i-24):(i+48),:].loc[:,predictors].values for i in range(24,len(dataframe),72) if ((i+72)<=len(dataframe))])
    #Convert to array
    return(wind_tensor)

w_ten=windows_tensor(dframe, dframe.columns.values[5:8],1)

class observations_generator(keras.utils.Sequence):
    """
    Observation generator, it takes windows of 72 hours and from such widows it generates random observations, to predict 24 lead time taing 24 hours before.
    data_source is a str with the location of a complete dataset
    station is the name of the measurement station
    predictors is an array of the desired predictor to be taken into account for the prediction model
    target is the variable to be predicted
    batch_size in the size of the batches to be generated
    """

    def __init__(self, data_source=pd.read_csv("data/Monterrey/imputed/data/NOROESTE.csv", parse_dates=["FECHA"], infer_datetime_format=True).set_index("FECHA"), station, predictors, target, samples_per_window=5, batch_size=64):
        self.data_source=data_source
        self.station=station
        self.predictors=predictors
        self.target=target
        self.windows_tensor=windows_tensor(data_source, predictors, target)
        self.batch_size=batch_size
        self.samples_per_window=samples_per_window


        #Generate the tensor with
    def __len__(self):
        #need to think how to stimate this length
        return(int(self.windows_tensor.shape[0]/self.batch_size))
    
    def __getitem__(self, idx):
        ##DdDdSDSdSD
        self.x_batch= self.windows_tensor[idx*self.batch_size:(1+idx)*self.batch_size,:,:]

pivot_index=np.random.choice(np.array(list(range(24,48))),size=1)
#windows_tensor[0,[(pivot_index-24):pivot_index],:].shape