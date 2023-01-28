import streamlit as st
from Bio import SeqIO
from io import StringIO
import pandas as pd
import numpy as np

st.set_page_config(page_title="GC Content Calculator", page_icon=":guardsman:", layout="wide")
st.title("GC Content Calculator")

seq_input = st.radio("Select input method", ("Paste sequences", "Upload file"))

if seq_input == "Paste sequences":
    sequences = StringIO(st.text_area("Enter sequences in FASTA format"))
else:
    file = st.file_uploader("Upload FASTA file", type=["fasta", "fa"])
    if file is not None:
        sequences = StringIO(file.read().decode("utf-8"))

button1 = st.button('Submit')

def calculate_gc_content(sequences):
    gc_content = {}
    for seq in SeqIO.parse(sequences, "fasta"):
        gc_content[seq.id] = str(round(((seq.seq.count("G") + seq.seq.count("C")) / len(seq) * 100),2))+'%'
    return gc_content

if button1:
    try:
        gc_content = calculate_gc_content(sequences)
        gc_content = pd.DataFrame(gc_content,index=[0])
        # gc_content = gc_content.apply(lambda x: np.round(x, decimals=2))
        st.write("GC Content:")
        st.table(gc_content)
    except Exception as e:
        st.error("Invalid input: " + str(e))