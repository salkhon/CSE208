from abc import abstractmethod
from collections import namedtuple
from dataclasses import dataclass
import random
from typing import Any, Callable, List, NamedTuple, Optional, Tuple
from dsa1lib.linkedlist import LinkedList
import randomword
from dsa1lib.sieve import SieveOfEratosthenes

LIMIT = 500000
sieve = SieveOfEratosthenes(LIMIT)


@dataclass
class KeyValPair:
    key: str
    val: Any


class HashTable:
    """Hash table for string keys. 
    """

    def __init__(self, maxlen: int):
        self.maxlen = maxlen

    @abstractmethod
    def put1(self, key: str, val: Any) -> int:
        """Puts key val pair in hash table using hash1, returns the number of probes. 

        Args:
            key (str): key
            val (Any): value

        Returns:
            int: number of probes required to insert k-v pair. 
        """
        pass

    @abstractmethod
    def get1(self, key: str) -> Tuple[Any, int]:
        """Retrieves the value associated to the key using hash1, also returns the number of probes.  

        Args:
            key (str): key

        Returns:
            Tuple[Any, int]: Tuple of
                The value associated with the key
                and the number of probes to find the k-v pair. 
        """
        pass

    @abstractmethod
    def put2(self, key: str, val: Any) -> int:  # return number of collisions
        """Puts key val pair in hash table using hash2, returns the number of probes. 

        Args:
            key (str): key
            val (Any): value

        Returns:
            int: number of probes required to insert k-v pair. 
        """
        pass

    @abstractmethod
    # also return number of probes
    def get2(self, key: str) -> Tuple[Any, int]:
        """Retrieves the value associated to the key using hash2, also returns the number of probes.  

        Args:
            key (str): key

        Returns:
            Tuple[Any, int]: Tuple of
                The value associated with the key
                and the number of probes to find the k-v pair. 
        """
        pass

    def hash1(self, key: str) -> int:
        """Implements Horner's hashing method. 

        Args:
            key (str): key string to be hashed. 

        Returns:
            int: hash value for key str. 
        """
        P = 31

        hashcode = 0
        for character in key:
            hashcode += ((hashcode * P) % self.maxlen +
                         ord(character)) % self.maxlen
        return hashcode % self.maxlen

    def hash2(self, key: str) -> int:
        """Implements FNV-1A hash function. 

        Args:
            key (str): key str to be hashed.

        Returns:
            int: hash value for key str. 
        """
        magicxor32 = 0x811c9dc5
        magicmul32 = 0x01000193
        magicxor64 = 0xcbf29ce484222325
        magicmul64 = 0x100000001b3

        hashcode = magicxor64
        for character in key:
            hashcode = ((hashcode ^ ord(character)) * magicmul64) % self.maxlen
        return hashcode  # can it be neg?


class SeparateChainingHashTable(HashTable):
    def __init__(self, maxlen: int):
        super().__init__(maxlen)
        self.table1 = [LinkedList[KeyValPair]() for _ in range(self.maxlen)]
        self.table2 = [LinkedList[KeyValPair]() for _ in range(self.maxlen)]

    def put1(self, key: str, val: Any) -> int:
        hashidx = self.hash1(key)
        if self.get1(key)[0]:
            for kvpair in self.table1[hashidx]:
                if kvpair.key == key:
                    kvpair.val = val
        else:
            self.table1[hashidx].prepend(KeyValPair(key, val))
        return 1 if len(self.table1[hashidx]) > 1 else 0

    def put2(self, key: str, val: Any) -> int:
        hashidx = self.hash2(key)
        if self.get2(key)[0]:
            for kvpair in self.table2[hashidx]:
                if kvpair.key == key:
                    kvpair.val = val
        else:
            self.table2[hashidx].prepend(KeyValPair(key, val))
        return 1 if len(self.table2[hashidx]) > 1 else 0

    def get1(self, key: str) -> Tuple[Any, int]:
        hashidx = self.hash1(key)
        num_probes = 0
        val1 = None
        for kvpair in self.table1[hashidx]:
            num_probes += 1
            if kvpair.key == key:
                val1 = kvpair.val
                break

        return val1, num_probes

    def get2(self, key: str) -> Tuple[Any, int]:
        hashidx = self.hash2(key)
        num_probes = 0
        val2 = None
        for kvpair in self.table2[hashidx]:
            num_probes += 1
            if kvpair.key == key:
                val2 = kvpair.val
                break

        return val2, num_probes


