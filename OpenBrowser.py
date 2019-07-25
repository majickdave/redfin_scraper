import urllib.request
from datetime import datetime

def openBrowser(driver):
    # create dictionary
    images =    {'image': "",
                   'stats': "", 'details': "", 'info': "",
                   'last_pulled': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                   'urls': []}
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
        image_count = driver.find_element_by_xpath('//*[@id="content"]/div[6]/div[7]/section/div/div[1]/div[4]/span/text()[3]')
        num_images = int(image_count)

        # create image urls list
        part = src.partition('.jpg')
        urls = [src]
        for i in range(1,num_images):
            urls.append(''.join([part[0][:-2], '_'+ str(i) + part[0][-2:] + part[1]]))
        images['urls'] = urls
    except:
        pass
    return images
