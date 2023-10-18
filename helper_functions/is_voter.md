# ```lremove```

This is a helper function!

## Purpose

The purpose of the function is to add a consistent and simple function, that will remove elements from a list, as this is not a built-in functionality of TCL

## Usage

Some of the collections and lists utilised for the triplication routines require removal of specific items. Furthermore, when looking at connections from/to a pin/port it is usually useful to remove the pin/port itself.

## Definition

```tcl
proc lremove { a_list elements_to_be_removed } {
    #######################################################
    # removes entries from a list.
    # 
    # input:  a list, and the elements to be removed (list)
    # output: the same list, without the items to be 
    #         removed
    #######################################################

    # remove elements from list by searching for all elements,
    # that are not the same as the element to-be-removed
    foreach element $elements_to_be_removed {
        set a_list [lsearch -all -inline -exact -not $a_list $element]
    }

    return $a_list
}

```

## Example

This function is independent of the DC NXT and the following example is simple TCL:

```tcl
>> set items [list "a" "b" "a" "c" "d"]
a b a c d
>> set items_to_be_removed [list "a" "d"]
a d
>> lremove $items $items_to_be_removed
b c
```
