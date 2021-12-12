import pandas as pd
pd.pandas.set_option('display.max_columns', None)

# persona.csv dosyasını okutalım ve veri seti ile ilgili genel bilgileri gösterelim.
df = pd.read_csv('datasets/persona.csv')

def check_df(dataframe, head=5, tail=5, quan=False, info=False, describe=False):
    print("------------DataFrame Summarize------------------")
    if info:
        print("##################### Info #####################")
        print(dataframe.info())
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Head #####################")
    print(dataframe.head(head))
    print("##################### Tail #####################")
    print(dataframe.tail(tail))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    if describe:
        print("################ Describe ###################")
        print(dataframe.describe().T)
    if quan:
        print("##################### Quantiles #####################")
        print(dataframe.quantile([0, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99, 1]).T)

check_df(df, info=True, describe=True, quan=True)


# Kaç unique SOURCE vardır ve Frekansları nedir?
df["SOURCE"].value_counts()


# Kaç unique PRICE vardır?
df["PRICE"].nunique()


# Hangi ülkeden kaçar tane satış olmuş?
df.groupby("COUNTRY").agg({"PRICE":"count"}).sort_values(["PRICE"], ascending=False)
# df["COUNTRY"].value_counts()


# Ülkelere göre satışlardan toplam ne kadar kazanılmış?
df.groupby("COUNTRY").agg({"PRICE":"sum"}).sort_values(["PRICE"], ascending=False)
# Toplam kazanç miktarı ise :
df.agg({"PRICE":"sum"})


# SOURCE türlerine göre göre satış sayıları nedir?
df.groupby("SOURCE").agg({"PRICE":"count"})
# Toplam satış adedi miktarı ise:
df.agg({"SOURCE":"count"})


# Ülkelere göre PRICE ortalamaları nedir?
df.groupby("COUNTRY").agg({"PRICE":"mean"}).round(2).sort_values(["PRICE"], ascending=False)


# SOURCE'lara göre PRICE ortalamaları nedir?
df.groupby("SOURCE").agg({"PRICE":"mean"}).round(2)

agg_df =df.groupby(["COUNTRY","SOURCE","SEX","AGE"]).agg({"PRICE":"mean"})
agg_df =agg_df.sort_values("PRICE",ascending=False)


# COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?
df.groupby(["COUNTRY","SOURCE"]).agg({"PRICE":"mean"}).round(2)


# Görev 2: COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
df.groupby(["COUNTRY","SOURCE","SEX","AGE"]).agg({"PRICE":"mean"}).round(2)


# Görev 3: Çıktıyı PRICE’a göre sıralayınız.
agg_df = df.groupby(["COUNTRY","SOURCE","SEX","AGE"]).agg({"PRICE":"mean"}).round(2).sort_values("PRICE",ascending=False)


# Görev 4: Index’te yer alan isimleri değişken ismine çeviriniz.
agg_df = agg_df.reset_index()


# Görev 5: age değişkenini kategorik değişkene çeviriniz ve agg_df’e ekleyiniz.
agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], bins=[0, 18, 23, 30, 40, agg_df["AGE"].max()], labels=["0_18", "19_23", "24_30", "31_40", "41_" + str(agg_df["AGE"].max())])

''' 2.YOL : 
listem = []
agg_df.values[1][2]
for row in agg_df.values:
    if row[3] < 19:
        listem.append("0_18")
    elif row[3] >= 19 and row[3] < 24:
        listem.append("0_23")
    elif row[3] >= 24 and row[3] < 31:
        listem.append("24_30")
    elif row[3] >= 31 and row[3] < 41:
        listem.append("31_40")
    else:
        listem.append("41_70")
agg_df["AGE_CAT"] = listem
agg_df
'''


# Görev 6: Yeni seviye tabanlı müşterileri (persona) tanımlayınız.
agg_df["customers_level_based"] = [str(row[0]).upper() + "_" + str(row[1]).upper() + "_" + str(row[2]).upper() + "_" + str(row[5]).upper()for row in agg_df.values]
agg_df = agg_df[["customers_level_based","PRICE"]]
agg_df = agg_df.groupby("customers_level_based").agg({"PRICE":"mean"}).round(2).sort_values("PRICE",ascending=False)
agg_df = agg_df.reset_index() # costumers_level_based index gözüküyor onun için resetledik.


# Görev 7: Yeni müşterileri (personaları) segmentlere ayırınız.
agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=["D", "C", "B", "A"])

# Görev 7.1: segmentleri betimleyiniz :
agg_df.groupby(["SEGMENT"]).agg({"PRICE": ["min", "max", "mean", "sum"]})

# Görev 7.2: C Segmentini analiz ediniz :
agg_df[agg_df["SEGMENT"] == 'C'].describe().T


# Görev 8: Yeni gelen müşterileri segmentlerine göre sınıflandırınız ve ne kadar gelir getirebileceğini tahmin ediniz

def predict(new_user):
    [print(i[2] + " Segmentine aittir ve tahmini ortalama gelir = " + str(i[1])) for i in agg_df.values if new_user == i[0]]

predict("TUR_IOS_MALE_24_30")
predict("TUR_ANDROID_FEMALE_31_40")
predict("FRA_IOS_FEMALE_31_40")

''' 2. YOL:
new_user = "TUR_IOS_MALE_24_30"
agg_df[agg_df["customers_level_based"] == new_user]
'''


