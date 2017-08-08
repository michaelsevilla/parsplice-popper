import warnings; warnings.filterwarnings('ignore')
import matplotlib, tarfile, shutil, os, glob
import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np

def plot_times(ax, label, results):
    df = pd.read_csv(results + "/times.out", delimiter=" ", index_col=False, names=["wc", "traj"])
    ax.plot(df["wc"], df["traj"], label=label)
    ax.set_ylabel("Trajectory (seconds)")
    ax.set_xlabel("Wall Clock Time (seconds)")
    ax.set_title("Trajectory Length vs. Wall Clock Time")
    ax.legend(ncol=2)

def plot_trajs(ax, label, results):
    # parse and find unique states
    df = pd.read_csv(results + "/traj.out", delimiter=" ", index_col=False, names=["space", "id", "len"])
    del df['space']    
    ids = pd.unique(df['id'].ravel())
    state = []
    for val in df['id']: 
        state.append(np.where(ids==val)[0][0])
    df['state'] = state
    
    # iterate to set x and y values
    x = []; y = []; i = 0
    for index, row in df.iterrows():
        for _ in range(0, row['len']):
            x.append(i)
            y.append(row['state'])
            i = i + 1
    ax.plot(x, y, label=label, marker='o')
    ax.set_title("Molecules Bouncing Between States")
    ax.set_ylabel("States")
    ax.set_xlabel("Wall Clock Time (seconds)")
    ax.legend(ncol=2)

# input: ax = where to plot
# input: results = directory with results
# input: op = operation to pull out
# input: nodes = list of nodes
def plot_keyspace(ax, op, nodes, title, results, off=0.3): 
    max_keyspace = pd.DataFrame(columns=['key', 'count']) # keyspace of server w/ biggest keyspace
    shift = 0
    for node in nodes:
        
        # preprocess data      
        try: shutil.rmtree("tmp")
        except: pass
        tar = tarfile.open(results + "/" + node[0] + "/parsplice-logs.tar.gz")
        tar.extractall()
        tar.close() 
        os.system("cat tmp/parsplice-logs/p.* | grep Semantic > tmp/keyspace.log") # hack!
        
        # transform data frame and count # of unique keys
        df = pd.read_csv("tmp/keyspace.log", names=['NULL', 'time', 'op', 'dbkey', 'key'])
        d = df[(df['op'] == op)].groupby('key').size()
        d = d.reset_index()
        d.columns=['key', 'count']
        
        # plot it (break if we don't find any ops)
        if len(d) == 0: continue 
        ax.bar(np.arange(len(d['key']))+shift, d['count'], width=0.3, label=node[1])
        shift = shift + off
        
        # collect statistics (save off largest keyspace)
        if len(d['key']) > len(max_keyspace['key']): 
            max_keyspace = d 

    # graph post processing
    x = np.arange(len(max_keyspace['key']))
    ax.set_xticks(x)
    ax.set_xticklabels([])
    ax.set_xlabel("Key ID")
    #ax.set_xticklabels(keys, rotation=90)
    ax.set_xlim(0, len(max_keyspace['key']))
    ax.set_title(title)
    ax.legend()

    # statistics
    hk_idx = max_keyspace['count'].idxmax() # index of hottest key
    hotkey = max_keyspace.loc[hk_idx]       # row of the hottest key
    print title + ":\tnkeys=" + str(len(hotkey['key'])) + ", hottest key=" + str(hotkey[0]) + " (count=" + str(hotkey[1]) + ")"

def plot_trinitite_keyspace(ax, op, title, results): 
    # preprocess data    
    try: shutil.rmtree("tmp")
    except: pass
    os.mkdir("tmp")            
    os.system("cat " + results + "/basic-psplice-* | grep Semantic > tmp/keyspace.log") # ouch!
    
    # transform data frame and count # of unique keys
    df = pd.read_csv("tmp/keyspace.log", names=['NULL', 'time', 'op', 'dbkey', 'key'])
    d = df[(df['op'] == op)].groupby('key').size()
    d = d.reset_index()
    d.columns=['key', 'count']
    
    # plot it (break if we don't find any ops)
    if len(d) == 0: return
    x = np.arange(len(d['key']))
    ax.bar(x, d['count'], width=0.3, label="all")
    ax.set_xticks(x)
    ax.set_xlabel("Key ID")
    ax.set_xticklabels([])    
    #ax.set_xticklabels(d['key'], rotation=90)
    ax.set_title(title)
    ax.legend()
    
    maxkey = d.loc[d['count'].idxmax()]
    print title + ":\tnkeys=" + str(len(d['key'])) + ", hottest key=" + str(maxkey[0]) + " (count=" + str(maxkey[1]) + ")"
    
def plot_op_sweep(op, piha_nodes, clab_nodes):
    fig, ax = plt.subplots(1, 4, figsize=(16, 3))
    dirname = "../experiments/baseline/results-parmsweep-keyspace"
    plot_keyspace(ax[0], op, piha_nodes, "PIHA (1K,  2K)", dirname + "/t1000it2000-rundev")
    plot_keyspace(ax[1], op, piha_nodes, "PIHA (2K,  4K)", dirname + "/t2000it4000-rundev")
    plot_keyspace(ax[2], op, piha_nodes, "PIHA (400, 2K)", dirname + "/t400it2000-rundev")
    plot_trinitite_keyspace(ax[3], op, "CRAY (1K, 2K)", "../experiments/baseline-trinitite/")
    x = ax[0].set_ylabel(op + " Ops")

    fig, ax = plt.subplots(1, 4, figsize=(16, 3))
    plot_keyspace(ax[0], op, clab_nodes, "CLAB (1K,  2K)", dirname + "/t1000it2000-runcloudlab")
    plot_keyspace(ax[1], op, clab_nodes, "CLAB (2K,  4K)", dirname + "/t2000it4000-runcloudlab")
    plot_keyspace(ax[2], op, clab_nodes, "CLAB (400, 2K)", dirname + "/t400it2000-runcloudlab")
    plot_keyspace(ax[3], op, clab_nodes, "CLAB (400, 8K)", dirname + "/t400it8000-runcloudlab")
    x = ax[0].set_ylabel(op + " Ops")

