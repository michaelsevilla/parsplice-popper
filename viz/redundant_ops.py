import warnings; warnings.filterwarnings('ignore')
import matplotlib, tarfile, shutil, os, glob
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

names = {"0": "Splicer", "1": "Worker", "2": "PersistentDB",
         "3": "InMemoryDB", "4": "WorkManager", -1: "all ranks"}

def untar(fname):
    try: shutil.rmtree("tmp")
    except: pass
    os.mkdir("tmp")
    tar = tarfile.open(fname)
    tar.extractall()
    tar.close()

### Boring Parsing Info
# The data structure we read into is a dictionary, where the key is a tuple that identifies the job and the 
# value is a tuple with parsed data in Python data frames. The `parse()` function reads the raw data and 
# puts it into the dictionary:
#
# dfs[(name, op, rank)] => {KEY TIMES, KEY COUNT}
#
# where `name` is a human readable string that describes the job, `op` is the type of database operation,
# `rank` is the MPI rank number, `KEY TIMES` has keys and timestamps, and `KEY COUNT` has keys and counts (i.e. # 
# of occurences). We save `countDF` because it takes forever to parse this data.
def parse(dfs, name, results):
    stats = []
    for rank in ["0", "1", "2", "3", "4"]:
        untar(results + "/out/semanticPerf." + rank + ".tar.gz")
        shutil.move("semanticPerf." + rank, "tmp/semanticPerf." + rank)
        for op in ["DBMemoryPut", "DBMemoryGet"]:
            os.system("cat tmp/semanticPerf." + rank + " | grep " + op + " > tmp/keyspace.log")
            df_op = pd.read_csv("tmp/keyspace.log", names=['ts', 'op', 'dbkey', 'key'])
            if len(df_op) == 0: 
                continue           
            dfs[(name, op, rank)] = {}
            dfs[(name, op, rank)]['DF_KEY_TIMES'] = {}
            dfs[(name, op, rank)]['DF_KEY_COUNT'] = {}
            dfs[(name, op, rank)]['DF_KEY_TIMES'] = df_op
            dfs[(name, op, rank)]['DF_KEY_COUNT'] = df_op.groupby('key').size().reset_index()
            dfs[(name, op, rank)]['DF_KEY_COUNT'].columns=['key', 'count']

            # print stats
            stat = dfs[(name, op, rank)]['DF_KEY_COUNT']
            hotK = stat.loc[stat['count'].idxmax()]
            stats.append(name + " " + op + " " + names[rank] + ": nkeys=" + str(len(stat['key']))
                         + ", hottest key=" + str(hotK[0]) + " (count=" + str(hotK[1]) + ")")
    print "... DONE!",
    return stats

def parse_workerops(dfs, name, results):
    stats = []
    for rank in ["0", "1", "2", "3", "4"]:
        untar(results + "/out/semanticPerf." + rank + ".tar.gz")
        shutil.move("semanticPerf." + rank, "tmp/semanticPerf." + rank)
        for op in ["WGetMINIMA", "WPutMINIMA"]:
            os.system("cat tmp/semanticPerf." + rank + " | grep " + op + " > tmp/keyspace.log")
            df_op = pd.read_csv("tmp/keyspace.log", names=['ts', 'op', 'ID', 'key'])
            if len(df_op) == 0: 
                continue           
            dfs[(name, op, rank)] = {}
            dfs[(name, op, rank)]['DF_KEY_TIMES'] = {}
            dfs[(name, op, rank)]['DF_KEY_COUNT'] = {}
            dfs[(name, op, rank)]['DF_KEY_TIMES'] = df_op
            dfs[(name, op, rank)]['DF_KEY_COUNT'] = df_op.groupby('key').size().reset_index()
            dfs[(name, op, rank)]['DF_KEY_COUNT'].columns=['key', 'count']

            # print stats
            stat = dfs[(name, op, rank)]['DF_KEY_COUNT']
            hotK = stat.loc[stat['count'].idxmax()]
            stats.append(name + " " + op + " " + names[rank] + ": nkeys=" + str(len(stat['key']))
                         + ", hottest key=" + str(hotK[0]) + " (count=" + str(hotK[1]) + ")")
    print "... DONE!", 
    return stats

