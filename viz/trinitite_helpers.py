import warnings; warnings.filterwarnings('ignore')
import matplotlib, tarfile, shutil, os, glob
import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np

RAW_DF   = 0
COUNT_DF = 1
# parsplice hard codes the ranks, so we can pretty print the names
rank_names = {"00": "Splicer", "01": "Worker", "02": "PersistentDB", "03":
              "InMemoryDB", "04": "WorkManager", -1: "all ranks"}

def keyspace(op, results, task="04"):
    
    # preprocess data    
    try: shutil.rmtree("tmp")
    except: pass
    os.mkdir("tmp")
    if "uo2" in results:
        os.system("cat " + results + "/basic-psplice-* | grep Semantic > tmp/keyspace.log") # ouch!
        df = pd.read_csv("tmp/keyspace.log", names=['NULL', 'time', 'op', 'dbkey', 'key'])
    elif "nano" in results:
        tar = tarfile.open(results + "/logs/perf." + task + ".tar.gz")
        tar.extractall(path="tmp")
        tar.close()
        df = pd.read_csv("tmp/perf." + task + ".log", names=['NULL', 'time', 'op', 'dbkey', 'key'])
    else:
        print "ERROR: can't figure out input type (uo2 or nano)"
        return -1

    # transform data frame and count # of unique keys
    df = df[(df['op'] == op)]
    df_join = df.groupby('key').size()
    df_join = df_join.reset_index()
    df_join.columns=['key', 'count']
    if len(df_join) == 0: return df_join
    maxkey = df_join.loc[df_join['count'].idxmax()]        
    print (op + " " + os.path.basename(results) + " task=" + task
           + ": nkeys=" + str(len(df_join['key']))
           + ", hottest key=" + str(maxkey[0])
           + " (count=" + str(maxkey[1]) + ")")
    return df, df_join

def plot_keyspace_size(ax, dfs, op, task, shift=0):
    # this is the order I want things graphed
    labels = [("UO2", op, -1),
              ("Delay 1M", op, task),
              ("Delay 500K", op, task),
              ("Delay 100K", op, task)]
    ax.bar(np.arange(len(labels)) + shift,
           [len(dfs[l][COUNT_DF]) for l in labels],
           width=0.2, label=rank_names[task])
    ax.set_yticklabels(['{:3.0f}K'.format(x/1000) for x in ax.get_yticks()])      
    ax.set_xticklabels([0] + [l[0] for l in labels], rotation=20)
    ax.set_title("Keyspace Size")
    ax.legend()
    
def plot_keyspace_ops(ax, dfs, op, task, shift=0, color='red'):
    # this is the order I want things graphed
    labels = [("UO2", op, -1),
              ("Delay 1M", op, task),
              ("Delay 500K", op, task),
              ("Delay 100K", op, task)]
    ax.bar(np.arange(len(labels)) + shift,
           [np.sum(dfs[l][COUNT_DF]['count']) for l in labels],
           width=0.2, label=op.split("Memory")[1], color=color)
    ax.set_yticklabels(['{:3.0f}K'.format(x/1000) for x in ax.get_yticks()])        
    ax.set_xticklabels([0] + [l[0] for l in labels], rotation=20)
    ax.set_title(rank_names[task] + "\nKeyspace Operation Counts")    
    ax.legend()

def plot_keyspace(ax, dfs, key, shift=0, nkeys=50):
    # parse and ingest
    dftop = dfs[key][COUNT_DF].nlargest(nkeys, 'count').head(50) # not sure why we need to do head here

    # plot it (break if we don't find any ops)
    if len(dftop) == 0: return -1
    x = np.arange(len(dftop['key']))
    ax.bar(x + shift, dftop['count'], width=0.3, label=rank_names[key[2]])
    
    # cleanup graphs
    ax.set_xticks(x); ax.set_xticklabels([])
    if np.max(ax.get_yticks()) > 2000:
        ax.set_yticklabels(['{:3.0f}K'.format(x/1000) for x in ax.get_yticks()])    
    ax.set_title("Top " + str(nkeys) + " Keys: " + key[0])
    #ax.set_xticklabels(d['key'], rotation=90)

def plot_keytimes(ax, dfs, key_tuple, shift=0, nkeys=50):
    # parse and ingest
    dftop = dfs[key_tuple][COUNT_DF].nlargest(nkeys, 'count').head(50) # not sure why we need to do head here
    #print dftop['key']

    # transform data frame and filter out keys
    raw = dfs[key_tuple][RAW_DF]

    for key in dftop['key']:
        d = raw[(raw['key'] == key)]
        d = d.groupby('time').size()
        d = d.reset_index()
        d.columns=['time', 'count']

        if len(d) == 0: continue
        first    = np.min(d['time'])
        last     = np.max(d['time'])
        ts_range = last - first + 1
        x = np.arange(ts_range) + first
        y = np.zeros(ts_range)
        for k, v in d.iterrows():
            y[v['time'] - first] = v['count']
        ax.plot(x, y, label=key)
        #return 

    # cleanup graphs
    ax.set_xticklabels([])
    ax.set_title(key_tuple[0])
    ax.set_ylabel(op + "/sec")
