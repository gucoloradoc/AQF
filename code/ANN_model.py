
import numpy as np
import pandas as pd
from tensorflow import keras


dframe=pd.read_csv("data/Monterrey/imputed/data/NOROESTE.csv", 
    parse_dates=["FECHA"], infer_datetime_format=True).set_index("FECHA")

def windows_tensor(dataframe, predictors, target, train_per=0.7, val_per=0.15):
    """
    This function generates the output arrays with the shape (:,0:72, predictors), to be used in the observations generator.
    Training, validation and testing datasets are returned.
    """
    wind_tensor=np.array([dataframe.iloc[(i-24):(i+48),:].loc[:,predictors].values for i in range(24,len(dataframe),72) if ((i+72)<=len(dataframe))])
    #Convert to array
    rand_indexes=np.random.choice(range(0,wind_tensor.shape[0]),size=wind_tensor.shape[0],replace=False)
    train_indexes=rand_indexes[0:int(np.ceil(train_per*wind_tensor.shape[0]))]
    val_indexes=rand_indexes[int(np.ceil(train_per*wind_tensor.shape[0])):int(np.ceil((train_per+val_per)*wind_tensor.shape[0]))]
    test_indexes=rand_indexes[int(np.ceil((train_per+val_per)*wind_tensor.shape[0])):]
    return(wind_tensor[train_indexes,:,:],wind_tensor[val_indexes,:,:],wind_tensor[test_indexes,:,:])

class observations_generator(keras.utils.Sequence):
    """
    Observation generator, it takes windows of 72 hours and from such widows it generates random observations, to predict 24 lead time taking 24 hours before.
    data_source is an array with the location of a complete dataset
    station is the name of the measurement station
    predictors is an array of the desired predictor to be taken into account for the prediction model
    target is the variable to be predicted
    batch_size in the size of the batches to be generated
    """

    def __init__(self, 
    data_source, station, predictors, target, 
    samples_per_window=5, batch_size=64):
        self.data_source=data_source
        self.station=station
        self.predictors=predictors
        self.target=target
        self.batch_size=batch_size
        self.samples_per_window=samples_per_window
        c=0
        self.indexes=[]
        for i in range(0, int(self.data_source.shape[0]*self.samples_per_window)):
            if c==self.samples_per_window:
                c=0
            if c==0:
                temp=i
            self.indexes.append((temp,np.random.choice(np.array(list(range(24,48))),size=1)[0]))
            c=c+1
    #Generate the tensor with
    def __len__(self):
        #Total lenght of the output
        return(self.data_source.shape[0])
        #Th following line is the legth of the array in case there is a restriction in batch size
        #return(int(np.ceil(self.data_source.shape[0]*self.samples_per_window/self.batch_size)))
    
    def __getitem__(self, idx):
        ##Generador de observaciones, ojo aca con el significado de cada bache
        self.x_batch= train_win[self.indexes[idx][0],list(range((self.indexes[idx][1]-23),self.indexes[idx][1]+1)),:]
        return self.x_batch

#Testing zone
#Testing the windows generator (working)
train_win,val_win,test_win=windows_tensor(dframe, dframe.columns.values[5:8],1)
#Testing the observation generator 


pivot_index=np.random.choice(np.array(list(range(24,48))),size=1)[0]
train_win[:,list(range((pivot_index-23),pivot_index+1)),:].shape