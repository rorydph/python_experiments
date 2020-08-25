# This script reads the ddl for a table and generates the code for the relevant backfill and bau branch objects
# Change History:
#   2020-06-21    Rory        First creation

import pyodbc, json, os, fileinput


# connect to json file and load contents to dict
def get_json(in_file_name):
    with open(in_file_name, 'r') as json_file:
        out_dict = json.load(json_file)
    return out_dict


# set global variables
def set_globals(in_param):
    global table_name, bau_path, bkf_path, process_name, bkf_table
    bau_path = 'generated_output/' + in_param['jira_ref'].upper() + '/BAU'
    bkf_path = 'generated_output/' + in_param['jira_ref'].upper() + '/BACKFILL'
    table_name = in_param['target_table'].upper()
    process_name = in_param['process_name'].upper()
    bkf_table = in_param['target_db'].upper() + '.' + table_name + '_BACKFILL_' + in_param['team_name'].upper() + '_' + in_param['datestamp']


# connect to the database and retrieve the relevant table's metadata
def get_metadata(in_table_name):
    connection = pyodbc.connect('DRIVER={SQLite3 ODBC Driver};SERVER=localhost;Database=pytest.db')
    # cursor = connection.cursor()
    return connection.execute('select sql from sqlite_master').fetchone()


# create subdirectories
def create_dir(in_path):
    try:
        os.makedirs(in_path)
    except OSError:
        print('Creation of the subfolder %s failed.' % in_path)
    else:
        print('Subfolder %s created.' % in_path)


# write the current target table ddl to file
def create_ddl_file(in_metadata):
    with open('temp_' + table_name + '.sql', 'w') as f:
        for row in in_metadata:
            f.write(row)
        f.close()


# create process XML file
def create_xml_file(in_stream, in_pattern):
    print('Creating BAU process XML file.')
    from xml.etree import ElementTree as et
    tree = et.parse('file_templates/process_xml.xml')
    tree.find('.//PROCESS_NAME').text = process_name
    tree.find('.//STREAM_KEY').text = in_stream
    if in_pattern == '23':
        tree.find('.//PATTERN').text = 'GCFR_Tfm_Full_Apply'
    elif in_pattern == '25':
        tree.find('.//PATTERN').text = 'GCFR_Tfm_Insert_Append'
    else:
        tree.find('.//PATTERN').text = '!!PATTERN UNDEFINED!!'
    tree.write(bau_path + '/' + process_name + '.xml')


# create backfill parameter file
def create_bkf_param(in_param):
    print('Generating backfill parameter file.')
    target_file = bkf_path + '/' + process_name.lower() + '_backfill_' + in_param['team_name'].lower() + '_' + in_param['jira_ref'].lower() + '.param'
    f1 = open('file_templates/backfill_process.param', 'r')
    filetext = f1.read()
    f1.close()
    filetext = filetext.replace('$stream', in_param['backfill_stream'])
    filetext = filetext.replace('$process_name', process_name)
    if in_param['pattern_type'] == '23':
        filetext = filetext.replace('$pattern', 'GCFR_PP_TfmFull')
    elif in_param['pattern_type'] == '25':
        filetext = filetext.replace('$pattern', 'GCFR_PP_TfmTxn')
    else:
        filetext = filetext.replace('$pattern', '!!PATTERN UNDEFINED!!')
    f2 = open(target_file, 'w')
    f2.write(filetext)
    f2.close()


# create backup and insert scripts
def create_bkp_ins(in_param):
    bkp_file = bau_path + '/001_' + in_param['team_name'].lower() + '_' + in_param['jira_ref'].lower() + '_backup.sql'
    ins_file = bau_path + '/002_' + in_param['team_name'].lower() + '_' + in_param['jira_ref'].lower() + '_insert.sql'
    bkp_table = in_param['target_db'].upper() + '.' + table_name + '_BKP_' + in_param['datestamp']
    print('Creating backup script.')
    with open(bkp_file, 'w') as f1:
        f1.write('RENAME TABLE ' + in_param['target_db'].upper() + '.' + table_name + ' AS ' + bkp_table + ';\n')
        f1.close()
    print('Creating insert script.')
    with open(ins_file, 'w') as f2:
        f2.write('INSERT INTO ' + in_param['target_db'].upper() + '.' + table_name + '\n')
        if in_param['existing_table'] == 'Y':
            f2.write('SELECT * FROM ' + bkp_table + '\n')
            f2.write('UNION ALL\n')
            f2.write('SELECT * FROM ' + bkf_table + ';\n')
        else:
            f2.write('SELECT * FROM ' + bkp_table + ';\n')
        f2.close()


print('Starting script generation process process........')
print('Retrieving input parameters.')
param = get_json('parameter.json')
set_globals(param)
print('Table to generate script for : ' + table_name)
create_dir(bau_path)
create_dir(bkf_path)
print('Executing script generation.')
create_ddl_file(get_metadata(table_name))
create_bkf_param(param)
create_bkp_ins(param)
create_xml_file(param['bau_stream'], param['pattern_type'])
print('Script generation complete.')
