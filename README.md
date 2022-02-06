
# Wildfire Mitigation: Computer Vision Identification of Hazard Fuels Using Landsat
Welcome to our submission to the AWS Disaster Response Hackathon.

## Description
Without intervention, diseased and dead trees become hazardous fuels that increase the likelihood and severity of wildfire and associated disasters. However, traditional tree assessment methods are time consuming and laborious. To aid Federal, state, and local land managers in quickly identifying and responding to tree disease and mortality, we developed a computer vision model to identify diseased and dead trees from open-source available 16-day 30m Landsat data. 

## Forest Damage Identification Model
### The Data
We used US Forest Service tree survey data for our model. Due to storage limitations on Github, we stored our data in a public S3 bucket: tree-disease-dl-public in us-east-1. 
### The Model
We created the ImageNet feature representation for classification using an image representation of bands and time. The representation's pixels are randomized. The pixels are then classified using a basic regression with partial fit. ...
Finally, we visualized our model output, error and ground truth using matplotlib and wrote the asset as a geotiff.

## Set Up
explain how to test the project

## Using Our Project
explain how to use our project

## Contributors
codychampion Cody Champion

