from tensorflow import keras
import numpy as np
class observations_generator(keras.utils.Sequence):
    """
    Observation generator, it takes windows of 72 hours and from such widows it generates random observations, to predict 24 lead time taing 24 hours before.
    data_source is a 3D array dimensions:(samples, hours, predictors)
    station is the name of the measurement station
    predictors is an array of the desired predictor to be taken into account for the prediction model
    target is the variable to be predicted
    batch_size in the size of the batches to be generated
    """

    def __init__(self, 
    data_source, station,
    samples_per_window=5, batch_size=64):
        self.data_source=data_source
        self.station=station
        self.batch_size=int(batch_size)
        self.samples_per_window=samples_per_window
        self.wind_per_batch=int(np.floor(batch_size/samples_per_window))
        c=0
        self.indexes=[]
        for i in range(0, int(self.data_source.shape[0])):
            self.indexes.append([np.random.choice(data_source.shape[0]),
            np.random.choice(raznge(24,48))])

    #Generate the tensor with
    def __len__(self):
        #Total lenght of the output
        return(int(self.data_source.shape[0]/self.batch_size))
    
    def __getitem__(self, idx):
        ##Generador de observaciones, ojo aca con el significado de cada bache
        #print(self.indexes)
        #self.x_batch= self.data_source[self.indexes[idx][0],list(range((self.indexes[idx][1]-23),self.indexes[idx][1]+1)),:]
        #self.batch=[]
        return self.indexes #np.array([i for i in self.x_batch])
#Testing zone
