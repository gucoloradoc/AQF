
import numpy as np
import pandas as pd
from tensorflow import keras
from observations_generator import observations_generator #Solve the relative path import problem

dframe=pd.read_csv("data/Monterrey/imputed/data/NOROESTE.csv", 
    parse_dates=["FECHA"], infer_datetime_format=True).set_index("FECHA")

def windows_tensor(dataframe, predictors, target, train_per=0.7, val_per=0.15):
    """
    This function generates the output arrays with the shape (:,0:72, predictors), to be used in the observations generator.
    Training, validation and testing datasets are returned.
    """
    wind_tensor=np.array([dataframe.iloc[(i-24):(i+48),:].loc[:,predictors].values for i in range(24,len(dataframe),72) if ((i+72)<=len(dataframe))])
    #Convert to array
    #pylint: disable=unsubscriptable-object
    rand_indexes=np.random.choice(range(0,wind_tensor.shape[0]),size=wind_tensor.shape[0],replace=False)
    train_indexes=rand_indexes[0:int(np.ceil(train_per*wind_tensor.shape[0]))]
    val_indexes=rand_indexes[int(np.ceil(train_per*wind_tensor.shape[0])):int(np.ceil((train_per+val_per)*wind_tensor.shape[0]))]
    test_indexes=rand_indexes[int(np.ceil((train_per+val_per)*wind_tensor.shape[0])):]
    return(wind_tensor[train_indexes,:,:],wind_tensor[val_indexes,:,:],wind_tensor[test_indexes,:,:])

train_win,val_win,test_win=windows_tensor(dframe, dframe.columns.values[5:8],1)

#pylint: disable=unsubscriptable-object
pivot_index=np.random.choice(np.array(list(range(24,48))),size=1)[0]
train_win[:,list(range((pivot_index-23),pivot_index+1)),:].shape

#Testing zone
test_train=observations_generator(train_win,'NOROSTE')
len(list(test_train))
np.array(list(test_train)).shape
