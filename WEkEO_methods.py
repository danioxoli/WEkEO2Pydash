import base64
import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
import ipywidgets as widgets
from ipywidgets import Layout
from PIL import Image
import IPython
import xarray as xr
import rioxarray as rxr
from urllib.request import urlopen
from ipyleaflet import Map, basemaps, basemap_to_tiles, DrawControl, LayersControl

#---WIDGETS---

def get_dropdown(dataset_list, descr):
    """
    General function used to create a dropdown providing a list and a description for the widget.
    """
    dropdown = widgets.Dropdown(
    options=list(dataset_list),
    description=str(descr),
    disabled=False,
    style= {'description_width': '150px'},
    layout = {'width': '400px'})
    return dropdown

def text_widget(type_text):
    widgets.Password(
    placeholder='Type something',
    description=str(type_text),
    disabled=False,
    style= {'description_width': '150px'},
    layout = {'width': '400px'})
    return text

def password_widget(type_password):
    password = widgets.Password(
    placeholder='Type password',
    description=str(type_password),
    disabled=False,
    style= {'description_width': '150px'},
    layout = {'width': '400px'})
    return password

def select_multiple(data_list, descr):
    selections = widgets.SelectMultiple(
    options=data_list,
    description=str(descr),
    disabled=False,
    style= {'description_width': '150px'},
    layout = {'width': '400px'})
    return selections

def select_buttons(data_list, descr, default_value):
    format_type_sel = widgets.RadioButtons(
    options=data_list,
    value=str(default_value),
    description=str(descr),
    disabled=False,
    style= {'description_width': '150px'},
    layout = {'width': '400px'})
    return format_type_sel

def get_date_picker(date_descr):
    """
    Function to create a date picker, providing a description name.
    """
    date = widgets.DatePicker(
        description=str(date_descr),
        disabled=False,
        style= {'description_width': '150px'},
        layout = {'width': '400px'})
    return date
    
def get_headers(username, password):
    """
    Provide username and password to allow the login for WEkEO data access.
    """
    message = str(username.value+":"+password.value)
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    headers = {'authorization': 'Basic '+base64_message}
    token_request = requests.get("https://wekeo-broker-k8s.apps.mercator.dpi.wekeo.eu/databroker/gettoken", headers=headers)
    token_text = token_request.text
    token = json.loads(token_text)
    print("Your access token is: "+token['access_token'])
    headers = {'authorization': token['access_token']}
    return headers

def display_image(data_df, dataset_id, w, f, h):
    """
    Function to display image from link and get a dataset preview.
    data_df: dataframe containing all the datasets
    dataset_id: containing the ID of the dataset
    w: image width
    f: image format
    h: image height
    """
    abstract = data_df.loc[data_df['datasetId'] == dataset_id.value]
    img_url = list(abstract["previewImage"])[0]
    image = IPython.display.Image(img_url, width = w)
    image = widgets.Image(
    value=image.data,
    format=str(f), 
    width=w,
    height=h)
    return image

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


#------

def download_zip(get_url):
    url = get_url['content'][0]['url']
    save_as = get_url['content'][0]['filename']
    with urlopen(url) as file:
        content = file.read()
        with open(save_as, 'wb') as download:
            download.write(content.read())

def get_all_data_request(size):
    """
    Function to get all the information about the datasets available for WEkEO.
    size: corresponds to the number of dataset to be required
    """
    dataset = requests.get("https://wekeo-broker-k8s.apps.mercator.dpi.wekeo.eu/databroker/datasets?size="+str(size))
    dataset_text = dataset.text
    data = json.loads(dataset_text)
    data_df = json_normalize(data['content'])
    return data_df

def get_data_from_name_request(size, dataset_name):
    """
    Function to get information about a specific dataset, such as "cams" or "era5".
    size: corresponds to the number of dataset to be required.
    dataset_name: corresponds to the dataset that is required.
    """
    dataset = requests.get("https://wekeo-broker-k8s.apps.mercator.dpi.wekeo.eu/databroker/datasets?size="+str(size))
    dataset_text = dataset.text
    data = json.loads(dataset_text)
    data_df = json_normalize(data['content'])
    data_df = data_df[data_df['datasetId'].str.contains(str(dataset_name),  case=False)]
    return data_df

    
def get_description(data_df, dataset_id):
    """
    Function used to preview the required dataset, from a pandas dataframe.
    It returns the preview image of the dataset and its description.
    """
    abstract = data_df.loc[data_df['datasetId'] == dataset_id.value]
    description = list(abstract["abstract"])[0]
    return description

