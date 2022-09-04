import time
from PyPDF2 import PdfReader
import re
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# converting pdf file to text
while True:
    sem = 0
    reader = PdfReader('collage.pdf')
    aicte_syllabus = []
    pdf_syllabus = []
    f = open('syllabus.txt', 'w')
    for i in range(len(reader.pages)):
        try:
            page = reader.pages[i]
            f.write(page.extract_text())
        except:
            continue
    f.close()
    # end of conversion of pdf to text
    # start extracting syllabus from text file
    f = open('syllabus.txt', 'r')
    file = open('topics.txt', 'w')
    count = 0
    write = False
    search = True
    while True:
        count += 1
        text = f.readline().lower()
        if not text:
            break
        if search and re.findall('syllabus', text):
            write = True
            search = False
            print("syllabus found on line ", count)
        if not search and (
                re.findall('outline', text) or re.findall('outcome', text) or re.findall('pedagogy',
                                                                                         text) or re.findall(
            'reference  books', text) or re.findall('objective', text)):
            write = False
            print("other found on line ", count)
            search = True
        if write:
            file.write(text)
    f.close()
    file.close()
    # completion of topics extraction
    file = open('model.txt', 'r').readlines()

    for line in file:
        line = line.replace('module ', '')
        lne = line.lstrip('0123456789.- ')
        aicte_syllabus.append(line)

    # creating list of given pdf

    with open("topics.txt", 'r') as file:
        for line in file:
            grade_data = line.strip().split(',')
            for i in range(len(grade_data)):
                pdf_syllabus.append(grade_data[i])

    found = []
    not_found = []
    important_found = []
    important_not_found = []

    # def create_dataframe(matrix, tokens):
    #     doc_names = [f'doc_{i + 1}' for i, _ in enumerate(matrix)]
    #     df = pd.DataFrame(data=matrix, index=doc_names, columns=tokens)
    #     return (df)

    pdf_syllabus = [x for x in pdf_syllabus if x != '']

    for str in pdf_syllabus:
        str.replace('\n', ' ')
    for str in aicte_syllabus:
        str.replace('\n', ' ')
    important_topics = ["Artificial Intelligence", "Machine Learning", "BlockChain"]
    for i in range(len(important_topics)):
        for j in range(len(pdf_syllabus)):
            try:
                data = [important_topics[i], pdf_syllabus[j]]
                print(data)
                count_vectorizer = CountVectorizer()
                vector_matrix = count_vectorizer.fit_transform(data)
                tokens = count_vectorizer.get_feature_names()
                vector_matrix.toarray()
                cosine_similarity_matrix = cosine_similarity(vector_matrix)
                # frame = create_dataframe(cosine_similarity_matrix, ['doc_1', 'doc_2'])
                if cosine_similarity_matrix[0][1] > 0.5:
                    found.append(important_topics[i])
            except:
                continue

    for i in range(len(pdf_syllabus)):
        for j in range(len(aicte_syllabus)):
            try:
                data = [pdf_syllabus[i], aicte_syllabus[j]]
                print(data)
                count_vectorizer = CountVectorizer()
                vector_matrix = count_vectorizer.fit_transform(data)
                tokens = count_vectorizer.get_feature_names()
                vector_matrix.toarray()
                cosine_similarity_matrix = cosine_similarity(vector_matrix)
                # frame = create_dataframe(cosine_similarity_matrix, ['doc_1', 'doc_2'])
                if cosine_similarity_matrix[0][1] > 0.5:
                    found.append(pdf_syllabus[i])
            except:
                continue
    not_found = [x for x in pdf_syllabus if x not in found]
    important_not_found = [x for x in important_topics if x not in important_found]
    found = list(set(found))
    not_found = list(set(not_found))
    important_found = list(set(important_found))
    important_not_found = list(set(important_not_found))
    # pd.DataFrame(found).to_excel('output1.xlsx', header=False, index=False)
    # pd.DataFrame(not_found).to_excel('output1.xlsx', header=False, index=False)
    # pd.DataFrame(important_found).to_excel('output1.xlsx', header=False, index=False)
    # pd.DataFrame(important_not_found).to_excel('output1.xlsx', header=False, index=False)
    print(found)
    print(not_found)
    print(important_found)
    print(important_not_found)
    time.sleep(3000)