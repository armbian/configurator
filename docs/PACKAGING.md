# Armbian configurator

## Packaging

In order to package a module, the following files are mandatory :

* `armbian/DESC`
* `armbian/${architecture_name_directory}/cli/module/module`

Then you also NEED a DEPS file in either `armbian/` or
`armbian/${architecture_name_directory}/cli`.

`armbian/${architecture_name_directory}/cli/module/module` NEEDS
to be executable.  
If the file is a symlink, the link target needs to be an executable
file.

### Architecture names

**${architecture_name_directory}** is a directory name that
represent an architecture, in the Debian sense.  
Examples of valid architectures directory names are :

* `all`  
  For all architectures. Useful for modules using scripting languages.
* `armv7`  
  For ARMv7 architecture.

You can also target a specific board family, by suffixing the board
family name to the architecture name, with a dot in-between :

For example :

* `armv7.rockchip`  
  This targets Rockchip boards using ARMv7 CPU.

### Most specific architecture

Least specific to most specific architecture names go
like this :

* `${debian_arch}.${armbian_board_family}.${armbian_board_name}`
* `${debian_arch}.${armbian_board_family}`
* `${debian_arch}`

For each architecture directory, the packaging system will
generate specific packages, depending of the presence of the
"cli" "gui" "tui" sub-directories.

Meaning that, if the following directories are present :

* `armbian/all/cli`
* `armbian/all/tui`
* `armbian/arm64`
* `armbian/arm64/cli`
* `armbian/arm64.allwiner`
* `armbian/arm64.allwiner/cli`
* `armbian/arm64.allwiner/gui`

The package will build :

* A CLI package for the architecture "all".
* A TUI package for the architecture "all".
* A CLI package for the architecture "arm64".
* A CLI package for the architecture "arm64", targeting AllWinner boards.
* A GUI package for the architecture "arm64", targeting AllWinner boards.

Note that the files used by the "all" package WILL NOT BE SHARED
with "arm64" or "arm64.allwinner" !  
Same thing, the CLI files from "arm64" WILL NOT BE SHARED with
the files in the "arm64.allwinner".  
Meaning that, in this example, if the same CLI files are used in "all",
"arm64" and "arm64.allwinner", they need to be COPIED OVER AND OVER,
in each "CLI" subdirectory of each architecture.

Also, for any architecture directory, the "cli" subdirectory IS MANDATORY.

### Files used by the packager

The packager will use all the files in the "Armbian" directory to
generate packages.  
The packager will first run the BUILD.sh if there's any, in order to
call a build script that will populate this **armbian** directory with
the right files.  
Then, whether a BUILD script was run or not, the packager will start
the packaging process anyway.

In the **armbian** directory, these are the files that can used by
the packager :

* `BUILD.sh`  
   If present, script is executed by the packager, from the root folder
   of the current module, in order to buildthe module and populate the
   `armbian` folder.  
   Its content will be concatenated with all the other
   specific `BUILD.sh` found.

* `DEPS.build`  
   Set of dependencies required to execute `BUILD.sh` correctly.

* `DEPS_${distribution}.build`
   Distribution specific set of dependencies, required to
   execute `BUILD.sh` correctly.

* `DESC*`  
   The short description of the module and its translations.  
   This will be installed in `/usr/share/armbian/configurator/modules/${module_name}`.  
   **DESC** IS MANDATORY.  
   The translations are not mandatory (`DESC.${locale}`).

* `DEPS`  
   Global list of packages to remove from the dependencies packages
   list, before installing them.  
   See **Dependencies management** afterward.

* `DEPS_${distribution}`  
   A global dependencies file, that will be concatenated with all
   the specifics dependencies files when building a package for
   that specific distribution.  
   See **Dependencies management** afterward.
   Example : `DEPS_ubuntu`.  

* `DEPS_${distribution}.remove`  
   A global list of packages names to remove from the list of
   dependencies packages.   
   See **Dependencies management** afterward.
   Example : `DEPS_ubuntu_2204.remove`

* `POSTINST.sh`  
   Part of the post-installation script that should be executed by
   the package manager, after installing the generated package.  
   See **Post installation scripts** afterward.

Then in each architecture subdirectory, the packager can also use the
the following files :

* `BUILD.sh`  
   This script must be executed by the packaging script, at
   the root folder of the current module, in order to build
   the module.  
   Its content will be concatenated with all the other
   specific `BUILD.sh` found.  
   See **Build phase**

* `DEPS.build`  
   Architecture specific set of dependencies required to
   execute `BUILD.sh` correctly.  
   See **Build phase**

