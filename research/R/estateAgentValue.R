#' 

library(magrittr)

# setwd("path/to/Sukasa")

propertyData <- getwd() %>%
  paste0("/research/data/propertyData.json") %>%
  jsonlite::fromJSON() %>%
  subset(!(priceInfo$price %in% c(NA, "POA")))

estateAgents <- propertyData$estateAgent$name %>% 
  unique()

# Find summary statistics for each estate agent

num <- totalValue <- avgValue <- c()
estateAgentStats <- list()
for (agent in estateAgents) {
  estateSubset <- propertyData %>% 
    subset(estateAgent$name == agent)
  estatePrices <- estateSubset$priceInfo$price %>%
    as.integer()
  num %<>% append(estateSubset %>% nrow())
  totalValue %<>% append(estatePrices %>% sum())
  avgValue %<>% append(estatePrices %>% mean())
  estateAgentStats[[agent]] <- list(
    number = estateSubset %>% 
      nrow(),
    totalPropertyValue = estatePrices %>% 
      sum(),
    avgPropertyValue = estatePrices %>%
      mean()
  )
}

df <- data.frame(
  name = estateAgents,
  num = numValue,
  total = totalValue,
  average = avgValue,
  stringsAsFactors = FALSE)

qplot(x = df$name, y = df$total)



