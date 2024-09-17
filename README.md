# Chiri (チリ)

Chiri (Japanese for the country "Chile") is a meta-build system, that is
designed as a scaffold over existing build systems. It is modeled very loosely
after Brazil which is used internally at Amazon.

This is mostly a personal pet project and personal workflow tool. I don't
plan to expand its feature set to dependency modeling.

## Design

Chiri is a CLI that is invoked via a package-agnostic interface
(e.g. `build`, `test`, `release`, `install`) to invoke the underlying build
system for that package (e.g. CMake). A Chiri-compatible package contains
two things:

* `build_tools/bin`: A directory housing an executable script that invokes the
underlying build system. By convention, it is written in Python but does not
need to be.
* `chiri_config.json5`: A JSON5 config pointing to the executable script
mentioned above as an entry point, as well as other config variables.

## Dependencies

* Python 3.8
* pyjson5

## How to install

The CLI must be bootstrapped as a first install.

```bash
cd chiri
./bootstrap.sh
```

Installation is located by default at `~/.chiri`. The path to the Chiri CLI
must be added to your PATH (ZShell as an example below):

```bash
echo 'export PATH="${PATH}:~/.chiri/bin"' >> ~/.zshrc
```

Afterwards, it can be installed via the CLI itself.

```bash
cd chiri
chiri pkg release
```

## How to invoke a package's build CLI

The Chiri CLI's command `package` (or `pkg`) reads the working directory's
Chiri config and invokes its executable build entry point.

This uses [mamba](https://github.com/antonsynd/mamba) as an example:

```bash
cd mamba
chiri pkg build
chiri pkg test
```
