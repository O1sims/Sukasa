library(plumber)
library(mongolite)

# Set up the function for mongo
setup_mongo <- function() {
  con <- NULL
  
  while (is.null(con)) {
    con <- tryCatch(
      expr = {
        mongolite::mongo(
          url = "mongodb://sukasa-db:8210", 
          db = "sukasa", 
          collection = "properties"
        )  
      }, 
      error = function(e) NULL
    )
    
    if (is.null(con)) {
      print("No connection - sleeping for 10")
      Sys.sleep(10) 
    }
  }
  
  return(con)
}


con <<- setup_mongo()

# Plumb the API!
r <- plumber::plumb(file = "plumber.R")

# Run the server
r$run(
  port = 10068, 
  host = "0.0.0.0"
)
