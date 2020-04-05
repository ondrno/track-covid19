![Python application](https://github.com/ondrno/track-covid19/workflows/Python%20application/badge.svg?branch=master)

----

# track-covid19
python program to track the covid-19 infection rate in different countries.

This program collects Corona ``SARS-CoV-2`` infection statistics for DACH region (Germany, Austria, Switzerland), 
the United Kingdom, and the United States on a daily basis. It collects the overall numbers of confirmed infections, 
people recovered (Austria only), and deaths twice a day. 

- Austria's numbers are based on information from the  
[Sozialministerium](https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html).
- Germany's numbers are based on information from the [Robert-Koch-Institute](https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html).
- Switzerland's numbers are based on information from the [Bundesamt für Gesundheit BAG](https://www.bag.admin.ch/bag/de/home/krankheiten/ausbrueche-epidemien-pandemien/aktuelle-ausbrueche-epidemien/novel-cov/situation-schweiz-und-international.html)
- United Kingdom's numbers are based on information from [GOV.uk](https://www.arcgis.com/home/item.html?id=e5fd11150d274bebaaf8fe2a7a2bda11)
- United State's numbers are based on information from [Centers for Disease Control and Prevention](https://www.cdc.gov/coronavirus/2019-ncov/cases-in-us.html)
 

The aim of the program is to have a timeline how the SARS-CoV-2 virus spread in these countries.
  
## How to use
I have prepared a docker image for the ease of use. It provides a python/dash web application on port '8050' 
which shows the statistics found in the log file. The log file is continuously updated every 4 hours.

    docker-compose build
    docker-compose -d up
    
The log file ``cov19_statistics.log`` can be found in the ``log`` directory.
    
## Log file 
The log file is from version v2.0.0 onwards in json format. For every country it contains 
the number of cases ("c") and the number of deaths ("d") at a certain time ("date").

Further, it may contain further information about the number of cases and death of certain 
provinces of that country.  

Example:

    {"country": "DE", "c": 91714, "d": 1342, "provinces": {"BW": {"c": 18614, "d": 367}, "BY": {"c": 23846, "d": 396}, "BE": {"c": 3613, "d": 24}, "BB": {"c": 1305, "d": 17}, "HB": {"c": 394, "d": 6}, "HH": {"c": 2945, "d": 19}, "HE": {"c": 4575, "d": 56}, "MV": {"c": 523, "d": 5}, "NI": {"c": 5712, "d": 89}, "NW": {"c": 18735, "d": 245}, "RP": {"c": 3663, "d": 32}, "SL": {"c": 1358, "d": 14}, "SN": {"c": 2741, "d": 32}, "ST": {"c": 919, "d": 12}, "SH": {"c": 1631, "d": 18}, "TH": {"c": 1140, "d": 10}}, "date": "2020-04-06T00:13:00"}
    {"country": "AT", "provinces": {"BL": {"c": 226, "d": 3}, "K": {"c": 319, "d": 4}, "NO": {"c": 1903, "d": 31}, "OO": {"c": 1932, "d": 20}, "SB": {"c": 1069, "d": 14}, "ST": {"c": 1311, "d": 53}, "T": {"c": 2704, "d": 35}, "V": {"c": 742, "d": 4}, "W": {"c": 1701, "d": 40}}, "c": 11907, "d": 204, "date": "2020-04-06T00:13:00"}
    {"country": "CH", "c": 21100, "d": 559, "date": "2020-04-06T00:13:00"}
    {"country": "UK", "c": 47806, "d": 4934, "date": "2020-04-06T00:13:00"}
    {"country": "US", "c": 304826, "d": 7616, "date": "2020-04-06T00:13:00"}

### Austria
For Austria the total numbers and the ones from the provinces are tracked.
- BL - Burgenland
- K - Carinthia / Kärnten
- NO - Lower Austria / Niederösterreich
- OO - Upper Austria / Oberösterreich
- SB - Salzburg
- ST - Styria / Steiermark
- T - Tyrol / Tirol
- V - Vorarlberg
- W - Vienna / Wien

### Germany
For Germany the total numbers and the ones from the provinces are tracked, short names similar to 
[ISO 3166-2:DE](https://de.wikipedia.org/wiki/ISO_3166-2%3ADE) are used, i.e.

- BW - Baden-Würtemberg
- BY - Bavaria / Bayern
- BE - Berlin
- BB - Brandenburg
- HB - Bremen
- HH - Hamburg
- HE - Hessia / Hessen
- MV - Mecklenburg-Western Pomerania / Mecklenburg-Vorpommern
- NI - Lower Saxony / Niedersachsen
- NW - North Rhine-Westphalia / Nordrhein-Westfalen
- RP - Rhineland Palatinate / Rheinland-Pfalz
- SL - Saarland
- SN - Saxony / Sachsen
- ST - Sachsen-Anhalt
- SH - Schleswig-Holstein
- TH - Thuringia / Thüringen
 