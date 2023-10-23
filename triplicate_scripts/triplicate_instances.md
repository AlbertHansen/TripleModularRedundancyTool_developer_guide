# ```triplicate_instances```

This is a *triplicate* script!

## Purpose

The purpose of the script is to triplicate module instantiations separately from cells and registers. There are some modifications which should only be applied to the module instantiations

## Usage

After the ```tmrt``` attribute has been updated appropriately on ports, cells, registers, and module instantiations, this script is run. The script triplicates all module instantiations and the inputs of the replicants are rewired to be driven by the same source as the original.

Renaming of ports from within a design is problematic, since there are no biult-in renaming functions. Replacing a port with an identical port of a different name is possible, however the original port should not be removed from within a design. If the ports are removed from within a design, the module instantations of the design will not recognise the correct designs. To compensate for this problem, when this script is called, the unconnected ports of the instantiations are removed using a built-in function.

## Definition

```tcl
proc triplicate_instances {} {
    ##########################################################################################
    # retrieves all module instantiations and triplicates them appropriately. This script also
    # replaces the original module instantiation with a replicant in order to change the name
    # and follow the naming conventions
    #
    # input:  none
    # output: none
    ##########################################################################################

    # remove old pin, and connect its triplicated counterparts
    set instances [get_synopsys_value "get_cells -filter {is_hierarchical==true}"]
    foreach instance $instances {
        set pins_in [get_synopsys_value "get_pins -of_object $instance -filter pin_direction==in"] 

        set tmrt [get_tmrt $instance]
        set_attribute $instance tmrt false
        foreach pin $pins_in {

            # check if triplicated 
            set pin_A [join [list $pin "A"] "_"]
            set pin_A [get_synopsys_value "get_pins -quiet $pin_A"]
            if {[llength $pin_A] == 0} {
                continue
            }

            # find replicants and connect to the same driver as the original
            set_attribute $pin_A tmrt true
            set pin_replicants [get_replicants $pin_A]
            set_attribute $pin_replicants tmrt true
            set pin_replicants [get_replicants $pin_A]
            set_attribute $pin_replicants tmrt true
            set driver         [get_driver_connection $pin]
            connect $driver $pin_replicants

            # disconnect original
            set base            [get_synopsys_value "cell_of [get_pins $pin]"]
            set base_replicants [get_replicants $base]
            set base_pin        [lindex [split $pin "/"] end]
            foreach cell $base_replicants {
                set cell_pin [join [list $cell $base_pin] "/"]
                set net [get_synopsys_value "all_connected $cell_pin"]
                disconnect_net $net $cell_pin
            }


        }
        set pins_out [get_synopsys_value "get_pins -of_object $instance -filter pin_direction==out"] 
        set pins_out [lsearch -all -inline -not -regexp $pins_out {[^ ]+_[ABC](?=\s|$)}]
        foreach pin $pins_out {

            # check if triplicated 
            set pin_A [join [list $pin "A"] "_"]
            set pin_A [get_synopsys_value "get_pins -quiet $pin_A"]
            if {[llength $pin_A] == 0} {
                continue
            }

            # find replicants and connect to the same driver as the original
            set_attribute $pin_A tmrt true
            set pin_replicants [get_replicants $pin_A]
            set_attribute $pin_replicants tmrt true
            set pin_replicants [get_replicants $pin_A]
            set_attribute $pin_replicants tmrt true
        
            set driven_pins    [get_driven_pins $pin]
            set driven_ports   [get_driven_ports $pin]
            set driven         [join [list $driven_pins $driven_ports]]
            connect $pin_A $driven

        }
        set_attribute $instance tmrt $tmrt
    }

    # uniquify the newly triplicated instances
    set instances [get_synopsys_value "get_cells -filter {is_hierarchical==true}"]
    foreach instance $instances {
        remove_unconnected_ports [get_cells $instance]
        uniquify -cell $instance
    }

    # triplicate the instance (reusing triplicate cell)
    set instances [get_synopsys_value "get_cells -filter {tmrt==true && is_hierarchical==true}"]
    foreach instance $instances {
        triplicate_cell $instance   
    }

    # update pin tmrt
    set instances [get_synopsys_value "get_cells -filter {is_hierarchical==true}"]
    foreach instance $instances {

        set pins [get_synopsys_value "get_pins -of_object $instance"]
        set pins [lsearch -all -inline -regexp $pins {[^ ]+_[ABC](?=\s|$)}]
        set_attribute $pins tmrt true
    }
}
```

This function will only work, if the following functions are sourced:

* ```get_synopsys_value```
* ```get_tmrt```
* ```get_replicants```
* ```get_driver_connection```
* ```get_driven_pins```
* ```get_driven_ports```
* ```connect```
* ```triplicate_cell```

## Example

The before and after of the script being called. The red outlines mark the targeted elements of the design, the orange text marks that the ```tmrt``` attribute is set to true and have been/should be triplicated. The blue outline or text indicates where the script has affected the design.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../figures/dark-mode/triplicate_scripts/triplicate_instances.drawio.svg">
  <img alt="Example triplication of a module instance" src="../figures/light-mode/triplicate_scripts/triplicate_instances.drawio.svg">
</picture>

Important to note is the removal of ```inst0/IN``` and ```inst0/OUT```. ```inst0/IN_B``` and ```inst0/IN_C``` have not been connected to the same source as ```inst0/IN_A``` as other functions/scripts might do, but this will be handled during the ```rewire_input_ports``` (and in other cases ```rewire_duped_cells```)
