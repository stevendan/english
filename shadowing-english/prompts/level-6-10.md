# Nhiệm vụ: Tạo khoá Level 6 → Level 10 cho Shadowing English

## 1. Bối cảnh
Thư mục `shadowing-english/` là bộ luyện shadowing tiếng Anh cho người Việt. Mỗi level có 12 unit, mỗi unit nằm trong `Level N/unit M/`:
- `unit M.md`: nội dung bài (6 khối, giống hệt các level khác)
- `unit M.pdf`: 1 trang A4, sinh bằng `tools/build_unit_pdf.py`
- 7 file mp3: sinh bằng `tools/build_unit_audio.py`
Trang `index.html` đọc `content.js` (sinh bằng `tools/build_manifest.py`).

Đã có Level 1–5 (A1 → A2+/B1-). Level 6–10 đưa người học từ B1 lên C1.
**Giữ nguyên bố cục unit**: 6 khối, PDF 1 trang. Bài dài thì tool tự thu cỡ chữ (8.8 → tối thiểu 7.8pt), không thêm trang.

## 2. File mẫu cần đọc trước
- `Level 1/unit 1/unit 1.md`, `Level 3/unit 1/unit 1.md`, `Level 3/unit 4/unit 4.md`: định dạng chuẩn, giọng văn tiếng Việt.
- `Level 10/unit 1/unit 1.md`: mẫu cho level cao (10 lượt, thành ngữ, ghi chú giọng Anh).
- `tools/build_unit_pdf.py`: `parse_unit`, `check_unit`, `LEVEL_RULES`.

## 3. Trình độ và luật kích thước (đã cài trong LEVEL_RULES)
| Level | CEFR | Lượt | Số từ hội thoại | Từ / lượt | Ví dụ ngữ pháp tối đa | Option drill | Tốc độ audio | Giọng |
|---|---|---|---|---|---|---|---|---|
| 6 | B1 | 8 | 70–85 | 3–16 | 10 từ | 1–5 từ | -5% | Mỹ |
| 7 | B1+ | 8 | 78–92 | 3–18 | 10 từ | 1–6 từ | 0% | Mỹ |
| 8 | B2 | 8 | 85–100 | 2–20 | 11 từ | 1–6 từ | 0% | Mỹ + Anh |
| 9 | B2+ | 10 | 92–106 | 2–20 | 12 từ | 1–6 từ | 0% | Mỹ + Anh + Úc |
| 10 | C1 | 10 | 100–115 | 2–22 | 12 từ | 1–6 từ | +5% | Mỹ + Anh + Úc + Ireland + NZ |

Mọi level: đúng 2 khối Grammar Focus (mỗi khối 2–3 ví dụ), đúng 2 Study Notes, 3 câu Speak Like a Native, 3 câu Substitution Drill (mỗi câu 3 option), 3 chỗ trống Role Play, in đậm điểm ngữ pháp ≥ 3 lần.

Trọng tâm Speak Like a Native theo level:
- L6: dạng yếu của have/has/been, rút gọn (I've, she'd), nối âm, nuốt âm /t/ /d/.
- L7: would've / could've / should've, I'd (had / would), nuốt phụ âm trong cụm (last week → “las-wik”), đồng hoá âm.
- L8: should have → “shoulda”, trọng âm tương phản, ngữ điệu lịch sự (lên-xuống), ngắt cụm trong câu dài.
- L9: nhịp và trọng âm câu, ngữ điệu mỉa mai, rút gọn khi nói nhanh (gonna, kinda, dunno), ngữ điệu của discourse markers.
- L10: nối âm ở tốc độ thật, đặc điểm giọng Anh / Úc / Ireland / NZ, nhấn và ngữ điệu tạo sắc thái.

Giọng đọc Level 8–10 (gán theo thứ tự unit, người nữ / người nam):
- L8: u1, u5, u9: nữ Anh, nam Mỹ · u2, u6, u10: nữ Mỹ, nam Anh · u3, u7, u11: nữ Anh, nam Mỹ · u4, u8, u12: nữ Mỹ, nam Anh.
- L9: u1, u7: nữ Anh, nam Mỹ · u2, u8: nữ Mỹ, nam Úc · u3, u9: nữ Úc, nam Mỹ · u4, u10: nữ Mỹ, nam Anh · u5, u11: nữ Anh, nam Mỹ · u6, u12: nữ Mỹ, nam Anh.
- L10: u1, u7: nữ Ireland, nam Anh · u2, u8: nữ Mỹ, nam New Zealand · u3, u9: nữ Úc, nam Mỹ · u4, u10: nữ Anh, nam Ireland · u5, u11: nữ New Zealand, nam Mỹ · u6, u12: nữ Mỹ, nam Úc.
Có thể cho nhân vật dùng từ vựng hợp với giọng (flat, rubbish… cho người Anh), và ghi chú đặc điểm giọng trong Speak Like a Native khi phù hợp.