def get_metadata(dataset_id, headers):
    """
    Function used to get metadata in JSON format for the selected dataset.
    """
    dataset = requests.get("https://wekeo-broker-k8s.apps.mercator.dpi.wekeo.eu/databroker/querymetadata/"+dataset_id.value, headers=headers)
    dataset_text = dataset.text
    metadata = json.loads(dataset_text)
    return metadata

def request_data(jobId, token):
    """
    Function to request data, check the status and get data url for download.
    """
    headers = {'authorization': 'Basic '+str(token)}
    status_request = requests.get('https://wekeo-broker.apps.mercator.dpi.wekeo.eu/databroker/datarequest/status/'+jobId, headers=headers)
    status = status_request.text
    status_message = json.loads(status)['status']
    if status_message == "running":
        print("Download status: "+ status_message, end='\r')
    if status_message == "completed":     
        print("Download status: "+ status_message)
    if status_message == "failed":
        print("Download status: "+ status_message, end='\r')

    while status_message == "running":
        status_request = requests.get('https://wekeo-broker.apps.mercator.dpi.wekeo.eu/databroker/datarequest/status/'+jobId, headers=headers)
        status = status_request.text
        status_message = json.loads(status)['status']
        if status_message == "running":
            print("Download status: "+ status_message, end='\r')
        if status_message == "completed":     
            print("Download status: "+ status_message)
        if status_message == "failed":
            print("Download status: "+ status_message)
        
    get_url_request = requests.get('https://wekeo-broker.apps.mercator.dpi.wekeo.eu/databroker/datarequest/jobs/'+jobId+'/result', headers=headers)
    get_url = json.loads(get_url_request.text)
    url = get_url['content'][0]['url']
    print('The URL for download is: '+ get_url['content'][0]['url'])
    return get_url

def data_order(job_id, get_url, token):
    '''
    Function to order data. Not all the datasets requires this function to download the data.
    '''
    url = get_url['content'][0]['url']
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'authorization': 'Basic '+str(token)}
    query = {
        "jobId":str(job_id),
        "uri":str(url)}
    data = json.dumps(query)
    dataset_post_order = requests.post("https://wekeo-broker-k8s.apps.mercator.dpi.wekeo.eu/databroker/dataorder", headers=headers, data=data)
    dataset_post_order_text = dataset_post_order.text
    order_id = json.loads(dataset_post_order_text)['orderId']

    return order_id

def era5_single_levels_list(metadata):
    '''
    Function to obtain the list of variables available in ERA5 Single Level.
    '''
    category = metadata['parameters']['multiStringSelects'][0]['details']['groupedValueLabels']
    category_list = []
    params_list = []
    for item in category:
        category_list.append(item['valuesLabels'])

    for item in category_list:
        key_list = list(item.keys())
        params_list.append(key_list)

    flat_list = [item for sublist in params_list for item in sublist]
    return flat_list

def api_query_era5_single_levels(dataset_id, params_sel, year_sel, month_sel, day_sel, time_sel, product_type_sel, format_type_sel, token):
    """
    Function used to query the data for the ERA5 single levels dataset.
    """
    query = {
      "datasetId": dataset_id.value,
      "multiStringSelectValues": [
        {
          "name": "variable",
          "value": list(params_sel.value)
        },
        {
          "name": "year",
          "value": list(year_sel.value)
        },
        {
          "name": "month",
          "value": list(month_sel.value)
        },
        {
          "name": "day",
          "value": list(day_sel.value)
        },
        {
          "name": "time",
          "value":list(time_sel.value)
        },
        {
          "name": "product_type",
          "value": list(product_type_sel.value)
        }
      ],
      "stringChoiceValues": [
        {
          "name": "format",
          "value": format_type_sel.value
        }
      ]
    }

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'authorization': 'Basic '+str(token)
    }

    data = json.dumps(query)
    dataset_post = requests.post("https://wekeo-broker-k8s.apps.mercator.dpi.wekeo.eu/databroker/datarequest", headers=headers, data=data)
    dataset_post_text = dataset_post.text
    job_id = json.loads(dataset_post_text)
    print(dataset_post_text)
    return job_id

