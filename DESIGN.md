Version: 1
Status: DRAFT

# Main design

## Adding a module

For each module you want to add :

1. Create a directory inside `modules/`.
2. Inside this directory add the following files :
    1. **module.cli**  
    The CLI version of the module that will be executed by default.  
    This can be symlinked to system binaries, if you know what you're
    doing.
    2. **DESC**  
    A description of the module.  
    The first line should be brief, as it is shown in the list
    provided by the main **configurator**, when listing all the modules.
    3. **armbian/cli/DEPS**  
    The list of additional Debian packages required to execute `module.cli`.  
    Only put the dependencies that are not required by the **configurator**
    itself.

## Adding a GUI (X11/Wayland) to a module

Adding a GUI to a module, inside `modules/{module_name}`,
you need to add :

1. **module.gui**  
The GUI version of the module.
2. **armbian/gui/DEPS**  
The list of additional Debian packages required to execute `module.gui`.  
Only put the dependencies that are not required by the **configurator**
itself.  
Dependencies shared with the CLI version still need to be written.

> **Symlinking to `module.cli`**
>
> It is possible to have a single executable managing
> both CLI and GUI, but remember that the CLI version
> **MUST NOT** depend on GUI libraries.  
> For example, you cannot ask for QT/GTK/OpenGL for CLI
> softwares.
>
> Which mean that single executables managing CLI and
> GUI must load GUI libraries dynamically.  
> For scripting languages, you can branch load the
> libraries after a few sanity checks.  
> For compiled languages, you'll need to deal with
> dynamically loaded libraries.
>
> So, think again before putting both in the same executable.
> Having two executables sharing the same configuration
> files and codebase might be far easier.

## Adding a translation

> Support for this feature will be added very soon

To add a translation for a module description,
inside `modules/{module_name}`, create a `DESC.{locale}` file.

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

