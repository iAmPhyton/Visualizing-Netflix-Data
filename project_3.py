import plotly.io as pio
pio.renderers.default = "png"
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly._subplots import make_subplots
import plotly.figure_factory as ff  
netflix_titles = pd.read_csv('netflix_titles.csv')
print(netflix_titles.head())
##dropping features that won't be used
netflix_titles = netflix_titles.dropna(how='any',subset=['cast','director'])
netflix_titles
#dropping null values
netflix_titles = netflix_titles.dropna()
netflix_titles
#converting some columns into proper date-time format
## cleaning the data
# checking for missing values
netflix_titles.isnull().sum()
# dropping columns that won't be used
netflix_titles = netflix_titles.dropna(how='any',subset=['cast','director'])
# dropping null values
netflix_titles =netflix_titles.dropna()
#converting some columns into proper date and time
netflix_titles["date_added"] = pd.to_datetime(netflix_titles['date_added'])
netflix_titles['year_added'] = netflix_titles['date_added'].dt.year
netflix_titles['month_added'] = netflix_titles['date_added'].dt.month
netflix_titles
#changing some values in columns that can be classified as seasons
netflix_titles['season_count'] = netflix_titles.apply(lambda x : 
    x['duration'].split(" "[0]) 
    if "Season" in x['duration']
    else "", axis= 1)
netflix_titles['duration'] = netflix_titles.apply(lambda x :
    x['duration'].split(" ")[0]
    if "Season" not in x['duration'] 
    else "", axis= 1) 
netflix_titles
#changing the column "Listed_in" to a genre which makes more sense
netflix_titles = netflix_titles.rename(columns={"listed_in":"genre"})
netflix_titles['genre'] = netflix_titles['genre'].apply(lambda x: 
    x.split(",")[0])
netflix_titles
#exploratory data analysis with netflix
fig_donut = px.pie(netflix_titles, names='type', height=300, width=600, hole=0.7,
									 title='Most watched on Netflix',
									 color_discrete_sequence=['#b20710', '#221f1f'])
fig_donut.update_traces(hovertemplate=None, textposition='outside',
												textinfo='percent+label', rotation=90)
fig_donut.update_layout(margin=dict(t=100, b=30, l=0, r=0),
  				 						  showlegend=False,
	  	 									plot_bgcolor='#333', paper_bgcolor='#333',
			    							title_font=dict(size=45, color='#8a8d93',
													 family="Lato, sans-serif"),
											  font=dict(size=17, color='#8a8d93'),
											  hoverlabel=dict(bgcolor="#444", font_size=13,
													 font_family="Lato, sans-serif"))
fig_donut.show() 

#impact on movies and tv shows over the years

tv_show = netflix_titles[netflix_titles["type"] == "TV Show"]
movies = netflix_titles[netflix_titles["type"] == "Movie"]

col = "year_added"

tvsc = tv_show[col].value_counts().reset_index().rename(columns = {col : "count", "index" : col,})
tvsc['percent'] = tvsc['count'].apply(lambda x : 100*x/sum(tvsc['count']))
tvsc = tvsc.sort_values(col)

mc = movies[col].value_counts().reset_index().rename(columns = {col : "count", "index" : col})
mc['percent'] = mc['count'].apply(lambda x : 100*x/sum(mc['count']))
mc = mc.sort_values(col)

tvs = go.Scatter(x=tvsc[col], y=tvsc["count"], name="Tv Shows", marker=dict(color="green"), )
ms =  go.Scatter(x=mc[col], y=mc["count"], name="Movies", marker=dict(color="#b20710") )
data = [tvs, ms] 
fig_line = go.Figure(data)

fig_line.update_traces(hovertemplate=None)
fig_line.update_xaxes(showgrid=False)
fig_line.update_yaxes(showgrid=False)

large_title_format = 'Impact of TV Shows and Movies Over the Year'
small_title_format = "<span style='font-size:13px; font-family:Tahoma'>Due to Covid, updating of content was slowed down."
fig_line.update_layout(title=large_title_format + "<br>" + small_title_format, height=400,
                       margin=dict(t=130, b=0, l=70, r=40),
                       hovermode="x unified",
                       xaxis_title=' ',yaxis_title=" ",
                       plot_bgcolor='#333', paper_bgcolor='#333',
                       title_font=dict(size=25, color='#8a8d93', family="Lato, sans-serif"),
                       font=dict(color='#8a8d93'),
                       legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="center", x=0.5))

fig_line.add_annotation(dict(x=0.8, y=0.4, ax=0, ay=0,
                        xref= "paper", yref= "paper",
                        text= "Highest Number of <b>TV Shows</b><br> Were Released<br> in <b>2020</b> Followed By a Decline in 2021"))
fig_line.add_annotation(dict(x=0.9, y=1.1, ax=0, ay=0,
                        xref= "paper", yref= "paper",
                        text= "Highest Number of <b>Movies</b><br> Were Released<br> in <b>2019</b> Followed By 2020"))
fig_line.show() 

#Best Month for Releasing Content
df_month = pd.DataFrame(netflix_titles['month_added'].value_counts().reset_index()).rename(columns={'index':'month', 'month_added':'count'})
# Converting month number to month name
df_month['month_final'] = df_month['month'].replace({1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'June', 7:'July', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'})

fig_month = px.funnel(df_month, x='count', y='month_final', title='Best Month for Releasing Content',
                      height=350, width=600, color_discrete_sequence=['#b20710'])
fig_month.update_xaxes(showgrid=False, ticksuffix=' ', showline=True)
fig_month.update_traces(hovertemplate=None, marker=dict(line=dict(width=0)))
fig_month.update_layout(margin=dict(t=60, b=20, l=70, r=40),
                        xaxis_title=' ', yaxis_title=" ",
                        plot_bgcolor='#333', paper_bgcolor='#333',
                        title_font=dict(size=25, color='#8a8d93', family="Lato, sans-serif"),
                        font=dict(color='#8a8d93'),
                        hoverlabel=dict(bgcolor="black", font_size=13, font_family="Lato, sans-serif"))
fig_month.show()

# highest number of shows watched in the country
# Data Preparation: Grouping by 'year_added' and 'country', and counting the number of titles
df_country = netflix_titles.groupby(['year_added', 'country'])['country'].count().reset_index(name='counts')

# Creating the Choropleth Map
fig = px.choropleth(df_country, locations="country", color="counts",
                    locationmode='country names',
                    title='Netflix Titles by Country',
                    range_color=[0, 200],  # Adjust the color range as needed
                    color_continuous_scale=px.colors.sequential.OrRd)

fig.show()

''''
#showing chart of country vs year

df_country = netflix_titles.groupby('year_added')['country'].value_counts().reset_index(name='counts')
fig = px.choropleth(df_country, locations="country", color="counts",
                    locationmode='country names',
                    animation_frame='year_added',
                    title='Country vs Year',
                    range_color=[0,200],
                    color_continuous_scale=px.colors.sequential.OrRd)
fig.show() '''