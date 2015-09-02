# rdm-predictor
An attempt to associate KEGG RDM patterns with enzyme structure and sequence using machine learning.

create_dataset.py creates a pickle containing [RDM+Smiles, sequence] for all entries with an EC number in BRENDA. The dataset as is is pretty unbalanced: "popular" EC numbers have (very) significantly more sequences than others. The pickle is also around 3 GB.

Same dataset in hdf5 format for use with DRAW (http://arxiv.org/abs/1502.04623) network: https://drive.google.com/file/d/0Bylz5f6u1p44WTdaMjlNckRxZ1E/view?usp=sharing
