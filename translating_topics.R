rm(list=ls())

setwd('/home/lua/EPFL/MA3/ADA/extension')

library('wikipediatrend')

terrorism_topics <- c('Al-Qaeda',
                      'terrorism',
                      'terror',
                      'attack',
                      'iraq',
                      'afghanistan',
                      'iran',
                      'pakistan',
                      'agro',
                      'Environmental_terrorism',
                      'Eco-terrorism',
                      'Conventional_weapon',
                      'Weapons-grade',
                      'Dirty_bomb',
                      'Nuclear_enrichment',
                      'nuclear',
                      'Chemical_weapon',
                      'Biological_weapon',
                      'Ammonium_nitrate',
                      'Improvised_explosive_device',
                      'Abu_Sayyaf',
                      'hamas',
                      'FARC',
                      'Irish_Republican_Army',
                      'Euskadi_ta_Askatasuna',
                      'hezbollah',
                      'Tamil_Tigers',
                      'Palestine_Liberation_Organization',
                      'Palestine_Liberation_Front',
                      'Car_bomb',
                      'jihad',
                      'taliban',
                      'Suicide_bomber',
                      'Suicide_attack',
                      'Al-Qaeda_in_the_Arabian_Peninsula',
                      'Al-Qaeda_in_the_Islamic_Maghreb',
                      'Tehrik-i-Taliban_Pakistan',
                      'yemen',
                      'pirates',
                      'extremism',
                      'somalia',
                      'nigeria',
                      'Political_radicalism',
                      'Al-Shabaab',
                      'nationalism',
                      'recruitment',
                      'fundamentalism',
                      'islamist')

domestic_topics <- c('United_States_Department_of_Homeland_Security',
                     'Federal_Emergency_Management_Agency',
                     'Coast_guard',
                     'Customs_and_Border_Protection',
                     'Border_Patrol',
                     'Secret_Service',
                     'Bureau_of_Land_Management',
                     'Homeland_defense',
                     'Espionage',
                     'Task_Force_88_(anti-terrorist_unit)',
                     'Central_Intelligence_Agency',
                     'Fusion_center',
                     'DEA',
                     'Secure_Border_Initiative',
                     'Federal_Bureau_of_Investigation',
                     'Alcohol_and_Tobacco_Tax_and_Trade_Bureau',
                     'United_States_Citizenship_and_Immigration_Services',
                     'Federal_Air_Marshal_Service',
                     'Transportation_Security_Administration',
                     'Air_marshal',
                     'Federal_Aviation_Administration',
                     'National_Guard',
                     'Emergency_management',
                     'U.S._Immigration_and_Customs_Enforcement',
                     'United_Nations')


languages <- c('de', 'fr', 'it', 'es', 'ru', 'ja', 'pt', 'ar', 'hi')


terrorism <- data.frame()
for (t in terrorism_topics) {
  res <- wp_linked_pages(
    page=t,
    lang='en'
  )
  res <- res[res$lang %in% languages, c('lang', 'title')]
  terrorism <- rbind(terrorism, res)
}
for (lang in languages) {
  write.table(terrorism$title[terrorism$lang == lang], paste('data/', lang, '_terrorism_topics.txt', sep=''), col.names=FALSE, row.names=FALSE, quote=FALSE)
}


domestic <- data.frame()
for (t in domestic_topics) {
  res <- wp_linked_pages(
    page=t,
    lang='en'
  )
  res <- res[res$lang %in% languages, c('lang', 'title')]
  domestic <- rbind(domestic, res)
}
for (lang in languages) {
  write.table(domestic$title[domestic$lang == lang], paste('data/', lang, '_domestic_topics.txt', sep=''), col.names=FALSE, row.names=FALSE, quote=FALSE)
}
