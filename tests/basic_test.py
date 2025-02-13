# SPDX-FileCopyrightText: 2025 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT


import subprocess

import oberon0_runtime


def test_true(capsys):
    subprocess.run(["wat2wasm", "-o", "add.wasm", "../examples/add.wat"], check=True)
    oberon0_runtime.run("add.wasm", "add", [29, 13])
    captured = capsys.readouterr()
    assert captured.out == "   42\n"
