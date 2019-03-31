library(ggplot2)
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
  
  ggplot(
    data = shapefileMap$data) + 
    geom_polygon(
      mapping = aes(
        x = long, 
        y = lat,
        fill = number,
        group = group))  +
    scale_fill_gradient(
      name = "Avg. price",
      low = "#CFD8DC", 
      high = "#7B1FA2") +
    labs(
      title = "Average price of houses by parliamentary, 2018", 
      subtitle = "Average price of sample £196,355.60",
      caption = "Source: Sukasa NI") +
    ggthemes::theme_map() +
    theme(legend.position = "right")
  
  getwd() %>%
    paste0("//images/ni-average-property-price-map") %>%
    ggsave(
      plot = propertyAreaMap, 
      device = "png")
  
  return(propertyAreaMap)
}


parliamentaries_violin_chart <- function(propertyData, propertyType = NA) {
  shapefileMap <- generate_shapefile_map()
  
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
  
  propertyData %<>% 
    subset(!(parliamentary %>% is.na()))
  
  stripped.property.data <- propertyData[0, ]
  for (p in propertyData$parliamentary %>% unique()) {
    parliamentary.data <- propertyData %>% 
      subset(parliamentary == p)
    parliamentary.data$mean <- parliamentaryMean <- parliamentary.data$price %>% mean()
    # parliamentarySd <- parliamentary.data$price %>% sd()
    # parliamentary.data %<>%
    #   subset(price >= parliamentaryMean - 2 * parliamentarySd &
    #            price = parliamentaryMean + 2 * parliamentarySd)
    stripped.property.data %<>% 
      rbind(parliamentary.data)
  }
  
  stripped.property.data$parliamentary %<>% 
    gsub(pattern = " and ", replacement = " & ", .)
  
  stripped.property.data %>%
    ggplot() + 
    geom_violin(
      mapping = aes(
        y = price, 
        x = parliamentary,
        colour = parliamentary,
        fill = parliamentary),
      alpha = 0.5) +
    scale_x_discrete(
      limits = stripped.property.data[order(-stripped.property.data$mean), ]$parliamentary %>% 
        unique()) +
    scale_y_continuous(
      breaks = seq(0, 2500000, 100000), 
      labels = seq(0, 2500000, 100000) %>% 
        as.integer() %>% 
        scales::comma() %>%
        as.character()) +
    xlab("") +
    ylab("") +
    labs(
      title = "NI Property price distribution for each parliamentary (March, 2019)",
      subtitle = "Decreasing, left-to-right, in terms of average house price",
      caption = "Source: Sukasa NI") +
    theme_minimal() +
    theme(legend.position = "none", axis.text.x = element_text(angle = 90, hjust = 1))
  
  return(propertyAreaMap)
}



postcode_violin_chart <- function(propertyData, propertyType = NA) {
  propertyData %<>%
    subset(group != "x")
  
  if (!(propertyType %>% is.na())) {
    propertyData %<>% 
      subset(aggregateStyle == propertyType)
  }
  
  belfastPostcodes <- c(
    "BT18", "BT1", "BT2", "BT3", "BT4", 
    "BT5", "BT6", "BT7", "BT9", "BT12",
    "BT10", "BT13", "BT11", "BT8", "BT16")
  
  postCodeData <- propertyData[0, ]
  for (pcode in belfastPostcodes) {
    b <- propertyData %>% 
      subset(postcode == pcode)
    b$mean <- b$price %>% 
      mean()
    postCodeData %<>% rbind(b)
  }
  
  postCodeData %>%
    ggplot() + 
    geom_violin(
      mapping = aes(
        y = price, 
        x = postcode,
        colour = postcode,
        fill = postcode),
      alpha = 0.5) +
    scale_x_discrete(
      limits = postCodeData[order(-postCodeData$mean), ]$postcode %>% 
        unique()) +
    scale_y_continuous(
      breaks = seq(0, 2500000, 100000), 
      labels = seq(0, 2500000, 100000) %>% 
        as.integer() %>% 
        scales::comma() %>%
        as.character()) +
    xlab("") +
    ylab("") +
    labs(
      title = "Greater Belfast property price distribution by postcode (March, 2019)",
      subtitle = "Decreasing, left-to-right, in terms of average house price",
      caption = "Source: Sukasa NI") +
    theme_minimal() +
    theme(
      legend.position = "none", 
      axis.text.x = element_text(angle = 90, hjust = 1))
  
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
  totalValuation <- totalNumber <- c()
  estateAgents <- propertyData$estateAgent %>% 
    unique()
  for (agent in estateAgents) {
    estateAgentData <- propertyData %>%
      subset(estateAgent == agent)
    totalValuation %<>% 
      append(estateAgentData$price %>% sum())
    totalNumber %<>%
      append(estateAgentData %>% nrow())
  }
  df <- data.frame(
    totalValuation = totalValuation,
    totalStock = totalNumber,
    averagePrice = totalValuation/totalNumber,
    estateAgents = estateAgents,
    stringsAsFactors = FALSE)
  
  return(df)
}



