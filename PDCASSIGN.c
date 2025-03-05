#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define N 100000000  // Large array size

int main() {
    double start_time, end_time;
    long long sum = 0;
    int *arr = (int *)malloc(N * sizeof(int));
    
    // Initialize array with values
    for (int i = 0; i < N; i++) {
        arr[i] = 1;  // Assigning all values as 1 for simplicity
    }

    // Sequential execution
    start_time = omp_get_wtime();
    for (int i = 0; i < N; i++) {
        sum += arr[i];
    }
    end_time = omp_get_wtime();
    printf("Sequential Sum: %lld, Time: %f seconds\n", sum, end_time - start_time);

    // Reset sum
    sum = 0;
    
    // Parallel execution with OpenMP (Static Scheduling)
    start_time = omp_get_wtime();
    #pragma omp parallel for reduction(+:sum) schedule(static)
    for (int i = 0; i < N; i++) {
        sum += arr[i];
    }
    end_time = omp_get_wtime();
    printf("Parallel Sum (Static): %lld, Time: %f seconds\n", sum, end_time - start_time);
    
    // Reset sum
    sum = 0;
    
    // Parallel execution with OpenMP (Dynamic Scheduling)
    start_time = omp_get_wtime();
    #pragma omp parallel for reduction(+:sum) schedule(dynamic)
    for (int i = 0; i < N; i++) {
        sum += arr[i];
    }
    end_time = omp_get_wtime();
    printf("Parallel Sum (Dynamic): %lld, Time: %f seconds\n", sum, end_time - start_time);
    
    free(arr);
    return 0;
}
