# Build Rust binaries (interpreter, etc.)

import os

if not os.path.exists("bin/"):
    os.mkdir("bin/")

os.system(
    "rustc interpreter/src/main.rs -o bin/interpreter -C opt-level=3 -C lto -C strip=symbols"
)
