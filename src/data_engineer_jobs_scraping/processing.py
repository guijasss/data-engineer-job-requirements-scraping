import duckdb

con = duckdb.connect("jobs.duckdb")

df = con.execute("SELECT * FROM jobs").fetch_df()
print(df.head())
