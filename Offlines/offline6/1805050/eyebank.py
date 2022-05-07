from dsa1lib.binomialheap import *

if __name__ == "__main__":
    with open("input.txt") as file:
        lines = file.readlines()
        binomial_heap = MaxBinomialHeap[int]()
        for line in lines:
            inputs = line.split()
            operation = inputs[0]
            args = [int(i) for i in inputs[1:]]

            if operation == "INS":
                binomial_heap.insert(args[0])
                print("Inserted", args[0])
            elif operation == "PRI":
                print(binomial_heap)
            elif operation == "INC":
                binomial_heap.increase_key(args[0], args[1])
                print(f"Increased {args[0]}. The updated value is {args[1]}")
            elif operation == "FIN":
                print("FindMax returned", binomial_heap.find_max())
            elif operation == "EXT":
                print("ExtractMax returned", binomial_heap.extract_max())
