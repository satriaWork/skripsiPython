## skripsiPython

Program ini Berisi tentang Analisis Sentimen menggunakan metode Naive Bayes Classifier dan Query Expansion
Data yang digunakan bersumber dari Komentar/twit terhadap Ridwan Kamil di Twitter.
didalam program ini terdapat proses :
1. Text Preprocessing(case folding, remove username, remove web address, remove hashtag, remove email, remove nonalphabet, remove stopword,
    dan stemming)
2. Perbaikan kata slang, typo dan singkatan.
3. Invers kata. contoh: "tidak sempurna" dikonversikan menjadi "cacat".
4. Qurey Expansion. contoh: "baik" diperluas menjadi "baik bagus rapi".
5. Klasifikasi teks menggunakan Naive Bayes Classifier
6. Menghitung akurasi menggunakan Train Test Split.
