# SPDX-FileCopyrightText: 2025 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT


import subprocess

from click.testing import CliRunner

from oberon0_runtime import main


def test_true():
    subprocess.run(["wat2wasm", "-o", "tests/add.wasm", "examples/add.wat"], check=True)
    runner = CliRunner()
    result = runner.invoke(main, ["tests/add.wasm", "add", "29", "13"])
    assert result.exit_code == 0
    assert result.output == "   42\n"
