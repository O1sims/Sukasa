library(ggplot2)
library(ggthemes)
library(jsonlite)
library(magrittr)


postcodePrices <- function(consolidateStyles = TRUE, removeAnomalies = FALSE) {
  propertyData <- getwd() %>%
    paste0("/research/data/propertyData.json") %>%
    jsonlite::fromJSON()
  
  propertyData %<>% subset(!(priceInfo$price %in% c(NA, "POA"))) %>%
    subset(!(postcode %>% is.na())) %>%
    subset(!(postcode %in% (
      propertyData$postcode %>%
        table() %>%
        as.data.frame() %>% 
        subset(Freq <= 10) %$% .))) %>%
    subset(!(details$style %>% is.na())) %>%
    subset(!(details$style %in% (
      propertyData$details$style %>%
        table() %>%
        as.data.frame() %>% 
        subset(Freq <= 10) %$% .)))
  
  if (consolidateStyles) {
    hashKeys <- c("Apartment", "Flat", "Bungalow", "Detached", 
                  "Semi-detached", "Terrace", "terrace", "Townhouse")
    hashValues <- c("Apartment", "Apartment", "Bungalow", "Detached house", 
                    "Semi-detached house", "Terrace house", "Terrace house", "Townhouse")
    
    consolidatedStyles <- hashmap::hashmap(
      keys = hashKeys,
      values = hashValues)
    
    for (key in hashKeys) {
      getValues <- grepl(
        pattern = key,
        x = propertyData$details$style, 
        ignore.case = FALSE)
      propertyData$details$style[getValues] <- consolidatedStyles[[key]]
    }
  }
  
  if (removeAnomalies) {
    # For each postcode and each property style we remove anomalous data points
    # Let's define an anomalous data point as some point that is a standard deviation
    # away from the mean.
    adjustedPropertyList <- list()
    for (postCode in propertyData$postcode %>% unique()) {
      subsetPropertyData <- propertyData %>% 
        subset(postcode == postCode)
      for (style in subsetPropertyData$details$style %>% unique()) {
        subsetStyle <- subsetPropertyData %>%
          subset(details$style == style)
        meanStylePrice <- subsetStyle$priceInfo$price %>%
          as.integer() %>%
          mean()
        stdDeviationPrice <- subsetStyle$priceInfo$price %>%
          as.integer() %>%
          sd()
        normalPropertydata <- subsetStyle %>%
          subset(
            priceInfo$price %>% as.integer() <= meanStylePrice + stdDeviationPrice)
        adjustedPropertyList %<>% 
          rbind(normalPropertydata %>% as.list())
      }
    }
    adjustedPropertyData <- adjustedPropertyList %>% as.data.frame(stringsAsFactors = FALSE)
  }
  
  postCodePlot <- ggplot(
    data = adjustedPropertyList,
    aes(x = postcode,
        y = priceInfo$price %>% as.integer(),
        colour = details$style)) +
    geom_violin() + 
    geom_jitter(
      height = 0, 
      width = 0.1) +
    ylab("Price (£)") +
    xlab("Postcode") +
    theme_minimal() + 
    theme(
      axis.text.x = element_text(
        angle = 45, 
        hjust = 1)) + 
    scale_colour_discrete(
      name = "Property style")
  
  getwd() %>%
    paste0("/research/images/postcode-prices",
           ifelse(
             test = consolidateStyles, 
             yes = "-consolidated", 
             no = ""), 
           ".png") %>%
    ggsave()
  
  return(postCodePlot)
}
