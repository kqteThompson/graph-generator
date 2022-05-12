# Dialogue Graph Generator

![Python Version](https://img.shields.io/badge/python-3.9-blue)

A CLI for generating discourse graphs from json data using the pydot/graphviz libraries.

## Contents
* [Getting started](#start)
* [CLI](#cli)
* [Data format](#json)
* [Coming soon](#features)

## Getting started

```bash
git clone https://github.com/kateThompson/graph-generator.git
cd graph-generator
```
Make sure the pydot library is installed. 
(NB you may have to install Graphviz separately.)

```bash
pip3 install -r requirements.txt
```

Move .json data file to graph-generator directory.
The graph_output directory and the svgs directory will be created in the graph-generator directory.

## CLI

```bash
python3 app.py dialogue_data.json [--update][--add_cdu][--monochrome]
```

Breakdown:

```bash
python3 app.py dialogue_data.json
```
Creates graph svgs from dialogue_data.json in ```graph-generator/svgs``` directory, 
then organizes in html files. Open ```graph-generator/index.html``` to view graphs by dialogue id. 

NB: dialogue_data.json should be in ```graph-generator/``` directory.

```bash
python3 app.py dialogue_data.json --update
```
When ```---update``` is not included, the existing ```graph-generator/svgs``` directory will be deleted
and recreated with the graphs from the new json. 

When ```---update``` is included, the existing ```graph-generator/svgs``` directory will be preserved, 
and the new graphs will be generated in a separate svg folder ```graph-generator/svgs_1```. 

New dialogues will be shown adjacent to old ones in the html.

NB: in order to create the comparison graphs the graph_generator uses the dialogue_id fields, so the dialogue_ids must be the same across all iterations of the data. 


```bash
python3 app.py dialogue_data.json --add_cdu
```
Includes CDUs in graphs if dialogue_data.json includes CDU information.

NB: If dialogue_data.json contains relations connecting CDUs and ```--add_cdu``` is not called, then
there will be an error while generating the graphs.

```bash
python3 app.py dialogue_data.json --monochrome
```
Visualizes attachments only, i.e. uses one relation color and does not include attachment types.


## Data format

The following fields are required in the json file input:

```bash
   {
        "data_id": "STAC",
        "dialogues": [
            {
                "dialogue_id":"pilot01_1",
                "edus": [
                    {
                        "seg_id": "pilot01_01_stac_1340734901",
                        "turn_id": 1.0,
                        "turn_no": 0,
                        "speaker": "Tomm",
                        "text": "ello",
                        "span_end": 16.0   
                    },
                ],
                "cdus": [
                    {
                        "cdu_id": "pilot01_01_nasher_1374067270589",
                        "members": [
                            "pilot01_01_stac_1340784903",
                            "pilot01_01_stac_1340784902"
                        ]
                    },
                ], 
                "relations":[
                    {
                        "rel_id": "pilot01_01_sleva_1340913596043",
                        "source": "pilot01_01_stac_1340734901",
                        "target": "pilot01_01_stac_1340744901",
                        "type": "Continuation"
                    },
                ]
            }, 
        ]
    }

```

Note:

-The "turn_no" field in "edus" will be automatically generated.

-If CDUs are not used then the "cdus" field isn't necessary.
(Otherwise ```--add_cdu ``` flag is necessary.)

-If relation types aren't needed (i.e. only 1/0 attachments will be visualized), 
 then the "type" field in "relations" isn't necessary.
(Specify with ```--monochrome ``` argument.)


## Coming soon

WIP: find solution to edus out of order in turns in graphs

WIP: dockerization

WIP: graphing AMI data

WIP: specifying subsets of relation types and colors
