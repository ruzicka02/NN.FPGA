if [ $# -lt 1 ]; then
	echo "Usage: $0 [XSA input file name, without suffix]"
	exit 1
fi

if [ $1 = "-h" ] || [ $1 = "--help" ]; then
	echo "Convert the XSA file generated from Vivado to needed DTBO file."
	echo -e "Uses the xsct console and dtc (Device Tree Compiler) from Vitis toolchain\n"
	echo "Usage: $0 [XSA input file name, without suffix]"
	exit 0
fi

DESIGN_NAME=$1
TEMP_DIR='temp'  # contains the dump of generate_target from xsct, but we only need one file

# not necessary, xsct does this automatically
# mkdir $TEMP_DIR

# run the following commands in the xsct shell
echo "Running xsct commands..."
xsct <<EOF && echo "xsct process done!"
hsi open_hw_design $DESIGN_NAME.xsa
hsi set_repo_path $HOME/device-tree-xlnx
hsi create_sw_design device-tree -os device_tree -proc psu_cortexa53_0
hsi set_property CONFIG.dt_overlay true [hsi get_os]
hsi set_property CONFIG.dt_zocl true [hsi get_os]
hsi generate_target -dir $TEMP_DIR
hsi close_hw_design [hsi current_hw_design]
EOF

cd $TEMP_DIR
dtc -@ -O dtb -o pl.dtbo pl.dtsi
cp pl.dtbo ../$DESIGN_NAME.dtbo
cd ..

# cleanup
rm -rf $TEMP_DIR extracted
rm psu_init_gpl.* psu_init.*
mv $DESIGN_NAME.bit $DESIGN_NAME.bit.bin  # naming convention for this project, taken from the guide by Xilinx
