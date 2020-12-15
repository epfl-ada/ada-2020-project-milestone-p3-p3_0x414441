library('wikipediatrend')

rm(list=ls())
setwd('/home/lua/EPFL/MA3/ADA/extension')
term_dir <- 'data/QueryTerms'
dest_dir <- 'data/Wikipedia'

languages <- c('en', 'de', 'fr', 'it', 'es', 'ru', 'pt')

terrorism <- data.frame()
for (lang in languages) {
  print(paste('-----', lang, '-----', sep=' '))
  terrorism_topics <- readLines(paste(term_dir, paste('terrorism_', lang, '.txt', sep=''), sep='/'))
  for (t in terrorism_topics) {
    print(t)
    individual <- wp_trend(
      page=t,
      from='2010-01-01',
      to='2019-12-31',
      lang=lang,
      warn=TRUE
    )
    if (nrow(individual) == 3652) {
      terrorism <- rbind(terrorism, individual)
    }
  }
}
write.csv(terrorism, paste(dest_dir, 'wiki_terrorism.csv', sep='/'), row.names=FALSE)


domestic <- data.frame()
for (lang in languages) {
  print(paste('-----', lang, '-----', sep=' '))
  domestic_topics <- readLines(paste(term_dir, paste('domestic_', lang, '.txt', sep=''), sep='/'))
  for (t in domestic_topics) {
    print(t)
    individual <- wp_trend(
      page=t,
      from='2010-01-01',
      to='2019-12-31',
      lang=lang,
      warn=TRUE
    )
    if (nrow(individual) == 3652) {
      domestic <- rbind(domestic, individual)
    }
  }
}
write.csv(domestic, paste(dest_dir, 'wiki_domestic.csv', sep='/'), row.names=FALSE)
