library(rgeos)
library(scales)
library(ggplot2)
library(jsonlite)
library(magrittr)
library(maptools)


numberOfPropertiesHeatmap <- function(property.data) {
  property.data <- property.data[
    complete.cases(property.data), ]
  
  number <- c()
  counties <- property.data$county %>% 
    unique()
  for (c in counties) {
    numberOfProperties <- property.data %>% 
      subset(county == c) %>% 
      nrow() %>% 
      as.integer()
    number %<>% append(numberOfProperties)
  }
  
  df <- data.frame(
    county = counties %>% 
      paste0(" County"),
    number = number,
    stringsAsFactors = FALSE)
  
  extend.df <- data.frame(
    county = c(
      "Dublin City",
      "Fingal",
      "Dún Laoghaire-Rathdown",
      "South Dublin", 
      "Limerick City", 
      "Cork City", 
      "Galway City", 
      "North Tipperary",
      "South Tipperary",
      "Waterford City"),
    number = c(
      df$number[match("Dublin County", df$county)],
      df$number[match("Dublin County", df$county)],
      df$number[match("Dublin County", df$county)],
      df$number[match("Dublin County", df$county)],
      df$number[match("Limerick County", df$county)],
      df$number[match("Cork County", df$county)],
      df$number[match("Galway County", df$county)],
      df$number[match("Tipperary County", df$county)],
      df$number[match("Tipperary County", df$county)],
      df$number[match("Waterford County", df$county)]),
    stringsAsFactors = FALSE)
  
  df %<>% rbind(extend.df)
  
  spdf <- getwd() %>%
    paste0("/research/data/map/ireland/ireland-admin-counties.shp") %>%
    maptools::readShapePoly()
  
  spdf@data$id <- rownames(spdf@data)
  spdf.points <- ggplot2::fortify(spdf, region = "id")
  counties <- dplyr::inner_join(
    spdf.points, 
    spdf@data, 
    by = "id")
  
  counties$COUNTYNAME %<>% as.vector()
  counties$COUNTYNAME[counties$COUNTYNAME=="D\xfan Laoghaire-Rathdown"] <- "Dún Laoghaire-Rathdown"
  
  heatmap.data <- dplyr::left_join(
    counties, 
    df, 
    by = c("COUNTYNAME" = "county"))
  
  propertyHeatmap <- ggplot(
    data = heatmap.data) + 
    geom_polygon(
      colour = "black",
      size = 0.5, 
      aes(
        x = long, 
        y = lat, 
        group = group, 
        fill = number)) +
    theme(
      axis.text = element_blank(),
      axis.ticks = element_blank(),
      panel.border = element_blank(), 
      panel.grid.major = element_blank(),
      panel.grid.minor = element_blank(),
      panel.background = element_blank()) + 
    scale_fill_gradient2(
      low = "red", 
      mid = "white", 
      high = "blue", 
      labels = comma) + 
    labs(
      fill = "Immigrants")
  
  getwd() %>%
    paste0("/research/images/ireland-heatmap.png") %>%
    ggsave(width = 13, height = 15, units = "cm")
  
  return(propertyHeatmap)
}


cleanPropertyPrices <- function(property.data) {
  property.data$price[agrepl(
    pattern = "on application", 
    x = property.data$price,
    ignore.case = TRUE)] <- NA
  property.data$price <- "AMV: " %>% 
    gsub(replacement = "", 
         x = property.data$price)
  property.data$price <- "In excess of " %>% 
    gsub(replacement = "", 
         x = property.data$price)
  property.data$price <- " .*$" %>% 
    gsub(replacement = "", 
         x = property.data$price)
  property.data$price %<>% as.integer()
  return(property.data)
}


propertyPriceHeatmap <- function(property.data) {
  property.data %<>% cleanPropertyPrices()
  property.data <- property.data[
    complete.cases(property.data), ]
  
  avgPrice <- c()
  counties <- property.data$county %>% 
    unique()
  for (c in counties) {
    subsetProperties <- property.data %>% 
      subset(county == c)
    avgPrice %<>% append(
      subsetProperties$price %>%
        mean())
  }
  
  df <- data.frame(
    county = counties %>% 
      paste0(" County"),
    avgPrice = avgPrice,
    stringsAsFactors = FALSE)
  
  extend.df <- data.frame(
    county = c(
      "Dublin City",
      "Fingal",
      "Dún Laoghaire-Rathdown",
      "South Dublin", 
      "Limerick City", 
      "Cork City", 
      "Galway City", 
      "North Tipperary",
      "South Tipperary",
      "Waterford City"),
    avgPrice = c(
      df$avgPrice[match("Dublin County", df$county)],
      df$avgPrice[match("Dublin County", df$county)],
      df$avgPrice[match("Dublin County", df$county)],
      df$avgPrice[match("Dublin County", df$county)],
      df$avgPrice[match("Limerick County", df$county)],
      df$avgPrice[match("Cork County", df$county)],
      df$avgPrice[match("Galway County", df$county)],
      df$avgPrice[match("Tipperary County", df$county)],
      df$avgPrice[match("Tipperary County", df$county)],
      df$avgPrice[match("Waterford County", df$county)]),
    stringsAsFactors = FALSE)
  
  df %<>% rbind(extend.df)
  
  spdf <- getwd() %>%
    paste0("/research/data/map/ireland/ireland-admin-counties.shp") %>%
    maptools::readShapePoly()
  
  spdf@data$id <- rownames(spdf@data)
  spdf.points <- ggplot2::fortify(spdf, region = "id")
  counties <- dplyr::inner_join(
    spdf.points, 
    spdf@data, 
    by = "id")
  
  counties$COUNTYNAME %<>% as.vector()
  counties$COUNTYNAME[counties$COUNTYNAME=="D\xfan Laoghaire-Rathdown"] <- "Dún Laoghaire-Rathdown"
  
  heatmap.data <- dplyr::left_join(
    counties, 
    df, 
    by = c("COUNTYNAME" = "county"))
  
  propertyHeatmap <- ggplot(
    data = heatmap.data) + 
    geom_polygon(
      colour = "black",
      size = 0.5,
      aes(
        x = long, 
        y = lat, 
        group = group, 
        fill = as.numeric(avgPrice))) +
    theme(
      axis.text = element_blank(),
      axis.ticks = element_blank(),
      panel.border = element_blank(), 
      panel.grid.major = element_blank(),
      panel.grid.minor = element_blank(),
      panel.background = element_blank()) + 
    scale_fill_gradient2(
      low = "red", 
      mid = "white", 
      high = "blue", 
      labels = comma) + 
    labs(
      fill = "Property price (€)")
  
  getwd() %>%
    paste0("/research/images/ireland-price-heatmap.png") %>%
    ggsave(width = 13, height = 15, units = "cm")
  
  return(propertyHeatmap)
}


generatePropertyHeatmaps <- function() {
  property.data <- getwd() %>%
    paste0("/research/data/property/IrishPropertyData.json") %>%
    jsonlite::fromJSON()
  
  stockHeatmap <- numberOfPropertiesHeatmap(
    property.data = property.data)
  
  priceHeatmap <- propertyPriceHeatmap(
    property.data = property.data)
  
  return(list(
    stock = stockHeatmap,
    price = priceHeatmap))
}

heatmaps <- generatePropertyHeatmaps()
