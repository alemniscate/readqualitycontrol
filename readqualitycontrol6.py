import gzip

def analysis(file):
    with gzip.open(file, "rt") as f:
        lines = f.readlines()

    #for line in lines:
    #    print(line.replace("\r", "").replace("\n", ""))

    reads = 0
    nreads = 0
    total_length = 0
    total_n_avg = 0
    total_gc_avg = 0
    genome_set = set()
    k = 0
    while k < len(lines):
        line = lines[k + 1].replace("\r", "").replace("\n", "")
        length = len(line)
        genome_set.add(line)
        n_count = 0
        gc_count = 0
        for nucleotide in line:
            if nucleotide in ("C", "G"):
                gc_count += 1
            elif nucleotide == "N":
                n_count += 1
        total_gc_avg += round(gc_count * 100 / length, 2)
        total_length += length
        if n_count:
            nreads += 1
        total_n_avg += round(n_count * 100 / length, 2)
        reads += 1
        k += 4

    avg_length = round(total_length / reads, 0)
    gc_avg = round(total_gc_avg / reads, 2)
    repeats = reads - len(genome_set)
    n_avg = round(total_n_avg / reads, 2)

    return reads, avg_length, repeats, nreads, gc_avg, n_avg

def print_result(result):
    reads, avg_length, repeats, nreads, gc_avg, n_avg = result
    print(f"Reads in the file = {reads}:")
    print(f"Reads sequence average length = {int(avg_length)}")
    print()
    print(f"Repeats = {repeats}")
    print(f"Reads with Ns = {nreads}")
    print()
    print(f"GC content average = {gc_avg}%")
    print(f"Ns per read sequence = {n_avg}%")
    
def get_best(results):
    max_gc_avg = max([x[-2] for x in results])
    if max_gc_avg < 50:
        for result in results:
            if result[-2] == max_gc_avg:
                return result

    min_gc_avg = min([x[-2] for x in results])
    if min_gc_avg > 60:
        for result in results:
            if result[-2] == min_gc_avg:
                return result

    min_n_avg = min([x[-1] for x in results if 60>= x[-2] >= 50]) 
    for result in results:
        if result[-1] == min_n_avg:
            return result

if __name__ == "__main__":
    file1 = input()
    file2 = input()
    file3 = input()
    file1 = "C:/private/src/python/idea/readqualitycontrol/" + file1
    file2 = "C:/private/src/python/idea/readqualitycontrol/" + file2
    file3 = "C:/private/src/python/idea/readqualitycontrol/" + file3
    #file1 = "C:/private/src/python/idea/readqualitycontrol/test/data1.gz"
    #file2 = "C:/private/src/python/idea/readqualitycontrol/test/data2.gz"
    #file3 = "C:/private/src/python/idea/readqualitycontrol/test/data3.gz"
   
    results = []
    results.append(analysis(file1))
    results.append(analysis(file2))
    results.append(analysis(file3))

    result = get_best(results)

    print_result(result)