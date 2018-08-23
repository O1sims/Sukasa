library(ggplot2)
library(magrittr)
library(jsonlite)



propertyData <- getwd() %>%
  paste0("/research/data/property/NIPropertyData.json") %>%
  jsonlite::fromJSON() %>%
  subset(!(priceInfo$price %in% c(NA, "POA")))

prepData <- data.frame(
  price = propertyData$priceInfo$price %>% 
    as.integer(),
  bedrooms = propertyData$details$bedrooms,
  style = propertyData$details$style,
  heating = propertyData$details$heating,
  garage = propertyData$details$amenities$garage,
  stringsAsFactors = FALSE)

prepData <- prepData[complete.cases(prepData), ]

linearMod <- lm(
  formula = price ~ bedrooms + style + heating + garage, 
  data = prepData) %>% 
  summary()


scatter.smooth(
  x = propertyData$details$bedrooms, 
  y = propertyData$priceInfo$price %>% 
    as.integer())


