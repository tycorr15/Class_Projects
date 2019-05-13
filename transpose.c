/*
 ***************  changed only the transpose_submit and trans_solution functions *************** 
 *
 * trans.c - Matrix transpose B = A^T
 *
 * Each transpose function must have a prototype of the form:
 * void trans(int M, int N, int A[N][M], int B[M][N]);
 *
 * A transpose function is evaluated by counting the number of misses
 * on a 1KB direct mapped cache with a block size of 32 bytes.
 */ 
#include <stdio.h>
#include "cachelab.h"

int is_transpose(int M, int N, int A[N][M], int B[M][N]);
void trans_solution(int M, int N, int A[N][M], int B[M][N]);
/* 
 * transpose_submit - This is the solution transpose function that you
 *     will be graded on for Part B of the assignment. Do not change
 *     the description string "Transpose submission", as the driver
 *     searches for that string to identify the transpose function to
 *     be graded. 
 */
char transpose_submit_desc[] = "Transpose submission";
void transpose_submit(int M, int N, int A[N][M], int B[M][N])
{
	trans_solution(M, N, A, B);
}

/* 
 * You can define additional transpose functions below. We've defined
 * a simple one below to help you get started. 
 */ 

/* 
 * trans - A simple baseline transpose function, not optimized for the cache.
 */
char trans_desc[] = "Simple row-wise scan transpose";
void trans(int M, int N, int A[N][M], int B[M][N])
{
    int i, j, tmp;

    for (i = 0; i < N; i++) {
        for (j = 0; j < M; j++) {
            tmp = A[i][j];
            B[j][i] = tmp;
        }
    }    

}

char trans_solution_desc[] = "Solution";

//Code based on O’Hallaron CS:APP2e Web Aside MEM:BLOCKING:
//Using Blocking to Increase Temporal Locality, figure 1
void trans_solution(int M, int N, int A[N][M], int B[M][N])
{
	int i, j, row, column, bsize;
				
	switch (M) {
		case 32: 
			//the only difference in code between the 32x32 and 64x64 arrays is the block size
			bsize = 8;
		case 64:
			if (M == 64) 
				bsize = 4;
			//go from 0-32 touching each column, incremented by bsize = 8
			//outermost loop = full 32x32 or 64x64 array 
			for (column = 0; column < M; column += bsize) {
				//also full 32x32 or 64x64 array
				//from 0-32 touching each row, incremented by bsize = 8
				for (row = 0; row < N; row += bsize) {
					//within each block, increment within the rows and columns of that smaller array
					for (i = column; i < column + bsize; i++) {
						//j are the rows of the smaller array of size bsize
						for (j = row; j < row + bsize; j++) {
						//deal with diagonals (if i == j, it's on the diagonal of the smaller array)
							if ((i != j))
								B[j][i] = A[i][j];
						} 
				
						//if row == column and i == j, then it's on the diagonal o fthe smaller array which is itself on the
						//diagonal of the larger array
						if (row == column)
							B[i][i] = A[i][i];
					}
				}
			}
			
			break;
		case 61:
			bsize = 16;
			//this is the same code as above, except that there is an added condition in the for loops of the smaller arrays
			//since the indexes could go out of bounds due to the assymetric dimensions of A and B
			for (column = 0; column < N; column += bsize) {
		        	for (row = 0; row < M; row += bsize) {
			        	for (i = column; (i < column + bsize) && (i < N); i++) {
			             	   	for (j = row; (j < row + bsize) && (j < M); j++) {
			                		if ((i != j))
			                    			B[j][i] = A[i][j];
			                	}
			                
					if (row == column)
			                	B[i][i] = A[i][i];
			      		}                               
                 		}
			}

			break;
	}
}

/*
 * registerFunctions - This function registers your transpose
 *     functions with the driver.  At runtime, the driver will
 *     evaluate each of the registered functions and summarize their
 *     performance. This is a handy way to experiment with different
 *     transpose strategies.
 */
void registerFunctions()
{
    /* Register your solution function */
   registerTransFunction(transpose_submit, transpose_submit_desc); 

    /* Register any additional transpose functions */
//    registerTransFunction(trans, trans_desc);

}

/* 
 * is_transpose - This helper function checks if B is the transpose of
 *     A. You can check the correctness of your transpose by calling
 *     it before returning from the transpose function.
 */
int is_transpose(int M, int N, int A[N][M], int B[M][N])
{
    int i, j;

    for (i = 0; i < N; i++) {
        for (j = 0; j < M; ++j) {
            if (A[i][j] != B[j][i]) {
                return 0;
            }
        }
    }
    return 1;
}

