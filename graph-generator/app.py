import os
import json
import argparse
import shutil
from create_graphs import write_svgs, write_html
from utilities import add_turns

# --------------------------
# args
# --------------------------

arg_parser = argparse.ArgumentParser(description='generate discourse graphs')
arg_parser.add_argument('json_file_name', metavar='CORPFILE', help='name of json file in current directory')
arg_parser.add_argument("--update", default=False, action='store_true', help='keep current graphs') 
arg_parser.add_argument("--add_cdu", default=False, action='store_true', help='include cdus in visualizations')
arg_parser.add_argument("--monochrome", default=False, action='store_true', help='visualize attachments only')

args = arg_parser.parse_args()

current_dir = os.getcwd()

##try to open json file and check turns 

json_path = current_dir + '/' + args.json_file_name

try:
    with open(json_path, encoding='utf-8') as f: 
        obj = f.read()
        data = json.loads(obj)
except IOError:
    print('cannot open json file ' + json_path)

try:
    add_turns(data)
except ValueError:
    print('cannot update json turn_no field')

##create directories 

output_path = current_dir + '/graph_output'
svg_path = output_path + '/svgs'
num_dirs = None
title = data['data_id']

if args.update:
    #find "graph_output" in current directory 
    #count how many folders starting with svg there are and add one
    num_dirs = len([d for d in os.listdir(output_path) if d.__contains__('svgs')])
    svg_path = output_path + '/svgs_' + str(num_dirs)
    os.makedirs(svg_path)
else:
    #erase current output directory 
    if os.path.exists(output_path):
        shutil.rmtree(output_path)

    #make a new graph_output directory containing a new svg directory
    os.makedirs(output_path)
    os.makedirs(svg_path)

write_svgs(data, svg_path, args.add_cdu, args.monochrome)

write_html(svg_path, output_path, title, num_dirs)