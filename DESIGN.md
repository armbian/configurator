Version: 1
Status: DRAFT

# Main design

## Adding a simple module directly on your system

For each module you want to add :

1. Create the following subdirectory :  
`/usr/share/armbian/configurator/modules/${module_name}/cli` .
2. Copy your module executable file to :  
`/usr/share/armbian/configurator/modules/${module_name}/cli/module` .  
The file can actually be an absolute symlink to a system executable
file too.
3. Write a short description of the module in  
`/usr/share/armbian/configurator/modules/${module_name}/DESC` .

That's about it.  

For deveopment purposes, you might want to actually symlink
`/usr/share/armbian/configurator/modules/${module_name}` to
a development directory inside your home directory.  
For example :
`sudo ln -s /usr/share/armbian/configurator/modules/${module_name} /home/YourUserName/module_name`

## Adding a GUI (X11/Wayland) to a module

1. Create the directory :  
`/usr/share/armbian/configurator/modules/${module_name}/gui`

2. Add at least the executable file to :  
`/usr/share/armbian/configurator/modules/${module_name}/gui/module`

Then copy all the files required by the GUI into its specific folder,  
`/usr/share/armbian/configurator/modules/${module_name}/gui`.

## Adding a translation to the short description

To add a translation for a module description,
add a `DESC.{locale}` file to
`/usr/share/armbian/configurator/modules/${module_name}/`

Precise locales are sampled before global ones, however
avoid using precise locales names when you can.

### Example

Let's say you want to add a French translation for a module
description.

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