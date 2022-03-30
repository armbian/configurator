# Armbian configurator

[![Build debian package](https://github.com/armbian/configurator/actions/workflows/debian.yml/badge.svg)](https://github.com/armbian/configurator/actions/workflows/debian.yml)

- [Open tasks](https://armbian.atlassian.net/browse/AR-967)

# Package repository

It is updated on this repository push.

    wget -qO- https://imola.armbian.com/apt/armbian.key | gpg --dearmor | sudo tee > /usr/share/keyrings/armbian.gpg
    sudo echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/armbian.gpg] https://armbian.github.io/configurator stable main" > /etc/apt/sources.list.d/armbian-development.list
    sudo apt-get install configurator
