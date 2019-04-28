# start from the rocker/r-ver:3.5.0 image
FROM rocker/r-ver:3.5.0

# install the linux libraries needed for plumber
RUN apt-get update -qq && apt-get install -y \
  libssl-dev \
  libcurl4-gnutls-dev \
  libsasl2-dev \
  zlib1g-dev

# copy everything from the current directory into the container
COPY / /

# install plumber
RUN R -e "source('installer.R')"

# open port 10068 to traffic
EXPOSE 10068

# when the container starts, start the main.R script
ENTRYPOINT ["Rscript", "main.R"]
