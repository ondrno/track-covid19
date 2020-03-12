# covid19
python program to track the covid-19 infection rate in Germany and Austria.

This program collects Corona ``SARS-CoV-2`` infection statistics for Germany and Austria on a daily basis.
It collects the overall numbers of confirmed infections, people recovered (Austria only), and 
deaths twice a day. 

- The Austria numbers are based on information from the  
[Sozialministerium](https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html).
- The German numbers are based on information from the [Robert-Koch-Institute](https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html).

The aim of the program is to have a timeline how the SARS-CoV-2 virus spread in the two countries.
  
## How to use
I have prepared a docker image for the ease of use. It writes the log file directly into the local ``log`` 
directory. 

    docker-compose build
    docker-compose -d up
    
The log file ``cov19_statistics.log`` can be found in the ``log`` directory.
 
    
## Log file format

    year;month;day;hour;minute;DE;cases;dead;AT;cases;recovered;dead
    2020;3;12;20;49;DE;2369;5;AT;361;4;1
