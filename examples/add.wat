;; SPDX-FileCopyrightText: 2025 Jacques Supcik <jacques.supcik@hefr.ch>
;;
;; SPDX-License-Identifier: Apache-2.0 OR MIT

(module
    (import "sys" "OpenInput" (func $open_input))
    (import "sys" "ReadInt" (func $read_int (param i32)))
    (import "sys" "eot" (func $eot (result i32)))
    (import "sys" "WriteChar" (func $write_char (param i32)))
    (import "sys" "WriteInt" (func $write_int (param i32 i32)))
    (import "sys" "WriteLn" (func $write_ln))
    (import "env" "memory" (memory 1))
    (import "env" "__stack_pointer" (global $sp (mut i32)))

    (func (export "add")
        ;; allocate space for 3 integers (x, y, z). 3 * 4 bytes = 12 bytes
        global.get $sp
        i32.const 12
        i32.sub
        global.set $sp

        ;; call OpenInput
        call $open_input

        ;; put the address of z (sp + 8) on the stack for the assignment z := x + y
        global.get $sp
        i32.const 8
        i32.add

        ;; put the address of x (sp) on the stack and call ReadInt
        global.get $sp
        i32.const 0
        i32.add
        call $read_int

        ;; put the address of y (sp + 4) on the stack and call ReadInt
        global.get $sp
        i32.const 4
        i32.add
        call $read_int

        ;; load x from memory
        global.get $sp
        i32.const 0
        i32.add
        i32.load

        ;; load y from memory
        global.get $sp
        i32.const 4
        i32.add
        i32.load

        ;; add x and y
        i32.add

        ;; store the result in z
        i32.store

        ;; load z from memory
        global.get $sp
        i32.const 8
        i32.add
        i32.load

        ;; put 5 on the stack and call WriteInt
        i32.const 5
        call $write_int

        ;; call WriteLn
        call $write_ln

        global.get $sp
        i32.const 12
        i32.add
        global.set $sp
    )
)
