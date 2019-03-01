library(jsonlite)

property.data <- getwd() %>%
  paste0("/research/data/property/ni-property-data-2019-02-28.json") %>%
  jsonlite::read_json()

latitude <- longitude <- address <- price <- estateAgent <- heating <- c()
for (property in property.data) {
  address %<>% append(property$address)
  if (is.null(property$details$location$lat)) {
    latitude %<>% append(NA)
  } else {
    latitude %<>% append(property$details$location$lat)
  }
  if (is.null(property$details$location$lon)) {
    longitude %<>% append(NA)
  } else {
    longitude %<>% append(property$details$location$lon)
  }
  price %<>% append(property$priceInfo$price)
  estateAgent %<>% append(property$estateAgent$name)
  heating %<>% append(property$details$heating)
}

slim.property.data <- data.frame(
  estateAgent = estateAgent,
  address = address,
  price = price,
  latitude = latitude,
  longitude = longitude,
  stringsAsFactors = FALSE)

a <- slim.property.data$estateAgent %>% 
  table() %>% 
  as.data.frame()

hmm <- a[order(-a$Freq),] 

slim.property.data %<>% subset(estateAgent %in% hmm$.[1:5])

hmm$.[1:5]

generate_shapefile_map() +
  geom_point(
    data = slim.property.data,
    aes(
      y = latitude,
      x = longitude,
      size = price,
      colour = estateAgent)) + 
  ylab("") + 
  xlab("") +
  coord_cartesian(
    xlim = c(
      min(longitude, na.rm = TRUE), 
      max(longitude, na.rm = TRUE)),
    ylim = c(
      min(latitude, na.rm = TRUE), 
      max(latitude, na.rm = TRUE))) +
  theme_minimal() + 
  theme(
    panel.border = element_blank(), 
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    axis.text = element_blank(),
    axis.ticks = element_blank(),
    panel.background = element_blank(),
    legend.position = "bottom")








library(leaflet)


leafIcon <- makeIcon(
  iconUrl = "http://leafletjs.com/examples/custom-icons/leaf-green.png",
  iconWidth = 38, iconHeight = 95,
  iconAnchorX = 22, iconAnchorY = 94,
  shadowUrl = "http://leafletjs.com/examples/custom-icons/leaf-shadow.png",
  shadowWidth = 50, shadowHeight = 64,
  shadowAnchorX = 4, shadowAnchorY = 62
)

leaflet(data = slim.property.data) %>% 
  addTiles() %>%
  addMarkers(
    lng = ~longitude, 
    lat = ~latitude, 
    popup = ~as.character(price), 
    label = ~as.character(address))
