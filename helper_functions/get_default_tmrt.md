# ```get_default_tmrt```

This is a helper function!

## Purpose

The purpose of this helper function is to fetch the value associated with the ```default_tmr``` **attribute**, which is an attribute that should be associated with a **module declaration**.

## Usage

As a part of the update routines, the ```default_tmr``` attribute is set on all module declarations and designs. This functions fetches the value set, which is then used for updating the ```default_tmr``` attribute for the children (non-overriding).

Furthermore, when updating the ```tmr``` attribute on registers, ports, and module instantiations, their parent design/module declaration is targeted and the value of the ```default_tmr``` attribute will also be the value of the ```tmr``` attribute of the "child" elements.

## Definition

```tcl
proc get_default_tmrt { module } {
    redirect -variable default {get_attribute $module default_tmrt}
    return $default
}
```

## Example

You have a module declaration:

```sv
(*default_tmr="false"*)
module INV (
    input  in,
    output out
);

always_comb 
    output = ~in;

endmodule
```

And you use ```get_default_tmrt``` to fetch the value:

```tcl
get_default_tmrt INV
>> false
```
