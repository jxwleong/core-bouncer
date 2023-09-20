# The core type returned by querying cpuid(0x1a, 0)[eax][31:24]
core_type_def = {
    "unknown": 0x0, 
    "atom": 0x20,
    "core": 0x40
}

# Give the relative path to core_type.exe for windows or core_type for linux
core_type_command = {
    "nt": "core_type.exe",
    "posix": "bin/linux/core_type" 
}