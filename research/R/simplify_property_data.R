library(magrittr)


generate_shapefile_map <- function() {
  spdf <- getwd() %>%
    paste0("/data/map/northern-ireland/parliamentaries/NI-parliamentary-boundaries.shp") %>%
    maptools::readShapePoly()
  
  spdf@data$id <- rownames(spdf@data)
  spdf.points <- ggplot2::fortify(spdf, region = "id")
  heatmap.data <- dplyr::inner_join(
    spdf.points, 
    spdf@data, 
    by = "id")
  
  heatmap.data$COUNTYNAME %<>% 
    as.vector()
  
  shapefileMap <- ggplot(
    data = heatmap.data) + 
    geom_polygon(
      fill = "grey",
      size = 0.5, 
      aes(
        x = long, 
        y = lat, 
        group = group))
  
  return(shapefileMap)
}


aggregate_style <- function(style) {
  if (grepl("cottage", style, ignore.case = TRUE)) {
    return("cottage")
  } else if (grepl("apartment", style, ignore.case = TRUE) || 
             grepl("flat", style, ignore.case = TRUE)) {
    return("apartment")
  } else if (grepl("terrace", style, ignore.case = TRUE) || 
             grepl("townhouse", style, ignore.case = TRUE)) {
    return("terrace")
  } else if (grepl("semi-detached", style, ignore.case = TRUE)) {
    return("semi-detached")
  } else if (grepl("detached", style, ignore.case = TRUE)) {
    return("detached")
  } else if (grepl("office", style, ignore.case = TRUE)) {
    return("office")
  } else {
    return(NULL)
  }
}


property.data <- getwd() %>%
  paste0("/data/property/ni-property-data-2019-03-23.json") %>%
  jsonlite::read_json()

for (property in property.data) {
  if (!(property$details$style %>% is.null())) {
    property$details$aggregateStyle <- property$details$style %>%
      aggregate_style()
  } else {
    property$details$aggregateStyle <- NULL
  }
}


group_properties_in_area <- function(propertyData) {
  propertyData$group <- "x"
  spdf <- getwd() %>% 
    paste0("/data/map/northern-ireland/parliamentaries/NI-parliamentary-boundaries.shp") %>%
    maptools::readShapePoly()
  spdf@data$id <- rownames(spdf@data)
  spdf.points <- ggplot2::fortify(
    spdf, region = "id")
  heatmap.data <- dplyr::inner_join(
    spdf.points, 
    spdf@data, 
    by = "id")
  heatmap.data$COUNTYNAME %<>% 
    as.vector()
  maximinCoordinates <- list(
    groupIds = heatmap.data$id %>%
      unique(),
    latMax = c(), 
    latMin = c(), 
    longMax = c(), 
    longMin = c())
  for (groupId in maximinCoordinates$groupIds) {
    sub.heatmap.data <- subset(
      x = heatmap.data, 
      subset = id == groupId)
    maximinCoordinates$latMax %<>% 
      append(sub.heatmap.data$lat %>% max())
    maximinCoordinates$latMin %<>% 
      append(sub.heatmap.data$lat %>% min())
    maximinCoordinates$longMax %<>% 
      append(sub.heatmap.data$long %>% max())
    maximinCoordinates$longMin %<>% 
      append(sub.heatmap.data$long %>% min())
  }
  for (i in 1:(maximinCoordinates$latMax %>% length())) {
    groupProperties <- propertyData %>% 
      subset(lat <= maximinCoordinates$latMax[i] & lat >= maximinCoordinates$latMin[i] &
               long <= maximinCoordinates$longMax[i] & long >= maximinCoordinates$longMin[i])
    m <- match(groupProperties$id, propertyData$id)
    propertyData$group[m] <- maximinCoordinates$groupIds[i]
  }
  return(propertyData)
}


generate_property_areas <- function(propertyData, propertyType = NA, mapType = c("stock", "price")) {
  shapefileMap <- generate_shapefile_map()
  
  propertyData %<>%
    subset(group != "x")
  
  if (!(propertyType %>% is.na())) {
    propertyData %<>% 
      subset(style == propertyType)
  }
  
  shapefileMap$data$number <- 0
  for (grp in propertyData$group %>% unique()) {
    if (mapType == "stock") {
      shapefileMap$data$number[shapefileMap$data$id == grp] <- subset(
        x = propertyData, 
        subset = group == grp) %>% 
        nrow()
    } else if (mapType == "price") {
      shapefileMap$data$number[shapefileMap$data$id == grp] <- subset(
        x = propertyData, 
        subset = group == grp) %$%
        price %>% mean()
    }
  }
  
  propertyAreaMap <- ggplot(
    data = shapefileMap$data) + 
    geom_polygon(
      mapping = aes(
        x = long, 
        y = lat, 
        fill = number,
        group = group)) +
    scale_fill_gradient(
      low = "#CFD8DC", 
      high = "#C2185B") +
    ggthemes::theme_map()
  
  return(propertyAreaMap)
}


generate_property_areas(propertyData = slim.property.df, mapType = "price")



lat <- long <- id <- style <-
  price <- c()
for (property in property.data) {
  if (!(property$details$location$lat %>% is.null()) && 
      !(property$details$location$lat %>% is.null())) {
    lat %<>% append(property$details$location$lat)
    id %<>% append(property$propertyId)
    long %<>% append(property$details$location$lon)
    price %<>% append(property$priceInfo$price)
    style %<>% append(property$details$style)
  }
}




slim.property.df <- data.frame(
  lat = lat,
  long = long,
  price = price,
  style = style,
  id = id,
  stringsAsFactors = FALSE) %>%
  group_properties_in_area()

too_little <- slim.property.df$group %>% 
  table() %>% 
  as.data.frame() %>% 
  subset(Freq <= 50) %$% 
  .

slim.property.df %<>% subset(!(group %in% too_little))

