# NN@FPGA

Series of projects implementing different Neural network architectures on FPGA using Verilog. Intended use is for the Kria KV260 board.

## Submodule description

Multiple different submodules (Git repositories) are contained within this main repo. These are:

- `VerilogNN`... Main codebase in Verilog, implementing the modules themselves before running them on the device.
- `FPU-IEEE-754`... Original repository for certain floating point operations. We took inspiration from this one and improved it with a Pull request.
- `devmem2`... Utility written in C which provides direct access to physical memory on any machine with Linux. Used on the FPGA, where block RAM is mapped
within the physical address space. This is a fork of the original repository, doing some minor simplification for our purposes.
- `mem_master`... Python wrapper for memory interactions using devmem2 command.

Some other directories which are not submodules are included:

- `scripts`... Shell scripts to perform multiple necessary tasks semi-automatically. Mostly copying files over SSH using rsync.
- **TODO**

When cloning the repositories, these submodules will not download automatically. To load all of the submodules correctly, run following command:

```
git submodule update --init --recursive
```

# Technical information

How to run this project, ...

## Run bitsream on target

As the resulting modules need to interact with the memory shared between FPGA and CPU on the Kria board, the process of uploading and running modules
on Kria board is not so straightforward. It seems that when the identical bitstream is uploaded directly from Vivado ("Program Device" button),
this memory interaction on the board is not working. Following steps are taken from this [Xilinx example](https://xilinx.github.io/kria-apps-docs/creating_applications/2022.1/build/html/docs/vivado_accel_example.html#).
(As Xilinx has the tendency to remove older online resources, in case previous link doesn’t work, [try this](http://web.archive.org/web/20240117153005/https://xilinx.github.io/kria-apps-docs/creating_applications/2022.1/build/html/docs/vivado_accel_example.html))

### Prerequisites
- Vivado (design modelling, `.bit.bin` bitstream, `.xsa` design file)
- Vitis (package contains `XSCT` shell, needed for generating `.dtsi` HW description file, and Device Tree Compiler `dtc`)
- [Device Tree Generator (DTG)](https://github.com/Xilinx/device-tree-xlnx)
- `devmem` or `devmem2` [OSS implementation - Github](https://github.com/radii/devmem2)

### Generate bitstream (`.bit.bin`)
- Using Vivado, create a valid module and finish synthesis + implementation
- Settings -> Bitstream -> set `-bin_file` as True (only once)
- Generate bitstream... saved as `[project_path]/nn-fpga.runs/impl_1/[design_name]_wrapper.bin`
- Copy file to desired location, rename to `[app_name].bit.bin`

### Generate binary device tree (`.dtbo`)
- In Vivado (after bitstream is generated), File -> Export -> Export Hardware -> include bitstream
- `.xsa` file is generated... `[project_path]/nn-fpga.runs/impl_1/[design_name]_wrapper.xsa`
- Copy file to desired location, rename to `[app_name].xsa`
- using `xsct`, run the following commands:

```
hsi open_hw_design $DESIGN_NAME.xsa
hsi set_repo_path $HOME/device-tree-xlnx  # path to DTG
hsi create_sw_design device-tree -os device_tree -proc psu_cortexa53_0
hsi set_property CONFIG.dt_overlay true [hsi get_os]
hsi set_property CONFIG.dt_zocl true [hsi get_os]
hsi generate_target -dir temp
hsi close_hw_design [hsi current_hw_design]
exit
```

- Directory `temp` has been generated that contains `pl.dtsi`
- Convert `pl.dtsi` to `[app_name].dtbo`... `dtc -@ -O dtb -o [app_name].dtbo pl.dtsi`
- Copy file to desired location, `temp` directory can be removed now

This process is partially automized by `xsa2dtbo.sh` script, present on atcremers.

### Configuration file (`shell.json`)

```json
{
    "shell_type" : "XRT_FLAT",
    "num_slots" : "1"
}
```

### Upload, run

- Upload the `[app_name].bit.bin`, `[app_name].dtbo`. and `shell,json` files to Kria board using SSH (scp, rsync)
- Copy these files to newly created directory `/lib/firmware/xilinx/[app_name]`

App should now be ready to run. This means it should be visible when running `sudo xmutil listapps`. In order to run the app,
use `sudo xmutil unloadapp; sudo xmutil loadapp [app_name]`.

Now, the app should be running. Using the `devmem` (or `devmem2`) command, you should be able to access the memory of the program,
assuming you know which addresses the program maps to (this information is visible in Vivado). Running `sudo devmem2 0xa0000000`
should output the memory contents on address `0x a000 0000`. Default accessed memory size is 1 word (8 bytes). This command can be used
for writing to memory as well as reading from it.