# input: ax = where to plot
# input: results = directory with results
# input: op = operation to pull out
# input: nodes = list of nodes
def plot_keytimes(ax, ax2, op, nodes, title, results, off=0.3): 
    max_keyspace = pd.DataFrame(columns=['key', 'count']) # keyspace of server w/ biggest keyspace
    shift = 0 
    for node in nodes:
        
        # preprocess data      
        try: shutil.rmtree("tmp")
        except: pass
        tar = tarfile.open(results + "/" + node[0] + "/parsplice-logs.tar.gz")
        tar.extractall()
        tar.close() 
        os.system("cat tmp/parsplice-logs/p.* | grep Semantic > tmp/keyspace.log") # hack!
        
        # transform data frame and filter by op
        df = pd.read_csv("tmp/keyspace.log", names=['NULL', 'time', 'op', 'dbkey', 'key'])
        df = df[df['op'] == op]
        d = df.groupby('time').size()
        d = d.reset_index()
        d.columns=['time', 'count']        
        
        # plot keyspace on y1 and time series on y2 (break if we don't find any ops)
        if len(df) == 0: continue
        ids = pd.unique(df['key'].ravel())
        state = []
        for val in df['key']: 
            state.append(np.where(ids==val)[0][0])
        df['state'] = state
        ax.scatter(df['time'], df['state'], label=node[1])        
        ax2.plot(d['time'], d['count'])        
        
        # collect statistics (save off largest keyspace)
        if len(df['key']) > len(max_keyspace['key']): 
            max_keyspace = df
        #print title + ":\tunique ts=" + str(len(df['key'])) + ", hottest key=" + str(hotkey[0]) + " (count=" + str(hotkey[1]) + ")"
        
    ax.set_xticklabels([])
    ax2.set_xticklabels([])    
    ax.set_xlabel("Wall Clock Time (seconds)")
    ax2.set_xlabel("Wall Clock Time (seconds)")    
    ax.set_title(title)

def plot_trinitite_keytimes(ax, ax2, op, title, results):
    # preprocess data    
    try: shutil.rmtree("tmp")
    except: pass
    os.mkdir("tmp")            
    os.system("cat " + results + "/basic-psplice-* | grep Semantic > tmp/keyspace.log") # ouch!
    
    # transform data frame and count # of unique keys
    df = pd.read_csv("tmp/keyspace.log", names=['NULL', 'time', 'op', 'dbkey', 'key'])
    df = df[df['op'] == op]
    d = df.groupby('time').size()
    d = d.reset_index()
    d.columns=['time', 'count']        
        
    # plot keyspace on y1 and time series on y2 (break if we don't find any ops)
    if len(df) == 0: return
    ids = pd.unique(df['key'].ravel())
    state = []
    for val in df['key']: 
        state.append(np.where(ids==val)[0][0])
    df['state'] = state
    ax.scatter(df['time'], df['state'], label="splicer/DB")        
    ax2.plot(d['time'], d['count'])        

    ax.set_xticklabels([])
    ax2.set_xticklabels([])    
    ax.set_xlabel("Wall Clock Time (seconds)")
    ax2.set_xlabel("Wall Clock Time (seconds)")    
    ax.set_title(title)
    
def plot_op_sweep_keytimes(op, piha_nodes, clab_nodes):
    fig, ax = plt.subplots(2, 4, figsize=(16, 5))
    dirname = "../experiments/baseline/results-parmsweep-keyspace"
    plot_keytimes(ax[0][0], ax[1][0], op, piha_nodes, "PIHA (1K, 2K)", dirname + "/t1000it2000-rundev")
    plot_keytimes(ax[0][1], ax[1][1], op, piha_nodes, "PIHA (2K, 4K)", dirname + "/t2000it4000-rundev")
    plot_keytimes(ax[0][2], ax[1][2], op, piha_nodes, "PIHA (400, 2K)", dirname + "/t400it2000-rundev")
    plot_trinitite_keytimes(ax[0][3], ax[1][3], op, "TRINITITE (1K, 2K)", "../experiments/baseline-trinitite/")
    x = ax[0][0].set_ylabel("State")
    x = ax[1][0].set_ylabel(op + " Ops/Sec")

    fig, ax = plt.subplots(2, 4, figsize=(16, 5))
    plot_keytimes(ax[0][0], ax[1][0], op, clab_nodes, "CLAB (1K,  2K)", dirname + "/t1000it2000-runcloudlab")
    plot_keytimes(ax[0][1], ax[1][1], op, clab_nodes, "CLAB (2K,  4K)", dirname + "/t2000it4000-runcloudlab")
    plot_keytimes(ax[0][2], ax[1][2], op, clab_nodes, "CLAB (400, 2K)", dirname + "/t400it2000-runcloudlab")
    plot_keytimes(ax[0][3], ax[1][3], op, clab_nodes, "CLAB (400, 8K)", dirname + "/t400it8000-runcloudlab")
    x = ax[0][0].set_ylabel("State")
    x = ax[1][0].set_ylabel(op + " Ops/Sec")

