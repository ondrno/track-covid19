![Python application](https://github.com/ondrno/track-covid19/workflows/Python%20application/badge.svg?branch=master)

----

# covid19
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
I have prepared a docker image for the ease of use. It writes the log file directly into the local ``log`` 
directory. 

    docker-compose build
    docker-compose -d up
    
The log file ``cov19_statistics.log`` can be found in the ``log`` directory.
    
## Log file format
    ts;country;cases;deaths;recovered
    2020-03-21T14:49:00;DE;16662;46
    2020-03-21T14:49:00;AT;2664;7;9
    2020-03-21T14:49:00;CH;6113;56
    2020-03-21T14:49:00;UK;3983;177
    2020-03-21T14:49:00;US;15219;201
