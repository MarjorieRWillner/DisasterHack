# Wildfire Mitigation: Computer Vision Identification of Hazard Fuels Using Landsat
Welcome to our submission to the AWS Disaster Response Hackathon.  [![Open In SageMaker Studio Lab](https://studiolab.sagemaker.aws/studiolab.svg)](https://studiolab.sagemaker.aws/import/github/github.com/MarjorieRWillner/DisasterHack/edit/main/tree_model/Data_extraction.ipynb)



## Description
Without intervention, diseased and dead trees become hazardous fuels that increase the likelihood and severity of wildfire and associated disasters. However, traditional tree assessment methods are time consuming and laborious. To aid Federal, state, and local land managers in quickly identifying and responding to tree disease and mortality, we developed a computer vision model to identify diseased and dead trees from open-source available 16-day 30m Landsat data. 

## Background

The cost associated with conducting tree mortality surveys reduces the frequency and coverage area of surveys creating the potential for forest managers to overlook areas of tree mortality outside of survey regions. Early detection and continuous monitoring of established species such as the Western Pine Beetle are critical to slowing their spread. However, the low frequency and limited coverage area of the National Insect and Disease detection survey reduces the capacity of USDA’s Animal Plant Health Inspection Service to rapidly detect tree mortality caused by outbreaks of invasive species. Due to the scalability of our CV model, Federal, state, and local land managers can rapidly detect and monitor tree mortality over large land areas, leading to faster treatment of affected areas and containment of invasive species.

Our CV model also has the potential to reduce the risk of power outages and forest fire outbreaks due to tree-conductor contact through faster identification and monitoring of tree mortality. On distribution systems, it is common for tree related outages to comprise 20%-50% of all unplanned outages. The vast majority of tree-related outages stem from tree failure. Tree mortality exposes a power line to a high risk of tree incidents over time. By continuously identifying dead trees over a large land area, our model will enable utility foresters, asset managers, arboriculture consultants, and regulators to improve tree risk assessments and line clearance programs through automated detection of tree mortality.


## Forest Damage Identification Model
### The Data

The Forest Service (FS) performs an annual survey insect and disease and detection survey (IDS). The open source 2020 IDS survey was used as training data for our computer vision (CV) model. The 2020 IDS Summary Map is shown, below. Specifically, a well annotated area on the California-Nevada board encompassing El Dorado and Humboldt-Toiyabe National Forests was used for training. The corresponding 30m Landsat imagery was downloaded from the United States Geological Survey at multiple timepoints. 

We used US Forest Service tree survey data for our model. Due to storage limitations on Github, we stored our data in a public S3 bucket: tree-disease-dl-public in us-east-1.  Alternatively, you can also download imagery tiles from USGS and arrange in the direcory structure indicated.  Note due to the feature extraction step that a specific sampling frequency is not needed and that any resolution of imagery can be used.

### The Model
We created the ImageNet feature representation for classification using an image representation of bands and time. The pixels are then classified using a logisitic basic regression with partial fit.  We have tested model perfromance by randomizing pixel representations and then retraining the model.  As expected RSME increase when data was randomized at the pixel/time series stage.  

Finally, we visualized our model output, error and ground truth using matplotlib and wrote the asset as a geotiff.


![image](https://user-images.githubusercontent.com/15643577/156848755-5df29fd5-92db-4e72-b318-575395aa627b.png)

## Set Up
Please obtain imagery data from the source of your choice and either 1) retrain the models or 2) use the pretrained models.

## Using Our Project
With further development (image asset download services) this model can be used to identify areas of concern in an entirely automated fashion.


## Contributors
codychampion Cody Champion


