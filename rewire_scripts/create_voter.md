[create_voter_figure]: ../figures/rewire_scripts/create_voter.drawio.svg

# ```create_voter```

This is a *rewire* function! Every inserted voter is generated from this function.

## Purpose

Triplication of specific elements require the possibility of inferring a majority voter (possibly multiple), which this script will generate. The voter circuit will be based on the number of inputs and outputs.

## Usage

During the *rewire* routines, this function will handle all connections that has to be drawn to non-triplicated driven elements. Furthermore, when all nets suffixed with "_Voted" are handled, this function will generate and connect the 3 majority voters.

## Definition

```tcl
proc create_voter { inputs outputs } {
    ##########################################################################
    # This function creates a set of majority voters based on the amount of
    # inputs and outputs. This is also used when making throughput voting
    # (3 inputs, 3 voters, 3 outputs)
    #
    # input:  triplicated pins/ports, that have to be voted
    # output: non-triplicated or triplicated pins/ports that require the voted
    #         output of the input pins/ports
    ##########################################################################

    set input_count  [llength $inputs]
    set output_count [llength $outputs]

    # 3-to-1
    if {$input_count == 3 && $output_count == 1} {

        # create name for voter and inverter
        set voter_name     ""
        set voter_inv_name ""
        if {![is_port [lindex $outputs 0]]} {
            set base_cell [get_synopsys_value "cell_of [lindex $outputs 0]"]
            set base_pin  [lindex [split [lindex $outputs 0] "/"] end]
            set voter_name     [join [list $base_cell $base_pin       "Voter"] "_"]
            set voter_inv_name [join [list $base_cell $base_pin "inv" "Voter"] "_"]
        } else {
            set voter_name     [join [list [lindex $outputs 0]        "Voter"] "_"]
            set voter_inv_name [join [list [lindex $outputs 0]  "inv" "Voter"] "_"]
        }

        # create voter and inverter
        create_cell $voter_name tcbn28hpcplusbwp7t30p140ffg0p88v0c/MAOI222D1BWP7T30P140
        create_cell $voter_inv_name tcbn28hpcplusbwp7t30p140ffg0p88v0c/INVD1BWP7T30P140
        set_dont_touch $voter_name
        set_dont_touch $voter_inv_name

        # join voter output and inv input
        set voter_out_pin    [get_synopsys_value "get_pins -of_object $voter_name     -filter {pin_direction == out}"]
        set voter_inv_in_pin [get_synopsys_value "get_pins -of_object $voter_inv_name -filter {pin_direction == in}"]
        create_net $voter_inv_name
        connect_net [get_nets $voter_inv_name] [get_pins $voter_out_pin]
        connect_net [get_nets $voter_inv_name] [get_pins $voter_inv_in_pin]
        
        # connect voter output to instance pin
        set vouter_out [get_synopsys_value "get_pins -of_object [get_cells $voter_inv_name] -filter pin_direction==out"]
        connect $vouter_out [lindex $outputs 0]

        # connect voter inputs and inputs
        set voter_in [get_synopsys_value "get_pins -of_object [get_cells $voter_name] -filter pin_direction==in"]
        for {set i 0} {$i < [llength $voter_in]} {incr i} {
            connect [lindex $inputs $i] [lindex $voter_in $i]
        }
        return
    }

    # 3-to-3
    if {$input_count == 3 && $output_count == 3} {

        # create names for voters and inverters
        set voter_names ""
        set voter_inv_names ""
        foreach output $outputs {
            if {![is_port $output]} {
                set base_cell [get_synopsys_value "cell_of $output"]
                set base_pin  [lindex [split $output "/"] end]
                set voter_name     [join [list $base_cell $base_pin       "Voter"] "_"]
                set voter_inv_name [join [list $base_cell $base_pin "inv" "Voter"] "_"]
            } else {
                set voter_name     [join [list $output                    "Voter"] "_"]
                set voter_inv_name [join [list $output              "inv" "Voter"] "_"]
            }
            set voter_names     [join [list $voter_names $voter_name]]
            set voter_inv_names [join [list $voter_inv_names $voter_inv_name]]
        }

        # create voters and invs
        create_cell $voter_names     tcbn28hpcplusbwp7t30p140ffg0p88v0c/MAOI222D1BWP7T30P140
        create_cell $voter_inv_names tcbn28hpcplusbwp7t30p140ffg0p88v0c/INVD1BWP7T30P140

        for {set i 0} {$i < 3} {incr i} {

            # join voter output and inv input
            set voter_out     [get_synopsys_value "get_pins -of_object [lindex $voter_names $i]     -filter pin_direction==out"]
            set voter_inv_in  [get_synopsys_value "get_pins -of_object [lindex $voter_inv_names $i] -filter pin_direction==in"]
            connect $voter_out $voter_inv_in

            # connect voter output to outputs
            set voter_inv_out [get_synopsys_value "get_pins -of_object [lindex $voter_inv_names $i] -filter pin_direction==out"]
            connect $voter_inv_out [lindex $outputs $i]

            # connect voter inputs and 
            set voter_in [get_synopsys_value "get_pins -of_object [lindex $voter_names $i] -filter pin_direction==in"]
            for {set j 0} {$j < 3} {incr j} {
                connect [lindex $inputs $j] [lindex $voter_in $j]
            }
        }
        return
    }

    # 9-to-1
    if {$input_count == 9 && $output_count == 1} {

        # create 1 master voter, and 3 subvoters
        set master_voter     ""
        set sub_voter_A ""
        set sub_voter_B ""
        set sub_voter_C ""
        if {![is_port [lindex $outputs 0]]} {
            set base_cell [get_synopsys_value "cell_of [lindex $tmrg_instance_pins 0]"]
            set base_cell    [join $base_cell]
            set base_pin     [lindex [split [lindex $outputs end] "/"] end]
            set master_voter [join [list $base_cell $base_pin "Master" "Voter"] "_"]
            set sub_voter_A  [join [list $base_cell $base_pin "A" "Sub" "Voter"] "_"]
            set sub_voter_B  [join [list $base_cell $base_pin "B" "Sub" "Voter"] "_"]
            set sub_voter_C  [join [list $base_cell $base_pin "C" "Sub" "Voter"] "_"]
        } else {
            set master_voter [join [list [lindex $outputs 0]  "Master" "Voter"] "_"]
            set sub_voter_A  [join [list [lindex $outputs 0]  "A" "Sub" "Voter"] "_"]
            set sub_voter_B  [join [list [lindex $outputs 0]  "B" "Sub" "Voter"] "_"]
            set sub_voter_C  [join [list [lindex $outputs 0]  "C" "Sub" "Voter"] "_"]
        }
        create_cell $master_voter tcbn28hpcplusbwp7t30p140ffg0p88v0c/MAOI222D1BWP7T30P140

        # connect master voter
        set master_out [get_synopsys_value "get_pins -of_object $master_voter -filter pin_direction==out"]
        connect $master_out [lindex $outputs 0]

        # create 3 sub voters and connect to master
        set sub_voters  [list $sub_voter_A $sub_voter_B $sub_voter_C]
        set master_in [get_synopsys_value "get_pins -of_object $master_voter -filter pin_direction==in"]
        set master_in [lsort -increasing [join $master_in]]
        for {set i 0} {$i < 3} {incr i} {
            create_cell [lindex $sub_voters $i] tcbn28hpcplusbwp7t30p140ffg0p88v0c/MAOI222D1BWP7T30P140
            create_net  [lindex $sub_voters $i]
            set sub_out [get_synopsys_value "get_pins -of_object [lindex $sub_voters $i] -filter pin_direction==out"]
            connect_net [get_nets [lindex $sub_voters $i]] [get_pins $sub_out]
            connect_net [get_nets [lindex $sub_voters $i]] [get_pins [lindex $master_in $i]]
        }

        # connect driver to subvoters
        set voter_pins_in ""
        foreach voter $sub_voters {
            set voter_pins_in_temp [get_synopsys_value "get_pins -of_object $voter -filter pin_direction==in"]
            set voter_pins_in [join [list $voter_pins_in $voter_pins_in_temp]]
        }
        set voter_pins_in [lsort -increasing [join $voter_pins_in]]
        set voter_pins_in [join [list [lindex $voter_pins_in 0] [lindex $voter_pins_in 3] [lindex $voter_pins_in 6] [lindex $voter_pins_in 1] [lindex $voter_pins_in 4] [lindex $voter_pins_in 7] [lindex $voter_pins_in 2] [lindex $voter_pins_in 5] [lindex $voter_pins_in 8] ]]

        for {set i 0} {$i < 9} {incr i} {
            connect [lindex $inputs $i] [lindex $voter_pins_in $i]
        }
        return
    }

    # 9-to-3
    if {$input_count == 9 && $output_count == 3} {
        # create names for voters and inverters
        set voter_names ""
        set voter_inv_names ""
        foreach output $outputs {
            if {![is_port $output]} {
                set base_cell [get_synopsys_value "cell_of $output"]
                set base_pin  [lindex [split $output "/"] end]
                set voter_name     [join [list $base_cell $base_pin       "Voter"] "_"]
                set voter_inv_name [join [list $base_cell $base_pin "inv" "Voter"] "_"]
            } else {
                set voter_name     [join [list $output                    "Voter"] "_"]
                set voter_inv_name [join [list $output              "inv" "Voter"] "_"]
            }
            set voter_names     [join [list $voter_names $voter_name]]
            set voter_inv_names [join [list $voter_inv_names $voter_inv_name]]
        }

        # create voters and invs
        create_cell $voter_names     tcbn28hpcplusbwp7t30p140ffg0p88v0c/MAOI222D1BWP7T30P140
        create_cell $voter_inv_names tcbn28hpcplusbwp7t30p140ffg0p88v0c/INVD1BWP7T30P140

        for {set i 0} {$i < 3} {incr i} {

            # join voter output and inv input
            set voter_out     [get_synopsys_value "get_pins -of_object [lindex $voter_names $i]     -filter pin_direction==out"]
            set voter_inv_in  [get_synopsys_value "get_pins -of_object [lindex $voter_inv_names $i] -filter pin_direction==in"]
            connect $voter_out $voter_inv_in

            # connect voter output to outputs
            set voter_inv_out [get_synopsys_value "get_pins -of_object [lindex $voter_inv_names $i] -filter pin_direction==out"]
            connect $voter_inv_out [lindex $outputs $i]

        }

        # connect driver to voters
        set voter_pins_in ""
        foreach voter $voter_names {
            set voter_pins_in_temp [get_synopsys_value "get_pins -of_object $voter -filter pin_direction==in"]
            set voter_pins_in [join [list $voter_pins_in $voter_pins_in_temp]]
        }
        set voter_pins_in [lsort -increasing [join $voter_pins_in]]
        set voter_pins_in [join [list [lindex $voter_pins_in 0] [lindex $voter_pins_in 3] [lindex $voter_pins_in 6] [lindex $voter_pins_in 1] [lindex $voter_pins_in 4] [lindex $voter_pins_in 7] [lindex $voter_pins_in 2] [lindex $voter_pins_in 5] [lindex $voter_pins_in 8] ]]

        for {set i 0} {$i < 9} {incr i} {
            connect [lindex $inputs $i] [lindex $voter_pins_in $i]
        }

        return
    }

######################### OBS NOT IMPLEMENTED CORRECTLY YET ###########################
    # 9-to-9
    if {$input_count == 9 && $output_count == 9} {
        # create names
        set voter_names ""
        set voter_inv_names ""
        foreach output $outputs {
            if {![is_port]} {
                set base_cell [get_synopsys_value "cell_of $output"]
                set base_pin  [lindex [split $output "/"] end]
                set voter_name     [join [list $base_cell $base_pin       "Voter"] "_"]
                set voter_inv_name [join [list $base_cell $base_pin "inv" "Voter"] "_"]
            } else {
                set voter_name     [join [list $output                    "Voter"] "_"]
                set voter_inv_name [join [list $output              "inv" "Voter"] "_"]
            }
            set voter_names     [join [list $voter_names $voter_name]]
            set voter_inv_names [join [list $voter_inv_names $voter_inv_name]]
        }

        # create voters and nots
        create_cell $voter_names     tcbn28hpcplusbwp7t30p140ffg0p88v0c/MAOI222D1BWP7T30P140
        create_cell $voter_inv_names tcbn28hpcplusbwp7t30p140ffg0p88v0c/INVD1BWP7T30P140

        for {set i 0} {$i < 9} {incr i} {

            # join voter output and inv input
            set voter_out     [get_synopsys_value "get_pins -of_object [lindex $voter_names $i]     -filter pin_direction==out"]
            set voter_inv_in  [get_synopsys_value "get_pins -of_object [lindex $voter_inv_names $i] -filter pin_direction==in"]
            connect $voter_out $voter_inv_in

            # connect voter output to outputs
            set voter_inv_out [get_synopsys_value "get_pins -of_object [lindex $voter_inv_names $i] -filter pin_direction==out"]
            connect $voter_inv_out [lindex $outputs $i]

            # connect voter inputs and 
            set voter_in [get_synopsys_value "get_pins -of_object [lindex $voter_names $i] -filter pin_direction==in"]
            for {set j 0} {$j < 3} {incr j} {
                connect [lindex $inputs $j] [lindex $voter_in $j]
            }
        }
    return
    }
########################################################################################
}
```

## Example

In the figure below, the outcome of a 3-to-1 vote can be seen. The corresponding function-call would look somewhat like:

```tcl
>> create_voter {U3_A/ZN U3_B/ZN U3_C/ZN} {OUT3}
```

However, this function works best in tandem with the helper function ```get_replicant```, as this function would find all identical pins created during the *triplicate* routines.

![Example of create_voter in action][create_voter_figure]
