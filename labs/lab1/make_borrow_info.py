import random
from datetime import date, timedelta

reader_ID=['00000001','00000002','00000003','00000004','00000005','00000006','00000007','00000008','00000009','00000010','00000011','00000012','00000013','00000014','00000015','00000016','00000017','00000018','00000019','00000020','00000021','00000022','00000023','00000024','00000025']
book_ID=['00000001','00000002','00000003','10000000','10000001','10000002','10000003','10000004','10000005','10000007','10000008','10000009','10000010','10000011']

existed = []
borrow_times = []
borrow_info = []
start_year = 2020
end_year = 2023
# 随机生成每本书的借阅次数
for i in range(len(book_ID)):
    borrow_times.append(random.randint(0, 8))
# 为每本书随机生成借阅信息
for i in range(len(borrow_times)):
    busy_time = []
    existed = []
    for j in range(borrow_times[i]):
        reader = random.choice(reader_ID)
        while reader in existed:
            reader = random.choice(reader_ID)
        existed.append(reader)
        start_date = date(random.randint(start_year, end_year), random.randint(1, 12), random.randint(1, 28))
        end_date = start_date + timedelta(days=random.randint(1, 30))
        while any(start_date <= end <= end_date or start <= start_date <= end for start, end in busy_time):
            start_date = date(random.randint(start_year, end_year), random.randint(1, 12), random.randint(1, 28))
            end_date = start_date + timedelta(days=random.randint(1, 30))
        busy_time.append((start_date, end_date))
        borrow_info.append((book_ID[i], reader, start_date, end_date))
        
# 将borrow_info按end_date升序排序
borrow_info.sort(key=lambda x: x[3])
for book, reader, start_date, end_date in borrow_info:
    print(f'(\'{book}\',\'{reader}\',\'{start_date}\',\'{end_date}\'),')