library(readr)
library(imputeTS)

stacked.imputation <- function(tseries) {
  tseriesimp <- na_seadec(tseries,  algorithm = "interpolation")
  if (length(tseriesimp[tseriesimp <0])>0) {
    tseriesimp[tseriesimp <0] <-NA
    tseriesimp <- na_seadec(tseriesimp, algorithm = "mean")
  }
  return(tseriesimp)
}

Gerimputation <- function(datapath,station) {
  #Fuction to read the csv file
  df.station <-read_csv(paste(datapath, station,".csv",sep=""), 
    col_types = cols(FECHA = col_datetime(format = "%Y-%m-%d %H:%M:%S")))
  
  df.tsstation<-ts(df.station[,2:16], start = c(2012,0), frequency = 365.25*24)
  df.tsstation_imputed=df.tsstation #initialization
  for (i in 1:(dim(df.tsstation)[2])){
    df.tsstation_imputed[,i] <- stacked.imputation(df.tsstation[,i])
  }

  #for each variable perform the imputation and save in a csv and plot 
  #in a folder imputedG with subfolders data and plots.
  return(df.tsstation_imputed)
}
