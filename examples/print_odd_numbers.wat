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

    (func (export "run")
        ;; allocate space for 2 integers
        ;; SP -> i
        ;; SP + 4 -> max
        global.get $sp
        i32.const 8
        i32.sub
        global.set $sp

        ;; call OpenInput
        call $open_input

        ;; ReadInt(max)
        global.get $sp
        i32.const 4
        i32.add
        call $read_int

        ;; i = 1
        global.get $sp
        i32.const 0
        i32.add
        i32.const 1
        i32.store

        (block $b1
            ;; check if i >= max (initial check)
            global.get $sp
            i32.const 0
            i32.add
            i32.load

            global.get $sp
            i32.const 4
            i32.add
            i32.load

            i32.ge_s
            br_if $b1

            ;; While loop
            (loop $l1
                ;; print i
                global.get $sp
                i32.const 0
                i32.add
                i32.load

                i32.const 5
                call $write_int
                call $write_ln

                ;; i = i + 2
                global.get $sp
                i32.const 0
                i32.add

                global.get $sp
                i32.const 0
                i32.add
                i32.load

                i32.const 2
                i32.add
                i32.store

                ;; repeat while i < max
                global.get $sp
                i32.const 0
                i32.add
                i32.load

                global.get $sp
                i32.const 4
                i32.add
                i32.load

                i32.lt_s
                br_if $l1
            )
        )

        ;; free stack space
        global.get $sp
        i32.const 8
        i32.add
        global.set $sp

    )
)
