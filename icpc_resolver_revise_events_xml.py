import os
import sys
from xml.etree.ElementTree import parse, Element, tostring

BASEPATH = os.path.abspath(os.path.dirname(__file__))

EVENTS_FILENAME = 'events.xml'
OUTPUT_FILENAME = 'postevents.xml'

TEAM_NECESSARY_INFO = [
    'id', 
    'name', 
    'university', 
    'university-short-name',
    'region'
]

FINALIZED_NECESSARY_INFO = {
    'last-gold' : 1,
    'last-silver' : 1,
    'last-bronze' : 1,
    'timestamp' : 0, 
}


def del_duplicated_contest_tag():
    with open(EVENTS_FILENAME, 'r') as f:
        lines = f.readlines()
        if len(lines) < 2:
            return 
        if lines[0].strip() == '<contest>' \
          and lines[1].strip() == lines[0].strip():
            print('delete dupliccated contest tag')
            lines = lines[1:]
            f = open(EVENTS_FILENAME, 'w')
            f.writelines(lines)
            f.close()


def problem_index_revise(doc):
    pid_nodes = doc.findall('problem/id')
    min_pid = None

    for pid_node in pid_nodes:
        pid = int(pid_node.text)
        if min_pid is None:
            min_pid = pid
        else:
            min_pid = min(min_pid, pid)

    if min_pid is not None and min_pid != 1:
        delta = 1 - min_pid
        for pid_node in pid_nodes:
            pid = int(pid_node.text)
            new_pid = pid + delta
            pid_node.text = str(new_pid)   
    

def del_teams_with_missing_info(doc):
    team_nodes = doc.findall('team')
    
    for team_node in team_nodes:   
        delete = False
        for info in TEAM_NECESSARY_INFO:
            tmp = team_node.find(info)
            if tmp is None:
                delete= True
        if delete:
            print('delete ', tostring(team_node))
            doc.getroot().remove(team_node) 


def append_finalized(doc):
    finalized_node = doc.find('finalized')
    if finalized_node is None:   
        finalized_node = Element('finalized')
    for key, value in FINALIZED_NECESSARY_INFO.items():
        key_node = finalized_node.find(key)
        if key_node is None:
            key_node = Element(key)
            key_node.text = str(value)
            finalized_node.append(key_node) 
    if doc.find('finalized') is None:
        doc.getroot().append(finalized_node) 
        

def main():
    global EVENTS_FILENAME, OUTPUT_FILENAME
    EVENTS_FILENAME = os.path.join(BASEPATH, EVENTS_FILENAME)
    OUTPUT_FILENAME = os.path.join(BASEPATH, OUTPUT_FILENAME)

    del_duplicated_contest_tag() 
   
    doc = parse(EVENTS_FILENAME)
    problem_index_revise(doc)
    del_teams_with_missing_info(doc)
    append_finalized(doc)

    doc.write(OUTPUT_FILENAME, encoding='utf-8', xml_declaration=False)

    print('Done.')

if __name__ == '__main__':
    main()