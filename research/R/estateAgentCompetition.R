library(ggmap)
library(ggplot2)
library(ggthemes)
library(jsonlite)
library(magrittr)


estateAgentCompetition <- function(topAgents = 5, projectMap = TRUE, 
                                   mapZoom = 12) {
  propertyData <- getwd() %>%
    paste0("/data/property/NIPropertyData.json") %>%
    jsonlite::fromJSON() %>%
    subset(!(priceInfo$price %in% c(NA, "POA")))
  
  a <- propertyData$estateAgent$name %>%
    table() %>%
    as.data.frame()
  
  a <- a[order(-a$Freq), ][1:topAgents, ]
  
  propertyData %<>% 
    subset(propertyData$estateAgent$name %in% a$.)
  
  if (projectMap) {
    belfastMap <- ggmap::get_map(
      location = c(-5.9, 54.6), 
      zoom = mapZoom, 
      maptype = "terrain") %>% 
      ggmap::ggmap()
    
    subscr <- data.frame(
      lat = propertyData$details$location$lat,
      lon = propertyData$details$location$lon,
      price = propertyData$priceInfo$price %>% as.integer() / 100000,
      agent = propertyData$estateAgent$name)
    subscr <- subscr[complete.cases(subscr), ]
    
    estateAgentPlot <- belfastMap  +
      geom_point(
        data = subscr, 
        aes(
          x = lon, 
          y = lat, 
          size = price, 
          colour = agent)) + 
      labs(color='Estate agent', size = "Price (£100,000)") +
      scale_color_ptol() +
      theme_minimal() +
      theme(
        axis.line = element_blank(), 
        axis.text.x = element_blank(),
        axis.text.y = element_blank(),
        axis.ticks = element_blank(),
        axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        legend.position = "bottom")
  } else {
    ggplot(
      data = propertyData,
      aes(x = propertyData$details$location$lon,
          y = propertyData$details$location$lat,
          colour = factor(propertyData$estateAgent$name),
          size = propertyData$priceInfo$price %>% as.integer() / 100000)) +
      geom_point() +
      ylab("Latitude") +
      xlab("Longitude") + 
      labs(color='Estate agent', size = "Price (£100,000)") +
      scale_color_ptol() +
      theme_minimal() + 
      theme()
  }
  
  getwd() %>%
    paste0("/research/images/estate-agent-comptition-", 
           topAgents, 
           ifelse(projectMap, '-map-' %>% 
                    paste0(mapZoom), ''),
           ".png") %>%
    ggsave(plot = estateAgentPlot)
  
  return(estateAgentPlot)
}
