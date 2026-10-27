from collections import Counter
from functools import reduce

class Protein:
  def __init__(self, name: str, sequence: str):
    self.name = name
    self.seq = sequence

  def seq_len(self) -> int: return len(self.seq)
  def cnt(self, amino_acid: str) -> int: return self.seq.count(amino_acid)
  def to_counter(self) -> Counter: return Counter(self.seq)
  def __str__(self): return f"{self.name}: {self.seq}"
  def __repr__(self): return f"{self.name}: {self.seq}"

def load_fasta() -> list[Protein]:
  with open("data/protein.fasta") as f:
    data = [part.split('\n') for part in f.read().split('>')]
  data = [Protein(d[0].split('|')[2], ''.join(d[1:])) for d in data[1:]]
  return data

proteins = load_fasta()
print(f"liczba sekwencji: {len(proteins)}")
print(f"srednia dlugosc sekwencji: {sum(p.seq_len() for p in proteins)/len(proteins)}")
print(f"liczba leucyn: {sum(p.cnt('L') for p in proteins)}")
print(f"liczby amino kwasów: {sum((p.to_counter() for p in proteins), Counter())}")
print(f"liczby amino kwasów: {}")