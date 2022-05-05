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
git clone https://github.com/graph-generator.git
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

To create graphs from dialogue_data.json:

```bash
python3 app.py dialogue_data.json
```

To include cdus in the graphs:

```bash
python3 app.py dialogue_data.json --add_cdu
```

To visuzalize attachments only:

```bash
python3 app.py dialogue_data.json --monochrome
```

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

-The turn_no field in "edus" will be automatically generated 

-If CDUs are not used then the "cdus" field isn't necessary
(Otherwise ```--add_cdu ``` flag is necessary.)

-If relation types aren't needed (i.e. only 1/0 attachments will be visualized), 
 then the "type" field in "relations" isn't necessary
(Specify with ```--monochrome ``` argument.)


## Coming soon

WIP: update function for graphs
