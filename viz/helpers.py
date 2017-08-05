import warnings; warnings.filterwarnings('ignore')
import matplotlib, tarfile, shutil, os, glob
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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
    ax = plt.subplot(111)

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
    ax.plot(df["time"], df["DBMemoryPut"], marker='x')
    ax.plot(df["time"], df["DBMemory"])
    ax.plot(df["time"], df["DBMemoryGet"], ls='--')
    ax.plot(df["time"], df["DBMemorySync"])

    # labels/axis: xticks don't make sense since its unix timestamped
    ax.set_xticklabels([])
    ax.legend(bbox_to_anchor=(1, 1.02, 1., .102))
    run = os.path.basename(results[i]).split('results-')[1].split('.')[0]
    ax.text(1.1,.5, run, horizontalalignment='left', transform=ax[i].transAxes)

def plot_psactivity_sweep(results, ylim=6):
    nodesofinterest = [2, 3, 4]
    fig, ax = plt.subplots(len(results), 3, figsize=(12, 1.5*len(results)))
    for i in range(0, len(results)):
        print results[i], 
        for j in range(0, len(nodesofinterest)):
            # ingest and process
            try: shutil.rmtree("tmp")
            except: pass
            fname = "../" + results[i] + "/node-" + str(nodesofinterest[j]) + "/parsplice-logs.tar.gz"
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
            ax[i][j].plot(df["time"], df["DBMemoryPut"], marker='x')
            ax[i][j].plot(df["time"], df["DBMemory"])
            ax[i][j].plot(df["time"], df["DBMemoryGet"], ls='--')
            ax[i][j].plot(df["time"], df["DBMemorySync"])

            # labels/axis: xticks don't make sense since its unix timestamped
            ax[i][j].set_xticklabels([])
            ax[i][j].set_ylim(0, 2500)
            if j == len(results) - 1:
                ax[i][j].legend(bbox_to_anchor=(1.3, 0.82, 1., .102))
                run = os.path.basename(results[i]).split('results-')[1].split('.')[0]
                ax[i][j].text(1.3,.5, run, horizontalalignment='left', transform=ax[i][j].transAxes)

    # only label the last plot    
    for i in range(0, len(nodesofinterest)):
        ax[len(results)-1][i].set_xlabel("Wall Clock Time (seconds)")
    for i in range(0, len(results)):
        ax[i][0].set_ylabel("ops")
    ax[0][0].set_title("In-MemoryDB Node")
    ax[0][1].set_title("Work Manager 0")
    ax[0][2].set_title("Work Manager 1")        


# unused...
def plot_cpu(dname):
    if not os.path.isdir(dname):
        print "No directory named " + dname + " please run ./prepare.sh"
        return -1
    def axlabel(i):
        label = ""
        if i == 0:    label = "Splicer"
        elif i == 1:  label = "LevelDB"
        elif i == 2:  label = "In-MemoryDB"
        else:         label = "Worker-" + str(i)
        if i > 2: return 1, label
        else:     return 0, label
    
    figcpu, axcpu = plt.subplots(1, 2, figsize=(14, 4))
    figmem, axmem = plt.subplots(1, 2, figsize=(14, 4))    
    plots = [('user', axcpu), ('used', axmem)]
    for i in range(0,10):
        for metric, ax in plots:
            df = pd.read_table(dname + "/node-" + str(i) + "." + metric + ".out",
                               header=None, sep=(","), skiprows=13,
                               names=("seconds", metric))
            df.loc[1] = df.loc[0]
            df.loc[0] = [0, 0.1]
            df = df[df[metric] != 0]
            axis, label = axlabel(i)
            
            if metric == 'used':
                ax[axis].plot(df[metric]/1048576, label=label, linewidth=2.0)
                ax[axis].set_ylabel("Memory Usage (GB)")
            else:
                ax[axis].plot(df[metric], label=label, linewidth=2.0)
                ax[axis].set_ylabel("CPU Utilization (%)")                
                #ax[axis].set_ylim(0, 100)
        
            ax[0].set_title("Control Plane Ranks")
            ax[1].set_title("Worker Ranks")
            for j in range(0, 2):
                ax[j].legend()

def plot_bar_cpu(dname):
    if not os.path.isdir(dname):
        print "No directory named " + dname + " please run ./prepare.sh"
        return -1

    fig, figax = plt.subplots(1, 2, figsize=(14, 4))    
    cpumeans = []; cpuerror = []; memmeans = []; memerror = []
    plots = [('user', figax[0], cpumeans, cpuerror, 1, 'red'),
             ('used', figax[1], memmeans, memerror, 1024*1024, 'blue')]
    for metric, ax, means, error, scale, color in plots:
        for i in range(0,9):
            df = pd.read_table(dname + "/node-" + str(i) + "." + metric + ".out",
                               header=None, sep=(","), skiprows=13,
                               names=("seconds", metric))
            df = df[df[metric] != 0]            
            means.append((df[metric].mean())/scale)
            error.append(df[metric].std()/scale)
            
        x = np.arange(len(means))
        

        ax.bar(x, means, width=0.75, color=color, yerr=error, linewidth=2, error_kw=dict(ecolor="black", capthick=4))
        ax.set_xticks(x)
        ax.set_xticklabels(["Splicer", "PersistentDB", "InMemoryDB", 
                            "Worker", "Worker", "Worker", "Worker", 
                            "Worker", "Worker", "Worker"], rotation=45)

    vals = figax[0].get_yticks()
    figax[0].set_yticklabels(['{:3.0f}%'.format(x*1) for x in vals])
    figax[0].set_ylabel('Average CPU Utilization')
    figax[1].set_ylabel('Average Memory Usage (GB)')
    figax[0].set_ylim(0, 100)
    figax[1].set_ylim(0, 20)

def plot_other_psactivity(results, ylim=6):
    nodesofinterest = [3, 4]
    fig, ax = plt.subplots(2, 1, figsize=(4, len(results)))
    for j in range(0, len(nodesofinterest)):
        # ingest and process
        try: shutil.rmtree("tmp")
        except: pass
        fname = "../" + results[i] + "/node-" + str(nodesofinterest[j]) + "/parsplice-logs.tar.gz"
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
        ax[j].plot(df["time"], df["DriverPull"], marker='x')
        ax[j].plot(df["time"], df["DriverProc"])
        ax[j].plot(df["time"], df["DriverPush"], ls='--')
        ax[j].plot(df["time"], df["ManagerSend"])
        ax[j].plot(df["time"], df["ManagerReceive"])
        ax[j].plot(df["time"], df["ManagerRelease"])
        ax[j].plot(df["time"], df["ManagerAssign"])

        # labels/axis: xticks don't make sense since its unix timestamped
        ax[j].set_xticklabels([])
        ax[j].legend()
    ax[0].set_title("Work Manager 0")
    ax[1].set_title("Work Manager 1")

