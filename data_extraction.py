import geopandas as gpd
import numpy
import pandas
import rasterio
from rasterio.mask import mask
import glob
import pyproj
from pyproj import Transformer
from shapely.ops import transform as sh_transform

#read layer of target date, https://www.fs.fed.us/foresthealth/applied-sciences/mapping-reporting/detection-surveys.shtml
data = gpd.read_file('CONUS_Region5_2020.gdb', layer=0)
import shapely.geometry
#download and save bands to local: https://earthexplorer.usgs.gov/
#should pivot to using stac catalog in .tar to ensure sorting is correct
#You should grab B1-B7.tiffs
bbox = [-120.278183, 38.520773, -119.943787, 38.764927]
bbox_poly = shapely.geometry.box(*bbox, ccw=True)


files = glob.glob('image_bands/*')

for i in range(0, len(files), 1):
    file_bands = glob.glob(f'{files[i]}\*')
    file_bands = sorted(file_bands, reverse=False)


    #reproject bbox to image coords

    #read first image again and make a mask with annotations
    with rasterio.open(file_bands[0]) as geo_fp:
        coord_transformer = Transformer.from_crs("epsg:4326", geo_fp.crs)
        profile = geo_fp.profile.copy()

        project = pyproj.Transformer.from_crs(4326, geo_fp.crs, always_xy=True).transform
        bbox_poly_project = sh_transform(project, bbox_poly)
        coord_upper_left = coord_transformer.transform(bbox[3], bbox[0])
        coord_lower_right = coord_transformer.transform(bbox[1], bbox[2])
        pixel_upper_left = geo_fp.index(coord_upper_left[0], coord_upper_left[1])
        pixel_lower_right = geo_fp.index(coord_lower_right[0], coord_lower_right[1])
        out, _ = rasterio.mask.mask(geo_fp, [bbox_poly_project], crop=True, invert=False)
        height, width = out[0].shape
        profile["width"] = width
        profile["height"] = height
        transform = profile["transform"]
        new_transform = rasterio.Affine(
            transform[0],
            transform[1],
            coord_upper_left[0],
            transform[3],
            transform[4],
            coord_upper_left[1],
        )
        profile["transform"] = new_transform
        # update metadata and make a stacked image
    profile.update(count=len(file_bands))
    with rasterio.open(f'processed/stack_bbox_{i}.tif', "w", **profile) as dst:
        for id_band, link in enumerate(file_bands, start=1):
            with rasterio.open(link) as geo_fp_sub:
                out, _ = rasterio.mask.mask(geo_fp_sub, [bbox_poly_project], crop=True, invert=False)
                dst.write_band(id_band, out[0])



#data chipping
files = glob.glob('processed/*')
profile.update(count=len(file_bands)*len(files))
with rasterio.open('processed_full/stack_bbox_stacked.tif', "w", **profile) as dst:
    for id_band, link in enumerate(files, start=1):
        with rasterio.open(link) as geo_fp_sub:
            subset = geo_fp_sub.read(1)
            dst.write_band(id_band, subset)



data = data.to_crs(profile.data['crs'])

df_out = pandas.DataFrame()
for i in range(0, len(data), 1):
    #read first image again and make a mask with annotations
    try:
        with rasterio.open('processed_full/stack_bbox_stacked.tif') as geo_fp:
            out,_ = rasterio.mask.mask(geo_fp, data['geometry'].iloc[i], crop= True, invert=False)
            data_flat = out.reshape(-1)
            df = pandas.DataFrame({"size_0": out.shape[0],
                                   "size_1": out.shape[1],
                                   "size_2": out.shape[2],
                                   "class_pixel": data['PERCENT_AFFECTED'].iloc[i],
                                   "data_flat": [data_flat]})

        df_out = pandas.concat([df_out, df], axis=0, ignore_index=True)
        print('site found')

    except:
        print('next')

df_out['data_flat_list'] = df_out['data_flat'].map(lambda x: ','.join(map(str, x)))

df_out.to_csv('data_v1.csv')
#############################################################################

import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import pickle
import cv2
from PIL import Image
import timm
from timm.data import resolve_data_config
from timm.data.transforms_factory import create_transform


model = timm.create_model('hrnet_w64', pretrained=True)
model.classifier = nn.Sequential(*list(model.classifier.children())[:-1])
model.eval()
config = resolve_data_config({}, model=model)
transform = create_transform(**config)

df_final_imagenet = pd.DataFrame()
for i in range(0, len(df_out), 1):
    data = df_out.iloc[i].data_flat.reshape((df_out.iloc[i].size_0,
                                      df_out.iloc[i].size_1,
                                      df_out.iloc[i].size_2))
    for ii in range(0, data.shape[1], 1):
        for iii in range(0, data.shape[2], 1):
            pixel = data[:, ii, iii]
            if numpy.all(pixel == 0) == False:
                pixel = pixel.reshape(8, int(pixel.shape[0]/8))
                pixel_out = np.zeros((3, pixel.shape[0] ,pixel.shape[1]))
                pixel_out[0,:,:] = pixel/3
                pixel_out[1,:,:] = pixel/3
                pixel_out[2,:,:] = pixel/3
                norm_image = cv2.normalize(pixel_out, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
                norm_image = norm_image.astype(np.uint8)
                PIL_image = Image.fromarray(norm_image.T, 'RGB')
                tensor = transform(PIL_image).unsqueeze(0)  # transform and add batch dimension
                with torch.no_grad():
                    out = model(tensor)
                results = out.detach().numpy()
                df = pd.DataFrame(results)
                data_flat = pixel.reshape(-1)
                df['data_flat'] = [df_out.iloc[i].data_flat]
                df['class_pixel'] = df_out.iloc[i].class_pixel
                df['pixel_0'] = ii
                df['pixel_1'] = iii
                df_final_imagenet = pd.concat([df_final_imagenet, df], ignore_index=True, sort=False)


df_final_imagenet['data_flat'] = df_final_imagenet['data_flat'].map(lambda x: ','.join(map(str, x)))
df_final_imagenet.to_csv('data_v1_imagenet.csv')






