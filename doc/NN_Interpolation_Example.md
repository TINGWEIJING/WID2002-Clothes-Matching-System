# NN Interpolation
Given a matrix with the size $3 \times 3$, we want to resize to the size $6 \times 6$

$$
\begin{bmatrix}
    10 & 4 & 22 \\
    2 & 18 & 7 \\
    9 & 14 & 25 \\
\end{bmatrix}
$$

$$
\begin{bmatrix}
    10 &10 & 4 & 4 & 22& 22 \\
    10 &10 & 4 & 4 & 22& 22 \\
    2 & 2 & 18 &18 & 7 & 7 \\
    2 & 2 & 18 &18 & 7 & 7 \\
    9 & 9 & 14 &14 & 25& 25 \\
    9 & 9 & 14 &14 & 25& 25 \\
\end{bmatrix}
$$


1. Get row ratio and column ratio by using the formula below:

$$
\begin{aligned}
    \text{row ratio} &= \frac{\text{target row size}}{\text{original row size}}\\[5mm]
    \text{column ratio} &= \frac{\text{target column size}}{\text{original column size}}\\
\end{aligned}
$$

$$
\begin{aligned}
    \text{row ratio} &= \frac{6}{3} &= 2\\[5mm]
    \text{column ratio} &= \frac{6}{3} &= 2\\
\end{aligned}
$$

2. Create 2 evenly spaced values vectors starting from 1, one for row, another for columns (row-wise pixel position vector and column-wise pixel position vector).

$$
\begin{aligned}
    \text{row}_{\text{ position}} &= 
    \begin{bmatrix}
    1 & 2 & 3 & \dots & 6 \\
    \end{bmatrix} \\[5mm]
    \text{column}_{\text{ position}} &= \begin{bmatrix}
    1 & 2 & 3 & \dots & 6 \\
    \end{bmatrix} \\
\end{aligned}
$$


3. Perform element-wise division for row-wise pixel position vector with height ratio and column-wise pixel position vector with column ratio. Then perform ceiling for every element in both vectors.

$$
\begin{aligned}
    \text{row}_{\text{ position}} &= 
    \lceil {
    \frac{
        \begin{bmatrix}
        1 & 2 & 3 & \dots & 6 \\
        \end{bmatrix}
    }{2}
    } \rceil \\
    &= 
    \begin{bmatrix}
    1 & 1 & 2 & 2 & 3 & 3 \\
    \end{bmatrix} \\[5mm]
    \text{column}_{\text{ position}} &= 
    \lceil {
    \frac{
        \begin{bmatrix}
        1 & 2 & 3 & \dots & 6 \\
        \end{bmatrix}
    }{2}
    } \rceil \\
    &= 
    \begin{bmatrix}
    1 & 1 & 2 & 2 & 3 & 3 \\
    \end{bmatrix} \\[5mm]
\end{aligned}
$$

4. Perform element-wise subtraction by 1.

$$
\begin{aligned}
    \text{row}_{\text{ position}} &= 
    \begin{bmatrix}
    0 \\ 0 \\ 1 \\ 1 \\ 2 \\ 2 \\
    \end{bmatrix} \\[5mm] \\
    \text{column}_{\text{ position}} &= \begin{bmatrix}
    0 & 0 & 1 & 1 & 2 & 2 \\
    \end{bmatrix} \\
\end{aligned}
$$

5. Perform row-wise interpolation on every column of the original matrix using row-wise pixel position vector.

$$
\begin{aligned}
    \begin{bmatrix}
        10 & 4 & 22 \\
        2 & 18 & 7 \\
        9 & 14 & 25 \\
    \end{bmatrix}
    \xRightarrow[\text{row}_{\text{ position}}]{\text{row-wise interpolation}}
    \begin{bmatrix}
        10 & 4 & 22 \\
        10 & 4 & 22 \\
        2 & 18 & 7 \\
        2 & 18 & 7 \\
        9 & 14 & 25 \\
        9 & 14 & 25 \\
    \end{bmatrix}
\end{aligned}
$$


6. Then perform column-wise interpolation on every row of the previous matrix using column-wise pixel position vector.


$$
\begin{aligned}
    \begin{bmatrix}
        10 & 4 & 22 \\
        10 & 4 & 22 \\
        2 & 18 & 7 \\
        2 & 18 & 7 \\
        9 & 14 & 25 \\
        9 & 14 & 25 \\
    \end{bmatrix}
    \xRightarrow[\text{column}_{\text{ position}}]{\text{column-wise interpolation}}
    \begin{bmatrix}
        10 &10 & 4 & 4 & 22& 22 \\
        10 &10 & 4 & 4 & 22& 22 \\
        2 & 2 & 18 &18 & 7 & 7 \\
        2 & 2 & 18 &18 & 7 & 7 \\
        9 & 9 & 14 &14 & 25& 25 \\
        9 & 9 & 14 &14 & 25& 25 \\
    \end{bmatrix}
\end{aligned}
$$