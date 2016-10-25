# PicoBlaze simulator & IDE
This project aims to create a simulator and IDE for PicoBlaze (8 bit processor) assembly.


...this might be a longish process so we will see how it goes. It might end up with just PicoBlade assembly simulator...

The PicoBlaze user guide can be found [here](http://www.xilinx.com/support/documentation/ip_documentation/ug129.pdf).


Steps that will be done here:

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

I would also aim to test more or less most of the stuff here. The testcases are created with [pytest](http://doc.pytest.org/en/latest/).

The requirements to launch the project are in `requirements.txt` file and can be installed through pip - Python package manager - just fire:

```
pip install -r requirements.txt
```

Currently the only thing that can be launched are tests. To launch them fire:
```
py.test .
```
