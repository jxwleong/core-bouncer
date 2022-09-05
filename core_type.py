import cpuid

cpu = cpuid.CPUID()
regs = cpu(0x1a, 0)
core_type = "Atom" if hex(regs[0] >> 24) == "0x20" else "Core" if hex(regs[0] >> 24) == "0x40" else f"Unknown type ({hex(regs[0] >> 24)})"
print(core_type)
