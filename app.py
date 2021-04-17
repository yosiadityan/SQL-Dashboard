import streamlit as st
import pandas as pd
import sqlalchemy as db
from dotenv import load_dotenv
import os


def set_up():
	load_dotenv()

def fetch_db(db_uri, tablename):
	engine = db.create_engine(db_uri)
	meta = db.reflect(engine)
	with engine.connect() as con:
		


def about_page():
	st.balloons()
	st.header('About This Project 😆')
	st.write('')

	st.image('https://media.giphy.com/media/xUySTQZfdpSkIIg88M/giphy.gif')

	st.markdown("""Hi, there! 👋🏼""")
	st.markdown("""My name is **Yosi** and welcome to my **SQL Dashboard project**!""")
	st.markdown("""As the name suggest, the goal of this project to create a dashboard that displays some data based on the questions using SQL queries only. In a way, this project serves as my portfolio project to practice and show my SQL skills 👍🏼. The datasets used in this project is obtained from various sources and cleaned before used in this dashboard""")
	st.markdown("""I do know that this project is not perfect (yet) and still has many flaws 😞. So, don't hesitate to give me feedback and reaching out to me via [LinkedIn](https://linkedin.com/in/yosiadityan/), [Github](https://github.com/yosiadityan/) or [my personal website](https://yosiadityan.xyz/)🍻""")
	st.markdown("""Now, go check out the SQL dashboard I've made by choosing other page from the sidebar on the left! 👈🏼""")


set_up()
st.set_page_config(page_title='SQL Dashboard', 
	page_icon='🗃', 
	layout='centered', 
	initial_sidebar_state='auto')


page = st.sidebar.selectbox(label="🚀 Where do you want to go?",
	options=("😆 About", "⚽ FIFA World Cup"))

if page == "😆 About":
	about_page()
elif page == "⚽ FIFA World Cup":
	st.header('SQL Dashboard: FIFA World Cup ⚽')

	st.subheader('📃 The Dataset')
	st.markdown('The dataset is obtained from [Kaggle](https://www.kaggle.com/abecklas/fifa-world-cup). The dataset list all matches and players during FIFA World Cup since 1930 until 2014 and contains 3 CSV files, namely **WorldCupMatches.csv**, **WorldCupPlayers.csv**, and **WorldCups.csv** (General information of each FIFA World Cup event, such as the winner, runner-up, number of matches played, etc.). Since the database is only limited to hold 10000 rows of data, the data from WorldCupPlayers.csv will not be used because it has 37k+ rows of data.')
	st.markdown('The dataset was going through data cleaning process before used in this project. The step and code for data cleaning process can be seen in this [repo](https://github.com).')

	st.subheader('👀 Dataset Preview')
	st.subheader('🕵🏼‍♂️ Question and Data')
	st.code('Other than About page')


# with st.echo(code_location='below'):     
# 	st.write('This code will be printed')