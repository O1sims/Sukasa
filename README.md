# Sukasa

## Overview

Sukasa is a Python-based web application that analyses current house prices to detect and report price imperfections. This application provides prospective house-buyers a way to investigate whether the houses they are purchasing are incorrectly valued based on social, economic, and geographic characteristics such as current wage levels, the price of similar houses in neighbouring areas, nearby amenities such as schools and shops, and the estate agent selling the house. The aim is to give more information--and therefore sovereignty--to potential consumers, or even just to help current homeowners overcome buyers remorse.

## Technology stack

The web application uses [Django](https://www.djangoproject.com/) as the backend framework and [Angular](https://angular.io/) as the frontend framework. Documentation of the RESTful API service is handled by [Swagger](https://swagger.io/). Development is done with [Docker](https://www.docker.com/) and run on [Google Kubernetes](https://cloud.google.com/python/django/kubernetes-engine). We use [ElasticSearch](https://www.elastic.co/) as our main database. [`R`](https://www.r-project.org/) is the language of choice for any statistical research.

## Bulding the application

We use Docker in the development of Sukasa to make it really easy to build, run and share the application. The following instructions show how it's built and run in Docker:
```
git clone https://github.com/O1sims/Sukasa.git
cd Sukasa
docker build -t kasa:latest .
docker-commpose run --service-ports sukasa
```
## Contact

The best way to troubleshoot or ask for new features or enhancements is to make issues above, but if you have any further questions you can contact [me](mailto:sims.owen@gmail.com) directly.
