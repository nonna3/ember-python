import json
import numpy as np
import pprint
from scipy.stats import norm

date="Apr26"

distributions = {}
def init_model():
    with open("../model/retention1s.csv", "r") as f:
        lines = f.readlines()
        for line in lines:
            tokens = line.split(',')
            tmin, tmax, distr = int(tokens[0]), int(tokens[1]), list(map(int, tokens[2:]))
            distributions[(tmin, tmax)] = distr
    # print(distributions)


def level_inference(BER):
    levels = []
    for tmin in range(0, 60):
        tmax = tmin + 4
        RelaxDistr = distributions[(tmin, tmax)]
        Rlow, Rhigh = getReadRange(RelaxDistr, BER)
        # assert Rlow <= tmin and tmax <= Rhigh, (Rlow, Rhigh, tmin, tmax)
        if len(levels) == 0:
            levels.append([Rlow, Rhigh, tmin, tmax])
        else:
            if Rlow >= levels[-1][1]: # current level does not overlap with prior level's Rhigh
                levels.append([Rlow, Rhigh, tmin, tmax])
    levels[0][0] = 0
    levels[len(levels)-1][1] = 63
    return levels

def longest_non_overlap(levels):
    # this is a greedy algorithm
    # levels is a list of levels, each level is a list of [Rlow, Rhigh, tmin, tmax]
    res = []
    # first sort by Rhigh
    sorted_levels = sorted(levels, key=lambda x: x[1])
    res.append(sorted_levels[0])
    cur = sorted_levels[0]
    for i in range(1, len(sorted_levels)):
        nxt = sorted_levels[i]
        # the next level's Rlow does not overlap with the current level's Rhigh
        if nxt[0] >= cur[1]:
            res.append(nxt)
            cur = nxt
    return res

def getReadRange(distr, number_of_sigma):
    '''
    Goal: get the read range based on the specified sigma

    distr: the resistance distribution
    number_of_sigma: the SBA technique's input, e.g., 3.
    3 simga is the reported number used in the paper: 
    - Resistive RAM With Multiple Bits Per Cell: Array-Level Demonstration of 3 Bits Per Cell

    API reference:
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html
    '''
    # here we get the read range based on the specified sigma
    sigma = np.std(distr)
    mean = np.mean(distr)
    # Get percentiles using Cumulative Distribution Function (cdf) for normal distribution
    # E.g., norm.cdf(-1, loc=0, scale=1) = 15.87%
    # E.g., normal.cdf(1, loc=0, scale=1) = 84.13%
    percentile1 = norm.cdf(-number_of_sigma, loc=0, scale=1)
    percentile2 = norm.cdf(number_of_sigma, loc=0, scale=1)
    # Given the percentile, and the distribution of write, get the read regions
    read_low = norm.ppf(percentile1, loc=mean, scale=sigma)
    read_high = norm.ppf(percentile2, loc=mean, scale=sigma)
    return read_low, read_high

def refine(level_alloc):
    '''
    close the gap between adjacent read ranges
    Example: list of [Rlow, Rhigh, tmin, tmax]
        [2, 14, 0, 4], [16, 28, 16, 20], [32, 44, 33, 37], [48, 56, 46, 50]
    --> [2, 15, 0, 4], [15, 30, 16, 20], [30, 46, 33, 37], [46, 56, 46, 50]
    --> [0, ...                                               , 63, ...  ]
    '''
    for i in range(1, len(level_alloc)):
        merge = int((level_alloc[i - 1][1] + level_alloc[i][0]) / 2)
        level_alloc[i - 1][1] = merge
        level_alloc[i][0] = merge
    level_alloc[0][0] = 0
    level_alloc[len(level_alloc)-1][1] = 63
    return level_alloc

def minimal_BER(sigma_start, sigma_end, sigma_delta):
    res = {}
    while sigma_start <= sigma_end:
        levels = level_inference(sigma_start)
        num_level = len(levels)
        print(f"Solved for {num_level}")
        if num_level not in res.keys():
            res[num_level] = levels
        sigma_start += sigma_delta
    return res

def read_from_json(filename):
    return json.load(open(filename))

def write_to_json(data, filename):
    json.dump(data, open(filename, "w"), indent=1)

def dump_to_json(level_alloc):
    if len(level_alloc) == 16:
        bits_per_cell = 4
    elif len(level_alloc) == 8:
        bits_per_cell = 3
    elif len(level_alloc) == 4:
        bits_per_cell = 2
    bpc = read_from_json(f"../settings/{bits_per_cell}bpc.json")
    for i in range(0, len(level_alloc)):
        # [Rlow, Rhigh, tmin, tmax]
        bpc['level_settings'][i]["adc_upper_read_ref_lvl"] = level_alloc[i][1]
        bpc['level_settings'][i]["adc_lower_write_ref_lvl"] = level_alloc[i][2]
        bpc['level_settings'][i]["adc_upper_write_ref_lvl"] = level_alloc[i][3]
    write_to_json(bpc, f"../settings/{bits_per_cell}bpc_SBA_{date}.json")


if __name__ == "__main__":
    init_model()
    res = minimal_BER(0.5, 2, 0.1)
    dump_to_json(res[4])
    dump_to_json(res[8])
