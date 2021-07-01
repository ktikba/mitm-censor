# Contributing

As an open source project, mitm-censor encourages community contribution. This brief
guide contains instructions for how to set up mitm-censor on your computer so you can start
hacking on it. As a word of warning, the author is not particularly familiar with Python,
and as such this may be a bumpier than usual setup. Please feel free to contribute to this
guide as well!

## Prerequisites

* **Python 3.9.6**

  You can see which version of python you have installed using `python --version`. You can install 
  the latest version of python from [the website](https://python.org), or using a third party tool like [homebrew](https://brew.sh/).

## Environment setup

These instructions were initially tested on Windows 10 Build 19042. They should generally work on
different versions of Windows, macOS, and Linux as well.

Start by cloning the repo...
```shell
git clone https://path/to/mitm-censor
cd mitm-censor
```

Create a [virtualenv](https://virtualenv.pypa.io/en/latest/) to work within...
```shell
python -m venv venv
```

Once created, you activate the virtualenv...

... on Windows...
```shell
# When activated, your shell prompt should be prefixed with `(venv)`.
venv/Scripts/activate
```

... or on Linux/Unix/Mac...
```shell
# When activated, your shell prompt should be prefixed with `(venv)`.
source venv/bin/activate
```

Install required dependencies using `pip`...
```shell
pip install -r requirements.txt
```

## Run mitm-censor

You're ready to run mitm-censor now! If all went well, you should be able to run the 
following command to start mitm-censor. On first run, mitm-censor will download the ML models for NudeNet, so let it do that before you try to use it...

```shell
mitmdump -s scripts/mitm-censor.py
```

You can use any of the mitmproxy commands, such as `mitmproxy` or `mitmweb`.

## Configure your proxy settings

Last, but not least, you'll want to configure your proxy settings to point to mitmproxy. By 
default, mitmproxy runs on port `8080`, so you'll want to point your local computer to `127.0.0.1:8080` or
your test device to whatever your internal IP is.

### Windows proxy settings

* Open Settings
* Go to Network and Internet
* Click on Proxy on the left sidebar
* At the bottom, you can enable proxy settings and specify the proxy server's IP address and port

### macOS proxy settings

* Open System Preferences
* Go to Network
* Click on your network connection method (Ethernet, Wi-Fi, etc.) and click Settings
* Go to the Proxies tab
* You can specify the proxy server's IP address and port here

### Other devices

Almost any device with proxy settings is supported. You can find instructions online for iOS, Android, etc. Google is your friend. :)

## Trust mitmproxy's certificate

Once you're connected to the proxy server, you won't be able to access the internet right away. However, you'll know it's working if you point your device's browser to http://mitm.it. This page will only work for you if you're connected to the proxy, and contains instructions for finishing your device setup. Download the certificate for your device's operating system, and follow the instructions carefully. You may need to close and re-open your browser after following the instructions to be able to access the internet again.

Once you've successfully added mitmproxy's certificate to your system, you'll be able to access the internet, and you're successfully running mitm-censor!

## Configuration

The heart of mitm-censor is in a single Python file in `scripts/mitm-censor.py`. Near the top of this file is a `config` object which lets you change the behavior of mitm-censor. Each config option is documented with comments. If you make changes to this script and save it, the script will be reloaded automatically by the mitmproxy instance.
