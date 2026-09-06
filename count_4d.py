import time
import math

def count_4d_brute_force(r):
    """Naive O(r^4) volume check."""
    r2 = r * r
    count = 0
    for w in range(-r, r + 1):
        w2 = w * w
        for z in range(-r, r + 1):
            z2 = z * z
            if w2 + z2 > r2:
                continue
            for y in range(-r, r + 1):
                y2 = y * y
                if w2 + z2 + y2 > r2:
                    continue
                for x in range(-r, r + 1):
                    if w2 + z2 + y2 + x * x <= r2:
                        count += 1
    return count

def count_4d_paired_profile(r):
    """
    Morris Dimension-Paired Framework:
    Collapses O(r^4) -> O(r^2) by mapping the 2D profile once
    and pairing the orthogonal (x,y) and (z,w) planes.
    """
    r2 = r * r
    
    # Step 1: Precompute 2D profile f[m] in O(r^2)
    f = [0] * (r2 + 1)
    for x in range(-r, r + 1):
        x2 = x * x
        for y in range(-r, r + 1):
            s = x2 + y * y
            if s <= r2:
                f[s] += 1
                
    # Step 2: Build cumulative disk profile F[k] in O(r^2)
    F = [0] * (r2 + 1)
    running_sum = 0
    for m in range(r2 + 1):
        running_sum += f[m]
        F[m] = running_sum
        
    # Step 3: Convolve the two identical profiles in O(r^2)
    total_4d = 0
    for v in range(r2 + 1):
        if f[v] != 0:
            total_4d += f[v] * F[r2 - v]
            
    return total_4d

if __name__ == "__main__":
    # Stage 1: Mathematical Equivalence Verification (Small Scale)
    r_test = 3
    print(f"--- Verification Check at r = {r_test} ---")
    val_brute = count_4d_brute_force(r_test)
    val_paired = count_4d_paired_profile(r_test)
    print(f"Brute Force O(r^4) Count   : {val_brute}")
    print(f"Paired Profile O(r^2) Count: {val_paired}")
    assert val_brute == val_paired, "Error: Counts do not match!"
    print("Exact Match Confirmed!\n")

    # Stage 2: Scaled Performance Run (O(r^2) Alone)
    r_scale = 200
    print(f"--- Dimension-Paired Execution at r = {r_scale} ---")
    t0 = time.perf_counter()
    val_scaled = count_4d_paired_profile(r_scale)
    t1 = time.perf_counter()
    
    print(f"Lattice Point Count : {val_scaled}")
    print(f"Python Compute Time : {(t1 - t0) * 1000:.2f} ms\n")