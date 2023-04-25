import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# cut ../data/retention1s.csv -f6 -d',' | grep 59 | wc -l
# Each level: 272 cells
data = pd.read_csv("../data/retention1s.csv", delimiter=',')
data["tmid"] = (data["tmin"] + data["tmax"]) / 2
data["write_dis"] = data["after_write"] - data["tmid"]
data["relax_dis"] = data["after_relax"] - data["tmid"]

# plot the distribution of write_dis
write_dis = data["write_dis"].to_numpy()
plt.hist(write_dis, bins=100)
plt.show()

write_dis = data["relax_dis"].to_numpy()
plt.hist(write_dis, bins=100)
plt.show()