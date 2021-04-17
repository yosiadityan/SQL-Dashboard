import streamlit as st
import pandas as pd
import sqlalchemy as db
from dotenv import load_dotenv
import os


def set_up():
	load_dotenv()


def credit():
	for i in range(10):
		st.write('')
	st.info('''Give me a 👋 by visiting my **[LinkedIn](https://linkedin.com/in/yosiadityan)**,  **[Github](https://github.com/yosiadityan/)** or **[personal website](https://yosiadityan.xyz/)** where you can see my other projects as well! 🍻''')


@st.cache(allow_output_mutation=True)
def fetch_db(db_uri):
	engine = db.create_engine(db_uri)
	meta = db.MetaData()
	meta.reflect(engine)
	all_df = {}
	with engine.connect() as con:
		for table in meta.tables.keys():
			query = db.select([meta.tables[table]])
			all_data = con.execute(query).fetchall()
			all_df[table] = pd.DataFrame(all_data, columns=meta.tables[table].c.keys())
	return engine, all_df		  


def about_page():
	st.balloons()
	st.title('About This Project 😆')
	st.write('')
	st.write('')

	st.image('https://media.giphy.com/media/xUySTQZfdpSkIIg88M/giphy.gif')

	st.markdown("""Hi, there! 👋🏼""")
	st.markdown("""My name is **Yosi** and welcome to my **SQL Dashboard project**!""")
	st.markdown("""As the name suggest, the goal of this project to create a dashboard that displays some data based on the questions using SQL queries only. In a way, this project serves as my portfolio project to practice and show my SQL skills 👍🏼. The datasets used in this project is obtained from various sources and cleaned before used in this dashboard. Each page use different datasets and answers different set of questions as well.""")
	st.markdown("""I do know that this project is not perfect *(yet)* and still has many flaws 😞. So, don't hesitate to give me feedback and reaching out to me via [LinkedIn](https://linkedin.com/in/yosiadityan/), [Github](https://github.com/yosiadityan/) or [my personal website](https://yosiadityan.xyz/)🍻""")
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
	st.title('SQL Dashboard: FIFA World Cup ⚽')
	st.write('')
	st.write('')

	st.header('📃 The Dataset')
	st.markdown('The dataset is obtained from [Kaggle](https://www.kaggle.com/abecklas/fifa-world-cup). The dataset list all matches and players during FIFA World Cup since 1930 until 2014 and contains 3 CSV files, namely **WorldCupMatches.csv**, **WorldCupPlayers.csv**, and **WorldCups.csv** (General information of each FIFA World Cup event, such as the winner, runner-up, number of matches played, etc.). Since the database is only limited to hold 10000 rows of data, the data from WorldCupPlayers.csv will not be used because it has 37k+ rows of data.')
	st.markdown('The dataset was going through data cleaning process before used in this project. The step and code for data cleaning process can be seen in this [repo](https://github.com/yosiadityan/SQL-Dashboard).')


	st.header('👀 Dataset Preview')
	st.markdown("""Here are some data sample from the database. **match** data obtained from WorldCupMatches.csv file and **info** got from WorldCups.csv file.""")
	engine, all_df = fetch_db(os.getenv('db-uri'))
	print(all_df.keys())
	for table in all_df:
		st.subheader(table)
		st.dataframe(all_df[table].head(15))


	st.header('🕵🏼‍♂️ The Question and Data')
	st.subheader("Choose The Question")

	quest_query = {
	'''How many stadium has been used to organize FIFA World Cup matches?''':
	'''SELECT COUNT(DISTINCT "Stadium") AS "Stadium Count"
FROM matches;''', 

	'''What kind of stages played in FIFA World Cup Matches?''':
	'''SELECT DISTINCT "Stage"
FROM matches
ORDER BY "Stage" ASC;''',

	'''How many times each stage is played in each year?''':
	'''SELECT "Year", "Stage", COUNT(1) AS "Number of Matches"
FROM matches
GROUP BY "Year", "Stage"
ORDER BY 1, 3 DESC;'''
}

	quest = st.selectbox(label="", options=list(quest_query.keys()))
	if len(quest) > 89:
		st.write(quest)

	st.subheader("The Data")
	st.markdown('SQL Query')
	st.code(quest_query[quest], language='SQL')

	st.write('')

	st.markdown('SQL Query Result')
	with engine.connect() as con:
		st.dataframe(pd.read_sql(quest_query[quest], con), height=600)
		# st.dataframe(pd.read_sql(quest_query[quest], con).style.highlight_max(axis=0))

	credit()

# with st.echo(code_location='below'):	 
# 	st.write('This code will be printed')