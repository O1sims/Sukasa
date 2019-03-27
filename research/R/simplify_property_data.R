library(magrittr)



PARLIAMENTRIES_ID = list(
  "north down" = "0",
  "upper bann" = "1",
  "east antrim"= "2",
  "north antrim" = "3",
  "south down" = "4",
  "mid ulster" = "5",
  "newry and armagh" = "6",
  "west tyrone" = "7",
  "east belfast" = "8",
  "south belfast" = "9",
  "strangford" = "10",
  "west belfast" = "11",
  "lagan valley" = "12",
  "south antrim" = "13",
  "north belfast" = "14",
  "east londonderry" = "15",
  "fermanagh and south tyrone" = "16",
  "foyle" = "17")


POSTCODE_TO_PARLIAMENTARIES <<- list(
  'bt1' = 'east belfast',
  'bt2' = 'south belfast',
  'bt3' = 'east belfast',
  'bt4' = 'east belfast',
  'bt5' = 'east belfast',
  'bt6' = 'east belfast',
  'bt7' = 'south belfast',
  'bt8' = 'south belfast',
  'bt9' = 'south belfast',
  'bt10' = 'south belfast',
  'bt11' = 'west belfast',
  'bt12' = 'west belfast',
  'bt13' = 'west belfast',
  'bt14' = 'north belfast',
  'bt15' = 'north belfast',
  'bt16' = 'east belfast',
  'bt17' = 'west belfast',
  'bt18' = 'north down',
  'bt19' = 'north down',
  'bt20' = 'north down',
  'bt21' = 'north down',
  'bt22' = 'strangford',
  'bt23' = 'strangford',
  'bt24' = 'strangford',
  'bt25' = 'lagan valley',
  'bt26' = 'lagan valley',
  'bt27' = 'lagan valley',
  'bt28' = 'lagan valley',
  'bt29' = 'south antrim',
  'bt30' = 'south down',
  'bt31' = 'south down',
  'bt32' = 'south down',
  'bt33' = 'south down',
  'bt34' = 'south down',
  'bt35' = 'newry and armagh',
  'bt36' = 'south antrim',
  'bt37' = 'north belfast',
  'bt38' = 'east antrim',
  'bt39' = 'south antrim',
  'bt40' = 'east antrim',
  'bt41' = 'south antrim',
  'bt42' = 'south antrim',
  'bt43' = 'north antrim',
  'bt44' = 'north antrim',
  'bt45' = 'mid ulster',
  'bt46' = 'mid ulster',
  'bt47' = 'east londonderry',
  'bt48' = 'foyle',
  'bt49' = 'east londonderry',
  'bt51' = 'east londonderry',
  'bt52' = 'east londonderry',
  'bt53' = 'north antrim',
  'bt54' = 'north antrim',
  'bt55' = 'east londonderry',
  'bt56' = 'east londonderry',
  'bt57' = 'north antrim',
  'bt58' = 'newtownabbey',
  'bt60' = 'newry and armagh',
  'bt61' = 'newry and armagh',
  'bt62' = 'upper bann',
  'bt63' = 'upper bann',
  'bt64' = 'upper bann',
  'bt65' = 'upper bann',
  'bt66' = 'upper bann',
  'bt67' = 'upper bann',
  'bt68' = 'newry and armagh',
  'bt69' = 'fermanagh and south tyrone',
  'bt70' = 'fermanagh and south tyrone',
  'bt71' = 'fermanagh and south tyrone',
  'bt74' = 'fermanagh and south tyrone',
  'bt75' = 'fermanagh and south tyrone',
  'bt76' = 'fermanagh and south tyrone',
  'bt77' = 'fermanagh and south tyrone',
  'bt78' = 'west tyrone',
  'bt79' = 'west tyrone',
  'bt80' = 'mid ulster',
  'bt81' = 'west tyrone',
  'bt82' = 'west tyrone',
  'bt92' = 'fermanagh and south tyrone',
  'bt93' = 'fermanagh and south tyrone',
  'bt94' = 'fermanagh and south tyrone')


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
      colour = "white",
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
    return(NA)
  }
}


