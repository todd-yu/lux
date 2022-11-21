import lux
import pandas as pd

lux.config.topk = False
lux.config.sampling = False

df = pd.read_csv("./data/500k.csv")


first_rec = df.recommendation

# df.delete_row(5)
# print("deleted row!")

df.expire_metadata()
df.expire_recs()


second_rec = df.recommendation