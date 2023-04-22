<p align="center">
  <a href="#build-framework">
  <img src="https://raw.githubusercontent.com/armbian/build/master/.github/armbian-logo.png" alt="Armbian logo" width="144">
  </a><br>
  <strong>configurator</strong><br>
</p>


[![GitHub last commit (branch)](https://img.shields.io/github/last-commit/armbian/build/master)](https://github.com/armbian/build/commits)
[![Debian repository](https://github.com/armbian/configurator/actions/workflows/debian.yml/badge.svg)](https://github.com/armbian/configurator/actions/workflows/debian.yml)
[![Unit testings](https://github.com/armbian/configurator/actions/workflows/tests.yml/badge.svg)](https://github.com/armbian/configurator/actions/workflows/tests.yml)
[![Twitter Follow](https://img.shields.io/twitter/follow/armbian?style=flat-square)](https://twitter.com/intent/follow?screen_name=armbian)
[![Join the Discord](https://img.shields.io/discord/854735915313659944.svg?color=7289da&label=Discord%20&logo=discord)](https://discord.com/invite/gNJ2fPZKvc)
[![Become a patron](https://img.shields.io/liberapay/patrons/armbian.svg?logo=liberapay)](https://liberapay.com/armbian)


- [Open tasks](https://armbian.atlassian.net/browse/AR-967)

# Package repository

It is updated on this repository push.

    wget -qO- https://imola.armbian.com/apt/armbian.key | gpg --dearmor | sudo tee /usr/share/keyrings/armbian.gpg > /dev/null
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/armbian.gpg] https://armbian.github.io/configurator stable main" | sudo tee /etc/apt/sources.list.d/armbian-development.list > /dev/null

Install:

    sudo apt-get update
    sudo apt-get install configurator
