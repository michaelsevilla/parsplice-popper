import warnings; warnings.filterwarnings('ignore')
import matplotlib, tarfile, shutil, os, glob
import matplotlib.pyplot as plt
import pandas as pd

def plot_times(results, xlim=1750, ylim=20):
    ax = plt.subplot(111)
    for i in range(0, len(results)):

        # ingest and plot it!
        df = pd.read_csv("../" + results[i] + "/times.out", 
                         delimiter=" ", index_col=False, names=["wc", "traj"])
	label = os.path.basename(results[i]).split('results-')[1].split('.')[0]
        ax.plot(df["wc"], df["traj"], label=label)

        # labels and axes
        ax.set_ylabel("Trajectory (seconds)")
        ax.set_xlabel("Wall Clock Time (seconds)")

    ax.legend(bbox_to_anchor=(0.75, 0.75, 1., .102), fontsize=14)
    ax.set_title("t = Temperature, it = Initial Temperature")

def plot_dbactivity(results, dbnode="issdm-11", ylim=6):
    fig, ax = plt.subplots(len(results), 1, figsize=(4, len(results)))
    for i in range(0, len(results)):

        # ingest and process
        try: shutil.rmtree("tmp")
        except: pass
        tar = tarfile.open("../" + results[i] + "/" + dbnode + "/parsplice-logs.tar.gz")
        tar.extractall()
        tar.close()
        df = pd.read_csv("tmp/parsplice-logs/perf.diff")

        # plot
        for op in [" ApiWrite",  " ApiGet", " ApiOpen"]:
            data = df[(df[" name"] == op)]
            ax[i].plot(data["time"], data[" count"], label=op)

        # labels and axis
        ax[i].set_xticklabels([])
        ax[i].set_ylim(0, ylim)
        ax[i].legend(bbox_to_anchor=(1, 1.02, 1., .102))
        run = os.path.basename(results[i]).split('results-')[1].split('.')[0]
        ax[i].text(1.1,.5, run, horizontalalignment='left', transform=ax[i].transAxes)

    # only label the last plot
    ax[(len(results)-1)/2].set_ylabel("Database Ops")
    ax[len(results)-1].set_xlabel("Wall Clock Time (seconds)")

def plot_psactivity(results, dbmemnode="issdm-12", ylim=6):
    fig, ax = plt.subplots(len(results), 1, figsize=(4, 1.5*len(results)))
    for i in range(0, len(results)):

        # ingest and process
        try: shutil.rmtree("tmp")
        except: pass
        fname = "../" + results[i] + "/" + dbmemnode + "/parsplice-logs.tar.gz"
        tar = tarfile.open(fname)
        tar.extractall()
        tar.close()
        df = pd.DataFrame()
        perfdumps = glob.glob("tmp/parsplice-logs/perf*")
        for p in perfdumps:
            d = pd.read_csv(p, index_col=False, names=["op", "count", "time"])
            t = d["time"][0]
            d = d[["op", "count"]]
            d = pd.pivot_table(d, columns=["op"])
            d = d.reset_index()
            d = d.drop('index', axis=1)
            d["time"] = t
            df = df.append(d)
            df = df.sort_values("time")
        ax[i].plot(df["time"], df["DBMemoryPut"], marker='x')
        ax[i].plot(df["time"], df["DBMemory"])
        ax[i].plot(df["time"], df["DBMemoryGet"], ls='--')
        ax[i].plot(df["time"], df["DBMemorySync"])

        # labels/axis: xticks don't make sense since its unix timestamped
        ax[i].set_xticklabels([])
        ax[i].legend(bbox_to_anchor=(1, 1.02, 1., .102))
        run = os.path.basename(results[i]).split('results-')[1].split('.')[0]
        ax[i].text(1.1,.5, run, horizontalalignment='left', transform=ax[i].transAxes)

    # only label the last plot
    ax[(len(results)-1)/2].set_ylabel("InMemoryDB Ops")
    ax[len(results)-1].set_xlabel("Wall Clock Time (seconds)")
