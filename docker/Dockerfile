FROM ubuntu:24.04
SHELL ["/bin/bash", "-c"]

WORKDIR /root
RUN apt update -y

RUN apt update && \
    apt install -y \
        git \
        git-lfs \
        vim \
        curl \
        telnet \
        iproute2 \
        x11-apps \
        python3-pip \
        iputils-ping \
        net-tools \
        software-properties-common && \
    rm -rf /var/lib/apt/lists/*

# set locale
RUN apt update && apt install locales -y
RUN locale-gen en_US en_US.UTF-8
RUN update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
RUN export LANG=en_US.UTF-8

# enable required repositories
RUN add-apt-repository universe
RUN export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}') && \
    curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
RUN dpkg -i /tmp/ros2-apt-source.deb

# install ros2
RUN apt update && apt install ros-dev-tools -y
RUN apt install -y ros-jazzy-desktop \
    ros-jazzy-ros-base

# source build of fanuc packages
RUN git lfs install

WORKDIR /root/fanuc_ws
RUN apt update -y
RUN rosdep init && rosdep update
RUN apt update && apt dist-upgrade -y

WORKDIR /root
RUN apt install python3-colcon-common-extensions python3-colcon-mixin python3-vcstool -y
RUN colcon mixin add default https://raw.githubusercontent.com/colcon/colcon-mixin-repository/master/index.yaml
RUN colcon mixin update default

COPY build.sh .
COPY install.sh .

RUN echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
RUN echo "source ~/fanuc_ws/install/setup.bash" >> ~/.bashrc
RUN echo "source ~/moveit_ws/install/setup.bash" >> ~/.bashrc
RUN echo "export ROS_DOMAIN_ID=72" >> ~/.bashrc