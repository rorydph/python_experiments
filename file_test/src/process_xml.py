# create process XML file
from pathlib import Path
from xml.etree import ElementTree as et

def create_xml_file(_filepath, _stream, _pattern, _process_name):
    filename = f'{_process_name.upper()}.xml'
    print('Creating BAU process XML file.')
    tree = et.parse(Path(f'{Path.home()}/github/python_experiments/file_test/file_templates/process_xml.xml'))
    tree.find('.//PROCESS_NAME').text = _process_name
    tree.find('.//STREAM_KEY').text = _stream
    if _pattern == '23':
        tree.find('.//PATTERN').text = 'GCFR_Tfm_Full_Apply'
    elif _pattern == '25':
        tree.find('.//PATTERN').text = 'GCFR_Tfm_Insert_Append'
    else:
        tree.find('.//PATTERN').text = '!!PATTERN UNDEFINED!!'
    tree.write(f'{_filepath}/{_process_name}.xml')
    print(f'Process xml file {filename} generated out to {_filepath}')
