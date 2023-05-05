import dala
# import matplotlib.pyplot as plt
dala_4 = [[0, 21, 6, 10], [21, 41, 30, 34], [41, 53, 45, 49], [53, 64, 56, 60]]
dala_8 = [[0, 8, 0, 4], [8, 21, 12, 16], [21, 34, 26, 30], [34, 41, 35, 39], 
          [41, 48, 42, 46], [48, 53, 48, 52], [53, 59, 54, 58], [59, 64, 59, 63]]

sba_4 = [[0, 10, 0, 4], [11, 29, 18, 22], [31, 45, 36, 40], [46, 64, 50, 54]]
sba_8 = [[0, 7, 0, 4], [7, 16, 9, 13], [16, 25, 18, 22], [26, 33, 27, 31],
         [33, 39, 34, 38], [40, 47, 41, 45], [47, 53, 48, 52], [53, 64, 54, 58]]
def simlute_error(level_alloc):
    count = 0
    total = 0
    for item in level_alloc:
        rmin, rmax, wmin, wmax = item    
        d1s = dala.distributions[(wmin, wmax)]
        # plt.hist(d1s, bins=[i for i in range(0,64)], range=(0,63))
        # plt.axvline(x=wmin, linewidth=2, color='g')
        # plt.axvline(x=wmax, linewidth=2, color='g')
        # plt.axvline(x=rmin, linewidth=2, color='r')
        # plt.axvline(x=rmax, linewidth=2, color='r')
        # plt.show()
        # cnt = 0
        # tot = 0
        for point in d1s:
            if rmin <= point and point < rmax:
                # success
                count += 1
            total += 1
    print("success rate", count / total)

def compare(level1, level2):
    simlute_error(level1)
    simlute_error(level2)
    print("-------")

if __name__ == "__main__":
    dala.init_model()
    compare(dala_4, sba_4)
    compare(dala_8, sba_8)
