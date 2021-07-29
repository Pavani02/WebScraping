import selenium
import bs4
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from msedge.selenium_tools import Edge,EdgeOptions
def get_url(required_product):
    base_url='https://www.amazon.com/s?k={}&ref=nb_sb_noss_1'
    required_product=required_product.replace(' ','+')   
    url=base_url.format(required_product)
    url+='&page={}'
    return url
def product_details(item):  
    try:
        description=item.find('span','a-size-medium a-color-base a-text-normal').text
        pro_linking=item.a
        product_link='https://www.amazon.com/'+pro_linking.get('href')
        whole_price=item.find('span','a-price-whole').text
        decimal_price=item.find('span','a-price-fraction').text
        price=whole_price+decimal_price
    except AttributeError:
        #As no price means item is currently out of stock, we return without fetching details of that product
        return
    try:
        rating=item.find('span','a-icon-alt').text
        no_of_reviews=item.find('span','a-size-base').text
    except AttributeError:
        #Though rating isn't there, product is still in stock
        rating=''
        no_of_reviews=''
    return_value=(description,price,rating,no_of_reviews,product_link)
    return return_value
def product_details_horizontal_allignment(item):
    try:
        description=item.find('span','a-size-base-plus a-color-base a-text-normal').text
        whole_price=item.find('span','a-price-whole').text
        fraction_price=item.find('span','a-price-fraction').text
        price=whole_price+fraction_price
        product_link='https://www.amazon.com'+item.find('a','a-link-normal').get('href')
    except AttributeError:
        return
    try:
        rating=item.find('span','a-icon-alt').text
        no_of_reviews=item.find('span','a-size-base').text
    except:
        rating=''
        no_of_reviews=''
    return_value=(description,price,rating,no_of_reviews,product_link)
    return return_value
def main_func(product_name):
    chromedriver="C:/Drivers/chromedriver_win32/chromedriver.exe" 
    driver=webdriver.Chrome(chromedriver)
    result=[]
    url=get_url(product_name)
    for i in range(1,21):
        new_url=url.format(i)
        driver.get(new_url)
        soup=BeautifulSoup(driver.page_source,'html.parser')
        products=soup.find_all('div',{'data-component-type':'s-search-result'})
        for item in products:
            item_data=product_details(item)
            if(item_data):
                result.append(item_data)
    driver.close()
    return result
def main_func_horizontal(product_name):
    chromedriver="C:/Drivers/chromedriver_win32/chromedriver.exe" 
    driver=webdriver.Chrome(chromedriver)
    result=[]
    url=get_url(product_name)
    for i in range(1,21):
        new_url=url.format(i)
        driver.get(new_url)
        soup=BeautifulSoup(driver.page_source,'html.parser')
        products=soup.find_all('div',{'data-component-type':'s-search-result'})
        for item in products:
            item_data=product_details_horizontal_allignment(item)
            if(item_data):
                result.append(item_data)
    driver.close()
    return result
def func(product_name):
    l=main_func(product_name)
    if(len(l)==0):
        l=main_func_horizontal(product_name)
    with open('Results.csv','w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f,delimiter=',')
        writer.writerow({'Description','Price','Rating','Number of reviews','Link'})
        writer.writerows(l)
