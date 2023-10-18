# ```get_replicants```

This is a helper function!

## Purpose

The purpose of this function is to make it more manageable to find replicant pins, ports, registers, cells, and module instantiations. In the case of module instantiations the instantiation and/or its pins can be triplicated, regardless, this function will return all of the replicants

## Usage

During the rewire process this function is heavily used, as it provides a simple way to retrieve all replicants of some element.

## Definition

```tcl
proc get_replicants { element } {
    #############################################################################
    # finds every replication of an element, be it
    # a triplicated cell, on a triplicated cell, or
    # both. Does not look across hierarchies.
    #
    # input:  element (cell/pin/instance/register)
    # output: replicants (1, 3, or 9)
    #############################################################################

    # cells (without pins)
    if {[is_cell $element]} {
        set tmrg [get_tmrg $element]
        if {$tmrg != "true"} {
            return $element
        }

        # remove suffix A, B, ...
        set base [join [lrange [split $element "_"] 0 end-1] "_"]

        # change all "[]", to ".", to help the regexp
        set l_bracket [string first "\[" $base]
        set r_bracket [string first "\]" $base]
        while {$l_bracket != -1 || $r_bracket != -1} {
            set base        [string replace $base $l_bracket $l_bracket "."]
            set base        [string replace $base $r_bracket $r_bracket "."]
            set l_bracket   [string first "\[" $base]
            set r_bracket   [string first "\]" $base]
        }
        set regex [join [list $base "\\\[ABC\\\]" ] "_"]

        # find the replicants based on the regexp
        puts "THIS IS THE REGEXP: $regex"
        set replicants [get_synopsys_value "get_cells -quiet -regexp $regex"]

        return [lsort -increasing $replicants]
    }

    # ports
    if {[is_port $element]} {
        set tmrg [get_tmrg $element]
        if {$tmrg != "true"} {
            return $element
        }

        # remove suffix A, B, ...
        set base [join [lrange [split $element "_"] 0 end-1] "_"]

        # change all "[]", to ".", to help the regexp
        set l_bracket [string first "\[" $base]
        set r_bracket [string first "\]" $base]
        while {$l_bracket != -1 || $r_bracket != -1} {
            set base        [string replace $base $l_bracket $l_bracket "."]
            set base        [string replace $base $r_bracket $r_bracket "."]
            set l_bracket   [string first "\[" $base]
            set r_bracket   [string first "\]" $base]
        }
        set regex [join [list $base "\\\[ABC\\\]" ] "_"]

        # find the replicants based on the regexp
        puts "THIS IS THE REGEXP: $regex"
        set replicants [get_synopsys_value "get_ports -quiet -regexp $regex"]

        return [lsort -increasing $replicants]
    }

    # pins (potentially on cells)
    set cell      [get_synopsys_value "cell_of $element"]
    set pin       [lindex [split $element "/"] end]
    set cell_tmrg [get_tmrg $cell]
    set pin_tmrg  [get_tmrg $element]

    # create regexp 
    set regex ""
    if {$cell_tmrg != "true"} {

        # use the basic cell 
        set regex [join [list $regex $cell] ""]

    } else {

        # remove suffix A, B, ...
        set base [join [lrange [split $cell "_"] 0 end-1] "_"]

        # change all "[]", to ".", to help the regexp
        set l_bracket [string first "\[" $base]
        set r_bracket [string first "\]" $base]
        while {$l_bracket != -1 || $r_bracket != -1} {
            set base        [string replace $base $l_bracket $l_bracket "."]
            set base        [string replace $base $r_bracket $r_bracket "."]
            set l_bracket   [string first "\[" $base]
            set r_bracket   [string first "\]" $base]
        }
        set regex [join [list $base "\\\[ABC\\\]" ] "_"]
        
    }
    if {$pin_tmrg != "true"} {

        # use the basic pin
        set regex [join [list $regex $pin] "/"]

    } else {

        # remove suffix A, B, ...
        set base [join [lrange [split $pin "_"] 0 end-1] "_"]

        # change all "[]", to ".", to help the regexp
        set l_bracket [string first "\[" $base]
        set r_bracket [string first "\]" $base]
        while {$l_bracket != -1 || $r_bracket != -1} {
            set base        [string replace $base $l_bracket $l_bracket "."]
            set base        [string replace $base $r_bracket $r_bracket "."]
            set l_bracket   [string first "\[" $base]
            set r_bracket   [string first "\]" $base]
        }
        set pin_regex [join [list $base "\\\[ABC\\\]" ] "_"]
        set regex [join [list $regex $pin_regex] "/"]

    }

    # find the replicants based on the regexp
    puts "THIS IS THE REGEXP, vi er her, right: $regex"
    set replicants [get_synopsys_value "get_pins -quiet -regexp $regex"]

    return [lsort -increasing $replicants]
}
```

This function will only work, if the following functions are sourced:

* ```is_cell```
* ```is_port```
* ```get_tmrg```
* ```get_synopsys_value```

## Example

Given a triplicated *cell*, calling the function on the cell itself will yield:

```tcl
>> get_replicants U1_A
U1_A U1_B U1_C
```

Given a triplicated *cell*, calling the function on one of its pins will yield:

```tcl
>> get_replicants U1_A/Z
U1_A/Z U1_B/Z U1_C/Z
```

Given a triplicated *module instantiation* with triplicated pins, calling the function on one of its pins will yield:

```tcl
>> get_replicants inst0_A/out_A
inst0_A/out_A inst0_A/out_B inst0_A/out_C inst0_B/out_A inst0_B/out_B inst0_B/out_C inst0_C/out_A inst0_C/out_B inst0_C/out_C
```
