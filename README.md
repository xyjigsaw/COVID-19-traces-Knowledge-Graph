# COVID-19-Knowledge-Graph
The project of Covid-19(2019-nCoV) patient-tracking data from Tencent news is based on Scrapy, PhantomJS and HanLP.
HanLP is used to recognize entity(Location, Time, Action etc.) and extract events.

## Features
- Structured Traces Data
- Event Extraction
- LDA Model Based Topic Classification
- Knowledge Graph Triples(Patient, Time, Location, Traces...)

# KG TABLE
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

Find more on [OmegaXYZ](https://www.omegaxyz.com).
