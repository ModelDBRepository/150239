# Test R_in, sag ratio, firing pattern
# 23/7/2012
# (c) 2012, C.Schmidt-Hieber, University College London

import sys

from neuron import h
import matplotlib.pyplot as plt
import numpy as np

sys.path.append("./nrn")
import loadcell

# general settings
morpho = "garden" # One of "garden" or "remme"
dt = 0.05 # integration interval (ms)
tstop = 1000.0 # sweep duration (ms)
istep = 0.05 # current step (nA)

# load NEURON's standard library
h.load_file("stdrun.hoc")
cell = loadcell.loadcell("garden")

h.dt = dt
h("forall {nseg=1}") # low spatial accuracy
h.dt = dt
h.steps_per_ms = 1.0/h.dt # NEURON quirk
h.tstop = tstop

ic = h.IClamp(cell.somaloc.secRef.sec(cell.somaloc.loc), sec=cell.somaloc.secRef.sec)
ic.delay = 200.0
ic.dur = 500.0

mrec = h.Vector()
mrec.record(cell.somaloc.secRef.sec(0.5)._ref_v)

runs = range(-1,10)
for nrun in runs:
    sys.stdout.write("%06.2f%% completed\r" % (float(nrun-runs[0])/len(runs)*100.0))
    sys.stdout.flush()
    ic.amp = nrun*istep
    h.v_init = cell.Vrest
    h.run()
    mrecnp = np.array(mrec)
    plt.plot(np.arange(len(mrecnp))*h.dt, mrecnp, '-k')
    plt.xlabel("Time (ms)")
    plt.ylabel("Membrane potential (mV)")
    if nrun == -1:
        first_idx = int(ic.delay/h.dt)
        last_idx = int((ic.delay+ic.dur)/h.dt)

        last_v = mrecnp[last_idx]-mrecnp[first_idx]
        amp_v = mrecnp[first_idx:last_idx].min()-mrecnp[first_idx]

        rin = last_v / ic.amp
        sag_ratio = last_v/amp_v

    if nrun == 0:
        vrest = mrecnp[-1]

sys.stdout.write("\nInput resistance: %.2f MOhm\n" % rin)
sys.stdout.write("Sag ratio: %.3f\n" % sag_ratio)
sys.stdout.write("Resting potential: %.2f mV\n" % vrest)

plt.show()

# wait for user input
raw_input()
