import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from lxml import html
from time import sleep
from random import randint
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.action_chains import ActionChains
import datetime

dataout = open("urban_ladder_playstore_reviews.csv","w")
datawrite = csv.writer(dataout)
header = ["Review NO", "Reviewer Name", "Review Stars", "Review Date", \
          "Review Helpful","Short Text", "Full Text"]
datawrite.writerow(header)

def removeNonAscii(s):
    return "".join(filter(lambda x: ord(x)<128, s))

def clean_text(input_given):
    input_given = removeNonAscii(input_given)
    input_given = str(input_given)
    input_given = input_given.replace("\n"," ").replace("\t"," ")
    return input_given

def multiple_space_remover(input_given):
    if type(input_given) == str:
        input_given = input_given.strip()
        input_given = clean_text(input_given)
        while("  " in input_given):
            input_given = input_given.replace("  "," ")
        input_given = input_given.strip()

        return input_given
    if type(input_given) == list:
        temp_list = []
        for il in range(0,len(input_given)):
            input_given[il] = input_given[il].strip()
            while("  " in input_given[il]):
                input_given[il] = input_given[il].replace("  "," ")
            input_given[il] = input_given[il].strip()
            input_given[il] = clean_text(input_given[il])
            if len(input_given[il]) > 0:
                temp_list.append(input_given[il])
        return temp_list


url = "https://play.google.com/store/apps/details?id=com.urbanladder.catalog&showAllReviews=true"

driver = webdriver.Firefox()
driver.get(url)
sleep(randint(15,20))

page_no = 1

count = 0
old_reviews = 0
scroll_count = 0
while(True):
    if count >= 5:
        break
    else:
        HTMLTree = html.fromstring(driver.page_source)
        review_hits =  HTMLTree.xpath('//div[@jsname="fk8dgd"]/div[@jsmodel="y8Aajc"]')
        total_reviews = len(review_hits)
        if total_reviews == old_reviews:
            count = count + 1
        else:
            count = 0
            old_reviews = total_reviews
        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.find_element_by_tag_name('body').send_keys(Keys.END)
        sleep(randint(4,6))
        scroll_count = scroll_count + 1
        print(scroll_count)
        try:
            more_box = driver.find_element_by_xpath('//content[@class="CwaK9"]\
                                            //span[@class="RveJvd snByac"]')
            more_box.click()
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(randint(3,5))
        except:
            pass

print ("Total Reviews Found : ",total_reviews)

print(total_reviews)

i = 1

print("Scrapping Started")

HTMLTree = html.fromstring(driver.page_source)

while(i < total_reviews + 1):
    if (i % 20) == 0:
        print("{} completed out of {}".format(i,total_reviews))
    
    row_data = []
    row_data.append(i)
    reviewer_name = HTMLTree.xpath('//div[@jsname="fk8dgd"]\
                                    //div[@jsmodel="y8Aajc"]['+str(i)+']\
                                    //div[@class="bAhLNe kx8XBd"]\
                                    //span[@class="X43Kjb"]//text()')

    reviewer_name = multiple_space_remover(reviewer_name)
    row_data.append((" | ".join(reviewer_name)))


    review_stars = HTMLTree.xpath('//div[@jsname="fk8dgd"]\
                                    //div[@jsmodel="y8Aajc"]['+str(i)+']\
                                    //div[@class="bAhLNe kx8XBd"]\
                                    //span[@class="nt2C1d"]\
                                    //div[@class="pf5lIe"]//div//@aria-label')

    review_stars = multiple_space_remover(review_stars)
    row_data.append((" | ".join(review_stars)))

    review_date = HTMLTree.xpath('//div[@jsname="fk8dgd"]\
                                    //div[@jsmodel="y8Aajc"]['+str(i)+']\
                                    //div[@class="bAhLNe kx8XBd"]\
                                    //span[@class="p2TkOb"]//text()')

    review_date = multiple_space_remover(review_date)
    row_data.append((" | ".join(review_date)))


    helpful_stmt = HTMLTree.xpath('//div[@jsname="fk8dgd"]\
                                    //div[@jsmodel="y8Aajc"]['+str(i)+']\
                                    //div[@class="YCMBp GVFJbb"]\
                                    //div[@class="jUL89d y92BAb"]//text()')

    helpful_stmt = multiple_space_remover(helpful_stmt)
    row_data.append((" | ".join(helpful_stmt)))


    short_text = HTMLTree.xpath('//div[@jsname="fk8dgd"]\
                                    //div[@jsmodel="y8Aajc"]['+str(i)+']\
                                    //div[@class="UD7Dzf"]\
                                    //span[@jsname="bN97Pc"]//text()')

    short_text = multiple_space_remover(short_text)
    row_data.append((" | ".join(short_text)))

    long_text = HTMLTree.xpath('//div[@jsname="fk8dgd"]\
                                    //div[@jsmodel="y8Aajc"]['+str(i)+']\
                                    //div[@class="UD7Dzf"]\
                                    //span[@jsname="fbQN7e"]//text()')

    long_text = multiple_space_remover(long_text)
    row_data.append((" | ".join(long_text)))

    datawrite.writerow(row_data)
    i = i + 1        

dataout.close()
print("Over")
