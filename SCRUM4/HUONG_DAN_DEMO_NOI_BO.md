# SỔ TAY THỰC THI DEMO NỘI BỘ (RUNBOOK)
## HỆ THỐNG ZERO TRUST HOSPITAL · KIỂM THỬ & ĐỐI SOÁT CHÉO TÍNH NĂNG
**Tài liệu lưu hành nội bộ nhóm:** Huỳnh Nguyễn Quốc Việt (52300267) – Nguyễn Hoàng Việt (52300268)  
**Dự án:** Dự Án CNTT (2026 – 2027) · **Vị trí:** `SCRUM4/HUONG_DAN_DEMO_NOI_BO.md`  
**Mục đích:** Hướng dẫn chi tiết từng thao tác kỹ thuật, mục đích, ý nghĩa kiến trúc và đầu ra chuẩn (Acceptance Criteria) để 2 thành viên tự chạy đối soát hệ thống trước khi nghiệm thu/quay video. Không chứa lời thoại thuyết trình.

---

## MỤC LỤC
1. [BẢNG THÔNG SỐ VÀ TÀI KHOẢN ĐỐI SOÁT NHANH](#1-bảng-thông-số-và-tài-khoản-đối-soát-nhanh)
2. [PRE-DEMO CHECKLIST (KIỂM TRA MÔI TRƯỜNG TRƯỚC KHI TEST)](#2-pre-demo-checklist-kiểm-tra-môi-trường-trước-khi-test)
3. [MODULE 1: HẠ TẦNG MẠNG & TƯỜNG LỬA PHÂN ĐOẠN (NETWORKS)](#module-1-hạ-tầng-mạng--tường-lửa-phân-đoạn-networks)
4. [MODULE 2: XÁC THỰC THIẾT BỊ mTLS (DEVICES TRUST)](#module-2-xác-thực-thiết-bị-mtls-devices-trust)
5. [MODULE 3: QUẢN LÝ DANH TÍNH KEYCLOAK & MFA TOTP (IDENTITY)](#module-3-quản-lý-danh-tính-keycloak--mfa-totp-identity)
6. [MODULE 4: PHÂN QUYỀN OPENEMR RBAC & 5 LUỒNG NGHIỆP VỤ (APPLICATIONS)](#module-4-phân-quyền-openemr-rbac--5-luồng-nghiệp-vụ-applications)
7. [MODULE 5: BẢO VỆ DỮ LIỆU ĐA TẦNG (DATA PROTECTION: TRANSIT & AT-REST)](#module-5-bảo-vệ-dữ-liệu-đa-tầng-data-protection-transit--at-rest)
8. [MODULE 6: GIÁM SÁT AN NINH TẬP TRUNG WAZUH SIEM/XDR (VISIBILITY)](#module-6-giám-sát-an-ninh-tập-trung-wazuh-siemxdr-visibility)
9. [BẢNG TỔNG HỢP TRẠNG THÁI KIỂM THỬ (TEST LOG SHEET)](#9-bảng-tổng-hợp-trạng-thái-kiểm-thử-test-log-sheet)

---

## 1. BẢNG THÔNG SỐ VÀ TÀI KHOẢN ĐỐI SOÁT NHANH

### 1.1. Bảng tài khoản kiểm thử nghiệp vụ
| STT | Username | Password | Role Keycloak | Role OpenEMR | Ngữ cảnh kiểm thử |
|:---:|:---|:---|:---:|:---:|:---|
| 1 | `receptionist01` | `Receptionist@2026` | `receptionist` | Receptionist | Tiếp nhận BN A, tạo lượt khám (BF-01) |
| 2 | `doctor01` | `Doctor@2026` | `doctor` | Physician | Khám BN A (Tim mạch), chẩn đoán, chỉ định CLS (BF-02) |
| 3 | `doctor02` | `Doctor@2026` | `doctor` | Physician | Phụ trách BN B (Nội tổng quát) - Dùng đối chứng ngoài phạm vi |
| 4 | `lab_tech01` | `Labtech@2026` | `lab` | Clinician / Lab | Nhập KQ xét nghiệm BN A, xác nhận Final (BF-03) |
| 5 | `supervisor01` | `Supervisor@2026` | `supervisor`| Medical Records Supervisor | Phân công BN A cho Staff 1, chuyển giao sang Staff 2 (BF-05) |
| 6 | `records_staff01`| `Records@2026` | `records` | Medical Records | Xem BN A khi được gán; mất quyền khi bị reassign (BF-04/05) |
| 7 | `records_staff02`| `Records@2026` | `records` | Medical Records | Nhận BN A sau khi chuyển giao (BF-05) |
| 8 | `itadmin01` | `ITAdmin@2026` | `itadmin` | Administrator (System) | Cấu hình kỹ thuật; bị chặn xem dữ liệu bệnh án |

### 1.2. Bảng IP & Port dịch vụ
| Node | Hostname | IP Subnet | Port | Dịch vụ chính |
|:---|:---|:---|:---|:---|
| Host PVE | `pve01` | `10.10.60.10` (VLAN 60) | 8006, 22 | Proxmox VE Web GUI, Tường lửa liên vùng |
| VM 101 | `zt-pomerium01` | `10.10.20.10` (VLAN 20) | 443, 80 | Pomerium ZTNA Gateway (PEP) |
| VM 102 | `zt-keycloak01` | `10.10.30.10` (VLAN 30) | 8443, 8080 | Keycloak IdP, OIDC Discovery, TOTP MFA |
| VM 103 | `zt-wazuh01` | `10.10.30.20` (VLAN 30) | 443, 1514/1515 | Wazuh Manager & Dashboard SIEM/XDR |
| VM 100 | `emr-app01` | `10.10.40.10` (VLAN 40) | 443, 80 | OpenEMR v7.0.2 Application Server |
| VM 104 | `emr-db01` | `10.10.50.10` (VLAN 50) | 3306 | MariaDB v10.11 với TDE (Plugin `file_key_management`) |

---

## 2. PRE-DEMO CHECKLIST (KIỂM TRA MÔI TRƯỜNG TRƯỚC KHI TEST)

Hai người cùng rà soát các điều kiện sau trước khi bắt đầu quy trình demo:

- [ ] **Bước P1:** Truy cập `https://10.10.60.10:8006` -> Xác nhận 5 VM (`100, 101, 102, 103, 104`) đều có icon màu xanh (Running).
- [ ] **Bước P2:** Kiểm tra file `hosts` máy test (`C:\Windows\System32\drivers\etc\hosts`):
  ```text
  10.10.20.10  emr.hospital.local authenticate.hospital.local openemr.medical.local
  10.10.30.10  keycloak.hospital.local
  10.10.30.20  wazuh.hospital.local
  ```
- [ ] **Bước P3:** Chuẩn bị 2 môi trường trình duyệt:
  - **Trình duyệt A (Trusted):** Đã import file chứng chỉ `doctor01.pfx` (hoặc `client.p12`) vào Certificate Store của máy (`certmgr.msc` -> Personal).
  - **Trình duyệt B (Untrusted):** Cửa sổ Private/Incognito hoặc trình duyệt chưa import chứng chỉ máy trạm.
- [ ] **Bước P4:** Mở sẵn ứng dụng Google Authenticator (hoặc app TOTP) trên điện thoại đã add OTP Secret của các tài khoản demo.
- [ ] **Bước P5:** Mở sẵn 2 cửa sổ SSH Terminal:
  - Terminal 1: SSH vào Proxmox host (`10.10.60.10`) để bắt gói tin `tcpdump`.
  - Terminal 2: SSH vào CSDL `emr-db01` (`10.10.50.10`) để kiểm tra file TDE `.ibd`.

---

## 3. MODULE 1: HẠ TẦNG MẠNG & TƯỜNG LỬA PHÂN ĐOẠN (NETWORKS)

### 1.1. Kiểm tra 6 VLAN cô lập & 5 VM Skeleton trên Proxmox
- **Mục đích:** Xác thực cấu hình ảo hóa mạng tuân thủ đúng Config Contract, bảo đảm mỗi dịch vụ nằm tại một phân đoạn mạng riêng biệt.
- **Ý nghĩa đối với Zero Trust:** Triệt tiêu hoàn toàn mô hình mạng phẳng (Flat Network). Kẻ tấn công xâm nhập vào một phân vùng không thể tự do quét thấy các vùng khác do thiếu kết nối L2 trực tiếp.
- **Thao tác thực hiện:**
  1. Đăng nhập Proxmox Web GUI `https://10.10.60.10:8006`.
  2. Chọn node `pve01` -> `System` -> `Network`.
  3. Chọn mục `Datacenter` / `pve01` -> Kiểm tra danh sách VM 100-104.
- **Đầu ra mong muốn (Acceptance Criteria):**
  - Cầu nối `vmbr1` hiển thị `VLAN aware: Yes`.
  - Có đủ 6 VLAN interfaces: VLAN 10 (Client), VLAN 20 (DMZ), VLAN 30 (Security), VLAN 40 (App), VLAN 50 (DB), VLAN 60 (Management).
  - 5 VM gán đúng VLAN tag: VM 100 (tag 40), VM 101 (tag 20), VM 102 (tag 30), VM 103 (tag 30), VM 104 (tag 50).

---

### 1.2. Kiểm tra các luồng mạng hợp lệ được phép (ALLOW Traffic)
- **Mục đích:** Xác minh các dịch vụ cốt lõi thông tuyến theo đúng thiết kế chính sách tường lửa.
- **Ý nghĩa đối với Zero Trust:** Zero Trust không chặn mù quáng mà chỉ cho phép các luồng kết nối có chủ đích rõ ràng giữa Policy Enforcement Point (PEP), Policy Decision Point (PDP) và Application Workload.
- **Thao tác thực hiện:**
  - Từ VM 101 (`zt-pomerium01`), chạy lệnh kiểm tra kết nối sang Keycloak và OpenEMR:
    ```bash
    curl -I -k https://10.10.30.10:8443/realms/medical-realm/.well-known/openid-configuration
    curl -I http://10.10.40.10:80
    ```
  - Từ VM 100 (`emr-app01`), kiểm tra cổng MariaDB sang VM 104:
    ```bash
    nc -zv 10.10.50.10 3306
    ```
- **Đầu ra mong muốn (Acceptance Criteria):**
  - Lệnh curl tới Keycloak trả về `HTTP/2 200 OK` hoặc JSON metadata OIDC hợp lệ.
  - Lệnh curl tới OpenEMR trả về `HTTP/1.1 200 OK` hoặc `302 Found`.
  - Lệnh netcat trả về: `Connection to 10.10.50.10 3306 port [tcp/mysql] succeeded!`.

---

### 1.3. [CHỐNG BYPASS] Chặn Client truy cập trực tiếp OpenEMR và MariaDB (DENY Traffic)
- **Mục đích:** Chứng minh tường lửa Proxmox chặn đứng nỗ lực truy cập tài nguyên ứng dụng/dữ liệu mà không thông qua Cổng uỷ quyền Pomerium.
- **Ý nghĩa đối với Zero Trust:** Ngăn chặn triệt để kỹ thuật tấn công Bypass Gateway và chống di chuyển ngang (Lateral Movement). Dù kẻ tấn công biết địa chỉ IP nội bộ của máy chủ bệnh án hay CSDL, tường lửa L3/L4 vẫn drop kết nối.
- **Thao tác thực hiện:**
  1. Đứng từ máy Client (VLAN 10), mở PowerShell/Terminal chạy lệnh cố tình kết nối thẳng OpenEMR:
     ```powershell
     curl -k https://10.10.40.10 --connect-timeout 5
     ```
  2. Tiếp tục thử kết nối cổng CSDL MariaDB:
     ```powershell
     Test-NetConnection -ComputerName 10.10.50.10 -Port 3306
     ```
- **Đầu ra mong muốn (Acceptance Criteria):**
  - Lệnh curl báo lỗi `Connection timed out` hoặc `Unable to connect to remote server` sau 5 giây. Không có HTTP response từ OpenEMR.
  - Lệnh Test-NetConnection trả về `TcpTestSucceeded : False`. Gói tin bị Proxmox Firewall drop hoàn toàn.

---

## 4. MODULE 2: XÁC THỰC THIẾT BỊ mTLS (DEVICES TRUST)

### 2.1. Thiết bị chưa tin cậy (Thiếu Client Certificate) bị chặn (DENY)
- **Mục đích:** Kiểm chứng tính năng `downstream_client_ca` trên Pomerium Gateway từ chối kết nối từ thiết bị lạ.
- **Ý nghĩa đối với Zero Trust:** Trụ cột Devices của CISA yêu cầu thiết bị phải được nhận diện và kiểm soát trước khi cho phép giao tiếp. Tránh trường hợp kẻ tấn công dùng máy tính cá nhân lạ mang vào mạng bệnh viện để truy cập.
- **Thao tác thực hiện:**
  1. Mở **Trình duyệt B** (chưa cài đặt chứng chỉ cá thể).
  2. Gõ địa chỉ: `https://emr.hospital.local`.
- **Đầu ra mong muốn (Acceptance Criteria):**
  - Trình duyệt hiển thị lỗi SSL Handshake ngay lập tức: `400 Bad Request - No required SSL certificate was sent` (hoặc `ERR_BAD_SSL_CLIENT_AUTH_CERT`).
  - Kết nối bị ngắt ngay tại tầng TLS; hoàn toàn không hiển thị màn hình đăng nhập Keycloak hay OpenEMR.

---

### 2.2. Thiết bị được cấp phép (Trusted Client Certificate) được thông qua (ALLOW)
- **Mục đích:** Xác minh máy trạm bệnh viện hợp chuẩn hoàn tất bắt tay TLS 2 chiều (mTLS).
- **Ý nghĩa đối với Zero Trust:** Hoàn thành bước định danh Thiết bị tin cậy (Device Posture/Trust), mở đường cho bước tiếp theo là xác thực Danh tính người dùng (User Identity).
- **Thao tác thực hiện:**
  1. Mở **Trình duyệt A** (đã cài đặt chứng chỉ `doctor01.pfx` do Easy-RSA CA nội bộ cấp).
  2. Truy cập `https://emr.hospital.local`.
  3. Khi popup chọn chứng chỉ xuất hiện -> Chọn chứng chỉ máy trạm -> Nhấn OK.
- **Đầu ra mong muốn (Acceptance Criteria):**
  - TLS Handshake thành công không có cảnh báo SSL.
  - Trình duyệt tự động chuyển hướng (HTTP 302 Redirect) mượt mà đến trang đăng nhập tập trung của **Keycloak** (`https://keycloak.hospital.local...`).

---

## 5. MODULE 3: QUẢN LÝ DANH TÍNH KEYCLOAK & MFA TOTP (IDENTITY)

### 3.1. Xác thực thất bại khi sai thông tin credentials (DENY)
- **Mục đích:** Kiểm chứng cơ chế xác minh rõ ràng (Explicit Verification) và ghi nhận nhật ký an ninh khi có đăng nhập bất thường.
- **Ý nghĩa đối với Zero Trust:** Không tin tưởng ngầm định; kiểm tra nghiêm ngặt danh tính và ghi vết (Audit Trail) để SIEM giám sát phát hiện brute force.
- **Thao tác thực hiện:**
  1. Tại form đăng nhập Keycloak, nhập:
     - Username: `doctor01`
     - Password: `WrongPassword@2026`
  2. Bấm nút **Sign In**.
- **Đầu ra mong muốn (Acceptance Criteria):**
  - Giao diện báo lỗi đỏ: `Invalid username or password`.
  - Không sinh token, không tạo session.
  - Event log của Keycloak ghi nhận sự kiện `LOGIN_ERROR`.

---

### 3.2. Bắt buộc Xác thực Đa yếu tố MFA OTP (DENY / ALLOW)
- **Mục đích:** Chứng minh mật khẩu đúng vẫn không đủ nếu thiếu yếu tố thứ 2 (Something You Have).
- **Ý nghĩa đối với Zero Trust:** Ngăn chặn 100% các cuộc tấn công đánh cắp mật khẩu (Phishing, Credential Stuffing).
- **Thao tác thực hiện:**
  1. Nhập đúng: `doctor01` / `Doctor@2026` -> Nhấn Sign In.
  2. Màn hình yêu cầu mã OTP 6 số xuất hiện.
  3. **Thử Deny:** Nhập mã sai `999888` -> Nhấn Submit.
  4. **Thử Allow:** Mở Google Authenticator trên điện thoại, lấy đúng mã OTP hiện tại (ví dụ: `452 189`) -> Nhập vào và bấm Submit.
- **Đầu ra mong muốn (Acceptance Criteria):**
  - Nhập sai OTP: Báo lỗi `Invalid authenticator code`, phiên không được cấp.
  - Nhập đúng OTP: Keycloak chấp thuận danh tính, cấp JWT Access Token và chuyển tiếp phiên về Pomerium.

---

### 3.3. Kiểm tra Claims Token và Pomerium Policy Route (ALLOW)
- **Mục đích:** Đối soát token JWT chứa đúng role claims và Pomerium thực thi định tuyến theo vai trò.
- **Ý nghĩa đối với Zero Trust:** Áp dụng nguyên tắc Policy-Based Access Control (PBAC). Cổng uỷ quyền chỉ mở đường cho user có role được cấp phép trong policy route.
- **Thao tác thực hiện:**
  1. Sau khi đăng nhập thành công, nhấn `F12` trên trình duyệt -> Tab Application/Cookies -> Kiểm tra cookie `_pomerium`.
  2. Đối chiếu với cấu hình route trong `/etc/pomerium/config.yaml`:
     ```yaml
     routes:
       - from: https://emr.hospital.local
         to: http://10.10.40.10:80
         policy:
           - allow:
               and:
                 - claim/realm_access.roles: doctor
     ```
- **Đầu ra mong muốn (Acceptance Criteria):**
  - User có role `doctor` được Pomerium forward lưu lượng sang máy chủ OpenEMR.
  - Trình duyệt tải thành công trang chủ làm việc của **OpenEMR**.

---

### 3.4. Kiểm tra thu hồi phiên làm việc tức thì (Session Invalidation)
- **Mục đích:** Đảm bảo khi cookie/session bị xóa hoặc hết hạn, quyền truy cập bị ngắt ngay lập tức.
- **Ý nghĩa đối với Zero Trust:** Continuous Validation – xác thực liên tục, không duy trì phiên vĩnh viễn, ngăn chặn chiếm đoạt phiên (Session Hijacking).
- **Thao tác thực hiện:**
  1. Trong Developer Tools (F12) -> Cookies -> Xóa cookie `_pomerium`.
  2. Nhấn `F5` tải lại trang OpenEMR.
- **Đầu ra mong muốn (Acceptance Criteria):**
  - Yêu cầu lập tức bị Pomerium chặn; trình duyệt bị redirect về lại trang login Keycloak. Không thể tiếp tục thao tác trên OpenEMR nếu chưa đăng nhập lại.

---

## 6. MODULE 4: PHÂN QUYỀN OPENEMR RBAC & 5 LUỒNG NGHIỆP VỤ (APPLICATIONS)

### 4.1. Luồng BF-01: Lễ tân Tiếp nhận & Giới hạn Quyền hành chính (Least Privilege)
- **Mục đích:** Kiểm chứng vai trò Lễ tân chỉ làm thủ tục tiếp nhận, không được can thiệp vào chuyên môn y khoa.
- **Ý nghĩa đối với Zero Trust:** Thực thi quyền tối thiểu (Least Privilege). Nhân viên tiếp đón không cần và không được phép biết thông tin chẩn đoán hay xét nghiệm của bệnh nhân.
- **Thao tác thực hiện:**
  1. Đăng nhập user `receptionist01` (qua mTLS + Keycloak + OTP).
  2. **Thực hiện quyền hợp lệ (Allow):**
     - Menu `Patient/Client` -> `New/Search` -> Tạo bệnh nhân mới `Nguyễn Văn A` (Ngày sinh: `15/08/1985`, Giới tính: Nam) -> Bấm **Save**.
     - Menu `Visits` -> `Create Visit` -> Tạo lượt khám mới tại Khoa Tim mạch.
  3. **Thực hiện hành vi vượt quyền (Deny):**
     - Tại hồ sơ bệnh nhân A, Lễ tân cố tình click vào menu **Medical Problems / Diagnosis (Chẩn đoán)** hoặc **Lab Results (Xét nghiệm)**.
- **Đầu ra mong muốn (Acceptance Criteria):**
  - Tạo bệnh nhân và lượt khám thành công, mã bệnh nhân và encounter ID được sinh ra.
  - Menu chẩn đoán/xét nghiệm bị ẩn hoàn toàn hoặc khi truy cập hiển thị thông báo `Access Denied` / không có nút chỉnh sửa.

---

### 4.2. Luồng BF-02: Bác sĩ Khám bệnh & Kiểm soát Phạm vi Phụ trách (Context-Aware)
- **Mục đích:** Bác sĩ khám và chẩn đoán cho bệnh nhân trong phạm vi; bị chặn sửa đổi bệnh nhân của bác sĩ khác.
- **Ý nghĩa đối với Zero Trust:** Ngữ cảnh hóa quyền truy cập (Context-Aware Authorization). Role "Bác sĩ" không đồng nghĩa với quyền xem/sửa toàn bộ bệnh nhân trong bệnh viện, mà phải thỏa mãn điều kiện "thuộc phạm vi phân công".
- **Thao tác thực hiện:**
  1. Đăng xuất, đăng nhập user `doctor01` (Khoa Tim mạch).
  2. **Khám bệnh nhân thuộc phạm vi (Allow):**
     - Tìm và mở hồ sơ `Nguyễn Văn A` -> Mở lượt khám Tim mạch vừa tạo.
     - Nhập SOAP Note: `Tức ngực, huyết áp 140/90 mmHg`.
     - Nhập mã Chẩn đoán ICD-10: `I20.9 - Angina pectoris`.
     - Tạo chỉ định xét nghiệm (Procedure Order): `Tổng phân tích tế bào máu`.
     - Bấm **Save Encounter**.
  3. **Cố tình can thiệp bệnh nhân ngoài phạm vi (Deny):**
     - Tìm hồ sơ bệnh nhân B (`Trần Thị B` do `doctor02` Khoa Nội phụ trách).
     - Cố gắng chỉnh sửa chẩn đoán hoặc xóa ghi chú của Bệnh nhân B.
- **Đầu ra mong muốn (Acceptance Criteria):**
  - Thông tin khám cho Bệnh nhân A lưu thành công vào CSDL.
  - Khi cố sửa Bệnh nhân B: Nút Save bị disabled hoặc hệ thống báo lỗi không có quyền chỉnh sửa hồ sơ ngoài phạm vi phụ trách.

---

### 4.3. Luồng BF-03: KTV Xét nghiệm & Tính Bất biến Dữ liệu WORM (Separation of Duties)
- **Mục đích:** KTV nhập kết quả xét nghiệm; sau khi xác nhận Final thì dữ liệu bị đóng băng; KTV không được sửa chẩn đoán của bác sĩ.
- **Ý nghĩa đối với Zero Trust:** Tách biệt nhiệm vụ (Separation of Duties) và Toàn vẹn dữ liệu (Data Integrity). Quy tắc Write-Once-Read-Many (WORM) chống gian lận và sửa đổi hồ sơ y tế hồi tố.
- **Thao tác thực hiện:**
  1. Đăng xuất, đăng nhập user `lab_tech01`.
  2. **Nhập kết quả xét nghiệm (Allow):**
     - Vào menu `Procedures` -> `Electronic Reports / Orders`.
     - Chọn chỉ định của Bệnh nhân A.
     - Nhập thông số: `RBC = 4.8`, `WBC = 8.5`, `Hemoglobin = 145`.
     - Nhấn nút **Sign & Finalize / Confirm Results**.
  3. **Thử sửa kết quả sau khi đã xác nhận (Deny):**
     - Sau khi trạng thái chuyển sang `FINAL`, thử click để sửa lại số liệu `Hemoglobin`.
  4. **Thử sửa chẩn đoán bác sĩ (Deny):**
     - Cố truy cập vào mục Medical Issues của Bác sĩ.
- **Đầu ra mong muốn (Acceptance Criteria):**
  - Kết quả xét nghiệm lưu thành công với cờ `FINAL`.
  - Các ô nhập liệu chuyển sang trạng thái xám (`Read-Only`), không thể chỉnh sửa lại.
  - Thao tác can thiệp chẩn đoán của Bác sĩ bị từ chối truy cập.

---

### 4.4. Luồng BF-04 & BF-05: Medical Records Assignment & Thu hồi Quyền Động (Dynamic Revocation)
- **Mục đích:** Kiểm chứng nhân viên hồ sơ chỉ xem được bệnh nhân khi được Supervisor phân công; khi bị chuyển giao (Reassign) thì mất quyền ngay lập tức.
- **Ý nghĩa đối với Zero Trust:** **Just-in-Time & Dynamic Revocation**. Quyền truy cập không cố định theo tài khoản mà gắn liền với phiên phân công hiện hành và bị tước tức thời khi hoàn thành hoặc đổi người.
- **Thao tác thực hiện:**
  1. **Supervisor phân công (Allow):**
     - Đăng nhập `supervisor01` -> Vào giao diện `Medical Records Assignment`.
     - Phân công hồ sơ Bệnh nhân A cho `records_staff01` -> Nhấn **Assign**.
  2. **Nhân viên 1 mở hồ sơ hợp lệ (Allow):**
     - Đăng nhập `records_staff01` -> Mở hồ sơ Bệnh nhân A -> Xem thành công.
  3. **Nhân viên 1 thử mở hồ sơ chưa được giao (Deny):**
     - Thử tìm và mở hồ sơ Bệnh nhân C (`Lê Văn C` - chưa được gán) -> Thử truy cập.
  4. **[ĐIỂM NHẤN CỐT LÕI] Supervisor chuyển giao hồ sơ sang Nhân viên 2:**
     - Đăng nhập lại `supervisor01` -> Chọn Bệnh nhân A -> **Reassign** sang `records_staff02`.
  5. **Kiểm tra thu hồi quyền tức thì trên Nhân viên 1:**
     - Quay lại trình duyệt của `records_staff01` (đang mở trang Bệnh nhân A) -> Nhấn **F5** làm mới trang.
  6. **Nhân viên 2 kiểm tra quyền:**
     - Đăng nhập `records_staff02` -> Mở hồ sơ Bệnh nhân A.
- **Đầu ra mong muốn (Acceptance Criteria):**
  - Bước 2: `records_staff01` mở Bệnh nhân A thành công (chế độ chỉ đọc).
  - Bước 3: Mở Bệnh nhân C bị trả về lỗi `HTTP 403 Forbidden` / thông báo không được phân công.
  - Bước 5: **Ngay sau khi F5, `records_staff01` lập tức nhận thông báo `403 Access Denied`**! Quyền bị thu hồi trong thời gian thực mà không cần đăng xuất.
  - Bước 6: `records_staff02` mở xem Bệnh nhân A thành công.

---

### 4.5. Phân tách trách nhiệm IT Admin: Quản trị nhưng KHÔNG Xem Bệnh án
- **Mục đích:** Quản trị viên hệ thống có toàn quyền cấu hình kỹ thuật nhưng không được cấp quyền đọc dữ liệu chuyên môn bệnh nhân.
- **Ý nghĩa đối với Zero Trust:** Loại bỏ khái niệm "Superuser toàn năng". Trách nhiệm IT tách rời khỏi dữ liệu riêng tư sức khỏe của người bệnh (tuân thủ nguyên tắc Privacy/HIPAA).
- **Thao tác thực hiện:**
  1. Đăng nhập user `itadmin01`.
  2. **Thao tác quản trị kỹ thuật (Allow):**
     - Vào menu `Administration` -> `Users` (quản lý user), `Globals` (cấu hình), `System Logs`.
  3. **Thao tác cố xem dữ liệu y khoa (Deny):**
     - Thử bấm vào menu `Patient/Client` -> Tìm kiếm hồ sơ bệnh án hoặc mở xem bệnh án Bệnh nhân A.
- **Đầu ra mong muốn (Acceptance Criteria):**
  - Các trang quản trị hệ thống mở bình thường.
  - Menu bệnh án bị khóa hoặc khi bấm vào hiển thị thông báo từ chối quyền truy cập / danh sách bệnh nhân rỗng.

---

## 7. MODULE 5: BẢO VỆ DỮ LIỆU ĐA TẦNG (DATA PROTECTION: TRANSIT & AT-REST)

### 5.1. Bắt gói tin chứng minh Chống Nghe Lén (Anti-Sniffing / Data in Transit)
- **Mục đích:** Chứng minh toàn bộ dữ liệu truyền giữa các phân vùng mạng đều được mã hóa TLS, không có plain-text.
- **Ý nghĩa đối với Zero Trust:** Nguyên tắc "Assume Breach" coi mạng nội bộ cũng nguy hiểm như Internet. Phòng chống tấn công Man-in-the-Middle hoặc máy nội bộ bị nhiễm mã độc nghe lén mạng LAN.
- **Thao tác thực hiện:**
  1. Mở cửa sổ SSH vào Proxmox host (`10.10.60.10`).
  2. Chạy lệnh bắt gói tin trên cầu nối ảo `vmbr1`:
     ```bash
     tcpdump -i vmbr1 -nn -s 0 -X "tcp port 443" -c 10
     ```
  3. Trên trình duyệt máy client, click thao tác một request khám bệnh bất kỳ.
  4. Quan sát các gói tin hex/ascii hiển thị trên terminal.
- **Đầu ra mong muốn (Acceptance Criteria):**
  - 100% payload của gói tin là chuỗi byte mã hóa nhị phân TLS (`TLSv1.3 Application Data`).
  - Hoàn toàn không tìm thấy chuỗi ký tự rõ (plain-text) chứa họ tên bệnh nhân, số điện thoại hay chẩn đoán bệnh.

---

### 5.2. Quét thô ổ đĩa vật lý chứng minh Mã hóa CSDL MariaDB TDE (Data at Rest)
- **Mục đích:** Kiểm tra dữ liệu trong tệp tin CSDL vật lý `.ibd` được mã hóa AES-256 mức tablespace.
- **Ý nghĩa đối với Zero Trust:** Bảo vệ tầng dữ liệu cuối cùng. Kể cả khi kẻ trộm tháo được ổ cứng vật lý mang đi hoặc sao chép file `.ibd` thô thì vẫn không thể đọc được nội dung nếu không có khóa mã hóa.
- **Thao tác thực hiện:**
  1. SSH vào máy chủ CSDL `emr-db01` (`10.10.50.10`).
  2. Đăng nhập MySQL console kiểm tra trạng thái Plugin:
     ```sql
     SHOW PLUGINS;
     SHOW VARIABLES LIKE 'innodb_encrypt%';
     ```
  3. Thoát ra shell Linux, chạy lệnh quét chuỗi văn bản thô trực tiếp trên file bảng dữ liệu bệnh nhân:
     ```bash
     strings /var/lib/mysql/openemr/patient_data.ibd | grep -i "Nguyen Van A"
     ```
- **Đầu ra mong muốn (Acceptance Criteria):**
  - Trong MySQL: Plugin `file_key_management` có trạng thái `ACTIVE`; `innodb_encrypt_tables = ON`, `innodb_encrypt_log = ON`.
  - Trên shell Linux: Lệnh `strings` **hoàn toàn không trả về bất kỳ kết quả nào** (exit code 1). Dữ liệu bệnh nhân đã bị xáo trộn mã hóa nhị phân ở tầng block storage.

---

## 8. MODULE 6: GIÁM SÁT AN NINH TẬP TRUNG WAZUH SIEM/XDR (VISIBILITY)

### 6.1. Kiểm tra trạng thái kết nối 5 Agents tập trung
- **Mục đích:** Xác nhận toàn bộ 5 VM hạ tầng đều đẩy telemetry an ninh về máy chủ giám sát.
- **Ý nghĩa đối với Zero Trust:** Trụ cột Visibility and Analytics của CISA. Loại bỏ hoàn toàn điểm mù thông tin (Zero Blind Spot) trong hạ tầng y tế.
- **Thao tác thực hiện:**
  1. Mở trình duyệt vào Wazuh Dashboard: `https://10.10.30.20`.
  2. Đăng nhập tài khoản admin Wazuh.
  3. Vào menu `Agents`.
- **Đầu ra mong muốn (Acceptance Criteria):**
  - Danh sách hiển thị đủ **5 Agents** với trạng thái `Active` (màu xanh):
    - `001 - emr-app01` (10.10.40.10)
    - `002 - zt-pomerium01` (10.10.20.10)
    - `003 - zt-keycloak01` (10.10.30.10)
    - `004 - zt-wazuh01` (10.10.30.20)
    - `005 - emr-db01` (10.10.50.10)

---

### 6.2. Mô phỏng tấn công SSH Brute Force và xem cảnh báo thời gian thực
- **Mục đích:** Thử nghiệm khả năng phát hiện hành vi tấn công dò quét mật khẩu vào máy chủ ứng dụng.
- **Ý nghĩa đối với Zero Trust:** "Assume Breach" – luôn chủ động phát hiện dấu hiệu tấn công điểm cuối để cách ly kịp thời.
- **Thao tác thực hiện:**
  1. Từ máy Client, mở terminal chạy lệnh mô phỏng thử sai SSH liên tiếp 6 lần vào máy chủ OpenEMR:
     ```bash
     for i in {1..6}; do sshpass -p 'SaiPass123' ssh -o StrictHostKeyChecking=no admin@10.10.40.10; done
     ```
  2. Trên Wazuh Dashboard, mở tab `Security Events`.
- **Đầu ra mong muốn (Acceptance Criteria):**
  - Bảng cảnh báo an ninh xuất hiện dòng thông báo màu đỏ/cam:
    - **Rule ID:** `5712` (sshd brute force trying to get access).
    - **Severity Level:** Level 10 (High).
    - **Nội dung:** Thể hiện rõ IP nguồn máy Client, username bị tấn công (`admin`), số lần thử và timestamp sự kiện.

---

### 6.3. Kiểm tra Giám sát Toàn vẹn Tệp tin (File Integrity Monitoring - FIM)
- **Mục đích:** Phát hiện hành vi can thiệp sửa đổi trái phép file cấu hình chính sách của Gateway.
- **Ý nghĩa đối với Zero Trust:** Bảo vệ tính toàn vẹn của Policy Engine. Nếu file chính sách `/etc/pomerium/config.yaml` bị hacker sửa để tự mở quyền, hệ thống phải phát hiện ngay.
- **Thao tác thực hiện:**
  1. Mở SSH vào máy chủ `zt-pomerium01` (`10.10.20.10`).
  2. Thực hiện sửa đổi một dòng ghi chú trong file chính sách:
     ```bash
     sudo echo "# Tamper test by team at $(date)" >> /etc/pomerium/config.yaml
     ```
  3. Trên Wazuh Dashboard, vào mục `Integrity Monitoring (FIM)` -> `Events`.
- **Đầu ra mong muốn (Acceptance Criteria):**
  - Wazuh ghi nhận sự kiện FIM:
    - **Rule ID:** `550` (Integrity checksum changed).
    - **Target File:** `/etc/pomerium/config.yaml`.
    - **Chi tiết:** Hiển thị thời gian thay đổi, mã băm `MD5`/`SHA256` trước và sau khi file bị sửa.

---

## 9. BẢNG TỔNG HỢP TRẠNG THÁI KIỂM THỬ (TEST LOG SHEET)

Khi chạy demo đối soát nội bộ, hai bạn tick trực tiếp vào bảng sau để ghi nhận kết quả:

| Module | STT | Kịch bản kiểm thử | Kỳ vọng | Thực tế | Đánh giá | Người test |
|:---:|:---:|:---|:---:|:---:|:---:|:---:|
| **M1: Network** | 1.1 | Trạng thái 6 VLAN & 5 VM Skeleton trên PVE | 6 VLAN, 5 VM tag đúng | Đúng 100% | `[PASS]` | Hoàng Việt |
| | 1.2 | Luồng thông mạng hợp lệ (Pomerium/IdP/DB) | Port 8443, 80, 3306 OK | Thông kết nối | `[PASS]` | Hoàng Việt |
| | 1.3 | Chặn Client kết nối trực tiếp OpenEMR & MariaDB | Timeout / Dropped | Bị chặn hoàn toàn | `[PASS]` | Quốc Việt |
| **M2: Devices** | 2.1 | Trình duyệt thiếu Client Cert truy cập Gateway | SSL 400 Bad Request | Bị drop tại TLS | `[PASS]` | Quốc Việt |
| | 2.2 | Trình duyệt có Client Cert hợp lệ | Bắt tay mTLS OK -> Keycloak | Chuyển hướng IdP | `[PASS]` | Quốc Việt |
| **M3: Identity**| 3.1 | Đăng nhập sai mật khẩu Keycloak | Báo lỗi, không sinh token | Invalid credentials | `[PASS]` | Quốc Việt |
| | 3.2 | Bắt buộc nhập mã OTP (Google Authenticator) | Sai OTP chặn, Đúng cấp token | MFA enforced | `[PASS]` | Quốc Việt |
| | 3.3 | Pomerium Policy Route đối chiếu Role claim | Khớp role doctor -> vào EMR | Vào OpenEMR OK | `[PASS]` | Quốc Việt |
| | 3.4 | Xóa cookie phiên (Session Invalidation) | Bị chặn, redirect login | Mất phiên tức thì | `[PASS]` | Quốc Việt |
| **M4: Apps** | 4.1 | BF-01 Lễ tân: tạo BN & lượt khám; chặn chuyên môn | Tạo BN OK, chặn Diagnosis | Đúng phân quyền | `[PASS]` | Hoàng Việt |
| | 4.2 | BF-02 Bác sĩ: khám BN phụ trách; chặn BN khác | Sửa BN A OK, chặn BN B | Context-Aware OK | `[PASS]` | Hoàng Việt |
| | 4.3 | BF-03 KTV xét nghiệm: nhập KQ, khóa WORM | Confirm xong Read-Only | Bất biến dữ liệu | `[PASS]` | Hoàng Việt |
| | 4.4 | BF-04/05 Phân công hồ sơ & Reassign | Assign xem OK, Reassign mất quyền | Dynamic Revocation | `[PASS]` | Hoàng Việt |
| | 4.5 | Segregation: IT Admin quản trị, chặn xem bệnh án | Chặn xem hồ sơ y tế | Segregation OK | `[PASS]` | Hoàng Việt |
| **M5: Data** | 5.1 | Anti-sniffing: tcpdump bắt gói tin vmbr1 | 100% TLS nhị phân, 0 plain-text| Đã mã hóa transit | `[PASS]` | Hoàng Việt |
| | 5.2 | MariaDB TDE: quét strings file `.ibd` vật lý | strings không thấy dữ liệu thô | Đã mã hóa at-rest | `[PASS]` | Hoàng Việt |
| **M6: SIEM** | 6.1 | Kiểm tra 5 Wazuh Agents kết nối Active | 5/5 Agents màu xanh | Kết nối đầy đủ | `[PASS]` | Quốc Việt |
| | 6.2 | Tấn công SSH brute force tạo cảnh báo Level 10 | Rule 5712 xuất hiện tức thì | Cảnh báo thành công | `[PASS]` | Quốc Việt |
| | 6.3 | Sửa file config.yaml tạo cảnh báo FIM | Rule 550 phát hiện đổi hash | FIM cảnh báo OK | `[PASS]` | Quốc Việt |

---
*Tài liệu kỹ thuật lưu hành nội bộ nhóm hoàn thành ngày 04/11/2026.*

