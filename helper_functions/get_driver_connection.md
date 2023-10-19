[get_driver_connection_figure]: ../figures/helper_functions/get_driver_connection.drawio.svg

# ```get_driver_connection```

This function is a helper function!

## Purpose

This function fetches the pin/port that drives the element used as the argument in the function call.

## Usage

This function is used mainly when triplicating cells, output ports, registers, and module instantiations to drive all replicants (or replicant pins/ports) with the same connection. This is important for the update-triplicate-rewire procedure and fanout.

## Definition

```tcl
proc get_driver_connection { driven_connection } {
    #########################################################################
    # finds the driving pin/port of a pin/port
    #
    # input:  a pin/port
    # output: a pin/port that drives the input pin/port
    #########################################################################

    # find net
    set net ""
    if {[is_port $driven_connection]} {
        set net [get_synopsys_value "all_connected [get_ports $driven_connection]"]
    } else {
        set net [get_synopsys_value "all_connected [get_pins  $driven_connection]"]  
    }
    if {[string length $net] < 1} {
        return ""
    }

    # find pins and ports, with the correct pin direction
    set pins  [get_synopsys_value "get_pins  -of_object [get_nets $net] -filter pin_direction==out"]
    set ports [get_synopsys_value "get_ports -of_object [get_nets $net] -filter pin_direction==in"]

    # return the driver
    if {[llength $pins] > 0} {
        return $pins
    } elseif {[llength $ports] > 0} {
        return $ports
    }
}
```

This function will only work, if the following function is sourced:

* ```get_synopsys_value```

## Example

Given the circuit below, if you use ```get_driver_connection``` on the OUT2 port (marked in red), the returned value would be port IN (marked in blue).

![get_driven_pins used on example circuit. Red textcolor indicates the input to the function call, and blue indicates the return.][get_driver_connection_figure]

When calling the function, it would look somewhat like:

```tcl
>> get_driver_connection OUT2
IN
```
