import streamlit as st
import pandas as pd

st.title('PHARMACY ALLERGY ALERT DASHBOARD')
try:
    drugs = pd.read_csv('drugs.csv')
    inventory = pd.read_csv('pharmacy_inventory.csv')
    active_ingredient= pd.read_csv('active_ingredient_table.csv')
    
    #to show inventory
    st.subheader('Current Inventory')
    st.dataframe(inventory)
    
    #pharmacist allergy query
    st.subheader('Allergy Interview with patient')
    
    ingredients = drugs['active_ingredient'].unique()
    
    st.write('Check patient allergies:')
    
    allergic_to = []
    for ingredient in ingredients:
        ans = st.radio(f'Are you allergic to {ingredient}?', ('No', 'Yes'), key=ingredient)
        if ans == 'Yes':
            allergic_to.append(ingredient)
    
    if allergic_to:
        st.warning('ALERGY ALERT! Patient is allergic to:')
        for ingredient in allergic_to:
            st.write(f'-{ingredient}')
    
            risky_drugs = drugs[drugs['active_ingredient'] == ingredient]
            if not risky_drugs.empty:
                st.info('Avoid these drugs; consider alternatives:')
                for index, row in risky_drugs.iterrows():
                    alt = row['alternative_drug'] if 'alternative_drug' in row else 'Check Inventory'
                    st.write(f"-{row['drug_name']}-alternative:{alt}")
    else:
        st.success('No allergies reported, all drugs are safe to dispense')
    
    st.subheader('Available Alternatives in Stock')
    if 'alternative_drug' in drugs.columns:
        alternatives = drugs[['drug_name', 'alternative_drug']].merge(inventory, left_on='alternative_drug', right_on='drug_name', how='left')
        st.dataframe(alternatives)

except FileNotFoundError as e:
    st.error(f'csv file missing: {e}')
    st.stop()
