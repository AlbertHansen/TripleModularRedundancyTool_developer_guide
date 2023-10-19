[remove_ports_top_figure]: ..\figures\rewire_scripts\remove_ports_top.drawio.svg

# ```remove_ports_top```

This is a *rewire* script!

## Purpose

When triplicating ports the name of the port should be changed. If a port ```clk``` is triplicated, it should be replaced with ```clk_A```, ```clk_B```, and ```clk_C```. By default ports cannot be renamed, and thus the port must be *replaced*. This is done with the ```replace_port``` function, however, if a port of a module instantiation within a hierarchy is removed from its design, DC NXT will not recognise the design. The ```replace_port``` will therefore not remove the original cell, but just let it be left disconnected to-be-removed from a layer above. This procedure will work for any layer except the top layer, and the disconnected ports in the top layer is removed by calling this script instead.

## Usage

After all *update*, *triplicate*, and *rewire* routines have been executed, this function is called to clean up disconnected ports in the top layer only.

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

The figure below is a design with 1 input and 1 output port originally, however they have both been triplicated, leaving the original ports disconnected. The disconnected ports are removed by calling the script.

![Example of removing the disconnected top ports][remove_ports_top_figure]