def parse_perfcounters(results):
    untar(results + "/out/perf.tar.gz")
    shutil.move("perf", "tmp/perf")
    frame = pd.DataFrame()
    list_ = []
    for ts in range(1503107100, 1503122101):
        file_ = "tmp/perf/perf.1."+str(ts)
        if not os.path.exists(file_):
            continue
        df = pd.read_csv(file_, names=['op', 'count', 'ts'])
        list_.append(df)
    frame = pd.concat(list_)
    print "... DONE!", 
    return frame

def plot_uniquekeys_per_ts(ax, dfs, key_tuple, ylim=800, shift=0):
    df = dfs[key_tuple]['DF_KEY_TIMES']            # get all timestamps for all keys
    
    df_t = df.groupby('ts').size().reset_index()   # throughput
    df_t.columns=['ts', 'count']
    
    df_u = df.drop_duplicates()                    # only find unique keys by dropping duplicates
    df_u = df_u.groupby('ts').size().reset_index() # for each time stamp, count the unique
    df_u.columns=['ts', 'count']
    
    ax.plot(df_t['ts'], df_t['count'], label="all keys\n(y1 axis)")
    ax2 = ax.twinx()
    ax2.scatter(df_u['ts'], df_u['count'], color='black', s=5, label="unique keys\n(y2 axis)", marker='X')
    ax.set_title("WM get/sec")
    ax.set_xticklabels([])
    ax.set_xlabel("Time (4 hour)")
    ax.yaxis.labelpad = 20
    ax.set_ylim(0, 1200)
    ax2.set_ylim(0, 60)
    ax.legend(loc='upper left', frameon=False)
    ax2.legend(loc='upper right', frameon=False)    
    return ax2

def plot_uniquekeys_per_worker(ax, dfs, jobid):
    df = dfs[jobid]['DF_KEY_TIMES']            # get all timestamps for all keys
    COLS = ['ts', 'count']
    for key in ["14045287823504495930", "7945113548248993750"]:
        for i in range(0, 2):
        
            df_key = df[(df['ID'] == i) & (df['key'] == key)]
            df_key = df_key.groupby('ts').size().reset_index()
            df_key.columns = COLS
        
            df_first = pd.DataFrame(columns=COLS)
            df_last  = pd.DataFrame(columns=COLS)
            df_first['ts'] = [np.min(df_key['ts'] - 1)]
            df_last['ts']  = [np.max(df_key['ts'] + 1)  ]    
            df_first['count'] = [0]
            df_last['count']= [0]        
        
            p = pd.concat([df_first, df_key, df_last])
            if i == 0: lw = 6
            else: lw = 2
            l = 'Worker=' + str(i) + '; Key=' + key[0:3] + "..."
            ax.plot(p['ts'], p['count'], lw=lw, label=l)
    ax.legend(loc='upper middle', bbox_to_anchor=(0.15, 0.57),)
    ax.set_xticklabels([])
    ax.set_xlabel("Time (1 Minute)")
    ax.set_title("2 Ws get/sec")
    ax.set_ylim(0, 20)
    ax.set_yticklabels(['{:3.0f}'.format(yval) for yval in ax.get_yticks()])    
    
def plot_redundant_puts(ax, frame):
    df_unique = frame[(frame['op'] == 'DBMemory')]
    df_totals = frame[(frame['op'] == 'DBMemoryPut')]
    df = pd.merge(df_unique, df_totals, on='ts')
    ax.plot(df['ts'], df['count_y'] - df['count_x'], color='red', lw=1, label="Redundant put()")
    ax.plot(df['ts'], df['count_y'], color='blue', lw=1, label="put()")
    ax.set_xticks([])
    ax.set_xticks([])
    ax.set_xlabel("Time (4 Hours)")
    ax.legend()
    ax.set_yticklabels(['{:3.1f}M'.format(yval/1000000) for yval in ax.get_yticks()])
    ax.set_title("WM total puts")
    
def plot_uniquekeys_puts(ax, frame):
    df = frame[(frame['op'] == 'DBMemory')]
    ax.plot(df['ts'], df['count'], color='red', lw=4, label="Unique Keys")
    ax.set_xticks([])
    ax.set_xticks([])
    ax.set_xlabel("Time (4 Hours)")
    ax.legend(loc='upper left')
    ax.set_yticklabels(['{:3.0f}K'.format(yval/1000) for yval in ax.get_yticks()])
    ax.set_title("WM keys")
    
