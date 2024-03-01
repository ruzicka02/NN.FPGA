# NN@FPGA

Series of projects implementing different Neural network architectures on FPGA using Verilog. Intended use is for the Kria KV260 board.

Authors:
- [Šimon Růžička](https://github.com/ruzicka02)
- [Philipp Wondra](https://github.com/Philippwon)

This project was created at [Technical University of Munich](https://www.tum.de) as a part of the Creation of Deep Learning Methods Practical Course. The project was supervised by Dr. Vladimir Golkov.

## Submodule description

Multiple different submodules (Git repositories) are contained within this main repo. These are:

- `VerilogNN`... Main codebase in Verilog, implementing the modules themselves before running them on the device.
- `FPU-IEEE-754`... Original repository for certain floating point operations. We took inspiration from this one and improved it with a Pull request.
- `devmem2`... Utility written in C which provides direct access to physical memory on any machine with Linux. Used on the FPGA, where block RAM is mapped
within the physical address space. This is a fork of the original repository, doing some minor simplification for our purposes.
- `mem_master`... Python wrapper for memory interactions using devmem2 command.

Some other directories which are not submodules are included:

- `VivadoProject.tar.gz`... gzipped directory of the source files from Vivado project. Following files should be sufficient to replicate all the project files, as suggested on [the closest thing to a Vivado documentation](https://electronics.stackexchange.com/a/500371). The complete project was not included due to limited space (circa 1.5 GB) and the overwhelming use of absolute addresses.
- `scripts`... Shell scripts to perform multiple necessary tasks semi-automatically. Mostly copying files over SSH using rsync.
- `docs`... Additional project documentation. Contains a Markdown document with detailed description of this project. Converted from a Word document shared with our supervisor and other students at TUM. Final presentation slides, `slides.pptx` and `slides.pdf` **TODO** are also included.

When cloning this repository, these submodules will not download automatically. To load all of the submodules correctly, run following command:

```
git submodule update --init --recursive
```

# Technical information

This guide should provide you with enough information to run the project.

## Simulate Verilog modules

The easiest way to simulate a Verilog module in our opinion is [Icarus Verilog](https://github.com/steveicarus/iverilog) simulator. For more details about its installation, see the linked repository. Keep in mind that this process still differs significantly from the HW implementation, for more details see `docs`.

Most common approach in Verilog simulation is to create a wrapper/testbench around the source file itself. This can be used to assign different values over time, use debugging printing methods etc., utilizing the simulation-only Verilog features. Such modules are included in the `VerilogNN/sim` directory. In order to "compile" a Verilog testbench file into the `vvp` format, use:

```
iverilog -o ModuleName.vvp sim/ModuleName.v -s ModuleName -I src/
```

Then, run simulation with:

```
vvp ModuleName.vvp -lxt2
```

By running the simulation, a waveform file is created in the `vcd/` directory. The `-lxt2` simulation switch results in significant compression of this file. This waveform can be displayed in multiple visualizers, such as GTKWave.

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
