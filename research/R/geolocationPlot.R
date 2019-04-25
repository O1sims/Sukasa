library(ggmap)
library(ggplot2)
library(ggthemes)
library(jsonlite)
library(magrittr)


geolocationPlot <- function() {
  property.data <- getwd() %>%
    paste0("/data/property/IrishPropertyData-3000.json") %>%
    jsonlite::fromJSON()
  
  property.data <- property.data[
    (property.data$details$longitude < -5 & 
       property.data$details$latitude >  40), ]
  
  spdf <- getwd() %>%
    paste0("/data/map/ireland/ireland-admin-counties.shp") %>%
    maptools::readShapePoly()
  
  spdf@data$id <- rownames(spdf@data)
  spdf.points <- ggplot2::fortify(spdf, region = "id")
  irelandMap <- dplyr::inner_join(
    spdf.points, 
    spdf@data, 
    by = "id")
  
  subscr <- data.frame(
    lat = property.data$details$latitude,
    lon = property.data$details$longitude,
    agentType = property.data$details$sellerType,
    propertyType = property.data$details$propertyType,
    stringsAsFactors = FALSE)
  subscr <- subscr[complete.cases(subscr), ]
  
  ggplot() +
    geom_polygon(
      data = irelandMap,
      fill = "#B0BEC5",
      colour = "white",
      aes(
        x = long, 
        y = lat, 
        group = group)) +
    geom_point(
      data = subscr, 
      aes(
        x = lat, 
        y = lon,
        colour = propertyType),
      alpha = 0.8) + 
    scale_color_ptol() +
    theme_minimal() +
    labs(color="Property type") +
    ggthemes::theme_map()
  
  getwd() %>%
    paste0("/images/ireland-property-geolocation.png") %>%
    ggsave()
  
  return(propertyGeolocationPlot)
}
