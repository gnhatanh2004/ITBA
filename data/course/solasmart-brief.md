# SolasMart – tóm tắt case study

Tóm từ 13 file trong `tai-lieu/solasmart/` (file "Quy trinh ban hang tai quay.docx" ở ngoài giống hệt bản trong zip). Dùng cho case study, bài tập và câu tình huống. Số liệu, tên người, tên NCC bên dưới là của tài liệu gốc.

## 1. Bối cảnh

- Siêu thị bán lẻ **SolasMart**, cơ sở **Hà Đông**. Có "Siêu thị chính", "Cửa hàng A" (nhận hàng xuất từ kho) và **kho tổng** (file Excel gọi là "kho chính").
- Hai kênh bán: **tại quầy** (máy POS, barcode) và **online** (7 kênh: Zalo OA, Zalo cá nhân, Facebook Fanpage, điện thoại, bình luận bài đăng, Messenger, SMS).
- **Chưa có hệ thống quản lý**: đơn online nhập tay vào Excel, chuyển đơn cho kho qua Zalo nhóm, kiểm tồn thủ công; kho dùng phiếu giấy và Excel.
- Ca làm: ca sáng, ca chiều, ca tối (báo cáo ghi "Ca 2 (14h–22h)"). Chấm công bằng máy vân tay.

## 2. Bộ phận và vai trò

| Bộ phận / vai trò | Việc chính | Xuất hiện ở |
|---|---|---|
| Ban Giám đốc / Quản lý siêu thị | Duyệt tuyển dụng, yêu cầu kiểm kê đột xuất, ký phiếu xuất kho | QĐ nhân sự, QĐ kho, Phiếu xuất |
| Trưởng ca / Quản lý quầy | Xác nhận giá sai, kiểm tra đơn hoàn/hủy/giao lỗi cuối ngày | QT tại quầy, QT online |
| Thu ngân | Quét mã, thu tiền, in hóa đơn; chịu trách nhiệm tiền trong két | QT tại quầy, QĐ vận hành |
| Nhân viên hỗ trợ quầy | Đổi sản phẩm thiếu tem, cân hàng, mang sản phẩm thay | QT tại quầy |
| Nhân viên CSKH (trực page) | Nhận đơn online, kiểm tồn, báo giá, nhập Excel, chuyển kho | QT online |
| Quản lý kho / Thủ kho / Phụ kho / NV kho | Nhận hàng, kiểm hàng, lập phiếu, soạn hàng, kiểm kê | QĐ kho, QT nhập kho, các phiếu |
| Nhân viên giao hàng (shipper nội bộ) | Giao hàng, thu COD | QT online |
| Kế toán | Xử lý chứng từ lệch, đối soát COD, ký phiếu kho, kiểm kê | QT nhập kho, QT online, các phiếu |
| Bảo vệ, kỹ thuật, bán hàng | Theo Quy định vận hành | QĐ vận hành |
| Bên ngoài: Khách hàng, Nhà cung cấp, Ngân hàng | Mua hàng; giao hàng + hóa đơn; xác nhận chuyển khoản | Các quy trình |

Nhà cung cấp trong Excel: GreenFarm Supplies (rau củ), FreshMeat Co. (thịt tươi), HomeCare VN (gia dụng).

## 3. Quy trình

### 3.1. Bán hàng tại quầy (8 bước)
Mục đích: tính tiền chính xác, nhanh; giảm thời gian chờ; kiểm soát tồn kho; thu chi minh bạch.

| Bước | Việc chính | Ngoại lệ → xử lý |
|---|---|---|
| 1 Khách đưa hàng lên quầy | Đặt lên băng chuyền/quầy | Thiếu tem giá → NV hỗ trợ đổi, hết thì hỏi kho; Hàng hỏng → hỏi khách đổi hay bỏ |
| 2 Bắt đầu phiên | Chào khách, bấm "Start Transaction", kiểm số lượng | POS chưa đăng nhập → login lại |
| 3 Quét mã | POS hiện tên, giá, số lượng, khuyến mãi; hàng cân phải có tem barcode | Chưa cân → NV hỗ trợ cân; Barcode không đọc → nhập tay; Sai giá → gọi trưởng ca; POS treo → đổi máy/reset |
| 4 Xác nhận giỏ | Đọc tổng tiền, tổng số lượng; khách xem màn hình | Bỏ bớt → sửa số lượng; Đổi sản phẩm → NV mang hàng mới |
| 5 Chọn phương thức | Tiền mặt, thẻ Visa/Master, chuyển khoản, hoặc kết hợp | Máy thẻ treo → QR/máy khác; Không đủ tiền → hủy hoặc đổi phương thức |
| 6 Thu tiền | Tiền mặt: đếm, trả thừa. Thẻ: chạm NFC, khách tự nhập PIN, in slip. Chuyển khoản: nhập số tiền, khách quét QR, chờ ngân hàng | Giao dịch thất bại → kiểm lại/đổi phương thức |
| 7 In hóa đơn, giao hàng | In hóa đơn, đưa túi hàng, chào khách | Hết giấy → thay; Hóa đơn mờ → in lại |
| 8 Kết thúc phiên | (tài liệu không mô tả) | – |

