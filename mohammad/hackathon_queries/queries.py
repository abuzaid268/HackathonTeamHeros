import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    db="hackathon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)
if connection.open:
    print("successfully connected ")


def getStoresNames():
    try:
        with connection.cursor() as cursor:
            query = f'select stores.storename from stores'
            cursor.execute(query)
        list = cursor.fetchall()
        return list
    except:
        print("Could insert stores into DB")


def getStoresProductsList():
    try:
        with connection.cursor() as cursor:
            query = f'select s.storename, p.productname, sp.price from stores_products as sp, stores as s, products ' \
                    f'as p where s.storeid=sp.storeid and p.productid = sp.productid '
            cursor.execute(query)
        list = cursor.fetchall()
        return list
    except:
        print("Could insert stores into DB")


def getDictionaryofAllStoresUnused():
    dict_of_stores = {}
    items_list = getStoresProductsList()
    stores_list = getStoresNames()
    for stores in stores_list:
        dict_of_stores[stores['storename']] = []
        for item in items_list:
            if item['storename'] == stores['storename']:
                dict_of_stores[stores['storename']].append(
                    {'product_name': item['productname'], 'price': item['price']})
    return dict_of_stores


def getDictionaryofStores():
    dict_of_stores = {}
    items_list = getStoresProductsList()
    stores_list = getStoresNames()
    for stores in stores_list:
        dict_of_stores[stores['storename']] = {}
        for item in items_list:
            if item['storename'] == stores['storename']:
                dict_of_stores[stores['storename']][item['productname']] = item['price']
    return dict_of_stores


def getPriceOfOneItem(item: str):
    dict_of_prices = {}
    try:
        with connection.cursor() as cursor:
            query = f'select p.productName, sp.price, s.storename from stores_products as sp, products as p, ' \
                    f'stores as s where p.productid = sp.productid and p.productname = "{item}" and s.storeid = ' \
                    f'sp.storeid '
            cursor.execute(query)
        list = cursor.fetchall()
        list_of_stores = getStoresNames()
        for store in list_of_stores:
            for product in list:
                if product['storename'] == store['storename']:
                    dict_of_prices[store['storename']] = product['price']
        return dict_of_prices
    except:
        print("Could not get item price from DB")

def getProductName(ProductCode: str):
    try:
        with connection.cursor() as cursor:
            query = f'select productname from coded_products where productcode = "{ProductCode}"'
            cursor.execute(query)
            Productname = cursor.fetchall()
            return Productname[0]['productname']
    except:
        print(f"could not get product name by code {ProductCode}")

def getUserTypeByChatId(chat_id: int):
    try:
        with connection.cursor() as cursor:
            query = f"select UserType from Users where ChatId = {chat_id}"
            cursor.execute(query)
            return cursor.fetchone()
    except Exception as e:
        print(e)
        return "failed to insert"


if __name__ == '__main__':
    items_list = getStoresProductsList()
    markets_list = getStoresNames()
    list_of_all_markets = getDictionaryofStores()
    print(getPriceOfOneItem('apple sauce'))
    print(getProductName('applesgalabag'))
    print(markets_list)
    print(list_of_all_markets)
    print(getPriceOfOneItem('apple sauce'))
    print(getPriceOfOneItem('apple sauce'))
    for i in range(123, 130):
        print(getUserTypeByChatId(i))
