FROM ubuntu:latest

# Install necessary packages
RUN apt update
RUN apt install -y wget nano qemu-system
RUN apt install -y build-essential

RUN mkdir /vm
WORKDIR /vm
RUN wget https://cloud-images.ubuntu.com/plucky/current/plucky-server-cloudimg-amd64.img

RUN apt install -y gcc ssh

COPY ./run-qemu.sh /vm/run-qemu.sh
COPY ./start_challenge.sh /VM_config/start_challenge.sh
COPY ./aiden_emulator.sh /VM_config/aiden_emulator.sh
COPY ./VM_config/ /VM_config/
COPY ./flag.txt /VM_config/flag.txt
COPY ./roomba_ids.c /vm/roomba_ids.c
COPY ./Makefile /vm/Makefile

RUN chmod +x ./run-qemu.sh
RUN qemu-img create -f qcow2 ubuntu.qcow2 8G

# me am paranoid, root shell not allowed
RUN make
RUN mv ./roomba_ids /VM_config/roomba_ids

CMD ["/vm/run-qemu.sh"]

# FROM fedora:latest
# RUN dnf install -y qemu-kvm libvirt libguestfs-tools virt-install rsync wget nano vagrant
# RUN mkdir /vm

# COPY ./Vagrantfile /vm/
# COPY ./flag.txt /vm/

# WORKDIR /vm/

# RUN echo "#!/bin/bash" > entrypoint.sh
# RUN echo "systemctl enable libvirtd && vagrant plugin install vagrant-libvirt && /bin/bash" >> entrypoint.sh
# RUN chmod +x ./entrypoint.sh

# # CMD ["./entrypoint.sh"]
# CMD ["/bin/bash"]

# FROM ubuntu:latest
# RUN apt update
# RUN apt install -y qemu-kvm
# RUN apt install -y  libvirt-daemon
# # RUN apt install -y libguestfs-tools 
# # RUN apt install -y virt-install 
# RUN apt install -y rsync 
# RUN apt install -y wget 
# RUN apt install -y nano 
# RUN apt install lsb-release
# RUN mkdir /vm

# COPY ./Vagrantfile /vm/
# COPY ./flag.txt /vm/

# WORKDIR /vm/

# COPY ./entrypoint.sh /vm/entrypoint.sh
# RUN chmod +x ./entrypoint.sh

# # CMD ["./entrypoint.sh"]
# CMD ["/bin/bash"]