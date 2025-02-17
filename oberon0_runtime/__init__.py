# SPDX-FileCopyrightText: 2025 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

# Description: Oberon0 runtime for WASM module

import sys

import click
from pydantic import BaseModel, ConfigDict
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


class Context(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    store: None | Store
    buffer: list[int]
    memory: None | Memory


context = Context(buffer=[], store=None, memory=None)

# Runtime functions


def open_input():
    """open-inout is a no-op for compatibility with the original Oberon0 runtime."""
    pass


def read_int(address: int):
    """Reads an integer from the input buffer and store it in the memory
    at the given address."""
    try:
        val = context.buffer.pop(0)
    except IndexError:
        click.secho("Error: no more input", fg="red")
        sys.exit(1)

    context.memory.write(context.store, val.to_bytes(4, "little"), address)


def eot_() -> int:
    """Check if there are still elements in the input buffer."""
    return 1 if len(context.buffer) == 0 else 0


def write_char(c):
    """
    Write a character to the standard output.
    """
    click.echo(chr(c), nl=False)


def write_int(i, len):
    """Write an integer to the standard output using a width of `len` characters
    (padded with spaces).
    """
    click.secho(f"{i:{len}d}", nl=False)


def write_ln():
    """Write a newline character to the standard output."""
    click.echo()


# Main function
@click.command()
@click.argument("wasm-file", type=click.Path(exists=True))
@click.argument("command")
@click.argument("numbers", type=int, nargs=-1)
def main(wasm_file, command, numbers):
    context.buffer.extend(numbers)
    context.store = Store()
    module = Module.from_file(context.store.engine, wasm_file)
    f_open_input = Func(context.store, FuncType([], []), open_input)
    f_read_int = Func(context.store, FuncType([ValType.i32()], []), read_int)
    f_eot = Func(context.store, FuncType([], [ValType.i32()]), eot_)
    f_write_char = Func(context.store, FuncType([ValType.i32()], []), write_char)
    f_write_int = Func(
        context.store, FuncType([ValType.i32(), ValType.i32()], []), write_int
    )
    f_write_ln = Func(context.store, FuncType([], []), write_ln)

    context.memory = Memory(context.store, MemoryType(Limits(1, None)))
    sp = Global(context.store, GlobalType(ValType.i32(), mutable=True), 1 << 16)

    instance = Instance(
        context.store,
        module,
        [
            f_open_input,
            f_read_int,
            f_eot,
            f_write_char,
            f_write_int,
            f_write_ln,
            context.memory,
            sp,
        ],
    )

    cmd = instance.exports(context.store)[command]
    cmd(context.store)


if __name__ == "__main__":
    main()
