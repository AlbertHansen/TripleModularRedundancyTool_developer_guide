[set_tmrg_figure]: ../figures/update_scripts/set_tmrg.drawio.svg

# ```set_tmrg```

This is an *update* function!

## Purpose

The purpose of this function is ensure consistency when setting the value of the ```tmrg``` attribute on cells, pins, ports, registers, and module instantiations. Furthermore, this function requires fewer arguments than using ```set_attribute``` (a built-in command).

## Usage

Whenever the ```tmrg``` attribute should be set (not updated!), this function is called.

## Definition

```tcl
proc set_tmrg { value elements } {
    ########################################################################################
    # takes a list of elements and sets their tmrg attribute (nonoverriding)
    #
    # input:  'value' that will be set as the tmrg attribute for all 'elements'
    #         will not override
    # output: nothing
    ########################################################################################

    # run through list of elements, if tmrg is already set, remove from list
    foreach element $elements {
        # check if tmrg is already set, and if so do not override
        set tmrg [get_tmrg $element]
        if {$tmrg > 0} {
            puts "tmrg is already set on $element and it will not be overridden!"
            set elements [lremove $elements $element]
        }
    }

    # set tmrg for remainding elements
    set_attribute $elements tmrg $value
}
```

This function will only work, if the following functions are sourced:

* ```get_tmrg```
* ```lremove```

## Example

In the figure below the red outline marks the target of the function, blue outline marks the affected elements, and the orange text indicates that the ```tmrg``` attributes is set to true. 

```tcl
>> set_tmrg true U1
```

![Example of setting the tmrg attribute][set_tmrg_figure]
