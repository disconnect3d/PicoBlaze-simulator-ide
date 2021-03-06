# PicoBlaze simulator & IDE

TLDR: This was an idea to create PicoBlaze 8-bit assembly simulator and IDE. It ended up only as a simulator.

See the source code to learn more; some of the README below might also be helpful (e.g. the PicoBlaze user guide).


## Old stuff

This project aims to create a simulator and IDE for PicoBlaze (8 bit processor) assembly.

...this might be a longish process so we will see how it goes. It might end up with just PicoBlaze assembly simulator...

The PicoBlaze user guide can be found [here](http://www.xilinx.com/support/documentation/ip_documentation/ug129.pdf).

**NOTE: I am not yet sure whether this will use KCPSM3 or pBlazIDE mnemonics (if you want to read more about this, see page 71 of the PicoBlaze user guide linked above).**

### Steps that will be done here:

* Instructions tokenizer
  * JUMP
  * LOAD
  * EQU
  * JUMP [with flags] to label/address
  * ADD, SUB
  * ADDCY, SUBCY
  * etc...
* Instructions decoder

* Virtual machine (code simulator)

* IDE (???)

For "already implemented stuff" check `src/test_*` files.

I would also aim to test more or less most of the stuff here. The testcases are created with [pytest](http://doc.pytest.org/en/latest/).

### Requirements
The requirements to launch the project are in `requirements.txt` file and can be installed through pip - Python package manager - just fire:

```
pip install -r requirements.txt
```

### Launching
Currently the only thing that can be launched are tests. To launch them get into `src` directory and fire:
```
py.test . -v  
```
