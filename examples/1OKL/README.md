# Tutorial for 1OKL
Here shows the similar tutorial for 1OKL with the official [1OKL](https://ambermd.org/tutorials/advanced/tutorial20/mcpbpy.php).

## Prepare inputs 
Prepre all the inputs files as there.

## MCPB.py: 1st step
For the MCPB.py, change the `software_version` to `orca`. then run:

```bash
MCPB.py -i 1OKL.in -s 1 
```

## MCPB.py: 2nd step
Then perform calculations with the generated ORCA input files:
```bash
orca 
```

Get the `.hess` and optimized `.xyz` file, then run:
```
MCPB.py -i 1OKL.in -s 2
```

## MCPB.py: 3rd step
Convert the large model `.gbw` file to molden input file by:
```
# do not add the .gbw suffix!
orca_2mkl 1OKL_orca_large_mk -molden
```
and run `Multiwfn` use the input file in `scripts`:
```bash
Multiwfn < .in
```
change the ESPfitting.pt to `.espfpt`
and run:
```
MCPB.py -i 1OKL.in -s 3
```
## MCPB.py: 4th step
Finally, generate the input for tleap:
```
MCPB.py -i 1OKL.in -s 4
```

and call tleap for the amber prmtop and inpcrd file:
```bash
tleap -f 1OKL_tleap.in
```
