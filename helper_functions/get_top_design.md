# ```get_top_design```

This is a helper function!

## Purpose

The purpose of this function is to look through the design and find the design of the top-layer..

## Usage

This function is called once just after reading the supplied RTL. Afterwards the ```current_design``` is changed to the returned value, as to ensure the correct starting point for the main script.

## Definition

```tcl
proc get_top_design {} {
    #######################################################################
    # This function looks through all recognised designs, and returns the 
    # design with the most layers
    #
    # input:  none
    # return: top layer design
    #######################################################################

    # create a list of  all designs 
    set designs [get_synopsys_value "list_designs"]
    set designs [lrange $designs 0 end-1]                           ;# removes returned bool from list_design call
    set designs [lsearch -all -inline -exact -not $designs {(*)}]   ;# removes indicator of current design

    # loop through designs, remove designs from list if they are a subdesign of another design
    set top_design ""
    while {[llength $designs] > 0} {
        # set current design to first in list
        set design [lindex $designs 0]
        current_design $design

        # retrieve subdesigns
        set subdesigns [get_synopsys_value "all_designs"]
        set subdesigns [lsearch -all -inline -not [join $subdesigns] $design]

        # remove subdesigns from list
        foreach subdesign $subdesigns {
            set designs [lsearch -all -inline -exact -not $designs $subdesign]
        }

        # change top_design (last man standing is the top design)
        set top_design $design
        set designs [lsearch -all -not -inline -exact $designs $design]
    }

    current_design $top_design
    return $top_design
}
```

This function will only work, if the following function is sourced:

* ```get_synopsys_value```

## Example

Given the hierarchy in the following figure:

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../figures/dark-mode/helper_functions/get_hierarchy.drawio.svg">
  <img alt="Example hierachy." src="../figures/light-mode/helper_functions/get_hierarchy.drawio.svg">
</picture>

Calling the function will return:

```tcl
>> get_top_design
TOP_LAYER
```