class DoubleHashing(HashTable):
    def __init__(self, maxlen: int):
        super().__init__(sieve.closest_prime(maxlen))
        self.table1: List[Optional[KeyValPair]] = [None] * self.maxlen
        self.table2: List[Optional[KeyValPair]] = [None] * self.maxlen

    def aux_hash(self, key: str) -> int:
        hashcode = 0
        for character in key:
            hashcode += ord(character) % self.maxlen
        return hashcode % self.maxlen

    def h(self, hashfunc: Callable[[str], int], key: str, i: int) -> int:
        return (hashfunc(key) + i * self.aux_hash(key) % self.maxlen) % self.maxlen

    def find_slot_with_key_or_None(self, key: str, is_method_one: bool) -> int:
        """Returns the slot index in the hash table that has the key or None. Whichever comes first. 

        Args:
            key (str): key
            is_method_one (bool): Which hash method to use

        Returns:
            int: Number of probes required to find key or none. 
        """
        table = self.table1 if is_method_one else self.table2
        hashfunc = self.hash1 if is_method_one else self.hash2

        num_probe = 0
        idx = self.h(hashfunc, key, num_probe)
        while table[idx] and table[idx].key != key:  # type: ignore
            num_probe += 1
            idx = self.h(hashfunc, key, num_probe)

        return num_probe

    def put1(self, key: str, val: Any) -> int:
        num_probe = self.find_slot_with_key_or_None(key, True)
        idx = self.h(self.hash1, key, num_probe)

        if self.table1[idx]:
            self.table1[idx].val = val  # type: ignore
        else:
            self.table1[idx] = KeyValPair(key, val)

        return num_probe  # collision starts from 0

    def get1(self, key: str) -> Tuple[Any, int]:
        num_probe = self.find_slot_with_key_or_None(key, True)
        val = self.table1[self.h(self.hash1, key, num_probe)]

        val = val.val if val else None
        return val, num_probe+1  # probes start from 1

    def put2(self, key: str, val: Any) -> int:
        num_probe = self.find_slot_with_key_or_None(key, False)
        idx = self.h(self.hash2, key, num_probe)

        if self.table2[idx]:
            self.table2[idx].val = val  # type: ignore
        else:
            self.table2[idx] = KeyValPair(key, val)

        return num_probe

    def get2(self, key: str) -> Tuple[Any, int]:
        num_probe = self.find_slot_with_key_or_None(key, False)
        val = self.table2[self.h(self.hash2, key, num_probe)]

        val = val.val if val else None
        return val, num_probe+1


class CustomProbing(DoubleHashing):
    def __init__(self, maxlen: int):
        super().__init__(maxlen)
        self.C1 = 7
        self.C2 = 13

    def h(self, hashfunc: Callable[[str], int], key: str, i: int) -> int:
        return (
            hashfunc(key) +
            (self.C1 * i * self.aux_hash(key) % self.maxlen) +
            (self.C2 * i * i) % self.maxlen
        ) % self.maxlen


def print_table(perf_table: List[List[float]]):
    print("\n")
    print("----------------------------------------------------------------------")
    print("\t\tHash 1\t\t\t\tHash2")
    print("------------------------")
    print("\t\tNo. Col\t\tAvg. Probes\t\tNo. Col\t\tAvg. Probes")
    print("---------------------------------------------------------------------")

    print("Chaining\t", end="")
    print(perf_table[0][0], perf_table[0][1],
          perf_table[0][2], perf_table[0][3], sep="\t\t\t")

    print("Double H\t", end="")
    print(perf_table[1][0], perf_table[1][1],
          perf_table[1][2], perf_table[1][3], sep="\t\t\t")

    print("Custom P\t", end="")
    print(perf_table[2][0], perf_table[2][1],
          perf_table[2][2], perf_table[2][3], sep="\t\t\t")
    print("\n")


if __name__ == "__main__":
    num_words = 10000
    num_samples = 1000
    num_char = 7

    perf_table = [[0.0] * 4, [0.0] * 4, [0.0] * 4]
    while True:
        tablesize = int(input('Enter table size (-1 to quit): '))
        if tablesize < 0:
            break

        sepchain_total_collisions1 = 0
        doubleh_total_collisions1 = 0
        customp_total_collisions1 = 0

        sepchain_total_probes1 = 0
        doubleh_total_probes1 = 0
        customp_total_probes1 = 0

        sepchain_total_collisions2 = 0
        doubleh_total_collisions2 = 0
        customp_total_collisions2 = 0

        sepchain_total_probes2 = 0
        doubleh_total_probes2 = 0
        customp_total_probes2 = 0

        random_words = [""] * num_words

        separate_chaining = SeparateChainingHashTable(tablesize)
        double_hashing = DoubleHashing(tablesize)
        custom_probing = CustomProbing(tablesize)

        for i in range(num_words):
            random_words[i] = randomword.random_word(num_char)
            while separate_chaining.get1(random_words[i])[0]:
                random_words[i] = randomword.random_word(num_char)

            sepchain_total_collisions1 += separate_chaining.put1(
                random_words[i], i)
            sepchain_total_collisions2 += separate_chaining.put2(
                random_words[i], i)

            doubleh_total_collisions1 += double_hashing.put1(
                random_words[i], i)
            doubleh_total_collisions2 += double_hashing.put2(
                random_words[i], i)

            customp_total_collisions1 += custom_probing.put1(
                random_words[i], i)
            customp_total_collisions2 += custom_probing.put2(
                random_words[i], i)

        for i in range(num_samples):
            idx = random.randint(0, num_words-1)
            # print(random_words[idx])

            _, col = separate_chaining.get1(random_words[idx])
            # print(_)
            sepchain_total_probes1 += col
            _, col = separate_chaining.get2(random_words[idx])
            # print(_)
            sepchain_total_probes2 += col

            _, col = double_hashing.get1(random_words[idx])
            # print(_)
            doubleh_total_probes1 += col
            _, col = double_hashing.get2(random_words[idx])
            # print(_)
            doubleh_total_probes2 += col

            _, col = custom_probing.get1(random_words[idx])
            # print(_)
            customp_total_probes1 += col
            _, col = custom_probing.get2(random_words[idx])
            # print(_)
            customp_total_probes2 += col

            # print("\n\n")

        perf_table[0][:] = sepchain_total_collisions1, sepchain_total_probes1 / \
            num_samples, sepchain_total_collisions2, sepchain_total_probes2 / num_samples

        perf_table[1][:] = doubleh_total_collisions1, doubleh_total_probes1 / \
            num_samples, doubleh_total_collisions2, doubleh_total_probes2 / num_samples

        perf_table[2][:] = customp_total_collisions1, customp_total_probes1 / \
            num_samples, customp_total_collisions2, customp_total_probes2 / num_samples

        print_table(perf_table)
