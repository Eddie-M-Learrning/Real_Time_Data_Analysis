#Greetings to Every_One
#In this code ,We converted the all printing statements to a Message
#Kindly remove the message statements only to visualize the output ,after learning above the code 
#To learn : visit Keith Galli youtube channel : "Solving real World data science task with python pandas video": 

import pandas as pd 
from glob import glob

stock = sorted(glob('Sales_*_2019.csv'))
#print(stock)

df = pd.concat((pd.read_csv(file).assign(filename = file)
         for file in stock),ignore_index =True)
#print(df.head())
#print(df.info)
#df.to_csv('Stock_Datas.csv',index = False)
df = df.drop(['filename'],axis ='columns')
#print(df.head())

df['month'] = df['Order Date'].str[0:2]
#print(df.head(10))

nan_df = df[df.isna().any(axis=1)]
#print(nan_df)
df = df.dropna(how ='all')
#print(df.head(5))

temp_df = df[df['Order Date'].str[0:2]== 'Or']
#print(temp_df.head())

df = df[df['Order Date'].str[0:2]!= 'Or']
#print(df.head())

df['month'] = df['month'].astype('int32')
#print(df.head())

#convert coulmn into correct type

df['Quantity Ordered'] = pd.to_numeric(df['Quantity Ordered'])
df['Price Each'] = pd.to_numeric(df['Price Each'])

#creating sales Column
df['Sales'] =df['Quantity Ordered']*df['Price Each']
#print(df['Sales'])

#genaral Question : What was the best month for the sales ? How much earned in the month ?

result = df.groupby('month').sum()
#print(sales)

#visualising the report
import matplotlib.pyplot as plt
months= range(1,13)
plt.bar(months,result['Sales'])
plt.xlabel("Months")
plt.title("Best Month in Sales")
plt.legend()
plt.ylabel("Sales")
plt.show()

#Ans : By analysing the graph , we conclude that the best month for sales is :December:

#General Question : which city done Highest sales?

# Creating City column
def get_state(address):
    return address.split(',')[2].split(' ')[1]
df['city'] =df['Purchase Address'].apply(lambda x : x.split(",")[1] + " ("+ get_state(x)+")")
#print(df['city'])

city = df.groupby('city').sum()

cities= [city for city ,df in df.groupby('city')]
plt.bar(cities,city['Sales'])
plt.title("Best City in Sales")
plt.xticks(cities,rotation = 'vertical' , size=8)
plt.legend()
plt.show()
#Ans : By analysing graph , We conclude that the Sanfransisco is best at selling 


#General Question : What time should we display Advertisements to maximize likelihood of customers buying product?

df['Order Date'] = pd.to_datetime(df['Order Date'])
#print(df['Order Date'])
df['Hour']  = df['Order Date'].dt.hour
#print(df['Hour'])
df['Minute'] = df['Order Date'].dt.minute
#print(df['Minute'])

hours= [hour for hour ,df in df.groupby('Hour')]
plt.plot(hours , df.groupby(['Hour']).count())
#print(df.groupby(['Hour']).count())
plt.xticks(hours)
plt.xlabel('Hour')
plt.title("Advertisement Timing Recommendation")
plt.ylabel("Number of Orders")
plt.grid()
plt.legend()
plt.show()
#Ans : By Analysing the graph , we can conclude that the recommended time to Advertise is 11 am (11) or 7 pm (19)

#General Question : Which products are most often sold together?
sn = df[df['Order ID'].duplicated(keep =False)]
#print(sn.head(10))
sn['grouped'] = df.groupby('Order ID')['Product'].transform(lambda x : ','.join(x))
sn = sn[['Order ID','grouped']].drop_duplicates()
#print(sn.head(10))

from itertools import combinations
from collections import Counter

count = Counter()

for row in sn['grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list , 2)))
for key , value in count.most_common(10):
    print(key ,value)
    
#Ans : Iphone and Lightning Charge Cable Combo Sells Most 
    
#General Question : Which product sold most?

product_group = df.groupby('Product')
Quantity_Ordered = product_group.sum()['Quantity Ordered']
products= [product for product ,sn in product_group]

plt.bar(products,Quantity_Ordered)
plt.xticks(products , rotation='vertical',size = 8)
plt.ylabel('Quantity_Ordered')
plt.xlabel("Products")
plt.legend()
plt.show()

prices = df.groupby('Product').mean()['Price Each']
print(prices)

fig,ax1 = plt.subplots()

ax2 =ax1.twinx()
ax1.bar(products,Quantity_Ordered,color = 'g')
ax2.plot(products,prices,'b')
plt.title("Most Sold Product")
ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered' , color ='g')
ax2.set_ylabel('Price($)',color = 'b')
ax1.set_xticklabels(products,rotation='vertical',size=8)
plt.legend()
plt.show()


#Ans : AAA batteries , because it was low in cost than all 




#Code_Credit : Keith Galli
#Recreated_by : Gughan.B ("Eddie-M-Learning")