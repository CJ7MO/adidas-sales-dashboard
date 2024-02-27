import datetime
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image

# load data
df = pd.read_excel(r"C:\Users\Administrator\PycharmProjects\dashboard_adidas_st\Adidas.xlsx")
st.set_page_config(page_title="Adidas Sales", page_icon=":earth_americas:", layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

image = Image.open(
    r"C:\Users\Administrator\PycharmProjects\dashboard_adidas_st\img\adidas.jpg")

col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.image(image, width=100)

html_title = """
<style>
    .title-test {
    font-weight:bold;
    padding:5px;
    border-radius:6px
    }
</style>
<center><h1 class="title-test">Adidas Interactive Sales Dashboard</h1></center>
"""
with col2:
    st.markdown(html_title, unsafe_allow_html=True)

col3, col4, col5 = st.columns([0.1, 0.45, 0.45])
with col3:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Last Update:   \n ", box_date)

with col4:
    fig = px.bar(df, x="Retailer", y="TotalSales", labels={"TotalSales": " Total Sales $ "},
                 title="Total Sales by Retailer", hover_data=["TotalSales"], template="gridon", height=500)
    st.plotly_chart(fig, use_container_width=True)

_, view1, down1, view2, down2 = st.columns([0.15, 0.20, 0.20, 0.20, 0.20])
with view1:
    expander = st.expander("Retailer wise sales")
    data = df[["Retailer", "TotalSales"]].groupby(by="Retailer")["TotalSales"].sum()
    data = data.sort_values(ascending=False)
    expander.write(data)

with down1:
    st.download_button("Get the Data", data=data.to_csv().encode("UTF-8"),
                       file_name="RetailerSales.csv", mime="text/csv")

df["Month_Year"] = df["InvoiceDate"].dt.strftime("%y - %m - %b")
result = df.groupby(by=df["Month_Year"])["TotalSales"].sum().reset_index()

with col5:
    fig1 = px.line(result, x="Month_Year", y="TotalSales", title="Total Sales Over the Time", template="gridon")
    st.plotly_chart(fig1, use_container_width=True)

with view2:
    expander = st.expander("Monthly Sales")
    data = result
    expander.write(data)

with down2:
    st.download_button("Get the Data", data=result.to_csv().encode("UTF-8"),
                       file_name="Monthly_sales.csv", mime="text/csv")

st.divider()

result2 = df.groupby(by="State")[["TotalSales", "UnitsSold"]].sum().reset_index()

# add units solds as a line chart on a secondary y-axis
fig3 = go.Figure()
fig3.add_trace(go.Bar(x=result2["State"], y=result2["TotalSales"], name="Total Sales"))
fig3.add_trace(go.Scatter(x=result2["State"], y=result2["UnitsSold"], mode="lines", name="Units Sold",
                          yaxis="y2"))
fig3.update_layout(
    title="Total Sales and Units Sold by State",
    xaxis=dict(title="State"),
    yaxis=dict(title="Total Sales", showgrid=False),
    yaxis2=dict(title="Units Sold", overlaying="y", side="right"),
    template="gridon",
    legend=dict(x=1, y=1)
)

_, col6 = st.columns([0.1, 1])
with col6:
    st.plotly_chart(fig3, use_container_width=True)

_, view3, down3 = st.columns([0.5, 0.45, 0.45])

with view3:
    expander = st.expander("View Data for Sales by Units Sold")
    expander.write(result2)

with down3:
    st.download_button("Get the Data", data=result2.to_csv().encode("UTF-8"),
                       file_name="Sales_by_units_sold.csv", mime="text/csv")
st.divider()

_, col7 = st.columns([0.1, 1])

tree_map = df[["Region", "City", "TotalSales"]].groupby(by=["Region", "City"])["TotalSales"].sum().reset_index()


def format_sales(value):
    if value >= 0:
        return '{:.2f} Lakh'.format(value / 1_000_00)


tree_map["TotalSales_format"] = tree_map["TotalSales"].apply(format_sales)

fig4 = px.treemap(tree_map, path=["Region", "City"], values="TotalSales",
                  hover_name="TotalSales_format",
                  hover_data=["TotalSales_format"],
                  color="City", height=700, width=600)

fig4.update_traces(textinfo="label+value")

with col7:
    st.subheader(":point_right: Total Sales by Region and City in TreeMap")
    st.plotly_chart(fig4, use_container_width=True)

_, view4, down4 = st.columns([0.1, 0.45, 0.45])
with view4:
    result2 = df[["Region", "City", "TotalSales"]].groupby(by=["Region", "City"])["TotalSales"].sum()
    result2 = result2.sort_values(ascending=False)
    expander = st.expander("View data for Total Sales by Region and City")
    expander.write(result2)

with down4:
    st.download_button("Get the Data", data=result2.to_csv().encode("UTF-8"),
                       file_name="Sales_by_region.csv", mime="text/csv")

_, view5, down5 = st.columns([0.1, 0.45, 0.45])
with view5:
    expander = st.expander("View Entire Data")
    expander.write(df)

with down5:
    st.download_button("Get raw Data", data=df.to_csv().encode("UTF-8"),
                       file_name="adidas_sales.csv", mime="text/csv")

st.divider()
