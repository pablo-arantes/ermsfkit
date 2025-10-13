import sys
import subprocess
import os

import pytest



@pytest.mark.parametrize(
        'command, has_test_data_dep',
        [
            ([sys.executable, '-m','pip', 'install', '.'], False),
            ([sys.executable, '-m','pip', 'install', '.[demo]'], True),
        ]
)
def test_install_cmd_pip_local(command: list, has_test_data_dep: bool):
    command.append('--dry-run')
    ret=subprocess.check_output(command)

    # raise RuntimeError(ret)

    ret_has_test_data_dep = 'MDAnalysisTests' in ret.decode()
    assert ret_has_test_data_dep == has_test_data_dep


