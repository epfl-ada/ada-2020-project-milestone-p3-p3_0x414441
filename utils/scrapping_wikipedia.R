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
write.csv(terrorism, 'wiki_terrorism.csv', row.names=FALSE)


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
write.csv(domestic, 'wiki_domestic.csv', row.names=FALSE)