### 3.2. Bán hàng online (10 bước)
1. Khách gửi yêu cầu qua 7 kênh: sản phẩm, số lượng, địa chỉ, SĐT, giờ nhận mong muốn.
2. CSKH kiểm tồn thủ công (hỏi kho), giá, khuyến mãi; gợi ý thay thế. Ngoại lệ: kho trả lời chậm; hết hàng mà page chưa cập nhật.
3. Báo giá: danh sách, giá, tổng tiền, phí ship, thời gian giao. Khách không đồng ý → hủy hoặc tư vấn tiếp.
4. Nhập đơn vào Excel: mã đơn, tên khách, SĐT, địa chỉ, kênh đặt, danh sách sản phẩm, tổng tiền, ghi chú.
5. Gửi đơn cho kho qua Zalo nhóm; kho báo lại phát sinh.
6. Kho soạn hàng: lấy hàng, kiểm hạn dùng, đóng gói, báo trạng thái. Thiếu hàng → báo CSKH xin xác nhận khách.
7. Bàn giao shipper nội bộ (hàng, địa chỉ, SĐT).
8. Giao: gọi trước, giao đúng địa chỉ, thu COD. Khách không nghe máy → nhờ CSKH, **sau 15 phút** không liên lạc được thì hàng về kho; sai địa chỉ → giao lại, báo CSKH; đổi giờ, hủy đột xuất, không nhận → báo CSKH, hàng về kho khi cần.
9. Hoàn tất: shipper báo CSKH, nộp COD; CSKH xác nhận, cập nhật Excel, nhắn cảm ơn.
10. Cuối ngày: CSKH tổng hợp đơn; kho tính lại tồn; kế toán đối soát COD; trưởng ca/quản lý kiểm đơn hoàn, hủy, giao lỗi.

### 3.3. Nhập kho tổng (7 bước)
1. Xe NCC đến; NV kho kiểm Delivery Note và PO. 2. Kiểm chứng từ (Invoice, phiếu giao hàng); không khớp → báo Kế toán. 3. Dỡ hàng, kiểm số lượng, chất lượng, hạn dùng, nhiệt độ (đông lạnh), mã/barcode; hàng lỗi → không nhận. 4. Đối chiếu số lượng đặt (PO) – NCC giao – thực nhận; lệch → Kế toán quyết nhập hay từ chối. 5. Lập Phiếu nhập kho (2 bản: lưu kho, gửi kế toán). 6. Nhập vào Excel. 7. Gắn nhãn, xếp theo khu (tươi sống, đông lạnh, đóng gói).

## 4. Biểu mẫu và báo cáo

| Biểu mẫu | Trường chính | Ký |
|---|---|---|
| Phiếu nhập kho (mã NK20201020-1) | STT, tên hàng, mã SP, ĐVT, số lượng, đơn giá, thành tiền, hạn dùng, tình trạng bao bì; tổng SL, tổng tiền, NCC, số chứng từ NCC | Người giao hàng, Quản lý kho, Kế toán |
| Phiếu xuất kho (XK20201020-1) | Bộ phận yêu cầu, mục đích xuất; tên hàng, mã SP, ĐVT, SL yêu cầu, SL xuất, ghi chú | Quản lý kho, Quản lý siêu thị, Kế toán |
| Phiếu kiểm kê kho (KK20201020) | Thành phần kiểm kê; tồn hệ thống, tồn thực tế, chênh lệch, lý do; kết luận tăng/giảm | Quản lý kho, Kế toán |
| Phiếu hủy hàng (HH20201020) | Lý do (hết hạn, bao bì hỏng, biến chất, lỗi NCC, khác); SL, hạn dùng, giá trị hủy | Người đề nghị, Thủ kho, Kế toán |
| Báo cáo cuối ca tại quầy | Ngày, cơ sở, ca, thu ngân; doanh thu theo hình thức (tiền mặt 85 đơn/42,5tr; thẻ 35/21,8tr; QR 12/9,2tr; tổng 132/73,5tr); sự cố; tiền mặt cuối ca (thu 42,5tr + ứng đầu ca 2tr = 44,5tr, lệch 0) | – |
| Báo cáo cuối ca online | Đơn theo trạng thái (hoàn tất 48, đang giao 10, hủy 5, chờ xác nhận 3; tổng 66 / 43,9tr); phí ship (thu 3,8tr, chi 3,2tr, +0,6tr); sự cố (đổi ý 2, hết hàng 1, không liên lạc 1, sai địa chỉ 1) | – |
| Excel "Danh sách sản phẩm trong kho chính" | 5 sheet: Tổng hợp tồn kho, Nhập kho (PNK-xxxx), Xuất kho (PXK-xxxx), Danh mục hàng (mã, nhóm, đơn vị, giá nhập chuẩn, hạn dùng theo ngày, NCC chính), Nhà cung cấp | – |

