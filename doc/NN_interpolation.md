# NN Interpolation
1. Get row ratio and column ratio by using the formula below:
$$
\begin{aligned}
    \text{row ratio} &= \frac{\text{target row size}}{\text{original row size}}\\[5mm]
    \text{column ratio} &= \frac{\text{target column size}}{\text{original column size}}\\
\end{aligned}
$$
2. Create 2 evenly spaced values vectors starting from 1, one for row, another for columns (row-wise pixel position vector and column-wise pixel position vector)
3. Performe element-wise division for row-wise pixel position vector with height ratio and column-wise pixel position vector with column ratio
4. Perform ceiling for every element in both vectors then perform element-wise subtraction by 1
5. Perform row-wise interpolation on every columns of the original matrix using row-wise pixel position vector
6. Then perform column-wise interpolation on every rom of the previous matrix using column-wise pixel position vector