import streamlit as st
import sys
from os.path import join
import os
from bs4 import BeautifulSoup

sys.path.append('..')
from task5.main import vector_search


def find():
    return vector_search(query)


def get_title(filepath: str) -> str:
    with open(filepath, 'r') as file:
        title = BeautifulSoup(file.read(), features="html.parser").text.split('\n')[0]
        return title


with st.form('find_form'):
    st.header('Shmoogle')
    query = st.text_input(label='Enter your request')
    submitted = st.form_submit_button('Find')


def create_index() -> dict:
    with open(join('..', 'task1', 'index.txt'), 'r') as file:
        response = dict()
        lines = file.readlines()
        lines = [line for line in lines if not line == '']
        for line in lines:
            splitted = line.split(' ')
            response.setdefault(splitted[0], splitted[1])
        return response


if submitted:
    result = find()
    index = create_index()
    markdown_str = ''
    for res in result:
        path_to_html = join('..', 'task1', 'downloaded_html', f'{res[0]}.html')
        title = get_title(path_to_html)
        link = index.get(res[0])
        markdown_str = \
            f'''{markdown_str}
            1. #### [{title}](file://{os.path.abspath(os.getcwd() + '/'+ path_to_html)})
                + {index.get(res[0])}
            '''
    st.markdown(markdown_str)
