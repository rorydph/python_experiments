import pytest
from pathlib import Path
import src.backfill_param as src_bkf
import src.process_xml as src_xml


#test parameters
bau_stream = '42'
bkf_stream = '500'
pattern = '25'
process_name = 'TX_123_TEST'
team_name = 'test_team'
jira_ref = 'ABC-123'
output_dir = f'{Path.home()}/github/python_experiments/file_test/tests/output_files'
ref_dir = f'{Path.home()}/github/python_experiments/file_test/tests/ref_files'


def test_bkf_param():
    src_bkf.create_bkf_param(output_dir, bkf_stream, pattern, process_name, team_name, jira_ref)
    gen = Path(f'{output_dir}/tx_123_test_backfill_test_team_abc-123.param').read_text()
    ref = Path(f'{ref_dir}/ref_backfill_param.param').read_text()
    assert gen == ref


def test_process_xml():
    src_xml.create_xml_file(output_dir, bau_stream, pattern, process_name)
    gen = Path(f'{output_dir}/TX_123_TEST.xml').read_text()
    ref = Path(f'{ref_dir}/ref_process_xml.xml').read_text()
    assert gen == ref


if __name__ == '__main__':
    test_bkf_param()
    test_process_xml()
