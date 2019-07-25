import json
from selenium import webdriver
import numpy as np
from datetime import datetime

lines = []
with open('urls.txt', 'r') as f:
    for line in f:
        lines.append(line.rstrip())

# Set web driver Options as needed

options = webdriver.ChromeOptions()

# load chrome with your profile settings from macbook root
options.add_argument("user-data-dir=/Users/dave-macbook/Library/Application Support/Google/Chrome/")

# headless browser invokes captcha, so don't go headless
# options.add_argument('--headless')

# additional options, use if needed.
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

print("\nwebdriver open")
driver = webdriver.Chrome('/Users/dave-macbook/Downloads/chromedriver', options=options) # < use options=options

def openBrowser(driver):
    # create dictionary
    images =    {'image': "",
                   'stats': "", 'details': "", 'info': "",
                   'last_pulled': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                   'urls': [],
                   'num_images': 1}
    try:
        # create stats like price and address from header
        stats = driver.find_element_by_xpath('//*[@id="overview-scroll"]/div/div/div[2]')
        try:
            # try locating read button and clicking
            read_button = driver.find_element_by_xpath('//*[@id="marketingRemarks-preview"]/div[2]/div/span')
        except:
            pass
        if read_button:
            read_button.click()

        # Try grabbing info and details
        info = driver.find_element_by_xpath('//*[@id="marketingRemarks-preview"]/div[1]/div/div/p/span')
        details = driver.find_element_by_xpath('//*[@id="house-info"]/div[1]/div/div[2]')

        # *** Warning redfin does not like this features grab***
        # features = driver.find_element_by_xpath('//*[@id="property-details-scroll"]/div/div')

        # create text stats
        images['stats'] = stats.text
        images['details'] = details.text
        images['info'] = info.text
        # images['features'] = features.text
    except:
        pass
    try:
        # set image as clickable element
        elem = driver.find_element_by_class_name('img-card')
        # get image url
        images['image'] = elem.get_attribute('src')
        elem.click()
        # set image element
        img = driver.find_element_by_class_name('img-card')
        # get base url for images
        src = img.get_attribute('src')
    except:
        pass

    try:
        # get image count text
        image_count = driver.find_element_by_css_selector('#content > div.criticalComponents.pageComponentsContainer > div:nth-child(13) > section > div > div.PhotoArea > div.PagerIndex.font-size-smaller > span')
        num_images = int(image_count.text.split('of ')[1])
        print(num_images)
        images['num_images'] = num_images
        # create image urls list
        part = src.partition('.jpg')
        urls = [src]
        for i in range(1,num_images):
            urls.append(''.join([part[0][:-2], '_'+ str(i) + part[0][-2:] + part[1]]))
        images['urls'] = urls
    except:
        pass
    return images

def run_crawler():
    for j, line in enumerate(lines[2:]):
        # create last id index
        # if last_id > 0:
        #     num = str(last_id + j +1)
        # else:
        num = str(j)
        print(num, line, '\n')

        driver.implicitly_wait(np.random.uniform(low=1.0, high=2.0))

        # fetch url and save .html
        driver.get(line)
        html = driver.page_source
        with open('./html/'+num+'.html', mode='w') as f:
            f.write(html)

        # save_screenshot
        driver.save_screenshot('./screenshots/'+ num +'.png')
        # open browser
        data = openBrowser(driver)
        # set listing url
        data['listing'] = line

        # create empty json
        with open('./data/'+num+'.json',
                mode='w', encoding='utf-8') as f:
            json.dump([], f)
        # dump json into empty file
        with open('./data/'+num+'.json', 'w') as f:
            json.dump(data, f)

        # close browser
        if j==0:
            driver.close()
            print("\nwebdriver closed")
            break

    # Quit webdriver
    driver.quit()

run_crawler()


