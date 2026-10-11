# Nhiệm vụ: Tạo khoá Level 2 và Level 3 cho Shadowing English

## 1. Bối cảnh
Thư mục `shadowing-english/` là bộ luyện shadowing tiếng Anh cho người Việt, mô phỏng sách
"Speak Up English Enhanced". Mỗi level có 12 unit, mỗi unit nằm trong `Level N/unit M/` gồm:
- `unit M.md`  — nội dung bài (template 6 khối)
- `unit M.pdf` — tài liệu 1 trang A4, sinh bằng `tools/build_unit_pdf.py`
- 7 file mp3   — sinh bằng `tools/build_unit_audio.py` (edge-tts)
Trang `index.html` đọc dữ liệu từ `content.js`, sinh bằng `tools/build_manifest.py`.

Hiện có: Level 1 (A1, do mình tạo), Level 4 (A2) và Level 5 (A2+/B1) (chép từ sách).
Cần tạo: Level 2 (A1+) và Level 3 (A2-) để người học đi mượt từ Level 1 lên Level 4.

## 2. Đọc trước khi làm (bắt buộc)
- `Level 1/unit 1/unit 1.md` và 2–3 unit Level 1 khác → MẪU ĐỊNH DẠNG CHUẨN, viết giống hệt cách
  trình bày này (khối Grammar Focus có dòng tiêu đề, dòng giải thích, rồi ví dụ).
- 3–4 unit Level 4 và Level 5 → để cảm nhận độ khó "đích" mà Level 3 phải tiến gần tới.
- `tools/build_unit_pdf.py` (parse_unit, check_unit, markup), `tools/build_unit_audio.py`
  (FEMALE_NAMES, cách gán giọng, B = người nói thứ 2), `tools/build_manifest.py`.

## 3. Trình độ mục tiêu
| | Level 1 (có) | Level 2 (tạo) | Level 3 (tạo) | Level 4 (có) |
|---|---|---|---|---|
| CEFR | A1 | A1+ | A2- | A2 |
| Số lượt thoại | 4 | 4 | 6 | 6 |
| Số từ mỗi lượt | 3–6 | 4–10 | 4–12 | tới ~15 |
| Tổng số từ hội thoại | 20–30 | 30–40 | 36–48 | 42–57 |
| Số khối Grammar Focus | 1 | 1–2 | 2 | 2–3 |
| Ví dụ ngữ pháp tối đa | 7 từ | 8 từ | 9 từ | – |
| Option Substitution Drill | 1–3 từ | 1–4 từ | 1–5 từ | – |

- Level 2: câu đơn + câu ghép ngắn (and, but), từ vựng đời sống ~1000 từ thông dụng nhất.
- Level 3: bắt đầu có because / so / when, câu hỏi nối tiếp, phản hồi tự nhiên
  (Really? / That sounds great. / No way!), từ vựng ~1500–2000 từ.
- Chỉ dùng ngữ pháp đã học ở level trước/unit trước + điểm ngữ pháp của unit đó.

## 4. Syllabus (12 unit/level; CD1 = unit 1–4, CD2 = 5–8, CD3 = 9–12)
Không trùng Grammar Focus của Level 1, 4, 5. Mỗi unit một cặp nhân vật MỚI và một tình huống MỚI
(trộn tên Việt và tên quốc tế như Level 1; không lặp bối cảnh đã dùng ở Level 1).