* `DEPS.remove.build`  
   Architecture specific list of packages, to remove from the
   list of packages to install in order to build the module.  
   See **Build phase**

* `DEPS_${distribution}.build`  
   Architecture and distribution specific set of dependencies,
   required to execute `BUILD.sh` correctly.  
   See **Build phase**

* `DEPS_${distribution}.remove.build`  
   Architecture and distribution specific list of packages, to
   remove from the list of packages to install in order to build
   the module.  
   See **Build phase**

* `DEPS`  
   Architecture specific dependencies files, that will be concatenated
   with all the specifics dependencies files.  
   See **Dependencies management** afterward.

* `DEPS.remove`  
   List of packages to remove from the dependencies packages list, before
   installing them.  
   See **Dependencies management** afterward.

* `DEPS_${distribution}`  
   An architecture specific dependencies file, that will be
   concatenated with all the modes specifics dependencies files when
   building a package for that specific distribution.  
   See **Dependencies management** afterward.
   Example : `DEPS_debian`.  

* `DEPS_${distribution}.remove`  
   A global list of packages names to remove from the list of
   dependencies packages.  
   See **Dependencies management** afterward.
   Example : `DEPS_debian_10.remove`

* `POSTINST.sh`  
   Part of the post-installation script that should be executed by
   the package manager, after installing the generated package.  
   See **Post installation scripts** afterward.

Then, in each of the "cli", "tui", "gui" subdirectories, the following files
might be used by the packager :

* `BUILD.sh`  
   This script must be executed by the packaging script, at
   the root folder of the current module, in order to build
   the module.  
   Its content will be concatenated with all the other
   specific `BUILD.sh` found.  
   See **Build phase**

* `DEPS.build`  
   Mode and architecture specific set of dependencies required to
   execute `BUILD.sh` correctly.  
   See **Build phase**

* `DEPS.remove.build`  
   Mode and architecture specific list of packages, to remove from the
   list of packages to install in order to build the module.  
   See **Build phase**

* `DEPS_${distribution}.build`  
   Mode, architecture and distribution specific set of dependencies
   required to execute `BUILD.sh` correctly.  
   See **Build phase**

* `DEPS_${distribution}.remove.build`  
   Mode, architecture and distribution specific list of packages that
   will be removed remove from the list of packages, defined in the
   various `DEPS.build` files.  
   See **Build phase**

* `DEPS`  
   Mode specific dependencies files. 
   See **Dependencies management** afterward.

* `DEPS.remove`  
   List of packages to remove from the dependencies packages list, before
   installing them.  
   See **Dependencies management** afterward.

* `DEPS_${distribution}`  
   Mode specific dependencies file.
   See **Dependencies management** afterward.
   Example : `DEPS_ubuntu`.  

* `DEPS_${distribution}.remove`  
   A global list of packages names to remove from the list of
   dependencies packages.  
   See **Dependencies management** afterward.
   Example : `DEPS_ubuntu_2204.remove`

* `POSTINST.sh`  
   Part of the post-installation script that should be executed by
   the package manager, after installing the generated package.  
   See **Post installation scripts** afterward.

* `module/`  
   The directory containing the files of the module, for that specific mode.  
   **THIS SUBDIRECTORY IS MANDATORY**.  
   **THIS SUBDIRECTORY MUST CONTAIN A `module` EXECUTABLE FILE**.

### Dependencies management

For each of the architecture subdirectory in the `armbian/` directory,
the packager will build a Debian package for each distribution.  
The list of dependencies package names setup in this package are a concatenation
of all the `DEPS` and `DEPS_${distribution}` names found, minus the
list of all the packages found in `DEPS.remove` and `DEPS_${distribution}.remove`.

#### Distributions names

Distribution names come in two forms :

* A global one like.  
  Example : `ubuntu`

* A specific one, where the version is suffixed with an underscore in-between.
  Example : `ubuntu_2204`

Only versions numbers should be supported, since they're clear to everyone.

#### Concatenation

The concatenation should be performed as follow :

* Parse the content of each file.
* In this content :
  * Replace each spacing character (space, tabs, newlines, ...) by a space.
  * Replace each occurence of multiple consecutive spaces by one space.
  * Remove leading and trailing spaces.
* Join all the contents, using one single space character as the delimiter.

#### List of concatenated files

So, when building the 'CLI' package for 'Ubuntu 22.04', architecture 'all', the
following `DEPS` files will be concatenated, if they're found :

* `armbian/DEPS`
* `armbian/DEPS_ubuntu`
* `armbian/DEPS_ubuntu_2204`
* `armbian/all/DEPS`
* `armbian/all/DEPS_ubuntu`
* `armbian/all/DEPS_ubuntu_2204`
* `armbian/all/cli/DEPS`
* `armbian/all/cli/DEPS_ubuntu`
* `armbian/all/cli/DEPS_ubuntu_2204`

