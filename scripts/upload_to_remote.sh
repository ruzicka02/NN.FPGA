ADDRESS="username@hostname"  # true crecentials redacted
SUBPATH="/path/to/directory/NN.FPGA"

echo "Uploading Verilog codebase (NN.FPGA/Codebase)..."
# -av == archive, verbose
# for non-default SSH ports, add --rsh 'ssh -p [PORT]'
rsync -av --info=progress2 \
      --exclude '.git' --exclude 'run' --exclude 'vcd' \
      ~/School/Praktikum/VerilogNN/ \
      $ADDRESS:$SUBPATH/Codebase \
      && echo "Done!"

# === BEFORE UNCOMMENTING, RESOLVE WHICH PARTS OF PROJECT SHOULD BE UPLOADED ===
# copying the entire project would most likely destroy all the edited paths etc.
# https://electronics.stackexchange.com/questions/641909/how-to-transfer-vivado-projects-properly-between-pcs

# echo "Uploading Vivado project (NN.FPGA/VivadoProject)..."
# rsync -av --info=progress2 \
#      ~/.Xilinx/projects/nn-fpga/ \
#      $ADDRESS:$SUBPATH/VivadoProject \
#      && echo "Done!"
