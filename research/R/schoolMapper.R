library(ggplot2)
library(magrittr)


allSchoolData <- "~/Code/Sukasa/research/data/school/AllNISchoolData.json" %>%
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

data.frame(
  schoolName = schoolName,
  schoolType = schoolType,
  latitude = latitude,
  longitude = longitude,
  stringsAsFactors = FALSE) %>%
  ggplot() +
  geom_point(
    aes(
      y = latitude, 
      x = longitude, 
      colour = schoolType)) + 
  theme_minimal()






spdf <- "/home/owen/Code/Sukasa/research/data/map/northern-ireland/parliamentaries/NI-parliamentary-boundaries.shp" %>%
  maptools::readShapePoly()

spdf@data$id <- rownames(spdf@data)
spdf.points <- ggplot2::fortify(spdf, region = "id")
heatmap.data <- dplyr::inner_join(
  spdf.points, 
  spdf@data, 
  by = "id")

heatmap.data$COUNTYNAME %<>% as.vector()

ggplot(
  data = heatmap.data) + 
  geom_polygon(
    colour = "white",
    size = 0.5, 
    aes(
      x = long, 
      y = lat, 
      group = group)) +
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
  ylab("") + xlab("") +
  theme_minimal() + 
  theme(
    panel.border = element_blank(), 
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    axis.text = element_blank(),
    axis.ticks = element_blank(),
    panel.background = element_blank())

