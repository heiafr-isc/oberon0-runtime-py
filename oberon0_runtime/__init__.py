# SPDX-FileCopyrightText: 2025 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

# Description: Oberon0 runtime for WASM module

import sys

import click
from wasmtime import (
    Func,
    FuncType,
    Global,
    GlobalType,
    Instance,
    Limits,
    Memory,
    MemoryType,
    Module,
    Store,
    ValType,
)

# Global buffer to store input numbers
buffer = []


# Runtime functions


def open_input():
    pass


def read_int() -> int:
    try:
        return buffer.pop(0)
    except IndexError:
        click.secho("Error: no more input", fg="red")
        sys.exit(1)


def eot_() -> int:
    return 1 if len(buffer) == 0 else 0


def write_char(c):
    click.echo(chr(c), nl=False)


def write_int(i, len):
    click.secho(f"{i:{len}d}", nl=False)


def write_ln():
    click.echo()


def run(wasm_file: str, command: str, numbers: list[int]):
    buffer.extend(numbers)
    store = Store()
    module = Module.from_file(store.engine, wasm_file)
    f_open_input = Func(store, FuncType([], []), open_input)
    f_read_int = Func(store, FuncType([], [ValType.i32()]), read_int)
    f_eot = Func(store, FuncType([], [ValType.i32()]), eot_)
    f_write_char = Func(store, FuncType([ValType.i32()], []), write_char)
    f_write_int = Func(store, FuncType([ValType.i32(), ValType.i32()], []), write_int)
    f_write_ln = Func(store, FuncType([], []), write_ln)

    mem = Memory(store, MemoryType(Limits(1, None)))
    sp = Global(store, GlobalType(ValType.i32(), mutable=True), 1 << 16)

    instance = Instance(
        store,
        module,
        [
            f_open_input,
            f_read_int,
            f_eot,
            f_write_char,
            f_write_int,
            f_write_ln,
            mem,
            sp,
        ],
    )

    cmd = instance.exports(store)[command]
    cmd(store)


# Main function
@click.command()
@click.argument("wasm-file", type=click.Path(exists=True))
@click.argument("command")
@click.argument("numbers", type=int, nargs=-1)
def main(wasm_file, command, numbers):
    run(wasm_file, command, numbers)


if __name__ == "__main__":
    main()