## 4. Syllabus (nhân vật đã cố định; tên nữ đã có trong FEMALE_NAMES)
### Level 6 (B1)
1. Hiện tại hoàn thành + for / since: Hazel & Owen tình cờ gặp lại nhau sau nhiều năm.
2. Hiện tại hoàn thành vs quá khứ đơn: phỏng vấn xin việc, Gavin (người phỏng vấn) & Thao (ứng viên, B).
3. used to / didn't use to: Hieu dẫn Nora thăm khu phố tuổi thơ ở Sài Gòn.
4. Câu điều kiện loại 2: Dennis & Erin mơ mộng giờ nghỉ trưa (nếu trúng xổ số…).
5. remember / forget / stop / try + to V hay V-ing: Chloe & Patrick kiểm tra đồ trước khi đi du lịch.
6. Mệnh đề quan hệ xác định who / which / that / where: Victor & Vivian ở tiệc cưới, hỏi khách là ai.
7. Bị động hiện tại / quá khứ: Paula (du khách) & Ivan (hướng dẫn viên, B) thăm một toà nhà cổ.
8. Câu tường thuật (said / told, lùi thì): Toan & Huong chuyển lời nhắn của sếp.
9. Suy đoán hiện tại (must / might / could / can't be): Monica & Stefan và gói hàng bí ẩn trước cửa.
10. Câu hỏi đuôi: Kyle & Sandra nói chuyện xã giao ở bếp văn phòng mới.
11. Phrasal verbs thông dụng (look after, run out of, put away, turn off…): Wendy dặn Bruno trông nhà, trông thú cưng.
12. Tương lai: will (quyết định tức thì) / be going to / hiện tại tiếp diễn: Harold & Gloria bị huỷ chuyến bay ở sân bay.

### Level 7 (B1+)
1. Hiện tại hoàn thành tiếp diễn: Bella & Aaron (“Trông bạn mệt quá, nãy giờ làm gì vậy?”), chuyển nhà.
2. Quá khứ hoàn thành: Colin & Jade kể một ngày đi lại tồi tệ.
3. Câu điều kiện loại 3: Leah & Derek lỡ mua vé hoà nhạc.
4. wish + quá khứ đơn / quá khứ hoàn thành: Elliot & Molly căng thẳng mùa thi.
5. Tường thuật câu hỏi và lời yêu cầu (asked if / asked me to): Felix kể cho Tessa về buổi phỏng vấn.
6. Bị động với modal và hiện tại hoàn thành: Gordon & Carmen rà danh sách chuẩn bị sự kiện công ty.
7. Mệnh đề quan hệ không xác định, whose, where: Giang dẫn Ian tham quan Huế.
8. have / get something done: Tung & Irene sửa sang mọi thứ trước bữa tiệc.
9. Suy đoán quá khứ (must have / might have / can't have): Joanna & Jonah lần lại chiếc ví bị mất.
10. Tương lai tiếp diễn / tương lai hoàn thành: Neil & Yvonne, hạn chót dự án và kỳ nghỉ sắp tới.
11. although / even though / despite / however: Rita & Wesley chọn giữa hai lời mời làm việc.
12. Phrasal verbs tách được / không tách được (put up with, sort out, turn down, look into…): Chau & Hoang và người hàng xóm ồn ào.

### Level 8 (B2)
1. Câu điều kiện hỗn hợp: Abigail & Adrian nói về những ngã rẽ sự nghiệp.
2. should have / could have / shouldn't have: Caleb & Bridget sau buổi thuyết trình không suôn sẻ.
3. wish + would / if only: Daisy & Dominic phàn nàn thói quen khó chịu của bạn cùng nhà.
4. Nêu ý kiến, đồng ý / phản đối lịch sự: Edward & Eleanor họp nhóm về làm việc từ xa.
5. Nói giảm, nói tránh (hedging): Freya góp ý kế hoạch mở quán cà phê của Khai.
6. Câu chẻ để nhấn mạnh, làm rõ (What I meant was… / It was… who…): Frank & Heidi giải toả hiểu lầm.
7. Các thì kể chuyện (quá khứ đơn / tiếp diễn / hoàn thành): Hong kể cho George một sự cố khi du lịch.
8. Thương lượng (What if…? / provided that / meet halfway): Lam & Ingrid thương lượng giá thuê nhà hoặc phí làm việc tự do.
9. Small talk, giữ mạch câu chuyện: Margot & Isaac ở sự kiện networking.
10. Thành ngữ hằng ngày (call it a day, under the weather, on the same page…): Jerome & Priya cuối một tuần làm việc dài.
11. Phàn nàn khéo léo: Selena (khách) & Liam (lễ tân, B) về sự cố phòng khách sạn.
12. Phrasal verbs trong công việc (follow up, carry out, put off, come up with…): Marco & Nhi khởi động dự án.

### Level 9 (B2+)
1. Đảo ngữ nhấn mạnh (Never have I… / Not only… but also…): Amber & Alfie khen một nhà hàng tuyệt vời.
2. Mệnh đề phân từ (Having…, -ing, Exhausted, …): Barry & Beatrice kể chuyến leo núi.
3. Bị động để đưa tin, giữ khoảng cách (It's said that… / is believed to…): Cora & Conor bàn tin đồn công ty bị thâu tóm.
4. Tỉnh lược và thay thế (I hope so / I'd love to / So do I / Neither have I): Declan & Delia hẹn hò kế hoạch cuối tuần.
5. Discourse markers (Anyway, Mind you, Speaking of which, As I was saying): Esther & Eddie hàn huyên bên ly cà phê.
6. Vague language (sort of, and stuff, or something, a bunch of, -ish): Frederick & Flora tả một bữa tiệc.
7. Ngắt lời và giữ lượt nói: Vy & Trung lên kế hoạch chuyến đi nhóm.
8. Thuyết phục: Graham rủ Gemma chạy bán marathon.
9. Collocations với make / do / take / have: Harriet khuyên Vu trước một quyết định lớn.
10. Hài hước, mỉa mai, nói giảm: Hamish & Imogen trong kỳ nghỉ mưa suốt.
11. Thành ngữ cảm xúc (over the moon, on edge, fed up, a weight off my shoulders…): Thu & Kieran chờ kết quả thi.
12. Kể chuyện cười có nhịp (You'll never guess…, So there I am…, Long story short…): Rupert & Lorna.

### Level 10 (C1)
1. It's high time + quá khứ / would rather + quá khứ: Annabel & Alistair bàn việc nhà (ĐÃ CÓ, là bài mẫu).
2. Modal nâng cao (be bound to / be supposed to / needn't have): Benedict & Celeste lo chuẩn bị đám cưới.
3. Nhượng bộ (Granted…, Admittedly…, That said…, Even so…): Danielle & Cyrus tranh luận sống ở thành phố hay nông thôn.
4. Ngoại giao khi bất đồng (I take your point / Where I'm coming from is…): Damian & Evelyn bất đồng về hạn chót.
5. Góp ý khó nói ở chỗ làm: Felicity (quản lý) & Elias (nhân viên, B).
6. Tranh luận chủ đề trừu tượng (I'd argue that… / On the flip side… / It boils down to…): Fergus & Georgia bàn về AI và việc làm.
7. Văn nói thân mật, tiếng lóng (gonna, kinda, no worries, I'm beat…): Ngan & Phuc thư giãn sau giờ làm.
8. Thành ngữ và phrasal verbs tốc độ thật (back to square one, the ball's in their court…): Gareth & Helena bàn tin tái cơ cấu công ty.
9. Kể chuyện có tường thuật suy nghĩ và tạo hồi hộp (So there I was… / I thought to myself…): Juliet & Thang.
10. Đùa qua lại (banter, teasing): Julian & Lydia, chuyện nấu ăn hoặc đội bóng.
11. Giải thích phong tục (Tết và Giáng sinh): Quynh giải thích cho Lionel.
12. Biến thể tiếng Anh: Miranda (Mỹ) & Nathan (Úc), arvo, brekkie, heaps, fortnight…

## 5. Định dạng (bám sát mẫu, các lỗi hay gặp)
- `[HEADER] unit M — CDx` với x = (M-1)//4 + 1. Track: a = 7·((M-1)%4) + 1; Conversation “track a, a+2, a+3”; Speak “track a+1”; Role Play “track a+5”; Drill “track a+6”.
- Conversation: dòng đầu là câu bối cảnh tiếng Anh (không chứa dấu “:”); sau đó “Tên: lời thoại”, luân phiên 2 nhân vật. Người nói đầu tiên là A, người thứ hai là B (người học đóng vai B).
- Đếm từ: mỗi cụm cách nhau bởi dấu cách và có chữ/số là 1 từ (I'm, washing-up = 1 từ).
- Speak Like a Native: câu phải là chuỗi con NGUYÊN VĂN (phân biệt hoa thường) của một lời thoại; nên lấy trọn một câu bắt đầu bằng chữ hoa. Nhãn smooth / linking / change / weak / strong; cụm trong “…” (ngoặc kép cong) phải có trong câu, dùng ‿ để đánh dấu nối âm. Phần giải thích trong ngoặc đơn không được đặt trong “…” những từ có trong câu (vì sẽ bị tô màu), ví dụ viết (t → d nhẹ), (mất âm t). Mỗi ghi chú tối đa ~30 từ; [MẸO PHÁT ÂM] 3–4 dòng ngắn.
- Study Notes: đúng 2 mục: **câu tiếng Anh** / nghĩa tiếng Việt / giải thích / “Cách nói tương đương: …”. Nên chọn thành ngữ, cụm từ hay trong hội thoại.
- Grammar Focus: đúng 2 khối, mỗi khối: dòng tiêu đề / MỘT dòng giải thích tiếng Việt (≤ ~35 từ) / 2–3 ví dụ có [[từ khoá]]. Ví dụ không chép từ hội thoại; câu hỏi – trả lời ngăn bằng “ – ”.
- Role Play: chép lại hội thoại với A/B; đúng 3 chỗ trống `________` (8 dấu gạch dưới), chỉ ở dòng của B. Điền lần lượt các cụm gốc của drill vào thì phải ra đúng nguyên văn lời thoại.
- Substitution Drill: 3 câu, mỗi câu là chuỗi con nguyên văn từ lời của B; phần thay thế bọc `__…__`; thứ tự drill = thứ tự chỗ trống trong Role Play; 3 option a/b/c cùng loại từ, tự nhiên, ưu tiên luyện điểm ngữ pháp của bài.
- Viết số bằng chữ (three thirty, two hundred dollars), không dùng ký hiệu &, /, emoji; tránh “Hmm”, “Ugh” (TTS đọc lạ); dùng dấu ' thẳng trong tiếng Anh.

## 6. Yêu cầu chất lượng
- Tiếng Anh tự nhiên như người bản xứ có học nói hằng ngày, đúng trình độ CEFR của level; hội thoại có phản ứng, hỏi lại, cảm xúc, không phải câu sách giáo khoa.
- Điểm ngữ pháp / chức năng xuất hiện tự nhiên ≥ 3 lần (in đậm).
- Giải thích tiếng Việt ngắn, chính xác, cùng giọng văn với Level 1–3; phiên âm gần đúng bằng âm tiết tiếng Việt trong “…”, IPA khi cần.
- Ghi chú phát âm phải đúng ngữ âm (kiểm tra lại từng ý).
- Mỗi unit một tình huống riêng, không lặp tình huống của Level 1–5 hay unit khác; không dùng tên thương hiệu, doanh nghiệp có thật.

## 7. Quy trình
1. Viết từng unit → `PYTHONIOENCODING=utf-8 python tools/build_unit_pdf.py "Level N/unit M/unit M.md" --check` (báo cả luật lẫn cỡ chữ khi vừa 1 trang) → sửa đến khi OK.
2. Xong 12 unit: chạy `--check` cho cả level và script kiểm tra nhãn / font chữ, rồi tự đánh giá lại từng unit theo mục 6 và sửa.
3. Sinh PDF: `python tools/build_unit_pdf.py "Level N"`; audio: `python tools/build_unit_audio.py "Level N"`; cuối cùng `python tools/build_manifest.py`.

## 8. Ghi chú sau khi tạo (khác so với đặc tả ở trên)
- Đổi vai A/B để người học (B) được nói mẫu câu trọng tâm: L7 u5 (Felix là B), L7 u7 (Giang là B, người học đóng vai hướng dẫn viên ở Huế), L8 u5–u8 (Freya, Frank, Hong, Lam là B), L10 u11 (Quynh là B, giải thích Tết).
- Mỗi level được viết, tự soát lại, rồi được một lượt phản biện độc lập sửa: độ tự nhiên, lỗi IPA và ghi chú phát âm, option drill sai ngữ pháp, Study Notes trùng giữa các level.
- Cỡ chữ PDF tự co theo độ dài: L6 8.4–8.8pt, L7 8.2–8.4pt, L8 7.8–8.8pt, L9 8.0–8.6pt, L10 7.8–8.2pt; tất cả vẫn 1 trang, cùng bố cục.
- Lời thoại không dùng viết tắt có dấu chấm (Mr., Dr., a.m.) vì tool audio tách câu ở dấu “. ”.
- Ghi chú về giọng Anh / Úc / Ireland / NZ là đặc điểm chuẩn, viết kèm “thường / hay”; nên nghe lại audio để chắc giọng TTS thể hiện đúng.
- TTS giọng Mỹ đọc “Hue” như từ tiếng Anh “hue” (L7 u7, chỉ ở câu bối cảnh).
