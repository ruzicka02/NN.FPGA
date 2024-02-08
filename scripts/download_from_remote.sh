ADDRESS="username@hostname"  # true crecentials redacted
SUBPATH="/path/to/directory/NN.FPGA"

echo "Downloading generated files (NN.FPGA/Generated)..."
# -av == archive, verbose
# for non-default SSH ports, add --rsh 'ssh -p [PORT]'
rsync -av --info=progress2 \
      $ADDRESS:$SUBPATH/Generated/ \
      --exclude '.Xil' \
      ~/School/Praktikum/Generated/ \
      && echo "Done!"
