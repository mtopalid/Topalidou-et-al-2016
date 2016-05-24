# -----------------------------------------------------------------------------
# Copyright (c) 2016, Meropi Topalidou
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from experiment import Experiment
import os
folder = "data/"
if not os.path.exists(folder):
    os.makedirs(folder)

folderRes = folder + "results/reverse/"
if not os.path.exists(folderRes):
    os.makedirs(folderRes)

folderRep = folder + "reports/reverse/"
if not os.path.exists(folderRep):
    os.makedirs(folderRep)

folderFig = folder + "figures/reverse/"
if not os.path.exists(folderFig):
    os.makedirs(folderFig)


def session(exp):
    exp.model.setup()
    for trial in exp.task:
        exp.model.process(exp.task, trial)
    return exp.task.records


mdl = "model-topalidou-.json"
revr = [50,100,200,300,400,500,600,700,800,900,1000,1100]

wh_explr = []
wh_explt = []

for i in revr:
    trial = str(i)
    tsk = "tasks/task-topalidou-reverse-" + trial + ".json"
    rslt = folderRes + trial + ".npy"
    rprt = folderRep + trial + ".txt"
    experiment = Experiment(model = mdl,
                            task = tsk,
                            result = rslt,
                            report = rprt,
                            n_session = 25, n_block = 1, seed = 123)#None)
    records = experiment.run(session)
    records = np.squeeze(records)


    P_mean = np.mean(records["best"],axis=0)
    P_std = np.std(records["best"],axis=0)

    temp = np.where(P_mean>0.0)[0]
    wh_explr.append(temp[np.where(temp>i)[0]][0])

    temp = np.where((P_mean==1.0) & ( P_std==0.0))[0]
    wh_explt.append(temp[np.where(temp>i)[0]][0])






plt.close("all")
plt.figure(figsize=(16, 10), facecolor="w")
n_trial = len(experiment.task)

ax = plt.subplot(111)

ax.patch.set_facecolor("w")
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.yaxis.set_ticks_position('left')
ax.yaxis.set_tick_params(direction="in")
ax.xaxis.set_ticks_position('bottom')
ax.xaxis.set_tick_params(direction="in")
X = 1 + np.arange(n_trial)

plt.plot(revr, np.array(wh_explr), c='b', lw=2)
plt.plot(revr, np.array(wh_explt), c='r', lw=2)

plt.xlabel("\nReverse trial", fontsize=16)
plt.ylabel("Number of trials\n", fontsize=16)
# plt.xlim(1,n_trial)
# plt.ylim(-0.25,1.25)
plt.xticks(revr)
plt.text(n_trial + 1, P_mean[-1], "%.2f" % P_mean[-1],
         ha="left", va="center", color="b")
plt.text(0, P_mean[0], "%.2f" % P_mean[0],
         ha="left", va="center", color="b")


fl = folderFig + "relearn-display.pdf"
plt.savefig(fl)
#
plt.show()