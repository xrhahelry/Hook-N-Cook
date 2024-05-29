def price_scraper():
    df = pd.read_csv("data/scraper/urls.csv")
    files = df["Filename"]
    links = df["Url"]
    today = date.today()

    for i, link in enumerate(links):
        if i < 884:
            continue
        if link in [
            "https://www.daraz.com.np/products/dell-precision-3430-sff-core-i7-8700-32ghz-32gb-ram-512gb-solid-state-drive-windows-11-pro-64bit-renewed-i129855105-s1037690646.html?search=1",
            "https://www.daraz.com.np/products/dell-vostro-3888-computer-set-i114454487-s1031087096.html?search=1",
            "https://www.daraz.com.np/products/dell-tiny-i5-6th-generation-8-gb-ram-256-ssd-with-mouse-keyboard-wifi-dongle-and-mouse-pad-i129272829-s1037294262.html?search=1",
        ]:
            continue

        filename = "data/prices/" + files[i]
        driver.get(link)
        try:
            try:
                actual_price = driver.find_element(
                    By.XPATH, '//*[@id="module_product_price_1"]/div/div/div/span[1]'
                ).text

                discount_price = driver.find_element(
                    By.XPATH, '//*[@id="module_product_price_1"]/div/div/span'
                ).text
            except:
                WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            '//*[@id="module_product_price_1"]/div/div/span',
                        )
                    )
                )
                actual_price = driver.find_element(
                    By.XPATH, '//*[@id="module_product_price_1"]/div/div/span'
                ).text

                discount_price = actual_price

            df = pd.DataFrame(
                [[today, actual_price, discount_price]],
                columns=["Date", "Actual Price", "Discount Price"],
            )
            df["Actual Price"] = (
                df["Actual Price"].str.replace("Rs. ", "").str.replace(",", "")
            )
            df["Discount Price"] = (
                df["Discount Price"].str.replace("Rs. ", "").str.replace(",", "")
            )
            print(i, filename)
        except:
            print(i, filename, link)
            pp = pd.read_csv(filename)
            df = pd.DataFrame(
                [[today, int(pp.iloc[-1, -2]), int(pp.iloc[-1, -1])]],
                columns=["Date", "Actual Price", "Discount Price"],
            )

        df.to_csv(filename, mode="a", header=not os.path.exists(filename), index=False)
