import re

# from collections import Counter

data = "Dell Vostro 3520 i3 12th Gen  16GB RAM  512GB SSD  15.6 120Hz FHD Display Laptop Brand Dell Model Vostro 3520 Processor Intel Core i3 12th Generation 1215U 10M Cache 6 Cores 8 Threads Memory 16GB DDR4 RAM Storage 512GB NVMe SSD  Display 15.6 120Hz FHD Battery 3Cell Battery Color Carbon Black Warranty 1Year WarrantyBrand No Brand SKU 129017788NP1037011250 Ram Memory 16GB Operating System DOS Generation 12th CPU Cores Not Specified Storage Capacity 512GB Display Size 15.6 Inch Processor Intel Core i3"
data = data.lower()

data = data.split(" ")
count = {}

for word in data:
    if word in count:
        count[word] += 1
    else:
        count[word] = 1

print(count)
# print(Counter(data).keys())
# print(Counter(data).values())
