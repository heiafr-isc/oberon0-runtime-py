# Oberon0 runtime system for WASM

You can test the runtime system by running the following command:

```bash
poetry install
wat2wasm examples/add.wat
wat2wasm examples/stack.wat
poetry run oberon0-rt add.wasm add 30 12
poetry run oberon0-rt stack.wasm test
```
