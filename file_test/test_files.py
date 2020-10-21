from pathlib import Path
import process_xml as src_xml
import backfill_param as src_bkf
import pytest
import difflib


@pytest.fixture
def test_parameters():
    return {
        "bau_stream": "42",
        "bkf_stream": "500",
        "pattern": "25",
        "process_name": 'TX_123_TEST',
        "team_name": 'test_team',
        "jira_ref": 'ABC-123',
        "output_dir": 'test_output_files',
        "ref_dir": 'test_ref_files'
    }


def peek(iterable):
    try:
        first = next(iterable)
    except StopIteration:
        return None
    return iterable


def compare_files(f1, f2):
    return difflib.unified_diff(open(f1, 'r').readlines(), open(f2, 'r').readlines())


def test_bkf_param(test_parameters):
    src_bkf.create_bkf_param(test_parameters['output_dir'], test_parameters['bkf_stream'], test_parameters['pattern'],
                             test_parameters['process_name'], test_parameters['team_name'], test_parameters['jira_ref'])
    gen = Path(f'{test_parameters["output_dir"]}/tx_123_test_backfill_test_team_abc-123.param')
    ref = Path(f'{test_parameters["ref_dir"]}/ref_backfill_param.param')
    test = compare_files(ref, gen)
    assert peek(test) is None, print(''.join(test))


def test_process_xml(test_parameters):
    src_xml.create_xml_file(test_parameters['output_dir'], test_parameters['bau_stream'], test_parameters['pattern'],
                            test_parameters['process_name'])
    gen = Path(f'{test_parameters["output_dir"]}/TX_123_TEST.xml')
    ref = Path(f'{test_parameters["ref_dir"]}/ref_process_xml.xml')
    test = compare_files(ref, gen)
    assert peek(test) is None, print(''.join(test))


def test_sql(test_parameters):
    test = compare_files(Path('./test_ref_files/gen_sql.sql'), Path('./test_ref_files/ref_sql.sql'))
    assert peek(test) is None, print(''.join(test))


if __name__ == '__main__':
    test_bkf_param()
    test_process_xml()
