# Setup and project

For the project, we'll write a small Python script for backing up files.

The reason for choosing Python is that it's pretty readable. I would like to reduce the friction in adoption jj as much as I can and I belive using Python as opposed to any other language with more syntax makes readers focus on the VCS and not the language. That, plus Python is usually pre-installed on most devices (or easily obtainable) whereas using C++, Rust or Java requires a more serious effort.

That said, the code that we're about to write is not the most performant and may not adhere to the best practices. It's meant to be simple and readable at a glance in order to showcase `jj` in the best way possible.

## Setup

### 1. Install `jj`

This tutorial is written when `jj` is at version 0.15.1. It may work for later versions, but you also may need to adapt.

For the full range of ways to install `jj`, you can visit the [Installation and Setup](https://martinvonz.github.io/jj/latest/install-and-setup/) page of the official documentation. In short, if you have `cargo` you can do this:

```sh
cargo install jj-cli@0.19.0 --locked
```

If you're not a Rust developer, please read the documentation to figure out how to install things on your platform; I could replicate that information here, but I'm not going to waste your time.

### 2. Create a new folder for the project

```sh
mkdir ~/bak
cd ~/bak
```
