# Housing stock

# 0 <- Antrim & Newtownabbey <- 2
# 1 <- Armagh City, Banbridge & Craigavon <- 3
# 2 <- Belfast <- 4
# 3 <- Causeway Coast & Glens <- 5
# 4 <- Derry City & Strabane <- 6
# 5 <- Fermanagh & Omagh <- 7
# 6 <- Lisburn & Castlereagh <- 8
# 7 <- Mid & East Antrim <- 9
# 8 <- Mid Ulster <- 10
# 9 <- Newry, Mourne & Down  <- 11
# 10 <- Ards & North Down <- 1


library(readr)
library(ggplot2)
library(magrittr)



generate_shapefile_map <- function() {
  spdf <- getwd() %>%
    paste0("/data/map/northern-ireland/districts/NI-district-boundaries.shp") %>%
    maptools::readShapePoly()
  
  spdf@data$id <- rownames(spdf@data)
  spdf.points <- ggplot2::fortify(spdf, region = "id")
  heatmap.data <- dplyr::inner_join(
    spdf.points, 
    spdf@data, 
    by = "id")
  
  heatmap.data$COUNTYNAME %<>% 
    as.vector()
  
  heatmap.data$count <- 0
  for (i in 0:10) {
    heatmap.data$count[which(
      heatmap.data$id == i %>% as.character)] <- property.stock.2018$Total[i+1]
  }
  
  ggplot(
    data = heatmap.data) + 
    geom_polygon(
      size = 0.5, 
      aes(
        x = long, 
        y = lat,
        fill = count,
        group = group)) +
    scale_fill_gradient(
      name = "Total count",
      low = "#CFD8DC", 
      high = "#558B2F") +
    labs(
      title = "NI housing stock by district, 2018",
      subtitle = "Total stock is 790,328",
      caption = "Source: Department of Finance") +
    ggthemes::theme_map() +
    theme(legend.position = "right")
  
  return(shapefileMap)
}


property.stock.2018 <- getwd() %>% 
  paste0("/data/property/property-stock-2018.csv") %>% 
  read_csv()

