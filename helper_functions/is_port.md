[is_cell_figure]: ..\figures\helper_functions\is_cell.drawio.svg

# ```ìs_port```

This is a helper function!

## Purpose

The purpose of this function is to check if an element is a port. Ports and their default associated nets are of the same name, and when one or the other is returned as a value, they are not easily distinguishable. Furthermore, ports and pins are similar in nature, but should be treated differently.

## Usage

This function is used anytime the discrepancy between pins and ports is important, which is especially the case when looking for driven/driver connection, as an output port is *driven* whereas an output pin *drives*. It is also used when distinguishing between nets and ports of the same name.

## Definition

```tcl
proc is_port { element } {
    ######################################################
    # pins and ports are treated differently, 
    # since the port is not associated with a cell
    #
    # input:  an existing element from the design
    # output: true/false based on whether the input
    #         is a port or not
    ######################################################
    
    # checks if a port exists with that name 
    set ports [get_synopsys_value "get_ports -quiet $element"]
    set path  [split $element "/"]

    # if a port exist with that name and it contains no "/" return true, 
    # otherwise return false
    if {[llength $ports] > 0 && [llength $path] < 2} {
        return true
    } else {
        return false
    }
}
```

## Example

Given a circuit:

![Example hierachy.][is_cell_figure]

Calling the function on some of the elements will yield:

```tcl
>> is_port U1
false
>> is_port OUT1
true
>> is_cell U1/A
false
```

Notice that calling this function on a pin of a cell will also return *false*!
