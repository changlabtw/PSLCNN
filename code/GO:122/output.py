import os
import glob
import os,fnmatch
for filename in os.listdir('./'):
    if fnmatch.fnmatch(filename,'*.fasta'):
         os.system('psiblast -query '+ filename +' -db ~/db/blast/swissprot -num_iterations=3 -evalue=0.0005  -outfmt=11 -out_ascii_pssm GO:122_'+filename+'.smp')
