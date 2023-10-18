[get_driven_pins_figure]: ..\figures\helper_functions\get_driven_pins.drawio.svg

# ```get_driven_pins```

This function is a helper function!

## Purpose

This function fetches all **input pins** connected to driving pin/port. If the given input is not an input port or an output pin, an appropriate statement will be displayed, and nothing will be returned.

## Usage

This function is used mainly for the *rewire* routines, as the driven elements of triplicated elements must be redistributed or voted.

## Definition

```tcl
proc get_driven_pins { element } {
    ##################################################################################
    # looks forward from pin and returns all connections, that 
    #       - are driven
    #       - are pins
    #
    # input:  pin/port
    # output: list of pins driven by the input pin/port
    ##################################################################################

    # empty list to hold all connections
    set connections ""

    # find connections based on whether the element is a port or a pin
    if {[is_port $element]} {   ;# element is a port

        # check if port is a driving connection
        set direction [get_synopsys_value "get_attribute [get_ports $element] pin_direction"]
        if {![string equal $direction "in"]} {
            puts "Port/pin $element is not a driving connection!"
            return
        }

        # retrieve all pins/ports connected to the same net as the element
        set net         [get_synopsys_value "all_connected [get_ports $element]"]
        if {[string length $net] < 1} {
            return ""
        }
        set connections [get_synopsys_value "all_connected [get_nets $net]"]

    } else {                    ;# element is a pin

        # check if port is a driving connection
        set direction [get_synopsys_value "get_attribute [get_pins $element] pin_direction"]
        if {[string equal $direction "in"]} {
            puts "Port/pin $element is not a driving connection!"
            return
        }

        # retrieve all pins/ports connected to the same net as the element
        set net         [get_synopsys_value "all_connected [get_pins $element]"]
        if {[string length $net] < 1} {
            return ""
        }
        set connections [get_synopsys_value "all_connected [get_nets $net]"]
    }

    # remove element from list of connections
    set connections [lremove $connections $element]

    # remove all ports from list of connections
    foreach connection $connections {
        if {[is_port $connection]} {
            set connections [lremove $connections $connection]
        }
    }

    # return all pins (except for element)
    return $connections
}
```

This function will only work, if the following functions are sourced:

* ```is_port```
* ```get_synopsys_value```
* ```lremove```

## Example

Given the circuit below, if you use ```get_driven_pins``` on the IN port (marked in red), the returned value would be the three pins connected to IN (marked in blue). Notice that port OUT2 will not be returned, as it is not a pin!

![get_driven_pins used on example circuit. Red textcolor indicates the input to the function call, and blue indicates the return.][get_driven_pins_figure]

When calling the function, it would look somewhat like:

```tcl
>> get_driven_pins IN
R1/D U1/A U2/A
```
