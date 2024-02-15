ADDRESS="username@hostname"  # true crecentials redacted
SUBPATH="/path/to/directory"

echo "Uploading generated files (NN.FPGA/Generated)..."
# -av == archive, verbose
# for non-default SSH ports, add --rsh 'ssh -p [PORT]'
rsync -av --info=progress2 \
      --exclude '.Xil' \
      ~/School/Praktikum/Generated/ \
      $ADDRESS:$SUBPATH/Generated/ \
      && echo "Done!"

echo "Uploading the NN controller (dist_packages/mem_master)..."
# upload needs sudo on remote
# https://askubuntu.com/questions/719439/using-rsync-with-sudo-on-the-destination-machine
rsync -av --info=progress2 \
      --rsync-path="sudo rsync" --exclude '.git' --exclude '__pycache__' \
      ~/School/Praktikum/mem_master/ \
      $ADDRESS:/lib/python3/dist-packages/mem_master/ \
      && echo "Done!"

echo "Uploading devmem2 source files..."
#     only the C files, ignores Makefile and binaries
rsync -av --info=progress2 \
      ~/School/Praktikum/devmem2/*.c \
      $ADDRESS:$SUBPATH/devmem2/ \
      && echo "Done!"
