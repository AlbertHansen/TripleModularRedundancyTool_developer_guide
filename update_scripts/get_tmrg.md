[get_tmrg_figure]: ../figures/update_scripts/get_tmrg.drawio.svg

# ```get_tmrg```

This is an *update* function!

## Purpose

The purpose of this function is ensure consistency when querying for the value of the ```tmrg``` attribute. Furthermore, this function requires fewer arguments than using ```get_attribute``` (a built-in command).

## Usage

Whenever the ```tmrg``` attribute is needed, this function is called; when triplicating the return value of this function dictates whether or not triplication will occur.

## Definition

```tcl
proc get_tmrg { element } {
    ###############################################################
    # replaces the need for 'redirect -variable..'
    #
    # input:  any cell/port/pin/register
    # output: return the value of the tmrg attribute of the element,
    #         will return -1 if tmrg is not set
    ###############################################################

    # retrieve tmrg attribute
    set tmrg [get_synopsys_value "get_attribute -quiet -return_null_values $element tmrg"]

    # check if tmrg is boolean, return -1 if not
    if {[string is boolean $tmrg] && [string length $tmrg] > 0} {
        return $tmrg
    } else {
        return -1
    }
}
```

This function will only work, if the following function is sourced:

* ```get_synopsys_value```

## Example

Given the incomplete design in the figure below, calling ```get_tmrg``` on some elements will yield:

```tcl
>> get_tmrg IN
false
>> get_tmrg inst0
false
>> get_tmrg inst0/IN_A
true
>> get_tmrg des0_A
true
>> get_tmrg des0_A/IN
false
```

The text marked in orange marks triplicated elements.

![Setup for calling get_tmrg][get_tmrg_figure]
