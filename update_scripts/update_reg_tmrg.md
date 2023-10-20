[update_reg_tmrg_figure]: ../figures/update_scripts/update_reg_tmrg.drawio.svg

# ```update_reg_tmrg```

This is an *update* script!

## Purpose

The purpose of this script is to propagate the ```default_tmrg``` attribute value to the ```tmrg``` attribute of all registers within each design.

## Usage

This function is called once after the ```default_tmrg``` attribute has been propagated to or defined on all designs.

## Definition

```tcl
proc update_reg_tmrg { top_design } {
    # loop through all designs (modules) and apply the correct tmrg for every register
    redirect -variable designs {get_designs}
    set designs [join $designs]

    foreach design $designs {

        # 'jump into design' and find default
        current_design $design
        redirect -variable default_tmrg    {get_attribute $design default_tmrg}
        redirect -variable default_tmrg    {get_attribute $design default_tmrg}
        puts $default_tmrg

        # retrieve all registers and apply tmrg (non-overriding)
        redirect -variable registers {all_registers -no_hierarchy}
        set registers [join $registers]
        puts $registers

        # go through each register, update tmrg if not already set
        foreach register $registers {
            redirect -variable tmrg {get_attribute -quiet -return_null_values $register tmrg}
            if {[string length $tmrg] < 1} {
                set_attribute $register tmrg $default_tmrg
            }
            redirect -variable tmrg {get_attribute -quiet -return_null_values $register tmrg}
        }
    }

    # go back to top design
    current_design $top_design
}
```

## Example

Below is a figure of the before and after of this script being called on a simple design. The red outlines mark the targets for the functions, the blue outlines mark the affected elements, the orange text indicates the ```default_tmrg``` or ```tmrg``` attribute is set to true (based on if it's a design or a port), and pink indicates false.

![Default_tmrg propagating to the registers of a design][update_reg_tmrg_figure]