slim.property.df$overpriced <- FALSE
slim.property.df$overpriced[runif(1340, 0, 8000)] <- TRUE

generate_shapefile_map() + 
  geom_point(
    data = slim.property.df %>% 
      subset(
        group != "x" & 
          !(aggregateStyle %>% is.na()) & 
          aggregateStyle != "office"),
    mapping = aes(
      x = long, 
      y = lat,
      colour = overpriced),
    alpha = 0.5, 
    size = 2) +
  scale_color_discrete(
    name = "Significantly overpriced") +
  labs(
    title = "Identification of overpriced properties",
    caption = "Source: Sukasa NI") +
  ggthemes::theme_map() +
  theme(legend.position = "bottom")





estate_agent_bar <- function(propertyData) {
  propertyData %<>% 
    subset(!(aggregateStyle %>% is.na())) %>% 
    subset(aggregateStyle != "cottage")
  
  a <- propertyData %$% 
    estateAgent %>% 
    table() %>% 
    as.data.frame() %>%
    .[order(-.$Freq), ]
  
  a %<>% 
    .[1:10, ]
  
  estateAgentPropertyData <- propertyData %>%
    subset(estateAgent %in% a$.)
  
  ggplot(estateAgentPropertyData) +
    geom_bar(
      mapping = aes(
        x = estateAgent, 
        fill = aggregateStyle),
      alpha = 0.8) +
    scale_fill_discrete(name = "") +
    coord_flip() + 
    labs(
      title = "Total number of properties on sale by top 10 estate agents (March, 2018)",
      caption = "Sukasa NI") + 
    ylab("") + 
    xlab("") +
    theme_minimal() +
    theme(legend.position = "bottom")
  
  totalAssets <- c()
  for (agent in propertyData$estateAgent %>% unique()) {
    totalAssets %<>% append(
      propertyData %>% 
        subset(estateAgent == agent) %$%
        price %>% 
        sum())
  }
  
  data.frame(
    estateAgent = propertyData$estateAgent %>% 
      unique(),
    totalAssets = totalAssets,
    stringsAsFactors = FALSE) %>% 
    .[order(-.$totalAssets), ] %<>% 
    .[1:10, ] %>%
    ggplot() +
    geom_bar(
      mapping = aes(
        x = estateAgent, 
        y = totalAssets), 
      stat = "identity", 
      alpha = 0.8) +
    coord_flip() + 
    scale_y_continuous(
      breaks = seq(0, 100000000, 25000000),
      labels = seq(0, 100000000, 25000000) %>% 
        as.integer() %>% 
        scales::comma() %>% 
        as.character()) +
    labs(
      title = "Top 10 estate agents by total valuation of assets on sale (March, 2018)",
      caption = "Sukasa NI") + 
    ylab("Total assets (£)") + 
    xlab("") +
    theme_minimal() 
}






slim.property.df %>%
  generate_property_areas(
    mapType = "Stock")

slim.property.df %<>%
  postcode_analysis()

estate.agent.data <- slim.property.df %>%
  estate_agent_bar()

