
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time 
from urlparse import urljoin


browser = webdriver.Firefox()

profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2) 
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', '/home/tmp')
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'video/mp4')

from retry import retry
from timeout_decorator import timeout, TimeoutError
from selenium.common.exceptions import TimeoutException  

@retry(TimeoutError, tries=3)
@timeout(40)
def get_with_retry(browser, url):
    browser.get(url)




for i in range (0,99):
	browser.maximize_window()

	try:
		get_with_retry(browser, "http://url/g/355/player-1-"+str(i)+".html")

		time.sleep(3)

		iframes = browser.find_elements(By.XPATH,'.//iframe')
	
		for frame in iframes:
			if(frame.get_attribute('id')=='cciframe'):
				browser.switch_to.frame(frame)
				iframes2 = browser.find_elements(By.XPATH,'.//iframe')
				for frame1 in iframes2:
					if(frame1.get_attribute('id')=='ifr'):
						src = frame1.get_attribute('src')

	
		url = urljoin('', src)
		get_with_retry(browser, url)
		time.sleep(3)

		iframes = browser.find_element(By.XPATH,'.//iframe')

		browser.switch_to.frame(iframes)

		time.sleep(3)
		link = browser.find_element(By.XPATH, '//video');

		browser.maximize_window()	

		ActionChains(browser).context_click(link).move_by_offset(87, 217).click().perform();	
		time.sleep(30)

	
	finally:
		time.sleep(3)
