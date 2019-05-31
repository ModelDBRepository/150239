# Load a NEURON cell model into python
# 23/7/2012
# (c) 2012, C.Schmidt-Hieber, University College London

import sys
from neuron import h

h.load_file("stdrun.hoc")
h.xopen("./nrn/cells/stellate-garden.hoc")
h.xopen("./nrn/cells/stellate-remme.hoc")

def loadcell(morpho="garden"):
    # load cell
    if morpho is "garden":
        cell = h.stellate_garden()
    elif morpho is "remme":
        cell = h.stellate_remme()
    else:
        sys.stderr.write("Unknown cell morphology: %s\n" % morpho)
        sys.exit(1)

    return cell
