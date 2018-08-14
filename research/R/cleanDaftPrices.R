property.data <- getwd() %>%
  paste0("/data/daftPropertyData.json") %>%
  jsonlite::fromJSON()

cleanDaftPrices <- function(property.data) {
  property.data$price[agrepl(
    pattern = "on application", 
    x = property.data$price,
    ignore.case = TRUE)] <- NA
  property.data$price <- "AMV: " %>% 
    gsub(replacement = "", 
         x = property.data$price)
  property.data$price <- "In excess of " %>% 
    gsub(replacement = "", 
         x = property.data$price)
  property.data$price <- " .*$" %>% 
    gsub(replacement = "", 
         x = property.data$price)
  
}