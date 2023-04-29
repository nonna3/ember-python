import dala
import matplotlib.pyplot as plt
'''
DALA's 8 level allocation
[[0, 13, 6, 10], [13, 18, 13, 17], [18, 26, 15, 19], [26, 33, 28, 32], 
[33, 37, 31, 35], [37, 45, 38, 42], [45, 51, 45, 49], [51, 64, 55, 59]]
'''
def visualize_8():
    alloc_8 = [[0, 13, 6, 10], [13, 18, 13, 17], [18, 26, 15, 19], [26, 33, 28, 32], 
               [33, 37, 31, 35], [37, 45, 38, 42], [45, 51, 45, 49], [51, 64, 55, 59]]
    for item in alloc_8:
        rmin, rmax, wmin, wmax = item    
        d1s = dala.distributions[(wmin, wmax)]
        # plt.hist(d1s, bins=[i for i in range(0,64)], range=(0,63))
        # plt.axvline(x=wmin, linewidth=2, color='g')
        # plt.axvline(x=wmax, linewidth=2, color='g')
        # plt.axvline(x=rmin, linewidth=2, color='r')
        # plt.axvline(x=rmax, linewidth=2, color='r')
        # plt.show()
        cnt = 0
        tot = 0
        for point in d1s:
            if rmin <= point and point < rmax:
                cnt += 1
            tot += 1
        print(cnt, tot)


if __name__ == "__main__":
    dala.init_model()
    visualize_8()
