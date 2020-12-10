library('wikipediatrend')

rm(list=ls())
setwd('/home/lua/EPFL/MA3/ADA/extension')
term_dir <- 'data/QueryTerms'
dest_dir <- 'data/Wikipedia'

terrorism_topics <- readLines(paste(term_dir, 'terrorism_en_topics.txt', sep='/'))
domestic_topics <- readLines(paste(term_dir, 'domestic_en_topics.txt', sep='/'))

terrorism <- data.frame()
for (t in terrorism_topics) {
  print(t)
  individual <- wp_trend(
    page=t,
    from='2010-01-01',
    to='2019-12-31',
    lang='en',
    warn=TRUE
  )
  terrorism <- rbind(terrorism, individual)
}
write.csv(terrorism, paste(dest_dir, 'wiki_terrorism.csv', sep='/'), row.names=FALSE)


domestic <- data.frame()
for (t in domestic_topics) {
  print(t)
  individual <- wp_trend(
    page=t,
    from='2010-01-01',
    to='2019-12-31',
    lang='en',
    warn=TRUE
  )
  domestic <- rbind(domestic, individual)
}
write.csv(domestic, paste(dest_dir, 'wiki_domestic.csv', sep='/'), row.names=FALSE)
