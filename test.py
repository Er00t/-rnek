from selenium import webdriver

# Mevcut açık olan Chrome penceresini bulmak için aynı session'ı kullanmak
options = webdriver.ChromeOptions()
options.debugger_address = "localhost:9222"  # Bu portu Chrome'un debug modu için kullanılan port ile değiştirmeniz gerekebilir

# Chrome penceresini bulma ve mevcut oturumu kullanma
driver = webdriver.Chrome(options=options)

# Yeni sekmenin açılması
new_tab_script = "window.open('https://pocketoption.com/tr/cabinet/demo-quick-high-low/', 'new tab')"
driver.execute_script(new_tab_script)
