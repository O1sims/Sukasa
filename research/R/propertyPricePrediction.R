library(MASS)
library(ggplot2)
library(magrittr)
library(jsonlite)


# Analysis of entire housing stock
# It's going to be difficult to build a pricing model 

propertyData <- getwd() %>%
  paste0("/research/data/property/NIPropertyData.json") %>%
  jsonlite::fromJSON() %>%
  subset(!(priceInfo$price %in% c(NA, "POA")))

prepData <- data.frame(
  id = propertyData$propertyId,
  price = propertyData$priceInfo$price %>% 
    as.integer(),
  bedrooms = propertyData$details$bedrooms,
  style = propertyData$details$style,
  heating = propertyData$details$heating,
  garage = propertyData$details$amenities$garage,
  postcode = propertyData$postcode,
  garden = propertyData$details$amenities$garden,
  receptions = propertyData$details$receptions,
  stringsAsFactors = FALSE)

prepData <- prepData[complete.cases(prepData), ]

propertyPriceModel <- lm(
  formula = price ~ bedrooms + style + heating + 
    garage + postcode + garden + receptions, 
  data = prepData)

propertyPriceModel %>% 
  summary()

predictedPrices <- predict(
  object = propertyPriceModel,
  newdata = prepData)

priceResiduals <- prepData$price - predictedPrices

qplot(
  x = 1:length(priceResiduals), 
  y = priceResiduals)


# Subset model for semi-detacthed homes

propertyStyle <- "Semi-detached house"

propertyData <- getwd() %>%
  paste0("/research/data/property/NIPropertyData.json") %>%
  jsonlite::fromJSON() %>%
  subset(!(priceInfo$price %in% c(NA, "POA"))) %>%
  subset(details$style == propertyStyle)

prepData <- data.frame(
  price = propertyData$priceInfo$price %>% 
    as.integer(),
  bedrooms = propertyData$details$bedrooms,
  heating = propertyData$details$heating,
  garage = propertyData$details$amenities$garage,
  postcode = propertyData$postcode,
  garden = propertyData$details$amenities$garden,
  receptions = propertyData$details$receptions,
  stringsAsFactors = FALSE)

prepData <- prepData[complete.cases(prepData), ]

propertyPriceModel <- MASS::rlm(
  formula = price ~ bedrooms + heating + 
    garage + postcode + garden + receptions, 
  data = prepData)

propertyPriceModel %>% 
  summary()

predictedPrices <- predict(
  object = propertyPriceModel,
  newdata = prepData)

prepData$residuals <- prepData$price - predictedPrices

qplot(
  x = 1:nrow(prepData), 
  y = prepData$residuals)

prepData$overValued <- ifelse(
  prepData$residuals >= prepData$price + sd(prepData$residuals), 'overvalued', NA)




