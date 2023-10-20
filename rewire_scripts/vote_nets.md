# ```vote_nets```

This is a *rewire* script!

## Purpose

The purpose of this script is to enable throughput voting using suffixed net-names. By suffixing net-names in the RTL design with "_Voted" this script fetch these nets, and create a throughput vote (3 inputs, 3 voters, 3 outputs).

## Usage

This script is called after ```rewire_duped_cells``` and ```rewire_input_ports```, as these scripts will check if involved nets are suffixed with "_Voted", and if so the replicants of both driving and driven connections will all be connected to one net and the net name will not be changed. The script fetches these nets and inserts 3 voters and rewires all connections on the net.

## Definition

```tcl
proc vote_nets {} {
    ###############################################################################
    # This script will find all nets suffixed with "_Voted" and insert
    # 3 voters and rewire every connection to create throughput voting
    #
    # input:  none
    # output: none
    ###############################################################################

    # retrieve nets from design and filter as to only have suffix _Voted
    set nets [get_synopsys_value "get_nets -quiet"]
    set nets [lsearch -all -inline -regexp $nets {\S+_Voted}]

    foreach net $nets {
        # separate driver- and driven pins/ports
        set net_connections [get_synopsys_value "all_connected [get_nets $net]"]
        set driver ""
        set driven ""
        foreach connection $net_connections {
            if {[is_port $connection]} {
                set direction [get_synopsys_value "get_attribute [get_ports $connection] pin_direction"]
                disconnect_net [get_nets $net] [get_ports $connection]
                if {$direction == "in"} {
                    set driver [join [list $driver $connection]]
                } else {
                    set driven [join [list $driven $connection]]
                }
            } else {
                set direction [get_synopsys_value "get_attribute [get_pins $connection] pin_direction"]
                disconnect_net [get_nets $net] [get_pins $connection]
                if {$direction == "out"} {
                    set driver [join [list $driver $connection]]
                } else {
                    set driven [join [list $driven $connection]]
                }
            }
        }

        # separate driven pins/ports by suffix
        set driven_A ""
        set driven_B ""
        set driven_C ""
        foreach connection $driven {
            set cell [get_synopsys_value "cell_of $connection"]
            set cell [regexp -all -inline {\S+_[ABC]} $cell]
            if {[llength $cell] > 0} {
                set suffix [lindex [split $cell "_"] end]
                if {$suffix == "A"} {
                    set driven_A [join [list $driven_A $connection]]
                } elseif {$suffix == "B"} {
                    set driven_B [join [list $driven_B $connection]]
                } elseif {$suffix == "C"} {
                    set driven_C [join [list $driven_C $connection]]
                }

                set $driven [lremove $driven $connection]
            }
        }

        # create voting circuit
        create_voter $driver [list [lindex $driven_A 0] [lindex $driven_B 0] [lindex $driven_C 0]]

        # connect the last cells to corresponding voter output
        set driver_A [get_driver_connection [lindex $driven_A 0]]
        set driver_B [get_driver_connection [lindex $driven_B 0]]
        set driver_C [get_driver_connection [lindex $driven_C 0]]
        for {set i 1} {$i < [llength $driven_A]} {incr i} {
            connect $driver_A [lindex $driven_A $i]
            connect $driver_B [lindex $driven_B $i]
            connect $driver_C [lindex $driven_C $i]
        }
    }
}
```

This function will only work, if the following functions are sourced:

* ```get_synopsys_value```
* ```lremove```
* ```get_replicants```
* ```get_driver_connection```
* ```connect```

## Example

The figure below is an example of the before and after of running this script. Three voters (marked with blue) are inserted on a net suffixed with "_Voted" (marked in red).

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../figures/dark-mode/rewire_scripts/vote_nets.drawio.svg">
  <img alt="A small example of a net being voted using the vote_nets routine" src="../figures/light-mode/rewire_scripts/vote_nets.drawio.svg">
</picture>
