import cPickle
import numpy

dfile = open("/path/to/raw/dataset.pkl", "rb")
data = cPickle.load(dfile)

data_filtered = [pair for pair in data if len(pair[1]) <= 500]
all_data_conv_keras = []

all_seq = [pair[1] for pair in data_filtered]

all_seq_int = []

all_seq_int_padded = []

all_seq_flat = ""

for string in all_seq:
    all_seq_flat += string

all_seq_flat = set(all_seq_flat)
all_seq_flat = list(all_seq_flat)

aa_dict = {all_seq_flat[x]: x + 1 for x in range(len(all_seq_flat))}

for seq in all_seq:
    int_seq = []
    for aa in seq:
        int_seq.append(aa_dict[aa])
    all_seq_int.append(int_seq)

for seq in all_seq_int:
    end_padding = [0 for x in range(500 - len(seq))]
    padded_seq = seq + end_padding
    all_seq_int_padded.append(padded_seq)

all_mol = [pair[0] for pair in data_filtered]

all_mol_int = []

all_mol_int_padded = []

all_mol_flat = ""

for string in all_mol:
    all_mol_flat += string

all_mol_flat = set(all_mol_flat)
all_mol_flat = list(all_mol_flat)

mol_dict = {all_mol_flat[x]: x + 1 for x in range(len(all_mol_flat))}

for mol in all_mol:
    int_mol = []
    for sym in mol:
        int_mol.append(mol_dict[sym])
    all_mol_int.append(int_mol)

for mol in all_mol_int:
    end_padding = [0 for x in range(250 - len(mol))]
    padded_mol = mol + end_padding
    all_mol_int_padded.append(padded_mol)

all_mol_int_padded = numpy.asarray(all_mol_int_padded, dtype=numpy.float32)
all_seq_int_padded = numpy.asarray(all_seq_int_padded, dtype=numpy.float32)

all_mol_int_padded /= numpy.max(all_mol_int_padded)
all_seq_int_padded /= numpy.max(all_seq_int_padded)

all_data_conv_keras.append(all_mol_int_padded)
all_data_conv_keras.append(all_seq_int_padded)

print str(all_data_conv_keras[0][0])
print str(all_data_conv_keras[0][1])

outputfile = open("aa_dict.pkl", "wb")
cPickle.dump(aa_dict, outputfile)
outputfile.close()

outputfile = open("mol_dict.pkl", "wb")
cPickle.dump(mol_dict, outputfile)
outputfile.close()

outputfile = open("/path/to/processed/dataset.pkl", "wb")
cPickle.dump(all_data_conv_keras, outputfile)
outputfile.close()
