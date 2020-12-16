library('wikipediatrend')

rm(list=ls())
setwd('/home/lua/EPFL/MA3/ADA/extension')
term_dir <- 'data/query-terms'

terrorism_topics <- readLines(paste(term_dir, 'terrorism_en.txt', sep='/'))
domestic_topics <- readLines(paste(term_dir, 'domestic_en.txt', sep='/'))

languages <- c('de', 'fr', 'it', 'es', 'pt')

terrorism <- data.frame()
for (t in terrorism_topics) {
  print(t)
  res <- wp_linked_pages(
    page=t,
    lang='en'
  )
  res <- res[res$lang %in% languages, c('lang', 'title')]
  terrorism <- rbind(terrorism, res)
}
for (lang in languages) {
  writeLines(terrorism$title[terrorism$lang == lang], paste(term_dir, '/terrorism_', lang, '.txt', sep=''))
}


domestic <- data.frame()
for (t in domestic_topics) {
  print(t)
  res <- wp_linked_pages(
    page=t,
    lang='en'
  )
  res <- res[res$lang %in% languages, c('lang', 'title')]
  domestic <- rbind(domestic, res)
}
for (lang in languages) {
  writeLines(domestic$title[domestic$lang == lang], paste(term_dir, '/domestic_', lang, '.txt', sep=''))
}
