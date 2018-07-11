library(ggplot2)
library(ggthemes)
library(magrittr)


postcodePrices <- function() {
  propertyData <- getwd() %>%
    paste0("/research/data/propertyData.json") %>%
    jsonlite::fromJSON() %>%
    subset(!(priceInfo$price %in% c(NA, "POA")))
  
  postcodeTable <- propertyData$postcode %>%
    table() %>%
    as.data.frame(
      stringsAsFactors = FALSE)
  
  rarePostcodes <- postcodeTable %>% 
    subset(Freq <= 10) %$% .
  
  propertyData %<>% subset(!(postcode %in% rarePostcodes))
  
  ggplot(
    data = propertyData,
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
        hjust = 1))
  
  
}