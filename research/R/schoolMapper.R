library(ggmap)
library(ggplot2)
library(magrittr)
library(maptools)


clean_school_name <- function(schoolName) {
  schoolName %<>% 
    tolower() %>% 
    gsub(' ', '', .) %>% 
    gsub("the", '', .) %>%
    gsub('school', '', .) %>%
    gsub('[[:punct:] ]+','', .)
  return(schoolName)
}


finance_school_mapper <- function(schoolData, financeData) {
  cleanedSchools <- c()
  for (i in 1:length(financeData)) {
    cleanedSchools %<>% 
      append(financeData[[i]]$schoolName %>% 
      clean_school_name())
  }
  
  for (i in 1:(schoolData %>% length())) {
    matchedSchoolName <- schoolData[[i]]$name %>% 
      clean_school_name() %>%
      match(cleanedSchools)
    
    if (matchedSchoolName %>% is.na()) {
      schoolData[[i]]$finance <- NA
    } else {
      schoolData[[i]]$finance <- financeData[[matchedSchoolName]]$amount
    }
  }
  
  return(schoolData)
}


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
      fill = "gray",
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
    ggmap::get_map(
      maptype = "roadmap") %>%
    ggmap::ggmap(
      padding = 0)
  
  return(googleMap)
}


allSchoolData <- getwd() %>%
  paste0("/research/data/school/allNISchoolData.json") %>%
  jsonlite::read_json()

schoolFinanceData <- getwd() %>%
  paste0("/research/data/school/schoolFinanceData.json") %>%
  jsonlite::read_json()

fullSchoolData <- finance_school_mapper(
  schoolData = allSchoolData,
  financeData = schoolFinanceData)

latitude <- longitude <- schoolName <- 
  schoolType <- numberOfPupils <- finance <- c()
for (school in fullSchoolData) {
  schoolName %<>% append(school$name)
  finance %<>% append(school$finance)
  latitude %<>% append(school$coordinate$latitude)
  longitude %<>% append(school$coordinate$longitude)
  schoolType %<>% append(school$type)
  if (!is.null(school$years[[1]]$numberOfPupils)) {
    numberOfPupils %<>% 
      append(school$years[[1]]$numberOfPupils)
  } else {
    totalAdmissions %<>% 
      append(NA)
  }
}

generate_shapefile_map() +
  geom_point(
    data = data.frame(
      schoolName = schoolName,
      schoolType = schoolType,
      latitude = latitude,
      longitude = longitude,
      finance = finance,
      numberOfPupils = numberOfPupils,
      stringsAsFactors = FALSE),
    aes(
      y = latitude, 
      x = longitude, 
      colour = finance,
      size = numberOfPupils,
      alpha = 0.5)) + 
  ylab("") + 
  xlab("") +
  theme_minimal() + 
  theme(
    panel.border = element_blank(), 
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    axis.text = element_blank(),
    axis.ticks = element_blank(),
    panel.background = element_blank(),
    legend.position = "bottom")

# Belfast only coordinates: 
# coord_cartesian(
#   xlim = c(-6.5, -5.5),
#   ylim = c(54.45, 54.75))

data.frame(
  schoolName = schoolName,
  schoolType = schoolType,
  latitude = latitude,
  longitude = longitude,
  finance = finance,
  numberOfPupils = numberOfPupils,
  financeAdmissionRatio = finance/numberOfPupils,
  stringsAsFactors = FALSE) %>%
  subset(schoolType == "primary") %>%
  ggplot() +
  geom_point(
    mapping = aes(
      x = numberOfPupils,
      y = finance,
      colour = schoolType,
      size = financeAdmissionRatio),
    alpha = 0.6) +
  theme_minimal() +
  theme(legend.position = "none")
