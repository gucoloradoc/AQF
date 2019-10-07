
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
    
    data_source is the tensor array of predictors and target variable
    
    target is the variable index to be predicted 
    
    batch_size in the size of the batches to be generated
    """

    def __init__(self, data_source, target, 
    samples_per_window=5, batch_size=64):
        self.data_source=data_source
        self.target=target
        self.batch_size=batch_size
        self.samples_per_window=samples_per_window
        c=0
        temp=0
        self.indexes=[]
        for i in range(0, int(self.data_source.shape[0]*self.samples_per_window)):
            self.indexes.append((temp,np.random.choice(np.array(list(range(24,48))),size=1)[0]))
            c=c+1
            if c==self.samples_per_window:
                c=0
            if c==0:
                temp+=1
                
    #Generate the tensor with
    def __len__(self):
        #Total lenght of the output
        return(int(np.ceil(self.data_source.shape[0]*self.samples_per_window)))
    
    def __getitem__(self, idx):
        ##Observations generator, Neural network input
        self.x_batch = self.data_source[self.indexes[idx][0],list(range((self.indexes[idx][1]-23),self.indexes[idx][1]+1)),:]
        self.y_batch = self.data_source[self.indexes[idx][0],int(self.indexes[idx][1]+24),self.target]
        return np.array(self.x_batch), np.array(self.y_batch)

#Testing zone
#Testing the windows generator (working)
train_win,val_win,test_win=windows_tensor(dframe, dframe.columns.values[5:8],1)
#Testing the observation generator 
test_gen_x =(list(observations_generator(train_win,2)))

pivot_index=np.random.choice(np.array(list(range(24,48))),size=1)[0]
train_win[:,list(range((pivot_index-23),pivot_index+1)),:].shape