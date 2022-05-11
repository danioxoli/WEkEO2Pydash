import base64
import requests
import json
import pandas as pd
import ipywidgets as widgets
from ipywidgets import Layout
from PIL import Image
import IPython
import xarray as xr
from urllib.request import urlopen
from ipyleaflet import Map, basemaps, basemap_to_tiles, DrawControl, LayersControl

def get_dropdown(dataset_list, descr):
    """
    General function used to create a dropdown providing a list and a description for the widget.
    """
    dropdown = widgets.Dropdown(
    options=list(dataset_list),
    description=str(descr),
    disabled=False,
    style= {'description_width': 'initial'})
    return dropdown

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

def select_multiple(data_list, descr):
    selections = widgets.SelectMultiple(
    options=data_list,
    description=str(descr),
    disabled=False,
    style= {'description_width': 'initial'})
    return selections

def select_buttons(data_list, descr, default_value):
    format_type_sel = widgets.RadioButtons(
    options=data_list,
    value=str(default_value),
    description=str(descr),
    disabled=False,
    style= {'description_width': 'initial'})
    return format_type_sel

def get_date_picker(date_descr):
    """
    Function to create a date picker, providing a description name.
    """
    date = widgets.DatePicker(
        description=str(date_descr),
        disabled=False,
        style= {'description_width': 'initial'})
    return date
    
def get_token(username, password):
    """
    Provide username and password to allow the login for WEkEO data access.
    """
    message = str(username.value+":"+password.value)
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    print("Your credential is: "+base64_message)
    headers = {'authorization': 'Basic '+base64_message}
    token_request = requests.get("https://wekeo-broker-k8s.apps.mercator.dpi.wekeo.eu/databroker/gettoken", headers=headers)
    token_text = token_request.text
    token = json.loads(token_text)
    print("Your access token is: "+token['access_token'])
    headers = {'authorization': token['access_token']}
    return headers

def get_all_data_request(size):
    """
    Function to get all the information about the datasets available for WEkEO.
    size: corresponds to the number of dataset to be required
    """
    dataset = requests.get("https://wekeo-broker-k8s.apps.mercator.dpi.wekeo.eu/databroker/datasets?size="+str(size))
    dataset_text = dataset.text
    data = json.loads(dataset_text)
    data_df = pd.json_normalize(data['content'])
    return data_df

def get_data_from_name_request(size, dataset_name):
    """
    Function to get information about a specific dataset, such as "cams" or "era5".
    size: corresponds to the number of dataset to be required.
    dataset_name: corresponds to the dataset that is required. For example is possible to require "cams" or "era5" data.
    """
    dataset = requests.get("https://wekeo-broker-k8s.apps.mercator.dpi.wekeo.eu/databroker/datasets?size="+str(size))
    dataset_text = dataset.text
    data = json.loads(dataset_text)
    data_df = pd.json_normalize(data['content'])
    data_df = data_df[data_df['datasetId'].str.contains(str(dataset_name),  case=False)]
    return data_df

    
def get_description(data_df, dataset_id):
    """
    Function used to preview the required dataset, from a pandas dataframe.
    It returns the preview image of the dataset and its description.
    """
    abstract = data_df.loc[data_df['datasetId'] == dataset_id.value]
    description = list(abstract["abstract"])
    return description

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

def get_metadata(dataset_id, headers):
    """
    Function used to get metadata in JSON format for the selected dataset.
    """
    dataset = requests.get("https://wekeo-broker-k8s.apps.mercator.dpi.wekeo.eu/databroker/querymetadata/"+dataset_id.value, headers=headers)
    dataset_text = dataset.text
    metadata = json.loads(dataset_text)
    return metadata

def era5_single_levels_list(metadata):
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

def request_data(jobId, token):
    """
    Function to request data, check the status and get the url.
    """
    headers = {'authorization': 'Basic '+str(token)}
    status_request = requests.get('https://wekeo-broker.apps.mercator.dpi.wekeo.eu/databroker/datarequest/status/'+jobId, headers=headers)
    status = status_request.text
    status_message = json.loads(status)['status']
    if status_message == "running":
        print("Download status: "+ status_message +"...")
    if status_message == "completed":     
        print("Download status: "+ status_message +"  \u2713")

    while status_message == "running":
        status_request = requests.get('https://wekeo-broker.apps.mercator.dpi.wekeo.eu/databroker/datarequest/status/'+jobId, headers=headers)
        status = status_request.text
        status_message = json.loads(status)['status']
        if status_message == "running":
            print("Download status: "+ status_message +"...", end='\r')
        if status_message == "completed":     
            print("Download status: "+ status_message +"  \u2713")
        if status_message == "failed":
            print("Download"+ status_message)
        
    get_url_request = requests.get('https://wekeo-broker.apps.mercator.dpi.wekeo.eu/databroker/datarequest/jobs/'+jobId+'/result', headers=headers)
    get_url = json.loads(get_url_request.text)
    url = get_url['content'][0]['url']
    print('The URL for download is: '+ get_url['content'][0]['url'])
    return get_url

def download_type(download_sel, download_list, get_url):
    """
    Function that can read the NetCDF file in memory or downloading it if a name is provided.
    """
    url = get_url['content'][0]['url']
    save_as = get_url['content'][0]['filename']
    
    if download_sel.value == download_list[1]: 
        fl = url
        # load into memory 
        with urlopen(fl) as f:
            ds = xr.open_dataset(f.read())
    elif download_sel.value == download_list[0]:
        with urlopen(url) as file:
            content = file.read()
            with open(save_as, 'wb') as download:
                download.write(content)
            ds = xr.open_dataset(str(save_as))
    return ds

def draw_map():
    """
    Function to draw a map and interact with it. It is possible to get the coordinates values from the dc variable. Two basemaps are available.
    """
    satellite = basemap_to_tiles(basemaps.Gaode.Satellite)
    osm = basemap_to_tiles(basemaps.OpenStreetMap.Mapnik)

    cams_map = Map(layers=(satellite, osm ), center=(45, 10), zoom=4)

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


def api_query_cams_forecast(dataset_id, params_sel, product_type_sel, level_sel, type_sel, hour_sel, leadtime_sel, start_date_sel, end_date_sel, format_type_sel,W,N,E,S, token):
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