import pandas as pd
import numpy as np
import ipywidgets as widgets
import xarray as xr
import rioxarray as rxr
from urllib.request import urlopen
from ipyleaflet import Map, basemaps, basemap_to_tiles, DrawControl, LayersControl

# Create widgets
def text_widget(type_text):
    text = widgets.Text(
    placeholder='Type something',
    description=str(type_text),
    disabled=False,
    style= {'description_width': 'initial'})
    return text

def password_widget(type_password):
    password = widgets.Password(
    placeholder='Type password',
    description=str(type_password),
    disabled=False,
    style= {'description_width': 'initial'})
    return password

def get_dropdown(dataset_list, descr):
    dropdown = widgets.Dropdown(
    options=list(dataset_list),
    description=str(descr),
    disabled=False,
    style= {'description_width': 'initial'})
    return dropdown

def select_multiple(data_list, descr):
    selections = widgets.SelectMultiple(
    options=data_list,
    description=str(descr),
    disabled=False,
    style= {'description_width': 'initial'})
    return selections

def select_buttons(data_list, descr, default_value):
    button_selection = widgets.RadioButtons(
    options=data_list,
    value=str(default_value),
    description=str(descr),
    disabled=False,
    style= {'description_width': 'initial'})
    return button_selection

def get_date_picker(date_descr):
    """
    Function to create a date picker, providing a description name.
    """
    date = widgets.DatePicker(
        description=str(date_descr),
        disabled=False,
        style= {'description_width': 'initial'})
    return date

def download_type(download_sel, download_list, get_url):
    """
    Function that can read the NetCDF file in memory or downloading it if a name is provided.
    """
    url = get_url['content'][0]['url']
    save_as = get_url['content'][0]['filename']
    
    if download_sel.value == "Read NETCDF in memory": 
        fl = url
        # load into memory 
        with urlopen(fl) as f:
            ds = xr.open_dataset(f.read())
    elif download_sel.value == "Download NETCDF":
        with urlopen(url) as file:
            content = file.read()
            with open(save_as, 'wb') as download:
                download.write(content)
            ds = xr.open_dataset(str(save_as))
    return ds

def draw_map(center_lat, center_lon, zoom_level):
    """
    Function to draw a map and interact with it. It is possible to get the coordinates values from the dc variable. Two basemaps are available.
    """
    satellite = basemap_to_tiles(basemaps.Gaode.Satellite)
    osm = basemap_to_tiles(basemaps.OpenStreetMap.Mapnik)

    cams_map = Map(layers=(satellite, osm ), center=(center_lat, center_lon), zoom=zoom_level)

    dc = DrawControl()
    lc = LayersControl(position='topright')

    dc = DrawControl(
        marker={"shapeOptions": {"color": "#0000FF"}},
        rectangle={"shapeOptions": {"color": "#0000FF"}},
        circle={"shapeOptions": {"color": "#0000FF"}},
        circlemarker={},
    )

    def handle_draw(target, action, geo_json):
        print(action)
        print(geo_json)


    dc.on_draw(handle_draw)
    cams_map.add_control(dc)
    cams_map.add_control(lc)
    
    return cams_map, dc
