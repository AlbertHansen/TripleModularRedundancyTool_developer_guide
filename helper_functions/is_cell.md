[is_cell_figure]: ..\figures\helper_functions\is_cell.drawio.svg

# ```ìs_cell```

This is a helper function!

## Purpose

The purpose of this function is to check if an element is a cell.

## Usage

This function is utilised in the ```get_replicants``` function, as this function will handle pins/ports/cells and must be able to distinguish between these.

## Definition

```tcl
proc is_cell { element } {
    ######################################################
    # in get_replicants, it is important to know,
    # if it is looking for cell or other. cells
    # include instances in this case
    #
    # input:  an existing element from the design
    # output: true/false based on whether the input
    #         is a cell or not
    ######################################################
    
    # checks if a cell exists with that name 
    set cell [get_synopsys_value "get_cells -quiet $element"]

    # if a port exist with that name and it contains no "/" return true, 
    # otherwise return false
    if {[llength $cell] > 0} {
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
>> is_cell U1
true
>> is_cell OUT1
false
>> is_cell U1/A
false
```

Notice that calling this function on a pin of a cell will also return *false*!