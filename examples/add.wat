;; SPDX-FileCopyrightText: 2025 Jacques Supcik <jacques.supcik@hefr.ch>
;;
;; SPDX-License-Identifier: Apache-2.0 OR MIT

(module
    (import "sys" "OpenInput" (func $open_input))
    (import "sys" "ReadInt" (func $read_int (result i32)))
    (import "sys" "eot" (func $eot (result i32)))
    (import "sys" "WriteChar" (func $write_char (param i32)))
    (import "sys" "WriteInt" (func $write_int (param i32 i32)))
    (import "sys" "WriteLn" (func $write_ln))
    (import "env" "memory" (memory 1))
    (import "env" "__stack_pointer" (global $sp (mut i32)))

    (func (export "add")
        (call $open_input)
        (call $read_int)
        (call $read_int)
        i32.add
        (i32.const 5)
        (call $write_int)
        (call $write_ln)
    )
)
