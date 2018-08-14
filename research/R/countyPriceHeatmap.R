library(rgdal)
library(scales)
library(ggplot2)
library(jsonlite)
library(magrittr)



# Load property data
property.data <- getwd() %>%
  paste0("/research/data/property/NIPropertyData.json") %>%
  jsonlite::fromJSON() %>%
  subset(!(priceInfo$price %in% c(NA, "POA")))

# Seperate data by county and run average price levels
property.data$county <- (property.data$postcode == "BT18") %>% 
  ifelse("Down", "Antrim")


# TODO: need to put resulting average price data in some data structure, idk...
for (c in property.data$county %>% unique()) {
  if (!is.na(c)) {
    property.data.subset <- property.data %>% 
      subset(county == c)
    prices <- property.data.subset$priceInfo$price %>% 
      na.omit() %>% 
      as.integer()
    mean(prices) %>% 
      print()
  } else {
    "A county has been flagged as `NA`" %>% 
      print()
  }
}



NIShapefile <- rgdal::readOGR(
  dsn = getwd() %>% 
    paste0("/research/data/map/northern-ireland/county/ni-county-boundaries.shp"),
  layer = "ni-county-boundaries")

# Use the NAME_2 field to create data frame
NICountyMap <- NIShapefile %>% 
  ggplot2::fortify()




## ID to county
# 
# 0 <- Tyrone
# 1 <- Antrim
# 2 <- Armagh
# 3 <- Fermanagh
# 4 <- Londonderry
# 5 <- Down



# Insert some dummy price data
NICountyMap$price <- 10000 * NICountyMap$id %>% 
  as.integer()

NIMapPlot <- NICountyMap %>% ggplot(
  aes(x = long, y = lat, group = group, fill = price)) + 
  geom_polygon(
    colour = "black", 
    size = 0.5, 
    aes(group = group))  + 
  scale_fill_gradient2(
    low = "red", 
    mid = "white", 
    high = "blue", 
    labels = comma) + 
  theme(
    axis.text = element_blank(),
    axis.ticks = element_blank(),
    panel.border = element_blank(),
    panel.background = element_blank(),
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank())



countyPriceHeatmap <- function() {
  
}