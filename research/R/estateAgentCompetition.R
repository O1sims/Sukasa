library(ggplot2)
library(ggthemes)
library(magrittr)


estateAgentCompetition <- function(topAgents = 5) {
  propertyData <- getwd() %>%
    paste0("/research/data/propertyData.json") %>%
    jsonlite::fromJSON() %>%
    subset(!(priceInfo$price %in% c(NA, "POA")))
  
  propertyData <- propertyData[-c(240),]
  
  a <- propertyData$estateAgent$name %>%
    table() %>%
    as.data.frame()
  
  a <- a[order(-a$Freq), ][1:topAgents, ]
  
  propertyData %<>% 
    subset(propertyData$estateAgent$name %in% a$.)
  
  estateAgentPlot <- ggplot(data = propertyData,
         aes(x = propertyData$details$location$lat,
             y = propertyData$details$location$lon,
             colour = factor(propertyData$estateAgent$name),
             size = propertyData$priceInfo$price %>% as.integer() / 100000)) +
    geom_point() +
    ylab("Latitude") +
    xlab("Longitude") + 
    labs(color='Estate agent', size = "Price (£100,000)") +
    scale_color_ptol() +
    theme_minimal() + 
    theme()
  
  getwd() %>%
    paste0("/research/images/estate-agent-comptition-", 
           topAgents, ".png") %>%
    ggsave()
  
  return(estateAgentPlot)
}
