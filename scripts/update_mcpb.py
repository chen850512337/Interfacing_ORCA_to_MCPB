#!/bin/bash

#AMBERHOME=/Your/path/to/AmberTools25
MCPBHOME=${AMBERHOME}/lib/python3.12/site-packages

cp ../pymsmt/tools/MCPB.py ${AMBERHOME}/bin/MCPB.py  

cp ../pymsmt/mcpb/gene_model_files.py       ${MCPBHOME}/pymsmt/mcpb/
cp ../pymsmt/mcpb/gene_final_frcmod_file.py ${MCPBHOME}/pymsmt/mcpb/
cp ../pymsmt/mcpb/resp_fitting.py           ${MCPBHOME}/pymsmt/mcpb/

cp ../pymsmt/mol/orcaio.py ${MCPBHOME}/pymsmt/mol/

