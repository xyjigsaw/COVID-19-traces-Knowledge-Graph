# COVID-19-Knowledge-Graph
The project of Covid-19(2019-nCoV) patient-tracking data from Tencent news is based on Scrapy, PhantomJS and HanLP.
HanLP is used to recognize entity(Location, Time, Action etc.) and extract events.

## Features
- Structured Traces Data
- Event Extraction
- LDA Model Based Topic Classification [More details](https://www.omegaxyz.com/2020/02/24/lda-topic/)
- Knowledge Graph Triples(Patient, Time, Location, Traces...)

# TABLES
- event：e_id, time, text
- patient：e_id, name, age, gender
- location：l_id, location
- topic：t_id, topic
- event-location：id, e_id, l_id
- event-topic:id, e_id, t_id
- patient-event：id, p_id, e_id
- patient-location：id, p_id, l_id


## Preview of the data

More than 4000 cases

![](https://github.com/xyjigsaw/COVID-19-nCoV-traces-data/blob/master/DEMO.png)


## KG Visualization

Please visit another [repository](https://github.com/xyjigsaw/Knowledge-Graph-And-Visualization-Demo)
![](https://github.com/xyjigsaw/COVID-19-nCoV-traces-data/blob/master/KG-Search3.png)

![](https://github.com/xyjigsaw/COVID-19-nCoV-traces-data/blob/master/KG-3D-2.png)

[Demo@Acemap](http://ncp.acemap.info/kg)

Find more on [NCP@Acemap](http://ncp.acemap.info/#tab=map).
