# Chủ đề: Crawl dữ liệu báo điện tử
## I. Mở đầu
### 1. Giới thiệu đề tài

- Báo chí từ lâu luôn là một kênh thông tin quan trọng phản ánh mọi
vấn đề, sự việc trong xã hội. Và với sự phát triển của Internet và các thiết bị di động hiện nay,
báo điện tử đã trở thành một loại phương tiện truyền thông phổ biến, 
cho phép người dùng có thể truy cập và đọc các tin tức, thông tin
từ mọi nơi trên thế giới.
- Sở hữu nhiều lợi thế so với báo giấy truyền thống như: dễ dàng truy cập, 
nội dung đa dạng, cập nhật nhanh chóng và tính tương tác cao, báo điện tử phát triển khá nhanh
chóng và thay đổi thói quen đọc báo của không ít người đọc. Tuy nhiên, báo điện
tử cũng tồn tại nhiều mặt trái khi những nội dung không lành mạnh, độc hại có thể được
lan truyền nhanh chóng.
- Một số trang báo điện tử lớn tại Việt Nam có thể kể đến như: Vnexpress, 24h, Dân trí,
Zingnews, Báo thanh niên, v.v...
- Việc thu thập dữ liệu từ các báo điện tử có tác dụng quan trọng trong việc phân tích, đánh giá
và dự báo các xu hướng của thị trường, kinh tế và chính trị, xã hội. Cùng với đó
cũng có thể được sử dụng để phát hiện và theo dõi các thông tin sai lệch, tin tức giả và các nội 
dung độc hại khác.

### 2. Mục tiêu dự án

- Mục tiêu dự án là xây dựng chương trình có khả năng tự động thu thập dữ liệu
từ các trang báo điện tử lớn ở Việt Nam và thực hiện lưu trữ vào database.
- Danh sách các tờ báo mà dự án thực hiện thu thập dữ liệu:
  + 24h
  + Báo Chính phủ
  + Thời báo tài chính Việt Nam
  + Báo Công an nhân dân
  + Báo Dân trí
  + Báo Kiểm sát
  + Báo Lao động
  + Báo Người lao động
  + Báo Nhân dân
  + Báo Thanh niên
  + Báo Tuổi trẻ
  + Báo Vietnamnet
  + Báo Vnexpress
  + Báo Vov
  + Báo Vtv
  + Zingnews

### 3. Công nghệ sử dụng

- Python: Ngôn ngữ lập trình chính của dự án
- Scrapy: framework cho phép thu thập dữ liệu trên web và bóc tách dữ liệu
- XPath: ngôn ngữ truy vấn sử dụng để truy xuất và lấy dữ liệu từ các tài liệu XML hoặc HTML
- MongoDB: hệ quản trị cơ sở dữ liệu NoSQL, sử dụng để lưu trữ dữ liệu thu thập được.

## II. Thực hiện

### 1. Lập trình Spiders

- Spiders trong Scrapy là các lớp Python thực hiện nhiệm vụ truy cập, thu thập
và bóc tách dữ liệu từ các trang Web. 
- Mỗi trang báo của dự án sẽ được thu thập bởi một spider. Các spiders sẽ thực hiện
thu thập dữ liệu theo chiến lược bắt đầu từ trang chủ, sử dụng Xpath để lấy đường
link của các thư mục con và các bài báo, đi theo các đường link đó để bóc tách và lấy
về những dữ liệu được chỉ định.
- Mô hình cơ bản của một spider sẽ như sau:
    ```
    class News_spider(scrapy.Spider):
        name = 'spider_name'
        allowed_domains = ['domain_1', 'domain_2', ...]
        start_urls = ['home_page_link']
  
        def parse(self, response):
            topic_links = response.xpath('xpath_expression').getall()
                # follow link for link in topic_links
            article_links = response.xpath('xpath_expression').getall()
                # follow link for link in article_links
        ...
        ...
        def parse_article(self, response):
            # Code to extract data
    ```
  
### 2. Tạo pipelines để xử lý và lưu trữ dữ liệu

- Dữ liệu sau khi được lấy về từ các trang Web khác nhau thường có thể không đồng nhất,
không đúng định dạng mong muốn hoặc dư thừa các dữ liệu lặp lại, không cần thiết.
- Vì vậy, các dữ liệu lấy về bởi spiders sẽ được đưa qua pipelines để xử lý và thực hiện
lưu trữ.
- Trong dự án này, pipelines sẽ thực hiện các thao tác sau:

    |Tên|Chức năng|
    |----|----|
    |CreateDateToDatetime|Chuyển đổi ngày xuất bản từ kiểu string sang datetime|
    |ShortFormDateToDatetime|Chuyển đổi ngày xuất bản từ kiểu string sang datetime|
|   