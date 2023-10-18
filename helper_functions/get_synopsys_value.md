# ```get_synopsys_value```

This is a helper function! To understand the following link may provide some additional information: [Synopsys Collections](https://spdocs.synopsys.com/dow_retrieve/qsc-u/dg/dcolh/U-2022.12/dcolh/olh_dc/man/man2/collections.html?hl=lifetime&searchQuery=lifetime&sc0=x), this resource requires a SolvNet user.

## Purpose

The purpose of this function is to alleviate the problems associated with ```get```-functions and the built-in ```redirect -variable var```-function:

* The lifetime of a returned value has some unwanted effects, which can be avoided by using ```redirect -variable var```. Setting a tcl variable to the returned value from ```get```-functions and the using ```puts``` reveals some sort of program-specific reference in the shape of ```_sel23```
* The returned value will always be an element consisting of a list, and if you want to loop over the returned values, you have to either index the element or 'join' it

Furthermore, using *regular expressions* to catch the important values from the returned statements, the functionality of the function is broadened.

## Usage

This function is used every time variables (collections) from Synopsys have to be saved in a variable in a tcl script

Tthis function is used in combination with ```duplicate_logic -report_only``` to find all logic cells between two points, which would otherwise have returned a block of text including the important information.

## Definition

```tcl
proc get_synopsys_value { function_call_string } {
    ################################################################################################
    # get_synopsys_value replaces the need to call "redirect -variable ..." followed by "[join ...]"
    #
    # input:    the function/expression whose output is wanted
    # output:   is the result from evaluating the expresion/function, 
    #           and only returning elements from within brackets {}
    ################################################################################################

    # construct the expression to call in design compiler NXT
    set  result         "" 
    set  redirect       "redirect -variable result"
    set  function_call  [join [list $redirect "\{" $function_call_string "\}"] " "]
    
    # evaluate the expression
    catch {eval $function_call} something_went_wrong
    if {[llength $something_went_wrong] != 0} {
        error "Something went wrong while trying to evaluate expression: \n\t\t$function_call\nin a 'get_synopsys_value' call"
    }

    # if the return is an error
    set returns_error [split $result ":"]
    if {[string equal [lindex $returns_error 0] "Error"]} {
        return
    }

    # extract valuable information; everything encapsulated by {}
    set is_not_simple [string first "\{" $result]
    if {$is_not_simple > 0} {
        set  regex          {\{[^{}]*\}}
        set  result         [join [regexp -all -inline $regex $result]]
    }

    # return result as ONE LIST
    return [join $result]
}
```

## Example

A synopsys function is used to fetch all pins of a cell:

```tcl
>> get_pins -quiet -of_object U1
{U1/I U1/Z}
```

The same function call, however wrapped in the ```get_synopsys_value``` function:

```tcl
>> get_synopsys_value "get_pins -quiet -of_object U1"
U1/I U1/Z
```

The difference is subtle, but important! In the first code-snippet the returned value is an element consisting of a list, whereas the returned value in the second code-snippet is the list itself.
