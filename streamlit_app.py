import seaborn as sb
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.dates as mdates



df_fake=pd.read_csv("Data_for_AI/fake_combined_after_categorization.csv")

df_complete=pd.read_csv("Data_for_AI/df_complete_after_categorization.csv")

df_selected=df_fake

st.set_page_config(
    page_title="Analysis of private Budget",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon=":dolar:"
)

st.title("Analysis of private budget")
st.markdown("---")

col1,col2=st.columns([0.2,0.8])

with col1:
   
    st.header("Filters")

    #setuping filters

    #time
    df_selected["Data of Transaction"]=pd.to_datetime(df_selected["Data of Transaction"])
    oldest_date=df_selected["Data of Transaction"].min().to_pydatetime().date()
    newest_date=df_selected["Data of Transaction"].max().to_pydatetime().date()
    date_range=st.slider("Please select date range that you want to analyse",min_value=oldest_date,max_value=newest_date,value=(oldest_date, newest_date))

   #Categories
    df_cat=df_selected[["Main_Category","Sub_Category"]]

    mapping_dict=df_cat.groupby("Main_Category")["Sub_Category"].unique().apply(list).to_dict()

    main_options=main_options = ["All"] + sorted(list(mapping_dict.keys()))

    selected_main_cat=st.multiselect("Choose Main Category",options=main_options,placeholder="Select categories...")

    available_subs=[]

    if "All" in selected_main_cat:
        for value in  mapping_dict.values():
            available_subs.extend(value)
    else:
        for main_cat in selected_main_cat:
                available_subs.extend(mapping_dict[main_cat])

    available_subs=sorted(list(set(available_subs)))
   
    if available_subs:
        sub_options=["All"] + available_subs
    else:
        sub_options=["All"]
    
    selected_sub=st.multiselect("Choose Sub-Category:",options=sub_options)

    #filters application
    df_filtered = df_selected.copy()
    df_filtered=df_filtered[
        (df_filtered["Data of Transaction"].dt.date >= date_range[0]) & 
        (df_filtered["Data of Transaction"].dt.date <= date_range[1])
        ]

    if selected_main_cat and "All" not in selected_main_cat:
        df_filtered = df_filtered[df_filtered["Main_Category"].isin(selected_main_cat)]

    if selected_sub and "All" not in selected_sub:
        df_filtered=df_filtered[df_filtered["Sub_Category"].isin(selected_sub)]

        
        
 
