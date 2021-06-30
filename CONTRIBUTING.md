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

```shell
# When activated, your shell prompt should be prefixed with `(venv)`.
venv/Scripts/activate
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

