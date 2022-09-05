# Contact: jxwleong/xleong
import cpuid
import psutil
import json

def get_core_type():
    cpu = cpuid.CPUID()
    regs = cpu(0x1a, 0)
    core_type = "Atom" if hex(regs[0] >> 24) == "0x20" else "Core" if hex(regs[0] >> 24) == "0x40" else f"Unknown type ({hex(regs[0] >> 24)})"
    return core_type

total_core_count = psutil.cpu_count()


def main():
    core_mapping = {}
    for core in range(total_core_count):
        current_process = psutil.Process()
    
        # Set affinity
        current_process.cpu_affinity([core])  # expecting list terable
        #print(f"Core{core}------------->{get_core_type()}")
        core_mapping[f"core_{core}"] = get_core_type()

    print(json.dumps(core_mapping, indent="\t"))

    
if __name__ == "__main__":
    main()
