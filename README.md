# Ba Cây POS

Hệ thống quản lý tồn kho và đơn hàng cho chuỗi cà phê Ba Cây (6 cửa hàng).

## Chạy

```
python server.py
```

Mở http://localhost:8080

## Tính năng

- Bán hàng tại quầy, trừ tồn kho tự động
- Quản lý tồn kho theo từng cửa hàng
- Cảnh báo sắp hết hàng
- Báo cáo doanh thu theo cửa hàng và theo ngày
- Trang menu cho khách

## Ghi chú

Tồn kho được trừ ngay khi tạo đơn. Nếu cần sửa tồn kho thì vào trang kiểm kê.

Chạy test: `python tests/test_orders.py`

Ghi chú: kiểm tra lại ngưỡng cảnh báo sắp hết hàng.
