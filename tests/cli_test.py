# SPDX-FileCopyrightText: 2026 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: MIT


import subprocess

from typer.testing import CliRunner

from oberon0_runtime import app


def test_cli() -> None:
    subprocess.run(["wat2wasm", "-o", "tests/add.wasm", "examples/add.wat"], check=True)
    runner = CliRunner()
    result = runner.invoke(app, ["run", "tests/add.wasm", "add", "29", "13"])
    assert result.exit_code == 0
    assert result.output.strip() == "42"
