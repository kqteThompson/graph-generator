import pydot
import re
import os
from collections import Counter, defaultdict

GLOZZ_COLORS = {'Acknowledgement': '#12FFFF',
              'Alternation': '#10495E',
              'Background': '#FF8200',
              'Clarification_question': '#FF40D1',
              'Contrast':'#FF7ECF',
              'Correction':'#FF174E',
              'Comment': '#FF8200',
              'Conditional': '#1C931A',
              'Continuation': '#10491B',
              'Elaboration': '#A621C7',
              'Explanation': '#A62139',
              'Narration': '#1C931A',
              'Parallel': '#0AB046',
              'Q_Elab':'#0D20FF',
              'Question_answer_pair': '#12FFFF',
              'Result': '#10FF0F',
              'Sequence': '#0D20FF', 
              'attach': '#0D20FF'}

def get_max_turns(edu_list):
    """
    takes edu field of dialogue object
    returns the max number of edus in a given turn 
    in that dialogue
    """
    nums = [edu['turn_no'] for edu in edu_list]
    max_edus = max(Counter(nums).values())
    return max_edus

def get_turns(edu_list):
    """
    takes edu field of dialogue object and returns
    a turn dict that can be used to create subgraphs
    for each turn
    {
        turn_no : [(span_end, speaker, text) ]
    }
    """
    turns_dict = defaultdict(list)
    for edu in edu_list:
        turns_dict[edu['turn_no']].append((edu['span_end'], edu['speaker'], edu['text'], edu['seg_id']))
    return turns_dict

def create_dot_object(dialogue_info, dialogue_path, add_cdu, mono):
    """
    :param dialogue info: {dialogue_id, edus (list), relations (list), cdus (list)} for one dialogue
    :param dialogue path: path to save .svg and .dot files
    :return: a folder of .svg and .dot graphical representations of dialogues

    NB: in this version, edus in the same turn are put on the same line
    and CDUs are visualized
    """

    dot_object = pydot.Dot(graph_name=dialogue_info['dialogue_id'], rankdir="TB", ranksep=0.25)
    dot_object.set_node_defaults(shape='circle', fixedsize='true', style='filled', height=.1, width=.1, fontsize=10)
    dot_object.set_edge_defaults(style='solid', arrowsize=0.5, color='grey', splines='line')

    cluster_main = pydot.Cluster(dialogue_info['dialogue_id'], label= dialogue_info['dialogue_id'], labeljust='l')

    max_turns = get_max_turns(dialogue_info['edus'])
    
    turns = get_turns(dialogue_info['edus'])

    verticals = []

    for turn in turns:
    
        S = pydot.Subgraph(rank='same')

        turn_list = turns[turn]
        turn_list.sort(key=lambda tup: tup[0])
        #arrange edus in order of span_end

        blanks = max_turns - len(turn_list) #calculate number of invisible edus to add 
        verticals.append(turn_list[0][3]) #add edu id of first edu of each turn
        
        last_seg = None
        for edu in turn_list:
            text = str(turn) + '  ' + edu[1] + '  ' + edu[2]
            seg_name = edu[3] #the name of each edu is the seg id
            node_eta = pydot.Node(name=seg_name, label='', fillcolor='black', tooltip=text)
            
            S.add_node(node_eta)

            if last_seg:
                dot_object.add_edge(pydot.Edge(last_seg, seg_name, style='invis'))
            last_seg = seg_name

        if blanks > 0:
            for b in range(blanks):
                blank_name = name=str(turn) + '_' + str(b)
                node_blank = pydot.Node(blank_name, label='', style='invis')
                S.add_node(node_blank)
                dot_object.add_edge(pydot.Edge(last_seg, blank_name, style='invis'))

        cluster_main.add_subgraph(S)

    dot_object.add_subgraph(cluster_main)

    # add invis vertical relations between first segment of each turn
    #!! would the graph structure be better if we put vertical relations between all segements??
    k = 0
    while k < len(verticals) - 1:
        dot_object.add_edge(pydot.Edge(verticals[k], verticals[k + 1], style='invis'))
        k += 1

    #add cdus if any
    if add_cdu:
        cdus = dialogue_info['cdus']
        if len(cdus) > 0:
            C = pydot.Subgraph()
            # go through CDUs once to add nodes
            for cdu in cdus:
                #print("cdu", cdu)
                node_cdu = pydot.Node(name=cdu['cdu_id'], label='', fillcolor='red', tooltip=cdu['cdu_id'])
                C.add_node(node_cdu)
        
            # go through CDUs a second time to connect all component nodes
            # (must do this in a separate pass incase CDUs are children nodes)
            for cdu in cdus:
                for member in cdu['members']:
                    dot_object.add_edge(pydot.Edge(member, cdu['cdu_id'], color='grey', style='dashed', dir='none'))

            dot_object.add_subgraph(C)

    #add all relations
    if mono:
        for rel in dialogue_info['relations']:
            rel_id = str(rel['source'])  + '_' + str(rel['target'])
            rel_text = re.sub('-', '', 'attach')

            if dot_object.get_edge(rel['source'], rel['target']):
                dot_object.del_edge(rel['source'], rel['target'])
                dot_object.add_edge(pydot.Edge(rel['source'], rel['target'], color=GLOZZ_COLORS['attach'], tooltip=rel_text, rel_id=rel_id))

            else:
                dot_object.add_edge(pydot.Edge(rel['source'], rel['target'], color=GLOZZ_COLORS['attach'], tooltip=rel_text, rel_id=rel_id))
    else:
        for rel in dialogue_info['relations']:

            rel_id = str(rel['source'])  + '_' + str(rel['target'])
            rel_text = re.sub('-', '', rel['type'])

            if dot_object.get_edge(rel['source'], rel['target']):
                dot_object.del_edge(rel['source'], rel['target'])
                dot_object.add_edge(pydot.Edge(rel['source'], rel['target'], color=GLOZZ_COLORS[rel['type']], tooltip=rel_text, rel_id=rel_id))

            else:
                dot_object.add_edge(pydot.Edge(rel['source'], rel['target'], color=GLOZZ_COLORS[rel['type']], tooltip=rel_text, rel_id=rel_id))
   

    dot_object.write_svg(dialogue_path + '.svg')

    return

