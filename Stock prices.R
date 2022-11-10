library('quantmod')

stocks <- c('AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA', 'BRK-B', 'GOOGL', 'UNH','JNJ', 'XOM')

end_date <- Sys.Date()
start_date <- end_date - (365*10)

df <- NULL

for(i in seq(length(stocks))){
  index = stocks[i]
  getSymbols(index,verbose = TRUE,src="yahoo",
             from=start_date,to=end_date)
  temp_df = as.data.frame(get(index))
  temp_df$Date = row.names(temp_df)
  temp_df$Index = index
  row.names(temp_df) = NULL
  colnames(temp_df) = c("Open", "High", "Low", "Close", 
                        "Volume", "Adjusted", "Date", "Index")
  temp_df = temp_df[c("Date", "Index", "Open", "High", 
                      "Low", "Close", "Volume", "Adjusted")]
  df = rbind(df,temp_df)
}

write.csv(df,"C:/Users/nhatp/Desktop/FE800/stockprices1.csv",row.names=TRUE)
