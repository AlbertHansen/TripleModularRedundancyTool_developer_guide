[triplicate_output_ports]: ../figures/triplicate_scripts/triplicate_output_ports.drawio.svg

# ```triplicate_output_ports```

This is a *triplicate* script

## Purpose

The purpose of this script is to triplicate all output ports with their ```tmrg``` attribute set to true.

## Usage

After the *update* routines have run, this script is called and it triplicates the output ports using the ```triplicate_port``` function.

## Definition

```tcl
proc triplicate_output_ports {} {
    ##########################################################
    # This script retrieves all outpit ports of the current
    # design and passes them as arguments to the triplicate_port
    # function, triplicating all output ports
    #
    # input:  none
    # output: none
    ##########################################################

    # retrieve all output ports in design
    set ports [get_synopsys_value "all_outputs"]

    # look through each port, 
    # if tmrg attribute is set to "true" apply triplication rule
    foreach port $ports {
        set tmrg [get_tmrg $port]
        if {[expr $tmrg]} {
            triplicate_port $port
        }
    }
}
```

This function will only work, if the following functions are sourced:

* ```get_synopsys_value```
* ```get_tmrg```
* ```triplicate_port```

## Example

The names marked in orange indicate that their ```tmrg``` attribute has been set to true. The red outline marks the target, and the blue outline marks the changes that has happened.

![Example of triplication step on input ports][triplicate_output_ports]