Then the following `DEPS.remove` files will be concatenated if they're found :

* `armbian/DEPS_ubuntu.remove`
* `armbian/DEPS_ubuntu_2204.remove`
* `armbian/all/DEPS.remove`
* `armbian/all/DEPS_ubuntu.remove`
* `armbian/all/DEPS_ubuntu_2204.remove`
* `armbian/all/cli/DEPS.remove`
* `armbian/all/cli/DEPS_ubuntu.remove`
* `armbian/all/cli/DEPS_ubuntu_2204.remove`

Then, all the packages obtained through `DEPS.remove` files will be removed
from the list `DEPS` packages.

#### Example

Let's say that concatenating all the `DEPS` files lead to the
following list :

`docker docker.io docker-compose python3 libpng14 libpng16-16`

Then let's say that concatenating all the `DEPS.remove` files lead to the
following list :

`docker libpng14`

Then the final list will of packages, that will be marked as DEPENDENCIES in
the generated Debian package will be :

`docker.io docker-compose python3 libpng16-16`

### Post-installation scripts

All the `POSTINST.sh` parts found are to be concatenated together.  
This time, the process is as follows :

* If any `POSTINST.sh` file is present :
  * Parse the content of each `POSTINST.sh` found
  * Prepare the following string :  
  `#!/bin/bash`
  * Join this string with all the other contents, using a newline
    character as the separator ('\n`).

For example, when building the 'GUI' package for 'Ubuntu 22.04',
architecture 'arm64', the following `POSTINST.sh` needs to be concatenated,
if they're found :

* `armbian/POSTINST.sh`
* `armbian/arm64/POSTINST.sh`
* `armbian/arm64/gui/POSTINST.sh`

These files need to be parsed in that, least-specific to most-specific order.

Let's say that all these three files exist and their contents goes like this :

**armbian/POSTINST.sh**

```bash
echo "Generic post-install script"
```

**armbian/arm64/POSTINST.sh**

```bash
echo "Architecture specific post-install script"
```

**armbian/arm64/gui/POSTINST.sh**

```bash
echo "GUI specific post-install script"
```

Then the content of the final POSTINST.sh used in the Debian package should
be as follows :

```bash
#!/bin/bash
echo "Generic post-install script"
echo "Architecture specific post-install script"
echo "GUI specific post-install script"
```

Note that `POSTINST.sh` are NOT MANDATORY.  
ONLY CREATE THESE FILES IF YOU NEED THEM.

### Module contents

The content of the modules should be located in :
* `armbian/${architecture}/${mode}/module/`

The main entry point for the module MUST be :
* `armbian/${architecture}/${mode}/module/module`

For each mode, the `module` executable file MUST EXIST.  
If the file does not exist, this module mode should be considered as
INVALID.

CLI modules subdirectories are mandatory for each architecture
found in `armbian/`.  

The content of this folder will be copied as-is in the following
directory when installing the package :  
`/usr/share/armbian/configurator/modules/${module_name}/${mode}`

Each module content should be considered as "standalone" and should
not depend on the presence of another submodule in the parent
directory or whatever.   
If dependencies are shared, they need to be copied in each single
`armbian/${architecture}/${mode}/module/` directory.  
If multiple modules depend on the same set of functions,
assemble them as a library, make this library a Debian package installable
on Armbian systems, and write the library package name inside `DEPS` files.

### DESC files

The DESC files will be copied in
`/usr/share/armbian/configurator/modules/${module_name}/` upon installation
of the package.

These files contain a short description of the module.  
These files are read by the **configurator** and shown to the user, when listing
the avaiable modules.

The `DESC` file IS MANDATORY.  
The package WILL NOT BE BUILT IF THIS FILE IS NOT PRESENT.

You can also add optional translations, by either suffixing the
global locale name or precise locale name pertaining to the language
of this translation.

For example, the content of the file `DESC.fr` will be shown by
**configurator** to all users defining a locale starting by `fr`
(Example : `fr_FR`, `fr_BE`, `fr_CA`, ...).

Another example, the file `DESC.zh_CN` will be only shown to the
users of the **configurator** using `zh_CN` as their locale.

The **configurator** will always show the most specific DESC
translation to the user.  

#### Example

If :
* a user with the locale `fr_CA` is executing the **configurator**;
* the scanned module provide following files DESC files :
  * `DESC`
  * `DESC.fr`
  * `DESC.fr_CA`

Then, the content of the `DESC.fr_CA` will be shown to the user.

Using the same directory configuration, if the user changes its
locale to `fr_FR`, then the **configurator** will show the content of
`DESC.fr`.  

Following, if the user changes its locale to `en_US`, then the
**configurator** will show the content of `DESC`.

### Build phase

The `BUILD.sh` is OPTIONAL.  
If present, it will be run by the packager, in order to populate
the `armbian` directory.  

The current working directory when executing the script is the
root of the module.  

If the script is present, before executing the script, the packager
will install the list of packages resulting from the concatenation
of `DEPS.build` and `DEPS_${distribution}.build`, mine the list of
packages resulting from the concatenation `DEPS.remove.build` and
`DEPS_${distribution}.remove.build` files.

Failing to install any of the packages, in the final list, will
fail the entire packaging process.

#### Concatenation of the dependencies

> The concatenation process is identical to the one described in
**Dependencies management**.

The concatenation should be performed as follow :

* Parse the content of each file.
* In this content :
  * Replace each spacing character (space, tabs, newlines, ...) by a space.
  * Replace each occurence of multiple consecutive spaces by one space.
  * Remove leading and trailing spaces.
* Join all the contents, using one single space character as the delimiter.

#### Example

So, when building the 'TUI' package for 'Debian 11', architecture 'armv7', the
following `DEPS.build` files will be concatenated, if they're found :

* `armbian/DEPS.build`
* `armbian/DEPS_debian.build`
* `armbian/DEPS.debian_11.build`
* `armbian/armv7/DEPS`
* `armbian/armv7/DEPS_debian.build`
* `armbian/armv7/DEPS_debian_11.build`
* `armbian/armv7/tui/DEPS`
* `armbian/armv7/tui/DEPS_debian.build`
* `armbian/armv7/tui/DEPS_debian_11.build`

Then the following `DEPS.remove.build` files will be concatenated
if they're found :

* `armbian/DEPS_debian.remove.build`
* `armbian/DEPS_debian_11.remove.build`
* `armbian/armv7/DEPS.remove.build`
* `armbian/armv7/DEPS_debian.remove.build`
* `armbian/armv7/DEPS_debian_11.remove.build`
* `armbian/armv7/tui/DEPS.remove.build`
* `armbian/armv7/tui/DEPS_debian.remove.build`
* `armbian/armv7/tui/DEPS_debian_11.remove.build`

If the concatenation of the `DEPS.build` files result in the
following list :

`gcc-9 gcc-10 make python3`

And the concatenation of the `DEPS.remove.build` files result in
the following list :

`gcc-9 python3`

Then the final list of packages installed, before running the
`BUILD.sh` script will be :

`gcc-10 make`

### Concatenation of the BUILD.sh parts

> The process is identical to the one used in
**Post installation scripts**

* If any `BUILD.sh` file is present :
  * Parse the content of each `BUILD.sh` found
  * Prepare the following string :  
  `#!/bin/bash`
  * Join this string with all the other contents, using a newline
    character as the separator ('\n`).

The order of concatenation of these scripts MUST be least-specific to
most-specific.

### Example

For example, when building the 'TUI' package for 'Debian 12',
architecture 'armv7', the following `BUILD.sh` needs to be
concatenated, if they're found :

* `armbian/BUILD.sh`
* `armbian/arm64/BUILD.sh`
* `armbian/arm64/gui/BUILD.sh`

If any of these files are found, then the following `DEPS.build` files
need to be concatenated :

* `armbian/DEPS.build`
* `armbian/DEPS_debian.build`
* `armbian/DEPS.debian_12.build`
* `armbian/armv7/DEPS`
* `armbian/armv7/DEPS_debian.build`
* `armbian/armv7/DEPS_debian_12.build`
* `armbian/armv7/tui/DEPS`
* `armbian/armv7/tui/DEPS_debian.build`
* `armbian/armv7/tui/DEPS_debian_12.build`

And then the following potentials `DEPS.remove.build` need to be
concatenated too :

* `armbian/DEPS_debian.remove.build`
* `armbian/DEPS_debian_12.remove.build`
* `armbian/armv7/DEPS.remove.build`
* `armbian/armv7/DEPS_debian.remove.build`
* `armbian/armv7/DEPS_debian_12.remove.build`
* `armbian/armv7/tui/DEPS.remove.build`
* `armbian/armv7/tui/DEPS_debian.remove.build`
* `armbian/armv7/tui/DEPS_debian_12.remove.build`

The packages listed in the `DEPS.remove.build` are then to be removed
from the list of packages obtainted from the `DEPS.build` files.  
The final packages list is then installed by the packager before
running the script resulting from the concatenation of the `BUILD.sh`
scripts.

