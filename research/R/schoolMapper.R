library(ggmap)
library(ggplot2)
library(magrittr)
library(maptools)


generate_shapefile_map <- function() {
  spdf <- getwd() %>% 
    paste0("/research/data/map/northern-ireland/parliamentaries/NI-parliamentary-boundaries.shp") %>%
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
      colour = "white",
      size = 0.5, 
      aes(
        x = long, 
        y = lat, 
        group = group))
  
  return(shapefileMap)
}


generate_google_map <- function(longitude = -6, latitude = 54.5) {
  googleMap <- c(
    lon = longitude, 
    lat = latitude) %>% 
    ggmap::get_map() %>%
    ggmap::ggmap()
  
  return(googleMap)
}


allSchoolData <- getwd() %>%
  paste0("/research/data/school/allNISchoolData.json") %>%
  jsonlite::read_json()


latitude <- longitude <- schoolName <- schoolType <- totalAdmissions <- c()
for (school in allSchoolData) {
  schoolName %<>% append(school$name)
  latitude %<>% append(school$coordinate$latitude)
  longitude %<>% append(school$coordinate$longitude)
  schoolType %<>% append(school$type)
  if (!is.null(school$years[[1]]$totalAdmissions)) {
    totalAdmissions %<>% append(school$years[[1]]$totalAdmissions %>% 
                                  as.integer())
  } else {
    totalAdmissions %<>% append(50)
  }
}

generate_shapefile_map() +
  geom_point(
    data = data.frame(
      schoolName = schoolName,
      schoolType = schoolType,
      latitude = latitude,
      longitude = longitude,
      stringsAsFactors = FALSE),
    aes(
      y = latitude, 
      x = longitude, 
      colour = schoolType, 
      alpha=0.5)) + 
  ylab("") + 
  xlab("") +
  coord_cartesian(
    xlim = c(-6.5, -5.5),
    ylim = c(54.45, 54.75)) +
  theme_minimal() + 
  theme(
    panel.border = element_blank(), 
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    axis.text = element_blank(),
    axis.ticks = element_blank(),
    panel.background = element_blank(),
    legend.position = "bottom")
