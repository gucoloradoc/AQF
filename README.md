# Short term PM10, PM2.5 and ozone deep learning forecasting model with incomplete data in the metropolitan area of Monterrey

A deep neural network model for the short term prediction of $O_{3}, PM_{2.5} $ and $PM_{10}$ over the Metropolitan Area of Monterrey is proposed. 
  In order to formulate such model, the data available from the local air quality automatic network is used for training and testing. Such data is 
  incomplete and a procedure of imputation using the R package \textit{ImputeTS} specialized for univariate time series is carried out. 
  
  The model predicts with high accuracy ($r^2_{O_{3}}=0.76,r^2_{PM_{2.5}}=0.57$ and $r^2_{PM_{10}}=0.82$) the concentration of the target pollutants
  and the training procedure, performance metrics and tools used are discussed in this work. 
