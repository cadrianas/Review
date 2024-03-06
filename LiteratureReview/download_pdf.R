library(readr)
library(RCurl)
# some of the urle are accessible in R :(
#reading the csv that contains what python said is not valid url
url <- read_csv("pdfs/invalid_urls.csv")

index <- which(url.exists(url$openAccessPdf)== FALSE)
url_cleaned <- url[-index,]
url_invalid <- url[index,]
# we save the invalid ones, in case we want to manualy downloade the files
write.csv(url_invalid, "pdfs/invalid_urls_R.csv", row.names=FALSE)

for (i in 1:dim(url_cleaned)[1]) {
  print(head(url_cleaned$URL[i]))
  title <- url_cleaned$title[i]  # we use the tile as the name of the pdf
  destfile <- paste0('pdfs/', title, '.pdf')
  download.file(url = url_cleaned$URL[i], 
                destfile = destfile, 
                method = 'libcurl')
}


