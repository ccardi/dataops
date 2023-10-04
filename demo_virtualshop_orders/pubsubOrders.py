from google.cloud import pubsub
import json
from pprint import pprint
import random
from random import randint
import time
import datetime
import os
import  psutil


publish_client = pubsub.PublisherClient()
topic = os.environ['PUBSUB_TOPIC'] #'projects/pod-fr-retail/topics/orders_stream'

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

#repartition function
def repartition (file,var):
	temparray=[]
	for line in open(file, 'r'):
	    JSONline= json.loads(line)
	    for x in range(0, int(JSONline["weight"])):
	    	temparray.append(JSONline[var]);
	random.shuffle(temparray)
	return temparray
	
#create repartition variables
age = repartition ('/repartition_age.json',"age")
gender = repartition ('/repartition_gender.json',"gender")
livraison = repartition ('/repartition_takeaway.json',"livraison")
paiement= repartition ('/repartition_paiement.json',"paiement")

#load products catalog
products = []
for line in open('/refproduct.json', 'r'):
    products.append(json.loads(line));

#load products catalog
with open('/repartition_panier.json') as data_file:    
    avgBasketCity = json.load(data_file)
    
#load trendsbyCity
trends =[]
for line in open('/trendsByCity.json', 'r'):
	trends.append(json.loads(line))

n=0
#Build all orders
for trend in trends:
	#ordersTotal to be compared be trends
	ordersTotal=0
	trendsTotal=int(trend["trends"])
	while ordersTotal < trendsTotal:
	    #initiate order variables
	    orderProductsQty=0
	    orderTotalPrice=0
	    #build cart
	    cart=[]
	    orderItemsQty=0
	    avgBasket=random.gauss(avgBasketCity[trend["city"]], 2) 
	    date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	    while orderTotalPrice < avgBasket:
	        product=products[randint(0, len(products)-1)]
	        #{"uniq_id","product_category_tree","brand","product_name","retail_price"}
	        line_cart=product
	        randQty= randint(1,3)
	        line_cart["quantity"]=str(randQty)
	        line_cart["price_total"]=float(product["retail_price"])*randQty
	        cart.append(line_cart)
	        orderItemsQty= orderItemsQty+randQty
	        orderTotalPrice= orderTotalPrice + line_cart["price_total"]
	        orderProductsQty = orderProductsQty + 1	    
	    #build order data
	    order={
	        "date":date
	        ,"city":trend["city"]
	        ,"age": age[randint(0, len(age)-1)]
	        ,"gender": gender[randint(0, len(gender)-1)]
	        ,"livraison": livraison[randint(0, len(livraison)-1)]
	        ,"paiement": paiement[randint(0, len(paiement)-1)]
	        ,"orderId":str(random_with_N_digits(15))
	        ,"orderProductsQty":orderProductsQty
	        ,"orderItemsQty":orderItemsQty
	        ,"orderTotalPrice":str(orderTotalPrice)
	        ,"orderDetails":cart
	    }
	    ordersTotal=ordersTotal+orderTotalPrice
	    n=n+1
	    if n % 1000 == 0 :
						pprint(str(n) + " events sent")
						process = psutil.Process()
						pprint(process.memory_info().rss) 
							
	    data= json.dumps(order)
	    data= data.encode('utf-8')
	    publish_client.publish(topic, data=data)

pprint(n)
pprint("All Done")