group_properties_in_area <- function(propertyData) {
  propertyData$group <- propertyData$parliamentary <- NA
  for (i in 1:(propertyData %>% nrow())) {
    if (!(propertyData$longPostcode[i] %>% is.null())) {
      pc <- strsplit(
        x = propertyData$longPostcode[i], 
        split = " ")[[1]][1] %>% 
        tolower()
      if (pc %in% names(POSTCODE_TO_PARLIAMENTARIES)) {
        propertyData$parliamentary[i] <- POSTCODE_TO_PARLIAMENTARIES[pc %>% tolower()][[1]]
        propertyData$group[i] <- PARLIAMENTRIES_ID[propertyData$parliamentary[i] %>% tolower()][[1]]
      } else {
        propertyData$parliamentary[i] <- NA
        propertyData$group[i] <- "x"
      }
    } else if (!(propertyData$postcode[i] %>% is.null())) {
      if (propertyData$postcode[i] %>% tolower() %in% names(POSTCODE_TO_PARLIAMENTARIES)) {
        propertyData$parliamentary[i] <- POSTCODE_TO_PARLIAMENTARIES[propertyData$postcode[i] %>% tolower()][[1]]
        propertyData$group[i] <- PARLIAMENTRIES_ID[propertyData$parliamentary[i] %>% tolower()][[1]]
      } else {
        propertyData$parliamentary[i] <- NA
        propertyData$group[i] <- "x"
      }
    } else {
      propertyData$parliamentary[i] <- NA
      propertyData$group[i] <- "x"
    }
  }
  return(propertyData)
}


myopic_property_grouping <- function(propertyData) {
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


generate_property_areas <- function(
  propertyData, propertyType = NA, mapType = c("Stock", "Price")) {
  shapefileMap <- generate_shapefile_map()
  
  propertyData %<>%
    subset(group != "x")
  
  if (!(propertyType %>% is.na())) {
    propertyData %<>% 
      subset(aggregateStyle == propertyType)
  }
  
  shapefileMap$data$number <- 0
  for (grp in propertyData$group %>% unique()) {
    if (mapType %>% tolower() == "stock") {
      shapefileMap$data$number[shapefileMap$data$id == grp] <- subset(
        x = propertyData, 
        subset = group == grp) %>% 
        nrow()
    } else if (mapType %>% tolower() == "price") {
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
        group = group))  +
    scale_fill_gradient(
      name = mapType,
      low = "#CFD8DC", 
      high = "#0277BD") +
    ggthemes::theme_map() +
    theme(legend.position = "right")
  
  return(propertyAreaMap)
}


parliamentaries_violin_chart <- function(propertyData, propertyType) {
  propertyData %<>%
    subset(group != "x")
  
  if (!(propertyType %>% is.na())) {
    propertyData %<>% 
      subset(aggregateStyle == propertyType)
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
  
  shapefileMap + 
    geom_point(
      data = propertyData,
      mapping = aes(
        x = long, 
        y = lat, 
        colour = price)) +
    coord_cartesian(
      xlim = c(
        min(propertyData$long), 
        max(propertyData$long)),
      ylim = c(
        min(propertyData$lat), 
        max(propertyData$lat))) +
    scale_colour_gradient(
      low = "#CFD8DC", 
      high = "#C2185B") +
    ggthemes::theme_map() +
    theme(legend.position = "right")
  
  return(propertyAreaMap)
}


property.data <- getwd() %>%
  paste0("/data/property/all-ni-property-data-2019-03-25.json") %>%
  jsonlite::read_json()

for (i in 1:(property.data %>% length())) {
  if (!(property.data[[i]]$details$style %>% is.null())) {
    property.data[[i]]$details$aggregateStyle <- property.data[[i]]$details$style %>%
      aggregate_style()
  } else {
    property.data[[i]]$details$aggregateStyle <- NA
  }
}

lat <- long <- id <- style <- longPostcode <-
  price <- aggregateStyle <- postcode <- estateAgent <- c()
for (property in property.data) {
  if (!(property$details$location$lat %>% is.null()) && 
      !(property$details$location$lat %>% is.null()) &&
      !(property$details$style %>% is.null()) &&
      !(property$estateAgent$name %>% is.null())) {
    lat %<>% append(property$details$location$lat)
    id %<>% append(property$propertyId)
    long %<>% append(property$details$location$lon)
    price %<>% append(property$priceInfo$price)
    style %<>% append(property$details$style)
    aggregateStyle %<>% append(property$details$aggregateStyle)
    postcode %<>% append(property$postcode)
    longPostcode %<>% append(property$postcode)
    estateAgent %<>% append(property$estateAgent$name)
  }
}

slim.property.df <- data.frame(
  lat = lat,
  long = long,
  price = price,
  style = style,
  id = id,
  postcode = postcode,
  longPostcode = longPostcode,
  aggregateStyle = aggregateStyle,
  estateAgent = estateAgent,
  stringsAsFactors = FALSE) %>%
  group_properties_in_area()


estate_agent_analysis <- function(propertyData) {
  totalValuation <- c()
  estateAgents <- propertyData$estateAgent %>% 
    unique()
  for (agent in estateAgents) {
    estateAgentData <- propertyData %>%
      subset(estateAgent == agent)
    totalValuation %<>% 
      append(estateAgentData$price %>% sum())
  }
  df <- data.frame(
    totalValuation = totalValuation,
    estateAgents = estateAgents,
    stringsAsFactors = FALSE)
  
  return(df)
}

slim.property.df %>%
  generate_property_areas(
    mapType = "Price")
