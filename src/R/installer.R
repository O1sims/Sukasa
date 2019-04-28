
allpkgs <- c(
  "magrittr",
  "plumber", # Requires libssl-dev, libcurl4-gnutls-dev
  "jsonlite",
  "mongolite"  # Requires libssl-dev, libsasl2-dev, zlib-dev
)

# Install them
for (pkg in allpkgs) {
  print(paste0("Installing :: ", pkg))
  install.packages(pkg)
}
