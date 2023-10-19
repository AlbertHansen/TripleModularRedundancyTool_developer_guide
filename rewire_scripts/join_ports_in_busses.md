[join_in_busses_figure]: ../figures/rewire_scripts/join_ports_in_busses.drawio.svg

# ```join_ports_in_busses```

This is a *rewire* script!

## Purpose

The purpose of this script is to maintain overview when viewing a triplicated design through Design Vision.

## Usage

This script is called after triplicating the ports of a design to reduce the amount of individual ports.

## Definition

```tcl
proc join_ports_in_busses {} {
    #####################################################################################
    # joins triplicated ports in appropriate busses. Covers all ports in current design
    #
    # input:  none
    # output: none
    #####################################################################################

    set ports [get_synopsys_value "get_ports"]
    set list_of_busses {}                       ;# empty list to store names of unique busses

    foreach port $ports {

        # find appropriate name for bus
        set l_bracket  [string first "\[" $port ]
        set r_bracket  [string first "\]" $port ]
        set identifier [string range $port 0 [expr $l_bracket - 1] ]
        set suffix     [string range $port [expr $r_bracket + 1] end]
        set bus_name   [string cat $identifier $suffix]

        # if no [] it won't be a part of a bus
        if { ( $l_bracket < 0 ) || ( $r_bracket < 0 ) } {
            continue
        }

        # add new bus to list if does not exist
        set list_of_busses_index_match [lsearch -exact $list_of_busses $bus_name]
        if { $list_of_busses_index_match < 0 } {  ;#no match
            lappend list_of_busses $bus_name
            set list_of_busses_index_match [lsearch -exact $list_of_busses $bus_name]   ;# update index after new entry has been created
        } 

        # add entry to bus
        lappend [lindex $list_of_busses $list_of_busses_index_match] $port
    }

    for {set i 0} { $i < [llength $list_of_busses]} {incr i} {
        # retrieve sublist from list_of_busses
        eval set bus_list_sublist $[lindex $list_of_busses $i]
        set bus_list_sublist [lsort -increasing $bus_list_sublist]

        # join bus
        create_bus $bus_list_sublist [lindex $list_of_busses $i]
    }
}
```

This function will only work, if the following function is sourced:

* ```get_synopsys_value```

## Example

![Before and after ports are joined in busses][join_in_busses_figure]
