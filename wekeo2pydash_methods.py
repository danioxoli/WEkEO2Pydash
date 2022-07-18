import xarray as xr
import rioxarray as rxr
from urllib.request import urlopen
from ipyleaflet import Map, basemaps, basemap_to_tiles, DrawControl, LayersControl  #if error run: jupyter labextension install @jupyter-widgets/jupyterlab-manager jupyter-leaflet


def download_type(download_sel, download_list, get_url):
    """
    Function to read a NetCDF file in memory or download it using its original filename.
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
    Function to draw an ipyleaflet map and interact with it. It is possible to get the coordinates values from the dc variable. Two basemaps are available.
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