def api_query_cams_forecast(dataset_id, params_sel, product_type_sel, level_sel, type_sel, hour_sel, leadtime_sel, start_date_sel, end_date_sel, format_type_sel,W,N,E,S, token):
    '''
    Function to request data from CAMS Forecast dataset.
    '''
    query = {
      "datasetId": dataset_id.value,
      "boundingBoxValues": [
        {
          "name": "area",
          "bbox": [
            W,
            N,
            E,
            S
          ]
        }
      ],
      "dateRangeSelectValues": [
        {
          "name": "date",
          "start": start_date_sel.value.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
          "end": end_date_sel.value.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        }
      ],
      "multiStringSelectValues": [
        {
          "name": "variable",
          "value": list(params_sel.value)
        },
        {
          "name": "model",
          "value": list(product_type_sel.value)
        },
        {
          "name": "level",
          "value": list(level_sel.value)
        },
        {
          "name": "type",
          "value": list(type_sel.value)
        },
        {
          "name": "time",
          "value": list(hour_sel.value)
        },
        {
          "name": "leadtime_hour",
          "value": list(leadtime_sel.value)
        }
      ],
      "stringChoiceValues": [
        {
          "name": "format",
          "value": format_type_sel.value
        }
      ]
    }
      
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'authorization': 'Basic '+str(token)}

    data = json.dumps(query)
    dataset_post = requests.post("https://wekeo-broker-k8s.apps.mercator.dpi.wekeo.eu/databroker/datarequest", headers=headers, data=data)
    dataset_post_text = dataset_post.text
    job_id = json.loads(dataset_post_text)
    print(dataset_post_text)
    
    return job_id
            
def api_query_efas_historical(dataset_id, variable_sel, model_levels_sel, system_version_sel, year_sel, month_sel, day_sel, time_sel, soil_level_sel, formats, token):
    '''
    Function to request EFAS Historical data (CEMS) - Emergency
    '''
    query = {
      "datasetId": dataset_id.value,
      "multiStringSelectValues": [
        {
          "name": "variable",
          "value": list(variable_sel.value)
        },
        {
          "name": "soil_level",
          "value": list(soil_level_sel.value)
        },
        {
          "name": "hyear",
          "value": list(year_sel.value)
        },
        {
          "name": "hmonth",
          "value": list(month_sel.value)
        },
        {
          "name": "hday",
          "value": list(day_sel.value)
        },
        {
          "name": "time",
          "value": list(time_sel.value)
        }
      ],
      "stringChoiceValues": [
        {
          "name": "system_version",
          "value": system_version_sel.value
        },
        {
          "name": "format",
          "value": formats.value
        },
        {
          "name": "model_levels",
          "value": model_levels_sel.value
        }
      ]
    }
      
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'authorization': 'Basic '+str(token)}

    data = json.dumps(query)
    dataset_post = requests.post("https://wekeo-broker-k8s.apps.mercator.dpi.wekeo.eu/databroker/datarequest", headers=headers, data=data)
    dataset_post_text = dataset_post.text
    job_id = json.loads(dataset_post_text)
    print(dataset_post_text)
    
    return job_id

def api_query_sea_floor_temperature(dataset_id, start_date_sel, end_date_sel, W, S, E, N, token):
    '''
    Function to request data Sea Bottom Temperature (CMEMS) - Marine
    '''
    query = {
      "datasetId": dataset_id.value,
      "boundingBoxValues": [
        {
          "name": "bbox",
          "bbox": [W, S, E, N]
        }
      ],
      "dateRangeSelectValues": [
        {
          "name": "position",
          "start": start_date_sel.value.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
          "end": end_date_sel.value.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        }
      ],
      "multiStringSelectValues": [
        {
          "name": "variable",
          "value": [
            "bottomT"
          ]
        }
      ],
      "stringChoiceValues": [
        {
          "name": "service",
          "value": "NWSHELF_ANALYSISFORECAST_PHY_LR_004_001-TDS"
        },
        {
          "name": "product",
          "value": "cmems_mod_nws_phy-bottomt_anfc_7km-2D_P1D-m"
        }
      ]
    }
      
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'authorization': 'Basic '+str(token)}

    data = json.dumps(query)
    dataset_post = requests.post("https://wekeo-broker-k8s.apps.mercator.dpi.wekeo.eu/databroker/datarequest", headers=headers, data=data)
    dataset_post_text = dataset_post.text
    job_id = json.loads(dataset_post_text)
    print(dataset_post_text)
    
    return job_id

def api_query_corine(dataset_id, dataset_name, formats, token):
    '''
    Function to request data for Corine dataset (CLMS)
    '''
    query = {
      "datasetId": dataset_id.value,
      "stringChoiceValues": [
        {
          "name": "product_type",
          "value": dataset_name.value
        },
        {
          "name": "format",
          "value": formats.value
        }
      ]
    }
      
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'authorization': 'Basic '+str(token)}

    data = json.dumps(query)
    dataset_post = requests.post("https://wekeo-broker-k8s.apps.mercator.dpi.wekeo.eu/databroker/datarequest", headers=headers, data=data)
    dataset_post_text = dataset_post.text
    job_id = json.loads(dataset_post_text)
    print(dataset_post_text)
    
    return job_id