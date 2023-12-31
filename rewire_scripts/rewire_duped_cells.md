# ```rewire_duped_cells```

This is a *rewire* script!

## Purpose

The purpose of this script is to draw the correct connections from triplicated cells, registers, module instantiations, and pins on module instantiations. The fanouts created during the *triplicate* routines are reeavluated and the driven connections are either redistributed between the newly triplicated element or voted and connected to the non-triplicated driven connections.

## Usage

This function is called once per design after the *update* and *triplicate* routines have been performed.  It is worth noting, that the output ports are handled indirectly handled by this function and ```rewire_input_ports``` as they target the driven elements from every driving element.

When rewiring the script will check if involved nets are suffixed with "_Voted", and if so the replicants of both driving and driven connections will all be connected to one net and the net name will not be changed! These nets will be handled in a later script, ```vote_nets```.

## Definition

```tcl
proc rewire_duped_cells {} {
    ###########################################################################
    # loops over every triplicated cell, register, and module instantiation
    # in order to redistribute the driven connections to its replicants, or
    # vote in case the driven connection has not been triplicated
    #
    # input:  none
    # output: none
    ###########################################################################

    # retrieve all cells with suffix _A (being one of a set of three replicants)
    set duped_cells [get_synopsys_value "get_cells -filter is_hierarchical==false -quiet *_A"]

    # fetch all registers with tmrt = true
    set registers [get_synopsys_value "all_registers -no_hierarchy"]
    set registers [lsearch -all -inline -regexp $registers "\\S+_A"]

    # fetch all hierarchical cells
    set instances [get_synopsys_value "get_cells -filter {is_hierarchical==true}"]
    set instances [lsearch -all -inline -not -regexp $instances {[^ ]+_[BC](?=\s|$)}] 

    set duped_cells [join [list $duped_cells $registers $instances]]
    set duped_cells [lsort -unique $duped_cells]
    foreach cell_A $duped_cells {
        puts "/// $cell_A ///"

        # retrieve all output pins
        set cell_A_outputs [get_synopsys_value "get_pins -of_object $cell_A -filter pin_direction==out"]
        set cell_A_outputs [lsearch -all -inline -not -regexp $cell_A_outputs {[^ ]+_[BC](?=\s|$)}] 
        
        # loop through all output pins on cell 
        foreach cell_A_output $cell_A_outputs {
            puts "--- $cell_A_output ---"

            # fetch corresponding pin on replicants
            set replicant_pins [get_replicants $cell_A_output]
            set replicant_pins [lsort -increasing $replicant_pins]

            # fetch driven pins by pin on cell_A
            set driven_pins  [get_driven_pins  $cell_A_output]
            set driven_ports [get_driven_ports $cell_A_output]
            set driven [join [list $driven_pins $driven_ports]]

            # flag to check if a voter has been created
            set voter_created 0
            set voter_out ""

            puts "Loop over the driven: $driven"
            while {[llength $driven] > 0} {
                puts "-- [lindex $driven 0]"

                # retrieve replicants (in the case no replicants are found the function returns the input!)
                set driven_replicants [get_replicants [lindex $driven 0]]
                set driven_replicants [lsort -increasing $driven_replicants]
                puts "replicants: $driven_replicants"

                # if the driven element does not exist, remove it from the list
                #if {[llength $driven_replicants] < 1} {
                #    set driven [lremove $driven [lindex $driven 0]]
                #    continue
                #}

                # if replicants are found, connect them to correspondingly
                if {[llength $driven_replicants] > 1 && [llength $driven_replicants] >= [llength $replicant_pins]} {
                    if {[llength $replicant_pins] == 1} {
                        connect $replicant_pins $driven_replicants
                    } elseif {[llength $driven_replicants] == [llength $replicant_pins]} {
                        for {set i 0} {$i < [llength $driven_replicants]} {incr i} {
                            connect [lindex $replicant_pins $i] [lindex $driven_replicants $i]
                        }
                    } elseif {[llength $driven_replicants] == 9 && [llength $replicant_pins] == 3} {
                        for {set i 0} {$i < 3} {incr i} {
                            connect [lindex $replicant_pins $i] [lindex $driven_replicants $i]
                            connect [lindex $replicant_pins $i] [lindex $driven_replicants [expr $i + 3]]
                            connect [lindex $replicant_pins $i] [lindex $driven_replicants [expr $i + 6]]
                        }
                    } 
                    set driven [lremove $driven $driven_replicants]
                    continue
                }

                # create unique voter if the driven pin/port is triplicated 
                if {[llength $driven_replicants] > 1} {
                    create_voter $replicant_pins $driven_replicants
                    set driven [lremove $driven $driven_replicants]
                    continue
                }

                # If a voter is already created, connect all non-triplicated driven pins/ports to its output
                if {$voter_created} {
                    if {[is_port $driven_replicants] == true} {
                        connect $voter_out [get_ports $driven_replicants]
                    } else {
                        connect $voter_out [get_pins  $driven_replicants]
                    }
                } else {
                    create_voter $replicant_pins $driven_replicants
                    set voter_created 1
                    set voter_out [get_driver_connection $driven_replicants]
                }
                set driven [lremove $driven $driven_replicants]
            }
        }
    }
}
```

This function will only work, if the following functions are sourced:

* ```get_synopsys_value```
* ```get_replicants```
* ```get_driven_pins```
* ```get_driven_ports```
* ```connect```
* ```create_voter```
* ```lremove```

## Example

The figure below is the before and after of the script. The cells outlined in red represents the targeted cells of the script. During the script the replicants are found and redistributed or voted. The redistributed nets, the rewired nets, and the inserted voters are all marked with a blue outline in the "after" part of the figure.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../figures/dark-mode/rewire_scripts/rewire_duped_cells.drawio.svg">
  <img alt="Small example of the rewire script, which affect the cells, registers, and module instantiations" src="../figures/light-mode/rewire_scripts/rewire_duped_cells.drawio.svg">
</picture>

Notice that port B has been triplicated, however it is not rewired after the script has been run. Input ports are handled in a separate function ```rewire_input_ports```.
