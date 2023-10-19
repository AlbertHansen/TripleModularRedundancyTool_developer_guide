[replace_port_figure]: ..\figures\rewire_scripts\replace_port.drawio.svg

# ```replace_port```

This is a *rewire* function!

## Purpose

When triplicating a port, the triplicated ports should follow some naming scheme. For this implementation the naming scheme is in form of suffixes, and triplicated elements will end with "_A", "_B", and "_C". Ports cannot be renamed using built-in functions, and thus they have to be replaced with a replicant with the correct name.

## Usage

After a port has been triplicated, this function is called and the connections of the original port is rewired to one of its replicants.

## Definition

```tcl
proc replace_port { original replacement } {
    ########################################################################################
    # replaces a port with a replicant of the same direction (connecting to net)
    # this function is used to rename ports, since seemingly this cannot be
    # done otherwise
    #
    # input:  two ports of the same direction
    # output: nothing
    ########################################################################################
    
    # check if ports have the same direction, if not abort
    set direction_original    [get_synopsys_value "get_attribute $original pin_direction"]
    set direction_replacement [get_synopsys_value "get_attribute $replacement pin_direction"]
    if {![string equal $direction_original $direction_replacement]} {
        puts "The direction of $original and $replacement are incongruent! "
        return
    }

    # disconnect original from net and connect replacement
    set net [get_synopsys_value "all_connected [get_ports $original]"]
    disconnect_net [get_nets $net] [get_ports $original]
    connect_net    [get_nets $net] [get_ports $replacement]
}
```

## Example

Calling the function:

```tcl
>> replace_port OUT OUT_A
```

This will yield the following result:

![Example of the replace_port function][replace_port_figure]

Notice that the old port is not removed, unlike the ```replace_cell``` function. This is done in order to ensure that DC NXT can recognise the design, if it is instantiated in another design. The ports will be removed from one layer above during the ```triplicate_instances``` script or if the ports are on the top layer from the ```remove_ports_top``` script
