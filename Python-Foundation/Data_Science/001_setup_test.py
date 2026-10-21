import numpy as np
import pandas as pd

print("--- Month 7 Environment Check ---")
print(f"NumPy Version: {np.__version__}")
print(f"Pandas Version: {pd.__version__}")

# Let's create a 1D Vector (just like the 3Blue1Brown video)
my_vector = np.array([10, 20, 30])
print(f"\nMy First NumPy Vector: {my_vector}")

# Let's scale the vector by multiplying it by 2
scaled_vector = my_vector * 2
print(f"Scaled Vector (x2): {scaled_vector}")
