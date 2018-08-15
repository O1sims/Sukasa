library(ggmap)
library(ggplot2)
library(ggthemes)
library(jsonlite)
library(magrittr)


geolocationPlot <- function() {
  property.data <- getwd() %>%
    paste0("/research/data/property/IrishPropertyData-3000.json") %>%
    jsonlite::fromJSON()
  
  property.data <- property.data[
    (property.data$details$longitude < -5 & 
       property.data$details$latitude >  40), ]
  
  irelandMap <- ggmap::get_map(
    location = c(-7.739754, 53.521773), 
    zoom = 7,
    maptype = "roadmap") %>% 
    ggmap::ggmap()
  
  subscr <- data.frame(
    lat = property.data$details$latitude,
    lon = property.data$details$longitude,
    agentType = property.data$details$sellerType,
    stringsAsFactors = FALSE)
  subscr <- subscr[complete.cases(subscr), ]
  
  propertyGeolocationPlot <- irelandMap +
    geom_point(
      data = subscr, 
      aes(
        x = lon, 
        y = lat,
        colour = agentType)) + 
    scale_color_ptol() +
    theme_minimal() +
    labs(color='Seller type') +
    theme(
      axis.line = element_blank(), 
      axis.text.x = element_blank(),
      axis.text.y = element_blank(),
      axis.ticks = element_blank(),
      axis.title.x = element_blank(),
      axis.title.y = element_blank(),
      legend.position = "bottom")
  
  getwd() %>%
    paste0("/research/images/ireland-property-geolocation.png") %>%
    ggsave()
  
  return(propertyGeolocationPlot)
}