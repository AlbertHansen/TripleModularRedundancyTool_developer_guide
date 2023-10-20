[update_design_default_tmrg_figure]: ../figures/update_scripts/update_design_dault_tmrg.drawio.svg

# ```update_design_default_tmrg```

This is an *update* script!

## Purpose

This script propagates the value of ```default_tmrg``` to lower layers of the hierarchy starting from the top design.

## Usage

This script is called once before any of the other *update* scripts/functions. This is due to ```default_tmrg``` being the default value for the ```tmrg``` attribute.

It is important to distinguish between module instantiations and designs. Designs are the blueprint for the module instantiations and the attributes are NOT SHARED between the two!

## Definition

```tcl
proc update_design_default_tmrg { } {
    #################################################################################
    # This function looks through the instances from the top design, and
    # assigns the appropriate default_tmrg on the DESIGNS! If contradictory 
    # default_tmrg exists, the DESIGN will be copied and treated as an
    # individual
    #
    # input:  nothing
    # output: nothing
    #################################################################################

    set top_design  [get_top_design]
    set top_default [get_synopsys_value "get_attribute -quiet $top_design default_tmrg"]
    set hierarchy   [get_hierarchy]
    set hierarchy   [lreverse $hierarchy]

    foreach level $hierarchy {
        foreach instance $level {
            # retrieve design for the instance and its associated default_tmrg
            set design       [get_synopsys_value "get_attribute -quiet $instance ref_name"]
            set default_tmrg [get_synopsys_value "get_attribute -quiet $design   default_tmrg"]

            # if default_tmrg is not set, or it was set from parent, update it (potentially creating another design)
            set default_from_parent [get_synopsys_value "get_attribute -quiet -return_null_values $design default_from_parent"]
            if { [string length $default_tmrg] < 1 || $default_from_parent == "true" } {

                # retrieve parent default_tmrg 
                set parent         [join [lrange [split $instance "/"] 0 end-1] "/"] 
                set parent_default ""
                if {[string length $parent] > 0} {  ;# if parent is found
                    set parent         [get_synopsys_value "get_attribute -quiet $parent ref_name"] 
                    set parent_default [get_synopsys_value "get_attribute -quiet $parent default_tmrg"]
                } else {                            ;# if parent is not found, use default from top design
                    set parent_default $top_default
                }

                # if default was already set from another parent (checking from another instance)
                # verify that the default_tmrg is the same, otherwise generate a new design, with the other 
                # type of default_tmrg
                if {$default_from_parent == "true"} {
                    if {$default_tmrg != $parent_default} {
                        set new_design   [join [list $design   $parent_default] "_"]
                        set new_instance [join [list $instance $parent_default] "_"]
                        copy_design $design $new_design
                        create_cell -hierarchical $new_instance $new_design
                        replace_cell $instance $new_instance "true"
                    }
                } else {
                    set_attribute $design default_tmrg        $parent_default
                    set_attribute $design default_from_parent true
                }

            }

            # set tmrg on instance if not already set
            set tmrg [get_tmrg $instance]
            if {$tmrg == -1} {
                set parent_default ""
                if {[string length $parent] > 0} {  ;# if parent is found
                    set parent         [get_synopsys_value "get_attribute -quiet $parent ref_name"] 
                    set parent_default [get_synopsys_value "get_attribute -quiet $parent default_tmrg"]
                } else {                            ;# if parent is not found, use default from top design
                    set parent_default $top_default
                }
                set_attribute $instance tmrg $parent_default
            }

        }
    }
}
```

This function will only work, if the following functions are sourced:

* ```get_top_design```
* ```get_synopsys_value```
* ```get_hierarchy```
* ```get_tmrg```
* ```get_synopsys_value```

## Example

The figure below depicts the propagation of the ```default_tmrg``` attribute through a hierarchy. Orange colour indicates that the ```default_tmrg``` attribute is set to true, whereas pink means false.

![Example of the default_tmrg attribute propagating through a hierarchy][update_design_default_tmrg_figure]

Notice that the attribute is already defined for DESIGN_2, and it will not be overridden, but rather the value will propagate to designs contained in DESIGN_2
