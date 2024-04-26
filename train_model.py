import data_handler as dh
import pandas as pd
data = dh.get_all_cdi()
le = dh.get_all_le()

pd.merge