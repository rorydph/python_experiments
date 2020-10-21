# This script takes in a handful of parameter and generates a backfill param file
from pathlib import Path


# create backfill parameter file
def create_bkf_param(_filepath, _stream, _pattern, _process_name, _team_name, _jira_ref):
    print('Generating backfill parameter file.')
    print(Path.cwd())
    filename = f'{_process_name.lower()}_backfill_{_team_name.lower()}_{_jira_ref.lower()}.param'
    filetext = Path(f'{Path.home()}/github/python_experiments/file_test/file_templates/backfill_process.param').read_text()
    filetext = filetext.replace('$stream', _stream)
    filetext = filetext.replace('$process_name', _process_name.upper())
    if _pattern == '23':
        filetext = filetext.replace('$pattern', 'GCFR_PP_TfmFull')
    elif _pattern == '25':
        filetext = filetext.replace('$pattern', 'GCFR_PP_TfmTxn')
    else:
        filetext = filetext.replace('$pattern', '!!PATTERN UNDEFINED!!')
    f2 = open(f'{_filepath}/{filename}', 'w')
    f2.write(filetext)
    f2.close()
    print(f'Backfill param file {filename} generated out to {_filepath}')
