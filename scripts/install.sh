#!/bin/bash
curl -L https://github.com/garethlau/floatingfile-cli/releases/download/v1.2.0/floatingfile-v1.2.0.tar.gz | tar -xz
sudo mv floatingfile /opt/
sudo ln -s /opt/floatingfile/floatingfile /usr/local/bin
