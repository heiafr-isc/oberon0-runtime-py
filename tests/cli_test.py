# SPDX-FileCopyrightText: 2025 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT


import subprocess

from typer.testing import CliRunner

from oberon0_runtime import app


def test_cli():
    subprocess.run(["wat2wasm", "-o", "tests/add.wasm", "examples/add.wat"], check=True)
    runner = CliRunner()
    result = runner.invoke(app, ["tests/add.wasm", "add", "29", "13"])
    assert result.exit_code == 0
    assert result.output == "   42\n"
