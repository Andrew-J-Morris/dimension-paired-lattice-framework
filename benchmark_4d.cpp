#include <iostream>
#include <vector>
#include <chrono>

using namespace std;
using namespace std::chrono;

// ============================================================================
// DIMENSION-PAIRED 4D ENUMERATION - O(r^2)
// Populates integer combinatorial arrays to collapse exponential nesting.
// Bypasses the FPU entirely through pure integer arrays and dot products.
// ============================================================================
long long count_4d_paired_profile(long long r) {
    long long r2 = r * r;

    // Step 1: Precompute 2D profile f[m] in O(r^2)
    vector<long long> f(r2 + 1, 0);
    for (long long x = -r; x <= r; ++x) {
        long long x2 = x * x;
        for (long long y = -r; y <= r; ++y) {
            long long s = x2 + y * y;
            if (s <= r2) {
                f[s]++;
            }
        }
    }

    // Step 2: Build cumulative disk profile F[k] in O(r^2)
    vector<long long> F(r2 + 1, 0);
    long long running_sum = 0;
    for (long long m = 0; m <= r2; ++m) {
        running_sum += f[m];
        F[m] = running_sum;
    }

    // Step 3: Convolve the two identical profiles in O(r^2)
    long long total_4d = 0;
    for (long long v = 0; v <= r2; ++v) {
        if (f[v] != 0) {
            total_4d += f[v] * F[r2 - v];
        }
    }

    return total_4d;
}

int main() {
    long long r = 500; // Demonstrates O(r^2) scaling without millisecond truncation
    cout << "Starting FPU-Free 4D Dimension-Paired Benchmark (r = " << r << ")..." << endl;
    cout << "--------------------------------------------------------" << endl;

    auto start = high_resolution_clock::now();
    long long points = count_4d_paired_profile(r);
    auto stop = high_resolution_clock::now();
    auto duration_us = duration_cast<microseconds>(stop - start);

    cout << "Dimension-Paired O(r^2) Engine:" << endl;
    cout << "Lattice Points : " << points << endl;
    cout << "Elapsed Time   : " << duration_us.count() / 1000.0 << " ms (" 
         << duration_us.count() << " us)" << endl;

    return 0;
}