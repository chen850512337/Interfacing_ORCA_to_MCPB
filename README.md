# Interfacing_orca_to_mcpb

This project provides an interface for calling `ORCA` from `MCPY.py`.
Both `ORCA` and `Multiwfn` are free and easy to use, please cite them 
appropriately.

## Software version required
All the development and test are performed using the following software 
version, older version software may still works, but are not guaranteed.
 - AmberTools25
 - ORCA 6.1
 - Multiwfn (3.8, obtained at 2023-Feb-15)


## Installation
### Using Conda or Mamba
If you install `AmberTools` by `conda` or `mamba`, just set `AMBERHOME` 
environment variable and run:
```bash
cd scripts
chmod +x update_mcpb.sh
./update_mcpb.sh
```

### Compile from source
If you install `AmberTools` from the source code, then replace your AmberTools 
source with files from `pymsmt` and recompile.
Note the file `orcaio.py` is new.


## Useage
A quick workflow:
- Prepare input files as usual for `MCPB.py`.
- Set `software_version = 'orca'` in the MCPB input file and run `MCPB.py`.
- After optimization and frequency calculation, copy the `.xyz` and `.hess` 
file to your working directory and run `MCPB.py`.
- After the large model calculation is finished, use `orca_2mkl` convert `.gbw` 
file to `.molden` file.
- Use Multiwfn to generate `.chg` file and `ESPfitpt.txt` file, change 
`ESPfitpt.txt` file to `.espfitpt`

For detailed instructions, see the 2 examples.

## Examples
Two examples are also make available in the example folder with detail command, 
which is the same system as the `MCPB.py`: 
 - 1OKL 
 - 4ZF6


## Citation
**Please proper cite ORCA and Multiwfn according to their respective documentation.**