### Level 2 (A1+)
1. Tính từ sở hữu + 's (my/your/his/her/their, Tom's), Whose…? — quầy đồ thất lạc
2. Đại từ tân ngữ (me/him/her/us/them) — chọn quà cho bạn
3. Câu mệnh lệnh (Go straight / Turn left / Don't…) — hỏi đường
4. Giới từ nơi chốn (next to / between / across from / behind) — tìm đồ trong căn hộ mới
5. would like: I'd like… / Would you like…? — gọi món ở quán cà phê
6. a / an / some với danh từ đếm được & không đếm được — đi chợ, lập danh sách mua sắm
7. like / love / hate + V-ing — nói về sở thích
8. How much is / are…? + giá tiền — mua quần áo
9. Quá khứ đơn: động từ có quy tắc (-ed) + 3 cách đọc /t/ /d/ /ɪd/ — kể cuối tuần
10. Quá khứ đơn: động từ bất quy tắc (went, ate, saw, had) — kể chuyến đi
11. Quá khứ đơn: câu hỏi & phủ định (Did you…? / I didn't…) — hỏi về bữa tiệc / bộ phim
12. be going to: kế hoạch tương lai — kế hoạch hè

### Level 3 (A2-)
1. Hiện tại tiếp diễn chỉ lịch hẹn tương lai (I'm meeting… tomorrow) — sắp xếp cuối tuần
2. Quá khứ tiếp diễn + when (I was cooking when…) — kể một sự cố
3. should / shouldn't — lời khuyên khi bị ốm
4. must / mustn't — nội quy (phòng gym, thư viện, chỗ làm mới)
5. So sánh nhất (the -est / the most) — chọn nhà hàng / khách sạn
6. Trạng từ chỉ cách thức (slowly, carefully, well, fast) — học lái xe / lớp nấu ăn
7. too + adj / adj + enough — thử giày, xem nhà thuê
8. a lot of / a few / a little — chuẩn bị tiệc
9. Đại từ sở hữu (mine / yours / hers / theirs) + Whose — dọn đồ sau buổi picnic
10. Let's… / Why don't we…? / How about + V-ing? — rủ đi chơi
11. to + V chỉ mục đích (I went there to buy…) — đi làm việc vặt
12. may / might — khả năng (It might rain) — lên kế hoạch chuyến đi

## 5. Định dạng file .md (theo đúng Level 1)
[HEADER] unit M — CDx                        (x = (M-1)//4 + 1)
[1] Conversation — track a, a+2, a+3          (a = 7·((M-1)%4) + 1)
  dòng 1: câu bối cảnh tiếng Anh; sau đó "Tên: lời thoại", luân phiên 2 nhân vật
  in đậm **...** điểm ngữ pháp, ít nhất 3 lần
[2] Speak Like a Native — track a+1
  3 câu, mỗi câu CHÉP NGUYÊN VĂN từ hội thoại; nhãn smooth / linking / change / weak / strong;
  giải thích bằng tiếng Việt; khối [MẸO PHÁT ÂM] 3–5 câu
[3] Study Notes — đúng 2 mục: **câu tiếng Anh** / nghĩa tiếng Việt / giải thích / "Cách nói tương đương: …"
[4] Grammar Focus — mỗi khối: tiêu đề / 1 dòng giải thích tiếng Việt / 2–3 ví dụ với [[từ khoá]];
  ví dụ KHÔNG được chép từ hội thoại
[5] Role Play — track a+5: hội thoại với A/B, đúng 3 chỗ trống ________ chỉ ở dòng của B;
  điền lại bằng cụm gốc của drill phải khớp 100% với hội thoại
[6] Substitution Drill — track a+6: 3 câu lấy từ lời của B (người nói thứ 2), phần thay thế
  bọc __...__, mỗi câu 3 option a/b/c, cùng loại ngữ pháp và hợp nghĩa
Ví dụ: unit 10 → CD3, track 8, 10, 11 / 9 / 13 / 14.

## 6. Yêu cầu chất lượng
- Tiếng Anh tự nhiên như người bản xứ nói (dùng dạng rút gọn), không phải câu sách giáo khoa cứng.
- Giải thích tiếng Việt ngắn gọn, đúng giọng văn Level 1; phiên âm IPA khi nói về weak form.
- Mỗi unit phải vừa 1 trang PDF A4 — nếu tràn, rút gọn phần giải thích tiếng Việt.
- Tên nhân vật nữ mới phải được thêm vào FEMALE_NAMES trong `tools/build_unit_audio.py`.
- Tránh tên có cách đọc mơ hồ cho TTS.

## 7. Sửa tool (làm trước khi viết unit)
- `tools/build_unit_pdf.py`: thay số hardcode trong `check_unit()` bằng bảng luật theo level
  (LEVEL_RULES = {1: …, 2: …, 3: …} theo bảng ở mục 3), lấy level từ đường dẫn file như `main()`
  đang làm. Level 1 phải vẫn pass y như cũ; level không có trong bảng (4, 5) thì bỏ qua check.
- Không đổi định dạng .md hay layout PDF.

## 8. Quy trình
1. Sửa tool, chạy `python tools/build_unit_pdf.py "Level 1" --check` → vẫn toàn OK.
2. Viết `Level 2/unit 1/unit 1.md`, chạy `--check`, DỪNG LẠI cho mình review.
3. Sau khi mình duyệt: viết unit 2–12, chạy `python tools/build_unit_pdf.py "Level 2" --check`
   tới khi toàn OK, rồi chạy không có `--check` để sinh PDF.
4. Sinh audio: `python tools/build_unit_audio.py "Level 2"` (cần `pip install edge-tts imageio-ffmpeg`).
5. Chạy `python tools/build_manifest.py`, mở `index.html` kiểm tra Level 2 hiện đủ 12 unit,
   7 track, PDF và nội dung.
6. Lặp lại bước 2–5 cho Level 3.
7. Báo cáo: bảng 24 unit (chủ đề, ngữ pháp, số từ), tên nữ đã thêm, lỗi còn lại nếu có.
   Không commit khi mình chưa yêu cầu.
