Version: 1
Status: DRAFT

# Status

While this tutorial will explain you how to start coding your own
module, it won't be prepared for packaging...

TODO : Add a 'build' script example that make the whole thing ready
for packaging.

# Main design

## Coding your own CLI module

1. Create a directory where you'll put the CLI module code and `cd` into it.  
   Example :  
```bash
mkdir -p ~/Documents/my_armbian_module
cd ~/Documents/my_armbian_module
```

2. Create a file named `DESC` and write a short description for this module.  
```bash
echo "Best module ever" > DESC
```

3. Add a `module` file and ensure it is executable.  
   This file will be the one executed by the configurator when running
   your module.  
```bash
echo '#!/bin/bash' > module
echo "echo 'I told you, best module ever \!'" >> module
chmod +x module
```

4. Create the directory `/usr/share/armbian/configurator/modules/${module_name}/cli`  
   Example, if your module is named 'my_module' :  
```bash
module_name=my_module
sudo mkdir -p "/usr/share/armbian/configurator/modules/${module_name}"
```
5. Link the `DESC` file to `/usr/share/armbian/configurator/modules/${module_name}/DESC`  
```bash
module_name=my_module
sudo ln -s "${PWD}/DESC" "/usr/share/armbian/configurator/modules/${module_name}/DESC"
```
6. Link the directory itself to `/usr/share/armbian/configurator/modules/${module_name}/cli`  
```bash
module_name=my_module
sudo ln -s "${PWD}" "/usr/share/armbian/configurator/modules/${module_name}/cli"
```

Now, the module is recognized by the configurator.

Launch the configurator without arguments to see your module in the list.  
Launch the configurator with the name of your module to launch it :

```bash
module_name=my_module
configurator ${module_name}
```

```
I told you, best module ever !
```

## Adding a GUI (X11/Wayland) to your module

1. Create a directory where you'll put the GUI executable of your module.
2. Make sure your GUI executable name is named `module`
3. Link it to `/usr/share/armbian/configurator/modules/${module_name}/gui`

You're done

## Adding a translation to the short description

To add a translation for a module description, add a `DESC.{locale}` file
to `/usr/share/armbian/configurator/modules/${module_name}/`

Precise locales are sampled before global ones, however
avoid using precise locales names when you can.

### Example

Let's say you want to add a French translation for a module description.

French locales start with `fr`.  
French locale for people living in France specifically is : `fr_FR`.  
French locale for people living in Canada specifically is : `fr_CA`.

So, if you want to add a french translation, add either a
`DESC.fr` or `DESC.fr_FR` file.

If you add both `DESC.fr_FR` and `DESC.fr`, the system will use :

* `DESC.fr_FR` for people using the `fr_FR` locale.  
* `DESC.fr` for people using `fr_CA` locale.

If you only add `DESC.fr`, the system will use :

* `DESC.fr` for people using the `fr_FR` locale.  
* `DESC.fr` for people using `fr_CA` locale.

if you only add `DESC.fr_FR`, the system will use :

* `DESC.fr_FR` for people using the `fr_FR` locale.  
* `DESC` (default english version) for people using the `fr_CA` locale.

## Prepare for packaging

In order to prepare the module for packaging, see **PACKAGING.md**.