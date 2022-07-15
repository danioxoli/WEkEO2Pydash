# WEkEO2Pydash - Explore Copernicus data interactively using the WEkEO HDA API
### WEkEO Jupyter Notebook competition: https://notebook.wekeo.eu

This Notebook showcases Python recipes to interact (access, browse, display and download) with the Copernicus data dispatched by the [<span style='color:Blue'>WEkEO DIAS</span>](https://www.wekeo.eu), through the development of flexible and interactive dashboards into a Jupyter notebook. 

**Interactivity** is here used as the key element to speed-up applications development by minimizing code editing for recursive steps such as variables definition and parameters setting.

The final goal is to provide the user with reusable code blocks which can be adapted *- with a small effort -* to manifold EO applications by leveraging the [<span style='color:Blue'>WEkEO Harmonised Data Access (HDA) API </span>](https://www.wekeo.eu/docs/harmonised-data-access-api) as exclusive data endpoint. 

### Resources

This Notebook make extensive use of the [<span style='color:Blue'> WEkEO HDA API</span>](https://www.wekeo.eu/docs/harmonised-data-access-api) to perform `GET` and `POST` requests[<sup>1</sup>](#1), necessary for automating the data access procedures.

Interactivity is enabled by cutting-edge Python libraries for dynamic widgets and maps generation including [<span style='color:Blue'>IPython</span>](https://ipython.org), [<span style='color:Blue'>itables</span>](https://mwouts.github.io/itables/advanced_parameters.html), [<span style='color:Blue'>IPyWidgets</span>](https://ipywidgets.readthedocs.io/en/latest/index.html#) and [<span style='color:Blue'>ipyleaflet</span>](https://ipyleaflet.readthedocs.io); alongside popular data mananging and analysis libraries such as [<span style='color:Blue'>Pandas</span>](https://pandas.pydata.org) and [<span style='color:Blue'>xarray</span>](https://docs.xarray.dev). All the selected libraries are released under open-license[<sup>2</sup>](#2) compatible with [<span style='color:Blue'>MIT license</span>](https://en.wikipedia.org/wiki/MIT_License). 


The pattern proposed by this Notebook is developed and demonstrated through few examples, adapted to different data products[<sup>3</sup>](#3) provided by the WEkEO DIAS. Specifically, the data products considered in this Notebook are reported in the following table.

| Product Description | Product Link | ID | Metadata |
|:--------------------:|:-----------------------:|:-----------------:|:-----------------:|
|ERA5 - Single Levels| <a href="https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=overview" target="_blank">link</a> | EO:ECMWF:DAT:REANALYSIS_ERA5_SINGLE_LEVELS | <a href="https://www.wekeo.eu/data?view=dataset&dataset=EO%3AECMWF%3ADAT%3AERA5_HOURLY_VARIABLES_ON_PRESSURE_LEVELS" target="_blank">link</a> |
|CAMS - European Air Quality Forecasts|<a href="https://atmosphere.copernicus.eu/" target="_blank">link</a>|EO:ECMWF:DAT:CAMS_EUROPE_AIR_QUALITY_FORECASTS|<a href="https://www.wekeo.eu/data?view=dataset&dataset=EO%3AECMWF%3ADAT%3ACAMS_EUROPE_AIR_QUALITY_FORECASTS" target="_blank">link</a>|
|CMEMS - Atlantic- European North West Shelf- Ocean Physics Reanalysis|<a href="https://resources.marine.copernicus.eu/product-detail/NWSHELF_MULTIYEAR_PHY_004_009/INFORMATION" target="_blank">link</a>|EO:MO:DAT:NWSHELF_ANALYSISFORECAST_PHY_LR_004_001:cmems_mod_nws_phy-bottomt_anfc_7km-2D_P1D-m|<a href="https://www.wekeo.eu/data?view=dataset&dataset=EO%3AMO%3ADAT%3ANWSHELF_ANALYSISFORECAST_PHY_LR_004_001" target="_blank">link</a>|
|Sentinel-5P|<a href="https://sentinels.copernicus.eu/web/sentinel/missions/sentinel-5p" target="_blank">link</a>|'EO:ESA:DAT:SENTINEL-5P:TROPOMI'|<a href="https://www.wekeo.eu/data?view=dataset&dataset=EO%3AESA%3ADAT%3ASENTINEL-5P%3ATROPOMI" target="_blank">link</a>|


Settings to adapt the Notebook functions and dynamic widgets to the different data products are explained throughout the Notebook sections.


### Learning outcomes

At the end of this Notebook you will know:
* How to programmatically access Copernicus data and metadata using the [<span style='color:Blue'>WEkEO HDA API</span>](https://www.wekeo.eu/docs/harmonised-data-access-api) in Python
* How to generate dynamic data previews using interactive Python widgets
* How to adapt and reuse Python functions and code blocks to deal with different WEkEO data products and applications


<span id="1">[$^1$Swagger UI](https://wekeo-broker.apps.mercator.dpi.wekeo.eu/databroker/ui/#!/HDA_-_dataorder/dataorder_get)</span> 

<span id="2">[$^2$About Open Source Licenses](https://opensource.org/licenses)</span> 

<span id="3">[$^3$WEkEO Data Discovery Platform](https://www.wekeo.eu/data)</span> 

<div class="alert alert-info">
<strong>Authors:</strong> Oxoli Daniele (_daniele.oxoli@polimi.it_), Capizzi Emanuele (_emanuele.capizzi@polimi.it_) - 2022 - Politecnico di Milano <br>
</div>
