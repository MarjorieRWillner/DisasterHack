
# Wildfire Mitigation: Computer Vision Identification of Hazard Fuels Using Landsat
Welcome to our submission to the AWS Disaster Response Hackathon.

## Description
Without intervention, diseased and dead trees become hazardous fuels that increase the likelihood and severity of wildfire and associated disasters. However, traditional tree assessment methods are time consuming and laborious. To aid Federal, state, and local land managers in quickly identifying and responding to tree disease and mortality, we developed a computer vision model to identify diseased and dead trees from open-source available 16-day 30m Landsat data. 

## Forest Damage Identification Model
### The Data

The Forest Service (FS) performs an annual survey insect and disease and detection survey (IDS). The open source 2020 IDS survey was used as training data for our computer vision (CV) model. The 2020 IDS Summary Map is shown, below. Specifically, a well annotated area on the California-Nevada board encompassing El Dorado and Humboldt-Toiyabe National Forests was used for training. The corresponding 30m Landsat imagery was downloaded from the United States Geological Survey at multiple timepoints. 

We used US Forest Service tree survey data for our model. Due to storage limitations on Github, we stored our data in a public S3 bucket: tree-disease-dl-public in us-east-1.  Alternatively, you can also download imagery tiles from USGS and arrange in the direcory structure indicated.  Note due to the feature extraction step that a specific sampling frequency is not needed and that any resolution of imagery can be used.

### The Model
We created the ImageNet feature representation for classification using an image representation of bands and time. The representation's pixels are randomized. The pixels are then classified using a logisitic basic regression with partial fit.

Finally, we visualized our model output, error and ground truth using matplotlib and wrote the asset as a geotiff.


## Set Up
Please obtain imagery data from the source of your choice and either 1) retrain the models or 2) use the pretrained models.

## Using Our Project
With further development (image asset download services) this model can be used to identify areas of concern in an entirely automated fashion.


## Contributors
codychampion Cody Champion




