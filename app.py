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
	st.markdown("""Now, go check out the SQL dashboard I've made by choosing other pages from the sidebar on the left! 👈🏼""")
	st.markdown("""Or go to `Write Your Own Queries` page to try write your own queries based on dataset available 😉""")


set_up()
st.set_page_config(page_title='SQL Dashboard', 
	page_icon='🗃', 
	layout='centered', 
	initial_sidebar_state='auto')


page = st.sidebar.selectbox(label="🚀 Where do you want to go?",
	options=("😆 About", "⚽ FIFA World Cup", "✍🏻 Write Your Own Queries"))

if page == "😆 About":
	about_page()
elif page == "✍🏻 Write Your Own Queries":
	st.title('Write Your Own Queries ✍🏻')
	st.write('')
	st.write('')

	st.header('📚 Choose The Dataset')
	dataset = st.selectbox(label="Pick one dataset that interests you",  
		options=["⚽ FIFA World Cup"])
	dataset_db = {"⚽ FIFA World Cup": os.getenv('fifa-db-uri')}
	st.write('')
	st.write('')

	st.header('🙈 Tables Preview')
	your_engine, all_df = fetch_db(os.getenv('fifa-db-uri'))
	for table in all_df:
		st.subheader(table)
		st.dataframe(all_df[table])

	st.header('📝 Your Query and Result')
	st.subheader('SQL Query')
	your_query = st.text_area(label="")

	if st.button('Get the Data!'):
		st.subheader('The Data Result')
		with your_engine.connect() as con:
			st.dataframe(pd.read_sql(your_query, con), height=600)

	credit()
elif page == "⚽ FIFA World Cup":
	st.title('SQL Dashboard: FIFA World Cup ⚽')
	st.write('')
	st.write('')

	st.header('📃 The Dataset')
	st.markdown('The dataset is obtained from [Kaggle](https://www.kaggle.com/abecklas/fifa-world-cup). The dataset list all matches and players during FIFA World Cup since 1930 until 2014 and contains 3 CSV files, namely **WorldCupMatches.csv**, **WorldCupPlayers.csv**, and **WorldCups.csv** (General information of each FIFA World Cup event, such as the winner, runner-up, number of matches played, etc.). Since the database is only limited to hold 10000 rows of data, the data from WorldCupPlayers.csv will not be used because it has 37k+ rows of data.')
	st.markdown('The dataset was going through data cleaning process before used in this project. The step and code for data cleaning process can be seen in this [repo](https://github.com/yosiadityan/SQL-Dashboard).')


	st.header('👀 Dataset Preview')
	st.markdown("""Here are some data sample from the database. **match** data obtained from WorldCupMatches.csv file and **info** got from WorldCups.csv file.""")
	engine, all_df = fetch_db(os.getenv('fifa-db-uri'))
	for table in all_df:
		st.subheader(table)
		st.dataframe(all_df[table])


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
ORDER BY 1, 3 DESC;''', 

	'''Since 1930 until 2014, how many number of matches win by each country?''':
	'''WITH match_result AS (
	SELECT
		CASE
			WHEN "Home Team Goals" > "Away Team Goals" THEN "Home Team Name"
			WHEN "Home Team Goals" < "Away Team Goals" THEN "Away Team Name"
			ELSE NULL
	END AS "Team Name"
	FROM matches
	)
SELECT "Team Name", COUNT(1) AS "Number of Matches"
FROM match_result
WHERE "Team Name" IS NOT NULL
GROUP BY 1
ORDER BY 2 DESC;''',

	'''What is the top 10 in terms of year that has the most country participants?''':
	'''WITH all_country_year AS (
	SELECT "Year", "Home Team Name" AS "Team Name"
	FROM matches
	UNION ALL
	SELECT "Year", "Away Team Name" AS "Team Name"
	FROM matches
)
SELECT
	"Year", 
	COUNT(DISTINCT "Team Name") AS "Number of Country Participants"
FROM all_country_year
GROUP BY "Year"
ORDER BY 2 DESC
LIMIT 10;''' ,

	'''What is the most frequent time to play matches?''':
	'''SELECT 
	CAST("Datetime" AS TIME) AS "Match Time", 
	COUNT(1) AS "Number of Matches"
FROM matches
GROUP BY "Match Time"
ORDER BY 2 DESC;''',

	'''How many times each country gets first, second, third place and its total times it gets into top three?''':
	'''WITH country_win AS (
	SELECT "Winner" AS "Country", '1st Place' AS "Win" FROM info
	UNION ALL
	SELECT "Runners-Up" AS "Country", '2nd Place' AS "Win" FROM info
	UNION ALL
	SELECT "Third" AS "Country", '3rd Place' AS "Win" FROM info
	UNION ALL
	SELECT "Fourth" AS "Country", '4th Place' AS "Win" FROM info
)

SELECT
	COALESCE("Country", 'Total') AS "Country",
	COALESCE("Win", 'All Wins') AS "Win",
	COUNT(*) AS "Number of win"
FROM country_win
GROUP BY ROLLUP("Country", "Win")
ORDER BY 1, 2;''',

	'''What is the running total of Attendances for each FIFA World Cup event since 1930 to 2014?''':
	'''SELECT
	"Year",
	SUM("Attendance") 
		OVER(ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) 
		AS "Total Attendances"
FROM info;''',

	'''What is the moving average of goals scored for the last three matches for each country?''':
	'''WITH all_team AS (
	SELECT 
		"Year", 
		"Datetime", 
		"Home Team Name" AS "Team", 
		"Home Team Goals" AS "Goals" 
	FROM matches
	UNION ALL
	SELECT 
		"Year", 
		"Datetime", 
		"Away Team Name" AS "Team", 
		"Away Team Goals" AS "Goals" 
	FROM matches
)
SELECT
	"Team",
	"Year",
	CONCAT(DATE("Datetime"), ' ', CAST("Datetime" AS TIME)) AS "Date Time",
	AVG("Goals")
		OVER(PARTITION BY "Team"
			ORDER BY "Datetime" ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) 
			AS "Goals Moving Avg"
FROM all_team;''',

	'''Which decades of FIFA World Cup event that has number of matches more than 100 and average goals scored more than 2.5?''':
	'''SELECT
	CONCAT(LEFT("Year"::VARCHAR(4), 3), '0') AS "Decade",
	COUNT(*) AS "Total Matches",
	AVG("Home Team Goals" + "Away Team Goals") AS "Avg Goals Scored"
FROM matches
GROUP BY 1
HAVING 
	COUNT(*) >= 100 AND
	AVG("Home Team Goals" + "Away Team Goals") >= 2.5;'''

## Decade with number of matches and goals scored more than xxxx >>> use having

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