with col2:

    #additional DF for better visualization and data Application
    df_filtered["Month"]=df_filtered["Data of Transaction"].dt.to_period("M").dt.to_timestamp()

    df_filtered_income=df_selected[df_selected["Main_Category"]=="Income"]
    df_filtered_income["Month"]=df_selected["Data of Transaction"].dt.to_period("M").dt.to_timestamp()
    df_filtered_income=df_filtered_income[
        (df_filtered_income["Data of Transaction"].dt.date >= date_range[0]) & 
        (df_filtered_income["Data of Transaction"].dt.date <= date_range[1])
        ]
    
    df_filtered_spendings=df_filtered[df_filtered["Main_Category"]!="Income"]
    df_filtered_spendings["Amt"]=df_filtered_spendings["Amt"].abs()

    #tables 
    #Spendings in Main Category

    df_Cat_spendings_to_analysis=df_filtered_spendings.groupby("Main_Category").agg(
        Total_Spendings_in_Categoty=("Amt","sum"),
        Mean_Spendings_in_Categoty=("Amt","mean"),
        Min_value_in_Category=("Amt","min"),
        Max_value_in_Category=("Amt",'max')
    ).round(2)

    #Spendings in Sub Category

    df_SubCat_spendings_to_analysis= df_filtered_spendings.groupby("Sub_Category").agg(
        Total_Spendings_in_SubCategoty=("Amt","sum"),
        Mean_Spendings_in_SubCategoty=("Amt","mean"),
        Min_value_in_SubCategory=("Amt","min"),
        Max_value_in_SubCategory=("Amt",'max'),
        Count_of_occurance=("Description","count")
    ).round(2)

    #General Income accros Sub categories

    df_SubCat_income_to_analysis= df_filtered_income.groupby("Sub_Category").agg(
        Total_Income_in_SubCategoty=("Amt","sum"),
        Mean_Income_in_SubCategoty=("Amt","mean"),
        Min_value_in_SubCategory=("Amt","min"),
        Max_value_in_SubCategory=("Amt",'max'),
        Count_of_occurance=("Description","count")
    ).round(2)



    #Charts and Tables in dashboard

    st.header("Analysis")


    #Sum of Income
    st.subheader("Sum of Income")
    fig_1,ax_1=plt.subplots(figsize=(15,6))
    sns.barplot(
        data= df_filtered_income,
        x="Main_Category",
        y="Amt",
        estimator="sum",
        errorbar=None,
        ax=ax_1,
        hue="Main_Category",
        palette="viridis",
        legend=False
        )
    
    ax_1.set_xlabel("Main Category")
    ax_1.set_ylabel("Amount")
    plt.xticks(rotation=45)


    for container in ax_1.containers:
        labels = [f'{v:,.1f}'.replace(',', ' ') for v in container.datavalues]
        ax_1.bar_label(container, labels=labels, padding=3)

    st.pyplot(fig_1)

    #Sum of Income in Sub-Categories
    st.subheader("Sum of Income in Sub-Categories")
    fig_1,ax_1=plt.subplots(figsize=(15,6))
    sns.barplot(
        data= df_filtered_income,
        x="Sub_Category",
        y="Amt",
        estimator="sum",
        errorbar=None,
        ax=ax_1,
        hue="Sub_Category",
        palette="viridis",
        legend=False
        )
    
    ax_1.set_xlabel("Main Category")
    ax_1.set_ylabel("Amount")
    plt.xticks(rotation=45)
    
    for container in ax_1.containers:
        labels = [f'{v:,.1f}'.replace(',', ' ') for v in container.datavalues]
        ax_1.bar_label(container, labels=labels, padding=3)

    st.pyplot(fig_1)

    #Income table
    st.subheader("Income Data in Sub Categories")
    st.dataframe(df_SubCat_income_to_analysis)

    #Change of Income

    st.subheader("Change of Income")
    fig_3,ax_3=plt.subplots(figsize=(15,6))
    sns.lineplot(
        data= df_filtered_income,
        x="Month",
        y="Amt",
        estimator="sum",
        errorbar=None,
        ax=ax_3,
        hue="Main_Category",
        palette="viridis",
        legend=True
        )
    
    ax_3.xaxis.set_major_locator(mdates.MonthLocator())
    ax_3.xaxis.set_major_formatter(mdates.DateFormatter('%B'))
    
    ax_3.set_xlabel("Time")
    ax_3.set_ylabel("Amount")
    st.pyplot(fig_3)

    #Sum of spendings accros Main Categories"
    st.subheader("Sum of spendings accros Main Categories")

    fig_1,ax_1=plt.subplots(figsize=(15,6))
    sns.barplot(
        data=df_filtered_spendings,
        x="Main_Category",
        y="Amt",
        estimator="sum",
        errorbar=None,
        ax=ax_1,
        hue="Main_Category",
        palette="viridis",
        legend=False
        )
    
    ax_1.set_xlabel("Main Category")
    ax_1.set_ylabel("Amount")
    plt.xticks(rotation=45)
    for container in ax_1.containers:
        labels = [f'{v:,.1f}'.replace(',', ' ') for v in container.datavalues]
        ax_1.bar_label(container, labels=labels, padding=3)

    st.pyplot(fig_1)

    # Table: Spenings in Main Category

    st.subheader("Spending Data in Main Categories")

    st.dataframe(df_Cat_spendings_to_analysis)

    #Sum of spendings accros Sub-Categories
    st.subheader("Sum of spendings accros Sub-Categories")

    fig_2,ax_2=plt.subplots(figsize=(15,6))
    sns.barplot(
        data=df_filtered_spendings,
        x="Sub_Category",
        y="Amt",
        estimator="sum",
        errorbar=None,
        ax=ax_2
        )
    
    ax_2.set_xlabel("Sub Category")
    ax_2.set_ylabel("Amount")
    plt.xticks(rotation=45)
    for container in ax_1.containers:
        labels = [f'{v:,.1f}'.replace(',', ' ') for v in container.datavalues]
        ax_1.bar_label(container, labels=labels, padding=3)
        
    st.pyplot(fig_2)

    # Table: Spenings in Sub Category

    st.subheader("Spending Data in Sub Categories")

    st.dataframe(df_SubCat_spendings_to_analysis)

    #Sum of spendings accros the time
    st.subheader("Mean spendings accros the time")

    fig_3,ax_3=plt.subplots(figsize=(15,6))
    sns.lineplot(
        data=df_filtered_spendings,
        x="Month",
        y="Amt",
        estimator="sum",
        errorbar=None,
        ax=ax_3,
        hue="Main_Category",
        palette="viridis",
        legend=True
        )
    ax_3.xaxis.set_major_locator(mdates.MonthLocator())
    ax_3.xaxis.set_major_formatter(mdates.DateFormatter('%B'))
    
    ax_3.set_xlabel("Time")
    ax_3.set_ylabel("Amount")
    st.pyplot(fig_3)

    st.subheader("AI Summary")

    from AI_financial_report import financial_report
    
    st.write(financial_report)



