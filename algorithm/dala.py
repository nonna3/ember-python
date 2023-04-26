import time
import tqdm
import sys

date="Apr25"

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
        levels.append([Rlow, Rhigh, tmin, tmax])
    return longest_non_overlap(levels)

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


def getReadRange(vals, BER):
    num_discard = int(BER * len(vals) / 2)
    return vals[num_discard], vals[-num_discard]

def refine(level_alloc):
    # close the gap between adjacent levels
    # List of [Rlow, Rhigh, tmin, tmax]
    for i in range(1, len(level_alloc)):
        merge = int((level_alloc[i - 1][1] + level_alloc[i][0]) / 2)
        level_alloc[i - 1][1] = merge
        level_alloc[i][0] = merge
    return level_alloc

def minimal_BER(specified_levels, eps, low_BER = 0, high_BER = 1):
    while high_BER - low_BER > eps:
        cur_BER = (low_BER + high_BER) / 2
        cur_levels = level_inference(cur_BER)
        print(len(cur_levels), cur_BER)
        if len(cur_levels) < specified_levels: # the precision requirement is too strict to be met
            low_BER = cur_BER # make next BER bigger
        elif len(cur_levels) > specified_levels:
            high_BER = cur_BER
        else:
            high_BER = cur_BER
            best_level, best_BER = cur_levels, cur_BER
    return refine(best_level), best_BER


if __name__ == "__main__":
    init_model()
    print(minimal_BER(4, 0.1))