## 5. Quy định chính (business rules)

**Vận hành**: có mặt trước giờ làm 15 phút; không tự đổi ca; đồng phục, bảng tên; chào khách 3 bước (chào – hỗ trợ – cảm ơn); vệ sinh trước và sau ca; nhãn hàng hướng ra ngoài, kệ trống không quá 20%; kiểm hạn dùng mỗi ca; thu ngân chịu trách nhiệm tiền két, không cho người khác dùng tài khoản/mã thu ngân; tiền thừa/thiếu cuối ca lập biên bản; hàng nhập phải có chứng từ, không xuất khi chưa có phiếu hợp lệ; sự cố (điện nước, cháy nổ, mất hàng, khiếu nại, POS) báo quản lý ca ngay, không tự cam kết bồi thường; không tiết lộ giá vốn, doanh thu, dữ liệu khách; vi phạm: nhắc nhở → biên bản → kỷ luật.

**Nhân sự**: tuyển theo nhu cầu được duyệt, mỗi vị trí có JD, yêu cầu năng lực, mức lương; nhân sự mới ký HĐ thử việc/CTV, nộp hồ sơ, đào tạo định hướng; tự chấm công vân tay; làm thêm cần quản lý đồng ý; phép báo trước 3 ngày, nghỉ cá nhân 1 ngày, ốm đột xuất báo trước 2 tiếng, ốm ≥ 2 ngày cần giấy y tế; nghỉ việc báo trước 3 ngày (thử việc) / 30 ngày (chính thức), bàn giao tài sản, thu hồi tài khoản, thẻ, quyền truy cập; kỷ luật 4 mức (lời → biên bản → cảnh cáo văn bản → xem xét chấm dứt HĐ), lỗi nghiêm trọng xử lý ngay; KPI theo bộ phận (thu ngân: tốc độ, sai sót quỹ, thái độ; bán hàng: doanh số, trưng bày, tồn kho; kho: chính xác nhập – xuất, thời gian xử lý).

**Kho**: bàn giao ca có chữ ký 2 bên; nhập phải có phiếu/chứng từ, từ chối hàng hỏng, sai chủng loại, thiếu thông tin, gần hết hạn; chỉ xuất khi có phiếu xuất hợp lệ và phê duyệt, cập nhật tồn ngay; kiểm kê 1 lần/tháng (đột xuất khi nghi sai lệch), tối thiểu thủ kho + kế toán, báo chênh lệch trong 24h; nhập trước xuất trước; hàng dễ cháy khu riêng; vệ sinh kho 2 lần/ngày, kiểm nhiệt độ kho lạnh ≥ 2 lần/ngày, diệt côn trùng 1 lần/quý; hàng hủy cần phiếu đề nghị hủy, biên bản, ảnh; kho khóa khi không có người, camera 24/7; chứng từ lưu theo tháng, tối thiểu 12 tháng; gian lận → chấm dứt HĐ, sắp xếp sai: lần 3 chấm dứt HĐ.

## 6. Vấn đề phát hiện khi phân tích tài liệu (dùng cho bài tập)

- **Pain point**: kiểm tồn thủ công, kho trả lời chậm; nhập đơn tay vào Excel; chuyển đơn qua Zalo; page chưa cập nhật hàng hết; 7 kênh nhận đơn rời rạc.
- **Mâu thuẫn**: mức kỷ luật 3 mức (vận hành) vs 4 mức (nhân sự) vs lần 3 chấm dứt (kho); hai báo cáo cuối ca cùng ca, cùng 2 người nhưng một bản là "thu ngân", bản kia là "CSKH"; mã chứng từ NK20201020-1 (phiếu) vs PNK-0001 (Excel); ghi hủy bằng Phiếu hủy hàng vs dòng "Xuất hủy" PXK-0003 trong Excel.
- **Số liệu sai**: Phiếu hủy dòng 1 ghi 9.000.000 (1.000 × 90.000 = 90.000.000), tổng 165.000.000 ≠ 84.000.000; Excel PNK-0003 tổng 720 vs thành tiền 720.000; đơn giá xuất (30, 50, 25) khác đơn vị với đơn giá nhập; phiếu kiểm kê lệch 100 nhưng lý do "Nguyên vẹn".
- **Lỗ hổng**: bước 8 bán tại quầy trống; không bước nào trừ tồn kho khi bán tại quầy; "gần hết hạn" chưa có ngưỡng; phiếu nhập không có số PO; phiếu xuất không có chữ ký người nhận; bước 6 nhập kho chỉ ghi "nhập vào excel".
- **Trùng lặp / lỗi trình bày**: ô "Hết hạn" lặp 2 lần trên phiếu hủy; QĐ kho đánh số mục trùng (hai mục 6, 9, 10); phiếu giao hàng kiểm ở cả bước 1 và 2 nhập kho; mẫu phiếu năm 2020, Excel ghi ngày yyyy-mm-dd trái ghi chú dd/mm/yyyy.
