from tkinter import *

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
import pandas as pd
import shutil
from time import sleep
import requests
import random
import os
import sys




root = Tk()


def from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb

def select_text_or_select_and_copy_text(e):
    e.widget.select_range(0, 'end')

def delete_text(e):
    e.widget.delete('0', 'end')






def display(message):
    print('0'*60)
    print(message)
    print('0' * 60)
    print()

class FB_IMAGES:

    def launch_facebook(driver):
        '''This fucntions launches the basic version of facebook that doesnot need javascript.
        Anyway i am using selenium instead of scrapy or other libraries because i find it really cool

        returns the driver '''
        driver.get('https://mbasic.facebook.com')
        display('Succesfully launched  Facebook LoginPage')
        return driver

    def login(username,password):
        ''' Logins to your facebook account
        Input :
            username: facebook username or email
            password: facebook password'''
        display('Logging  in....')
        driver.find_element(By.XPATH,'//*[@class="bk bl bm"]').send_keys(username)
        driver.find_element(By.XPATH,'//*[@class="bk bl bn bo"]').send_keys(password)
        driver.find_element(By.XPATH,'//*[@class="m s n bp bq br"]').click()
        display('Logged in succesfully')

        # disp('Saving cookies for next login')
        # pickle.dump(driver.get_cookies(), open("facebook.pkl", "wb"))

        #loading the cookie
        # for cookie in pickle.load(open("QuoraCookies.pkl", "rb")):
        #     driver.add_cookie(cookie)

        return driver

    def check_login_with_one_tap():
        '''This might be useful if you did login sometimes facebook asks if you want
        to enable on tap login.'''
        try:
            driver.find_element_by_xpath('//form/div/input').click()
            display('Login with one tap Notifications cleared')
        except Exception as e:
            display('No login with one tap detected')
            display(e)

    def open_photos(driver):
        '''As name suggests launches the photos page of the page it is currently in'''
        driver.find_element(By.LINK_TEXT,'Photos').click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="pages_msite_body_contents"]/div/div[1]/div[2]')))

        display('All Photos loaded succesfully')
        return  driver

    def launch_page(driver, page):
        '''Launches the facebook page we are supposed to scrape image from
        Input:
            page= link to the facebook page'''
        driver.get(page)
        return driver



    def download_images(driver,page_name):
        '''
        it downloads all the images using get_imagelink() function'''
        try:
            os.mkdir(page_name)
            display('Created folder named'+page_name)
        except Exception as e:
            display('Couldnot create folder named '+page_name+'. Maybe it already exists'+'\nError:'+str(e))
        try:
            os.chdir(page_name)
            display('Navigating to'+page_name)
        except:
            pass

        link=driver.find_element_by_xpath('//table[@role="presentation"]/tbody/tr/td[1]/a').get_attribute('href')




        driver.get(link)
        first_image =driver.find_element(By.LINK_TEXT,'View Full Size').get_attribute('href')
        count=1
        decide=0
        wrong = 0
        while True:
            try:
                image = driver.find_element(By.LINK_TEXT,'View Full Size').get_attribute('href')
                
            except Exception as e:
                wrong+=1
                print('Error occured',e)
                print('Trying to login and get photos. This might get your account banned')
                driver = login('ray@instaboostmedia.com','ibmmon3y')
                    
            if image == first_image: # here we are looking if the first image repeats itself. this is because when clicking next the images loop
                decide+=1
            if image == first_image and decide  >  1:
                display('Looks like the last image')
                os.chdir('../')
                display('First link:'+first_image+'\nCurrent Link:'+image)
                display('Succesfully downloaded '+str(count)+' images')
                display('Leaving'+page_name+'folder')
                break
            
            
            if wrong > 4:
                
                display('Something went wrong while getting further images. Maybe images are private')
                os.chdir('../')
                display('First link:'+first_image+'\nCurrent Link:'+image)
                display('Succesfully downloaded '+str(count)+' images')
                display('Leaving'+page_name+'folder')
                break            

            ext= image.split('?')[0][-4:]

            try:
                t=random.randint(3,6)
                display('Sleeping for '+ str(t)+' Seconds before downloading the image')
                sleep(t)
                response = requests.get(image, stream=True)
                with open(str(count) + ext, 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                del response
                loc=os.getcwd()
                downloaded = loc + '/' + str(count)+ext
                display('Image downloaded at '+downloaded)
            except Exception as e:
                display('Couldnot download image'+image+'\nError'+str(e)+'\nSkipping.......')

            val = random.randint(1,4)
            display('Waiting for '+str(val)+'seconds to prevent ip block')
            sleep(val)
            count+=1
            next=driver.find_element(By.LINK_TEXT,'Next').get_attribute('href')
            driver.get(next)




    def random():
        val  = random.randint(1,4)
        display('Waiting randomly for ' + str(val) +' seconds')
        return val



def main(isproxy, proxy, isfacebookLink,facebookLink, filename):

    if isproxy == True:
        # =============================================================================
        #proxy is optional but recommended
        PROXY = proxy

        prox = Proxy()
        prox.proxy_type = ProxyType.MANUAL
        prox.http_proxy = PROXY
        prox.socks_proxy = PROXY
        prox.ssl_proxy = PROXY

        capabilities = webdriver.DesiredCapabilities.CHROME
        prox.add_to_capabilities(capabilities)
        display('Succesfully used the proxy {a}'.format(a=PROXY))
        driver = webdriver.Chrome(executable_path=r"chromedriver",desired_capabilities=capabilities)

        # =============================================================================
    else:
        display('No proxy given. Scraping without proxy')
        driver = webdriver.Chrome(executable_path=r"chromedriver")


    if isfacebookLink == True:
        links=[]
        links.append(facebookLink)
    else:
        input_file = filename
        display('Reading the {a} file'.format(a=filename))
        try:
            data = pd.read_csv(input_file)

            links = data['Links']
        except Exception as e:
            display('There appears to be something wrong with your file./n{a}.\nError:{b}./n/nExiting the program'.format(a=filename,b=str(e)))
            sys.exit()

    scraper = FB_IMAGES

    #opening facebook in chrome browser
    driver = scraper.launch_facebook(driver)
    #logging ing
    # scraper.login('hero.hiralal.161214','amit2015')
    sleep(scraper.random())
    #removing notification
    # scraper.check_login_with_one_tap()
    sleep(scraper.random())


    #here we will load all the facebook pages sequentially  and scrape all the images from each page

    no_pages=0
    for link in links:
        display(link)
        link = link.rstrip('/')
        page_name=link.split('/')[-1]
        display('Visiting page '+page_name+'\n'+link)

        driver = scraper.launch_page(driver,link) #opening the facebook page
        sleep(scraper.random())
        driver = scraper.open_photos(driver) # navigating to photos
        sleep(scraper.random())
        scraper.download_images(driver, page_name) # it will create a folder for the page. Navigate inside it  and download all the images for it and then leave the folder
        no_pages+=1

    print('*'*50)
    display('Succesfully crawled '+ str(no_pages-1) + 'pages)')

# defining the top welcome message

welcome = Label(root, text='Facebook Scraper v1.1',relief=SUNKEN,font=('Helvetica',20),fg='white',bg=from_rgb((56,161,243)))
welcome.grid(column = 1, row= 0 ,sticky='e',pady=20)

photo = PhotoImage(file = 'facebook.png')
photolabel = Label(root, image = photo,relief=SUNKEN)
photolabel.grid(column = 0, row= 0, sticky='e')

#proxy this is optional

proxy = Label(root, text='Proxy  ', font=('Helvetica',16),fg='black')
proxy.grid(column=0,row=1,sticky='e',pady=4)

proxyEntry = Entry(root,font=('Helvetica',16),fg='black',borderwidth=2)
proxyEntry.grid(column=1,row=1,pady=4,sticky='w')
proxyEntry.focus()
#press control c to copy all the text or select all the text
#delete will delete everything

proxyEntry.bind('<Control-c>', select_text_or_select_and_copy_text)
proxyEntry.bind('<Delete>', delete_text)


facebookLink = Label(root, text='Facebook Page Link  *',font=('Helvetica',16),fg='black')
facebookLink.grid(column=0,row=6,pady=5,sticky='e')

facebookLinkEntry= Entry(root, font=('Helvetica',16),fg='black',borderwidth=2, width=50)
facebookLinkEntry.grid(column=1,row=6,sticky='w',columnspan=200,pady=10)

facebookLinkEntry.bind('<Control-a>', select_text_or_select_and_copy_text)
facebookLinkEntry.bind('<Control-c>', select_text_or_select_and_copy_text)
facebookLinkEntry.bind('<Delete>', delete_text)

#or enter the file name
choice  = Label(text='or').grid(column=1,row=7)


file = Label(root, text='File Name  *',font=('Helvetica',16),fg='black')
file.grid(column=0,row=9,pady=5,sticky='e')

filename  = Entry(root, font=('Helvetica',16),fg='black',borderwidth=2, width=50)
filename.grid(column=1,row=9,sticky='w', columnspan=100)


filename.bind('<Control-c>', select_text_or_select_and_copy_text)
filename.bind('<Delete>', delete_text)



def show():
    global username
    global password
    global filename
    global facebook

    try:
        proxy =proxyEntry.get()
    except:
        pass

    try:
        filename = filename.get()
    except:
        pass

    try:
        facebook = facebookLinkEntry.get()
    except:
        pass
    global root
    root.quit()
    root.destroy()

    print('Proxy:',proxy)
    print('Facebook Link:',facebook)
    print('File Name:',filename)
    #calling the main function to start scraping

    if proxy == '':
        isproxy = False
    else:
        isproxy = True

    if facebook == '':
        isfacebookLink = False
    else:
        isfacebookLink = True

    if facebook == '' and filename == '':
        display('Please enter the facebook page link or an csv file name.\nBoth cannot be empty.\nExiting the program')
        sys.exit()
    if facebook != '' and filename !='':
        display('You can only use one input either facebook page link or an csv file.\nBoth cannot be used.\nExiting the program')
        sys.exit()

    #begining of scraping
    main(isproxy,proxy,isfacebookLink,facebook,filename)



submit = Button(root, text='SCRAPE IMAGES',font=('Helvetica',18),fg='white',bg=from_rgb((66,103,178)), command=show)
submit.grid(column=0,row=10,sticky='w',padx=20,pady=10)

#running the GUI continuoulsy
root.mainloop()