def html_first(svg_folder_path, html_folder_path, collection_name):
    """
    :param svg folder path: path to folder of svgs created using create_dot_object()
    :param html folder path: path to folder where .html files will created
    :param collection name: name of the dialogue collection 
    :return: a folder of .html organizing .svg files to be viewed in the browser
    """

    index_html_file = open(html_folder_path + '/' + 'index.html', 'w')
    index_html_file.write('<html><h2>' + collection_name + '</h2><ul style="list-style: none;">')

    #for svg in svg folder create html file in html folder and write index file

    svg_list = []

    for svg in os.listdir(svg_folder_path):
        svg_trim = os.path.split(svg)[-1]
        svg_list.append(svg_trim)

    svg_list.sort(key = lambda x : int(x.split('_')[0]))
    for svg in svg_list:

        identifier = svg.split('-')[-1].split('.')[0]
        svg_file = open(html_folder_path + '/' + identifier + '.html', 'w')
        svg_file.write('<html><div id =\"wrapper\"style=\"width:100%;\"><div id=\"header\"'
                'style=\"width:100%;background:grey;z-index:10;text-align:center;\"><h2>' + identifier + '</h2></div>')
        svg_file.write('<div style=\"display:inline-block;vertical-align:top;height:100vh;overflow:auto;margin:0 40px 0 20px;padding:0 20px 0 20px;\">')
        svg_file.write( '<div class=\"base\" style=\"display:block\"><object data=\"svgs/' + svg + '\" type =\"image/svg+xml\"></object></div>')
        svg_file.write('</div>')
        svg_file.write('</div>')
        svg_file.write('</html>')
        svg_file.close()

        index_html_file.write('<li> <a href=\"' + identifier + '.html' + '\"</a>' + identifier + '</a></li>')

    index_html_file.write('</ul></html>')
    index_html_file.close()

    return

def html_compare():
    ##WIP rewrite html so that it is easier to compare
    print('function does not exist')
    return 

def write_svgs(data, svg_path, add_cdu=False, mono=False):
    """
    writes dialogue graph svgs to svg folder
    """
    title = data['data_id']

    abs_idfr = 0

    for dialogue in data['dialogues']:

        title_underscore = title.replace(' ', '_')
        dialogue_underscore = dialogue['dialogue_id'].replace(' ', '_')

        svg_save_path = svg_path + '/' +  str(abs_idfr) + '_' + title_underscore + '-' + dialogue_underscore
        create_dot_object(dialogue, svg_save_path, add_cdu, mono)
    
        abs_idfr += 1

    return

def write_html(svg_path, output_path, title, num_dirs):

    if num_dirs:
        html_compare()
    else:
        html_first(svg_path, output_path, title)
    return