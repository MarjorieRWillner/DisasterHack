# DisasterHackathon

The Forest Service (FS) performs an annual survey insect and disease and detection survey (IDS). The open source 2020 IDS survey was used as training data for our computer vision (CV) model. The 2020 IDS Summary Map is shown, below. Specifically, a well annotated area on the California-Nevada board encompassing El Dorado and Humboldt-Toiyabe National Forests was used for training. The corresponding 30m Landsat imagery was downloaded from the United States Geological Survey at multiple timepoints. 

For each landsat geotiff, 80% of the image was used for training and the other 20% was used for testing.  Once timeseries features were extracted with HRNet a logistic regression was used to classify each pixel and hazard maps were created. 

Please note that inorder to run please download imagery tiles from USGS and arrange in the direcory structure indicated.  Note due to the feature extraction step that a specific sampling frequency is not needed and that any resolution of imagery can be used.
