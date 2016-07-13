# The following is a demonstration of using python's sqlite package to run SQL queries
# This will use information from the 'World Fact Book' database
# available at https://github.com/factbook/factbook.sql
import sqlite3 as sql

# initialize a connection to factbook.db
conn = sql.connect('factbook.db')

# examine the schema of the facts table
schema = conn.execute('pragma table_info(facts);').fetchall()
for s in schema:
    print(s)

# fetch all records in the facts table
facts = conn.execute('SELECT * FROM facts;').fetchall()
print(facts)

# count the number of non-null values in the birth_rate column of the facts table
birth_rate_tuple = conn.execute('SELECT COUNT(birth_rate) FROM facts;').fetchall()
birth_rate_count = birth_rate_tuple[0][0]
print(birth_rate_count)

# find the minimum value in the population_growth column
pop_growth_tuple = conn.execute('SELECT MIN(population_growth) FROM facts;').fetchall()
min_population_growth = pop_growth_tuple[0][0]
print(min_population_growth)

# find the maximum value in the death_rate column
death_rate_tuple = conn.execute('SELECT MAX(death_rate) FROM facts;').fetchall()
max_death_rate = death_rate_tuple[0][0]
print(max_death_rate)

# find the sum of the area_land column
total_land_tuple = conn.execute('SELECT SUM(area_land) FROM facts;').fetchall()
total_land_area = total_land_tuple[0][0]
print(total_land_area)

# find the mean of the area_water column
avg_water_tuple = conn.execute('SELECT AVG(area_water) FROM facts;').fetchall()
avg_water_area = avg_water_tuple[0][0]
print(avg_water_area)

# use one query to find the mean country population, total world population, and maximum birth_rate
facts_stats = conn.execute('SELECT AVG(population), SUM(population), MAX(birth_rate) FROM facts;').fetchall()
print(facts_stats)

# find the mean population_growth for countries with a population greater than 10,000,000
pop_query = conn.execute('SELECT AVG(population_growth) FROM facts WHERE population > 10000000;').fetchall()
population_growth = pop_query[0][0]
print(population_growth)

# find the individual birth rates for all countries
unique_birth_rates = conn.execute('SELECT DISTINCT birth_rate FROM facts;').fetchall()
print(unique_birth_rates)

# find the average birth rate of all countries with populations over 20,000,000
abr_query = conn.execute('SELECT AVG(DISTINCT birth_rate) FROM facts WHERE population > 20000000;').fetchall()
average_birth_rate = abr_query[0][0]
print(average_birth_rate)

# find the total population of all countries which occupy more than 1,000,000 square miles
pop_land_query = conn.execute('SELECT SUM(DISTINCT population) FROM facts WHERE area_land > 1000000;').fetchall()
sum_population = pop_land_query[0][0]
print(sum_population)

# find global population growth, in terms of millions (as float)
population_growth_millions = conn.execute('SELECT population_growth / 1000000.0 FROM facts;').fetchall()
print(population_growth_millions)

# estimate next year's global population, based on current population and population growth
next_year_population = conn.execute('SELECT population_growth * population + population FROM facts;').fetchall()
print(next_year_population)

# examples of query plans -- first three scan entire table, which is inefficient; O(N) complexity
# the fourth query plan uses specific row id, thus uses binary search; O(log N) complexity
query_plan_one = conn.execute('explain query plan select * from facts where area > 40000;').fetchall()
query_plan_two = conn.execute('explain query plan select area from facts where area > 40000;').fetchall()
query_plan_three = conn.execute('explain query plan select * from facts where name = "Czech Republic";').fetchall()
query_plan_four = conn.execute('explain query plan select * from facts where id = 20;').fetchall()
print(query_plan_one)
print(query_plan_two)
print(query_plan_three)
print(query_plan_four)

# find the id value for the row in the name_idx table where the name value equals India.
india_index = conn.execute('select id from name_idx where name = "India";').fetchall()[0][0]
print(india_index)

# find the row in the facts table where id equals india_index
india_row = conn.execute('select * from facts where id = ?;', (india_index,)).fetchall()
print(india_row)

# plans for the previous two queries are as follows:
first_query_plan = conn.execute('explain query plan select id from name_idx where name = "India";').fetchall()
second_query_plan = conn.execute('explain query plan select * from facts where id = ?;', (india_index,)).fetchall()
print(first_query_plan)
print(second_query_plan)

# create single or multi-column indices
conn.execute("create index if not exists pop_idx on facts(population);").fetchall()
conn.execute("create index if not exists pop_growth_idx on facts(population_growth);").fetchall()
conn.execute("create index if not exists pop_pop_growth_idx on facts(population, population_growth);").fetchall()

# executes query plan for a query that returns all rows where population is greater than 1,000,000
# and where population_growth is less than 0.05.
conn.execute("explain query plan select * from facts where population > 1000000 and population_growth < 0.05;").fetchall()