# KỊCH BẢN DEMO TOÀN DIỆN HỆ THỐNG ZERO TRUST HOSPITAL
## BẢO MẬT HỒ SƠ Y TẾ ĐIỆN TỬ BẰNG KIẾN TRÚC ZERO TRUST (ZTNA + IAM + DATA PROTECTION + SIEM)

---

- **Đơn vị:** Đại học Tôn Đức Thắng (TDTU) – Khoa Công nghệ Thông tin
- **Dự án:** Dự Án CNTT (Khóa 2026 – 2027)
- **Sinh viên thực hiện:**
  - **Huỳnh Nguyễn Quốc Việt** (MSSV: 52300267) – Phụ trách: Kiến trúc ZTNA, Gateway Pomerium, Identity Keycloak, SIEM Wazuh
  - **Nguyễn Hoàng Việt** (MSSV: 52300268) – Phụ trách: Hạ tầng Proxmox VE, OpenEMR RBAC, MariaDB TDE, PKI Easy-RSA
- **Giảng viên hướng dẫn:** TS. Bùi Quy Anh
- **Thời lượng dự kiến:** 20 – 25 phút
- **Vị trí lưu trữ:** `DU_AN_CNTT/SCRUM4/`

---

## MỤC LỤC TỔNG QUAN

1. [THÔNG TIN CHUNG & BỐI CẢNH DỰ ÁN](#1-thông-tin-chung--bối-cảnh-dự-án)
2. [BẢNG TÀI KHOẢN, THIẾT BỊ VÀ THÔNG SỐ DEMO](#2-bảng-tài-khoản-thiết-bị-và-thông-số-demo)
3. [CHECKLIST CHUẨN BỊ TRƯỚC BUỔI DEMO (PRE-FLIGHT CHECKLIST)](#3-checklist-chuẩn-bị-trước-buổi-demo-pre-flight-checklist)
4. [KỊCH BẢN CHI TIẾT THEO 6 PHÂN ĐOẠN DEMO](#4-kịch-bản-chi-tiết-theo-6-phân-đoạn-demo)
   - [Phần 1: Hạ tầng mạng & Phân đoạn Micro-segmentation (Networks)](#phần-1-hạ-tầng-mạng--phân-đoạn-micro-segmentation-networks)
   - [Phần 2: Trụ cột Thiết bị (Devices) — Xác thực mTLS & Device Trust](#phần-2-trụ-cột-thiết-bị-devices--xác-thực-mtls--device-trust)
   - [Phần 3: Trụ cột Danh tính (Identity) — Keycloak IAM, MFA TOTP & Session Security](#phần-3-trụ-cột-danh-tính-identity--keycloak-iam-mfa-totp--session-security)
   - [Phần 4: Trụ cột Ứng dụng & Nghiệp vụ (Applications & Workloads) — 5 Luồng BF-01 đến BF-05](#phần-4-trụ-cột-ứng-dụng--nghiệp-vụ-applications--workloads--5-luồng-bf-01-đến-bf-05)
   - [Phần 5: Trụ cột Dữ liệu (Data) — Bảo vệ Đa tầng (Transit & At-Rest)](#phần-5-trụ-cột-dữ-liệu-data--bảo-vệ-đa-tầng-transit--at-rest)
   - [Phần 6: Trụ cột Giám sát An ninh (Visibility & Analytics) — Wazuh SIEM/XDR](#phần-6-trụ-cột-giám-sát-an-ninh-visibility--analytics--wazuh-siemxdr)
5. [MA TRẬN ĐỐI CHIẾU TIÊU CHUẨN (TRACEABILITY MATRIX)](#5-ma-trận-đối-chiếu-tiêu-chuẩn-traceability-matrix)
6. [BẢNG XỬ LÝ SỰ CỐ NHANH TRONG BUỔI DEMO (TROUBLESHOOTING CHEAT SHEET)](#6-bảng-xử-lý-sự-cố-nhanh-trong-buổi-demo-troubleshooting-cheat-sheet)

---

## 1. THÔNG TIN CHUNG & BỐI CẢNH DỰ ÁN

### 1.1. Mục đích của Buổi Trình diễn (Demo)
Buổi trình diễn nhằm mục đích thực chứng (Proof of Concept) rằng kiến trúc **Zero Trust Architecture (ZTA)** theo chuẩn **NIST SP 800-207** và **Khung trưởng thành 5 trụ cột CISA** đã được hiện thực hóa thành công trên hệ thống quản lý Hồ sơ Y tế Điện tử (**OpenEMR**). 

Hệ thống chứng minh nguyên tắc cốt lõi:
> **"Never Trust, Always Verify" (Không bao giờ tin tưởng ngầm định, Luôn luôn xác minh tường minh)**
> và **"Assume Breach" (Luôn giả định hệ thống đã bị xâm nhập)**.

Mọi truy cập đều phải trải qua **3 vòng kiểm soát độc lập**:
1. **Vòng 1 - Thiết bị (Device Trust):** Phải có Client Certificate hợp lệ được cấp bởi CA nội bộ bệnh viện (mTLS).
2. **Vòng 2 - Danh tính (Identity Trust):** Phải xác thực tài khoản + Mật khẩu + Mã xác thực đa yếu tố (TOTP 6 số từ Google Authenticator) qua Keycloak IAM, nhận JWT mang đúng vai trò (Role Claims).
3. **Vòng 3 - Ngữ cảnh Nghiệp vụ (Context & Least Privilege):** Phải thỏa mãn phân quyền chi tiết (ACL/RBAC/ABAC) bên trong OpenEMR: đúng vai trò, đúng phạm vi phụ trách bệnh nhân, đúng quy tắc chuyển giao hồ sơ và tính bất biến dữ liệu y khoa (WORM).

### 1.2. Phân công Trình bày (Presenter Allocation)
- **Quốc Việt (Người dẫn 1):** Phụ trách tổng quan kiến trúc, Cổng uỷ quyền Pomerium, Xác thực mTLS thiết bị, Keycloak IAM/MFA, và Giám sát an ninh Wazuh SIEM.
- **Hoàng Việt (Người dẫn 2):** Phụ trách hạ tầng phân đoạn mạng Proxmox Firewall, nghiệp vụ OpenEMR (5 luồng BF-01 đến BF-05), mã hóa CSDL MariaDB TDE, và kiểm tra tính toàn vẹn gói tin (Anti-Sniffing).

---

## 2. BẢNG TÀI KHOẢN, THIẾT BỊ VÀ THÔNG SỐ DEMO

### 2.1. Danh sách Tài khoản Kiểm thử Hệ thống

| STT | Username | Mật khẩu mặc định | Vai trò (Role) | Phòng ban / Ngữ cảnh | Mục đích trong Demo |
|:---:|:---|:---|:---|:---|:---|
| 1 | `receptionist01` | `Receptionist@2026` | `Receptionist` (Lễ tân) | Khoa Tiếp nhận | Demo BF-01 (Tạo BN, tạo lượt khám; Bị chặn xem chẩn đoán/xét nghiệm) |
| 2 | `doctor01` | `Doctor@2026` | `Doctor` (Bác sĩ) | Khoa Tim mạch (Cardiology) | Demo BF-02 (Khám BN thuộc phạm vi; Bị chặn sửa BN ngoài phạm vi) |
| 3 | `doctor02` | `Doctor@2026` | `Doctor` (Bác sĩ) | Khoa Nội tổng quát | Dùng làm bác sĩ đối chứng (phụ trách BN khác) |
| 4 | `lab_tech01` | `Labtech@2026` | `Lab` (KTV Xét nghiệm) | Khoa Huyết học | Demo BF-03 (Nhập KQ xét nghiệm, Confirm; Bị chặn sửa sau confirm) |
| 5 | `records_staff01`| `Records@2026` | `Records` (NV Hồ sơ 1) | Phòng Kế hoạch - Tổng hợp | Demo BF-04 & BF-05 (Chỉ xem hồ sơ được assign; Mất quyền khi reassign) |
| 6 | `records_staff02`| `Records@2026` | `Records` (NV Hồ sơ 2) | Phòng Kế hoạch - Tổng hợp | Demo BF-05 (Nhận quyền sau khi Supervisor reassign) |
| 7 | `supervisor01` | `Supervisor@2026` | `Supervisor` (Giám sát) | Trưởng phòng KHTH | Demo BF-05 (Phân công & chuyển giao hồ sơ; Không xem chuyên môn) |
| 8 | `itadmin01` | `ITAdmin@2026` | `ITAdmin` (Quản trị IT)| Phòng CNTT | Demo Segregation of Duties (Quản trị hệ thống; Bị chặn xem bệnh án) |

### 2.2. Phân loại Thiết bị Đầu cuối (Device Matrix)

| Thiết bị Demo | Trạng thái Chứng chỉ (mTLS) | Địa chỉ IP / Mạng | Trạng thái Tin cậy | Kết quả Mong đợi khi truy cập |
|:---|:---|:---|:---|:---|
| **Máy Trạm A (Trusted Workstation)** | Đã cài đặt `doctor01.pfx` do CA Easy-RSA nội bộ cấp | VLAN 10 (Client: `10.10.10.105`) | **TRUSTED** | Hoàn thành TLS Handshake -> Chuyển sang Keycloak Login -> Cho phép truy cập OpenEMR |
| **Máy Trạm B (Untrusted / Attacker)** | **KHÔNG** có Client Certificate hoặc Cert giả mạo | VLAN 10 hoặc Internet | **UNTRUSTED** | **BỊ CHẶN NGAY TẠI TLS** (`ERR_BAD_SSL_CLIENT_AUTH_CERT`). Không chạm được tới Keycloak |

### 2.3. Quy hoạch Hạ tầng Mạng & Địa chỉ Dịch vụ

| Node / Máy ảo | VMID | VLAN ID | IP Address | Port dịch vụ | Vai trò trong Kiến trúc Zero Trust |
|:---|:---:|:---:|:---|:---|:---|
| `pve01` (Host) | - | VLAN 60 | `10.10.60.10` | 8006 (HTTPS), 22 (SSH) | Nền tảng ảo hóa Proxmox VE 9.2-1 & Tường lửa liên vùng |
| `zt-pomerium01`| 101 | VLAN 20 | `10.10.20.10` | 443 (HTTPS), 80 (HTTP) | **PEP (Policy Enforcement Point)** - Cổng uỷ quyền mTLS & OIDC |
| `zt-keycloak01`| 102 | VLAN 30 | `10.10.30.10` | 8443 (HTTPS), 8080 (HTTP)| **PDP / IdP** - Xác thực tập trung, Quản lý vai trò & MFA OTP |
| `zt-wazuh01` | 103 | VLAN 30 | `10.10.30.20` | 443 (Web UI), 1514/1515 | **Visibility & Analytics** - Giám sát an ninh SIEM/XDR tập trung |
| `emr-app01` | 100 | VLAN 40 | `10.10.40.10` | 443 (HTTPS), 80 (HTTP) | **Application Server** - Ứng dụng OpenEMR v7.0.2 |
| `emr-db01` | 104 | VLAN 50 | `10.10.50.10` | 3306 (TCP MySQL) | **Data Layer** - MariaDB v10.11 với Transparent Data Encryption (TDE)|

---

## 3. CHECKLIST CHUẨN BỊ TRƯỚC BUỔI DEMO (PRE-FLIGHT CHECKLIST)

Trước khi bắt đầu bài thuyết trình trước Hội đồng / Giảng viên, sinh viên thực hiện kiểm tra nhanh danh sách sau:

- [ ] **1. Kiểm tra 5 Máy ảo trên Proxmox:** Đảm bảo cả 5 VM (`100, 101, 102, 103, 104`) đều có trạng thái **Running (màu xanh)** trên Web GUI `https://10.10.60.10:8006`.
- [ ] **2. Kiểm tra Cổng Pomerium PEP:** Truy cập thử `curl -k https://10.10.20.10` từ console VM101 xác nhận service `pomerium` đang active.
- [ ] **3. Kiểm tra Keycloak Realm:** Đảm bảo Realm `medical-realm` đã import đủ 8 tài khoản và 6 roles; kiểm tra ứng dụng Google Authenticator trên điện thoại đã scan mã QR OTP cho các user demo (`doctor01`, `receptionist01`, `lab_tech01`, `supervisor01`, `records_staff01`, `itadmin01`).
- [ ] **4. Kiểm tra Cài đặt Chứng chỉ Thiết bị:**
  - Máy trình duyệt chính (Chrome/Edge): Đã import chứng chỉ `doctor-device.p12` hoặc `.pfx` vào Personal Certificates.
  - Trình duyệt ẩn danh (Incognito) hoặc trình duyệt phụ (Firefox): **Chưa import** cert để demo kịch bản Deny thiết bị.
- [ ] **5. File hosts phân giải tên miền nội bộ:** Máy client đã cấu hình trong `C:\Windows\System32\drivers\etc\hosts`:
  ```text
  10.10.20.10  emr.hospital.local authenticate.hospital.local openemr.medical.local
  10.10.30.10  keycloak.hospital.local
  10.10.30.20  wazuh.hospital.local
  ```
- [ ] **6. Dữ liệu bệnh nhân mẫu trong OpenEMR:**
  - Bệnh nhân A: `Nguyễn Văn A` (Mã BN: `BN-001`, Khoa Tim mạch, phân công cho `doctor01`).
  - Bệnh nhân B: `Trần Thị B` (Mã BN: `BN-002`, Khoa Nội, phân công cho `doctor02`).
  - Bệnh nhân C: `Lê Văn C` (Mã BN: `BN-003`, Chưa phân công cho nhân viên hồ sơ).

---

## 4. KỊCH BẢN CHI TIẾT THEO 6 PHÂN ĐOẠN DEMO

```
+---------------------------------------------------------------------------------------------------------+
|                                    TỔNG THỂ TIẾN TRÌNH TRÌNH DIỄN (25 PHÚT)                            |
|                                                                                                         |
|  [PHẦN 1: MẠNG & FW]  ->  [PHẦN 2: mTLS DEVICE]  ->  [PHẦN 3: IAM & MFA]                                |
|   (Proxmox 6 VLANs         (Chứng chỉ thiết bị        (Keycloak OTP MFA                                 |
|    Chặn Bypass Direct)      Chặn máy không cert)       Cấp Token OIDC)                                  |
|                                                                                                         |
|                                         |                                                               |
|                                         v                                                               |
|                                                                                                         |
|  [PHẦN 4: 5 LUỒNG NGHIỆP VỤ BF-01 -> BF-05]  ->  [PHẦN 5: BẢO VỆ DỮ LIỆU]  ->  [PHẦN 6: SIEM WAZUH]    |
|   (Lễ tân -> Bác sĩ -> KTV Xét nghiệm             (Anti-Sniffing Wireshark       (Phát hiện Brute Force |
|    Hồ sơ bệnh án & Thu hồi quyền động              MariaDB TDE Mã hóa ổ cứng)     FIM cảnh báo sửa file)|
+---------------------------------------------------------------------------------------------------------+
```

---

### PHẦN 1: HẠ TẦNG MẠNG & PHÂN ĐOẠN MICRO-SEGMENTATION (NETWORKS)
*Thời lượng: 3 phút | Người trình bày: Hoàng Việt | Mục tiêu: Chứng minh tính cô lập 6 VLAN và tường lửa chặn bypass.*

#### Kịch bản 1.1: Trình diễn 6 Phân vùng VLAN và 5 VM Skeleton trên Proxmox VE
> **Lời dẫn thuyết trình:**  
> *"Kính thưa Thầy, bước đầu tiên em xin trình diễn hạ tầng mạng của hệ thống. Khác với mô hình bệnh viện truyền thống dùng mạng phẳng (Flat Network) nơi mọi máy tính đều có thể quét thấy nhau, đồ án chúng em triển khai Micro-segmentation với 6 vùng mạng ảo độc lập trên cầu nối ảo `vmbr1` VLAN-aware của Proxmox VE 9.2-1."*

- **Thao tác 1.1.1:** Mở trình duyệt truy cập Web UI Proxmox VE: `https://10.10.60.10:8006` (Đăng nhập tài khoản `root`).
- **Thao tác 1.1.2:** Vào mục `pve01` -> `System` -> `Network`.
  - Chỉ rõ cầu nối `vmbr1` với cờ `bridge-vlan-aware = yes`.
  - Hiển thị danh sách 6 VLAN interfaces: VLAN 10 (Client), VLAN 20 (DMZ), VLAN 30 (Security), VLAN 40 (App), VLAN 50 (DB), VLAN 60 (Management).
- **Thao tác 1.1.3:** Vào mục `pve01` -> Danh sách VM:
  - Chỉ rõ 5 máy ảo Skeleton (VMID 100 đến 104) đang chạy với đúng card mạng VLAN tương ứng.

#### Kịch bản 1.2: Chứng minh Luồng Mạng Hợp lệ (ALLOW)
> **Lời dẫn thuyết trình:**  
> *"Theo chính sách Zero Trust, các máy chủ chỉ được phép giao tiếp theo các luồng nghiệp vụ tối thiểu đã được định nghĩa tường minh."*

- **Thao tác 1.2.1:** Mở terminal trên VM101 (`zt-pomerium01`), thực hiện kiểm tra kết nối tới Keycloak và OpenEMR:
  ```bash
  # Kết nối từ Pomerium Gateway tới Keycloak (OIDC):
  curl -I -k https://10.10.30.10:8443/realms/medical-realm/.well-known/openid-configuration
  # -> Kết quả: HTTP/2 200 OK [ALLOW]

  # Kết nối từ Pomerium Gateway tới OpenEMR:
  curl -I http://10.10.40.10:80
  # -> Kết quả: HTTP/1.1 200 OK hoặc 302 Found [ALLOW]
  ```
- **Thao tác 1.2.2:** Mở terminal trên VM100 (`emr-app01`), kiểm tra kết nối CSDL sang VM104:
  ```bash
  nc -zv 10.10.50.10 3306
  # -> Kết quả: Connection to 10.10.50.10 3306 port [tcp/mysql] succeeded! [ALLOW]
  ```

#### Kịch bản 1.3: [MINH CHỨNG ZERO TRUST] Tường lửa Chặn Bypass Truy cập Trực tiếp (DENY)
> **Lời dẫn thuyết trình:**  
> *"Bây giờ, em xin mô phỏng tình huống tấn công: Kẻ tấn công ngồi tại Client Zone (VLAN 10) biết được địa chỉ IP nội bộ của máy chủ OpenEMR (10.10.40.10) hoặc MariaDB (10.10.50.10) và cố tình kết nối trực tiếp để vượt mặt (Bypass) Cổng uỷ quyền Pomerium."*

- **Thao tác 1.3.1 (Thử bypass vào OpenEMR):** Từ máy Client (VLAN 10), mở PowerShell chạy lệnh:
  ```powershell
  curl https://10.10.40.10 --connect-timeout 5
  ```
  - **Kết quả hiển thị trên màn hình:** `Connection timed out` hoặc `Unable to connect to remote server`.
  - **Khẳng định ZT:** Quy tắc tường lửa Proxmox Firewall `FW-03` đã DROP hoàn toàn gói tin từ VLAN 10 sang VLAN 40. **[DENY THÀNH CÔNG]**
- **Thao tác 1.3.2 (Thử bypass vào CSDL MariaDB):** Từ máy Client, chạy lệnh:
  ```powershell
  Test-NetConnection -ComputerName 10.10.50.10 -Port 3306
  ```
  - **Kết quả hiển thị trên màn hình:** `TcpTestSucceeded : False`. Gói tin bị drop hoàn toàn. **[DENY THÀNH CÔNG]**

---

### PHẦN 2: TRỤ CỘT THIẾT BỊ (DEVICES) — XÁC THỰC mTLS & DEVICE TRUST
*Thời lượng: 3 phút | Người trình bày: Quốc Việt | Mục tiêu: Chứng minh chỉ thiết bị có chứng chỉ mới được kết nối.*

#### Kịch bản 2.1: [DENY] Thiết bị Chưa tin cậy (Thiếu Chứng chỉ) Bị từ chối tại TLS Handshake
> **Lời dẫn thuyết trình:**  
> *"Theo nguyên tắc Device Trust của CISA, hệ thống không chỉ xác thực người dùng mà bắt buộc phải xác thực thiết bị điểm cuối. Bây giờ, em sử dụng một trình duyệt không được cài đặt chứng chỉ máy trạm của bệnh viện để truy cập vào Cổng dịch vụ y tế."*

- **Thao tác 2.1.1:** Mở trình duyệt ẩn danh (Firefox hoặc Chrome Incognito không có cert).
- **Thao tác 2.1.2:** Nhập địa chỉ: `https://emr.hospital.local` (hoặc `https://openemr.medical.local`).
- **Kết quả quan sát trên màn hình:**
  - Trình duyệt ngay lập tức hiển thị thông báo lỗi bảo mật TLS Handshake:
    `400 Bad Request - No required SSL certificate was sent` hoặc `ERR_BAD_SSL_CLIENT_AUTH_CERT`.
  - Không hề có giao diện đăng nhập hay cơ hội nhập username/password!
- **Phân tích của người thuyết trình:**
  - Pomerium PEP kiểm tra chứng chỉ `downstream_client_ca`. Do thiết bị không gửi kèm chứng chỉ ký bởi Easy-RSA CA nội bộ, kết nối bị cắt đứt ngay tại tầng giao vận TLS (Layer 4/Layer 7). Điều này ngăn chặn 100% các thiết bị cá nhân lạ của tin tặc kết nối vào hệ thống.

#### Kịch bản 2.2: [ALLOW] Thiết bị Được Cấp phép (Trusted Workstation với mTLS)
> **Lời dẫn thuyết trình:**  
> *"Bây giờ, em chuyển sang máy trạm y tế đã được Phòng CNTT bệnh viện chứng thực và cài đặt Client Certificate cá thể mang tên `doctor-workstation.p12`."*

- **Thao tác 2.2.1:** Mở trình duyệt chính (đã cài đặt chứng chỉ trong Windows Certificate Store: `certmgr.msc` -> `Personal`).
- **Thao tác 2.2.2:** Truy cập `https://emr.hospital.local`.
- **Kết quả quan sát trên màn hình:**
  - Hộp thoại trình duyệt xuất hiện: *"Select a certificate for authentication"* -> Chọn chứng chỉ `doctor01@hospital.local` -> Nhấn **OK**.
  - Bắt tay mTLS thành công lập tức! Trình duyệt chuyển hướng mượt mà sang giao diện đăng nhập tập trung **Keycloak Identity Provider**. **[ALLOW THÀNH CÔNG]**

---

### PHẦN 3: TRỤ CỘT DANH TÍNH (IDENTITY) — KEYCLOAK IAM, MFA TOTP & SESSION SECURITY
*Thời lượng: 4 phút | Người trình bày: Quốc Việt | Mục tiêu: Xác thực rõ ràng, MFA bắt buộc, cấp JWT claims.*

#### Kịch bản 3.1: [DENY] Xác thực Thất bại khi Sai Mật khẩu (Explicit Verification)
- **Thao tác 3.1.1:** Tại màn hình đăng nhập Keycloak, nhập:
  - Username: `doctor01`
  - Password: `SaiMatKhau123!@#`
- **Kết quả:** Keycloak báo lỗi: *"Invalid username or password"*. Phiên đăng nhập không được khởi tạo. Sự kiện thất bại được ghi nhận vào Event Log của Keycloak. **[DENY]**

#### Kịch bản 3.2: [DENY / ALLOW] Bắt buộc Xác thực Đa yếu tố (MFA / TOTP Enforcement)
> **Lời dẫn thuyết trình:**  
> *"Để đối phó với nguy cơ lộ lọt mật khẩu qua phishing, Zero Trust bắt buộc lớp phòng thủ thứ hai: Multi-Factor Authentication. Mật khẩu đúng vẫn chưa đủ để vào hệ thống."*

- **Thao tác 3.2.1:** Nhập đúng credentials:
  - Username: `doctor01`
  - Password: `Doctor@2026` -> Nhấn **Log In**.
- **Thao tác 3.2.2 (Thử nghiệm Deny OTP):**
  - Màn hình chuyển sang yêu cầu: *"Enter 6-digit code from your authenticator application"*.
  - Nhập sai mã OTP: `111222` -> Nhấn **Submit**.
  - **Kết quả:** Keycloak báo lỗi *"Invalid authenticator code"*, kiên quyết không cấp Token. **[DENY]**
- **Thao tác 3.2.3 (Thử nghiệm Allow OTP):**
  - Mở ứng dụng **Google Authenticator** trên điện thoại thông minh (hoặc công cụ TOTP giả lập).
  - Lấy mã 6 số hiện tại (ví dụ: `849 201`), nhập vào ô và nhấn **Submit**.
  - **Kết quả:** Keycloak xác thực danh tính thành công! **[ALLOW]**

#### Kịch bản 3.3: Phân tích JWT Token & Định tuyến Pomerium Policy Route
> **Lời dẫn thuyết trình:**  
> *"Sau khi người dùng vượt qua MFA, Keycloak phát hành một JWT Access Token có chữ ký số. Cổng Pomerium sẽ đọc payload của token này để ra quyết định uỷ quyền (Policy Decision)."*

- **Thao tác 3.3.1:** Mở Developer Tools trên trình duyệt (F12) -> Tab Application/Cookies -> Kiểm tra cookie `_pomerium`.
- **Thao tác 3.3.2:** Trình chiếu nội dung giải mã của Access Token (Decode JWT):
  ```json
  {
    "preferred_username": "doctor01",
    "email": "doctor01@hospital.local",
    "realm_access": {
      "roles": ["Doctor"]
    },
    "department": "Cardiology"
  }
  ```
- **Thao tác 3.3.3:** Pomerium đối chiếu với file cấu hình `/etc/pomerium/config.yaml`:
  ```yaml
  routes:
    - from: https://emr.hospital.local
      to: http://10.10.40.10:80
      policy:
        - allow:
            and:
              - claim/realm_access.roles: Doctor
  ```
  - Do `realm_access.roles` chứa role `Doctor`, Pomerium cho phép uỷ quyền và forward traffic tới giao diện OpenEMR. Trình duyệt tải thành công trang chủ OpenEMR!

#### Kịch bản 3.4: [DENY] Kiểm soát Phiên làm việc (Session Invalidation)
- **Thao tác:** Trên Developer Tools (F12), xoá cookie `_pomerium` (mô phỏng token hết hạn) -> Nhấn F5 tải lại trang.
- **Kết quả:** Pomerium lập tức chặn kết nối tới OpenEMR và redirect người dùng về trang đăng nhập Keycloak. **[DENY]**

---

### PHẦN 4: TRỤ CỘT ỨNG DỤNG & NGHIỆP VỤ (APPLICATIONS & WORKLOADS) — 5 LUỒNG BF-01 ĐẾN BF-05
*Thời lượng: 8 phút | Người trình bày: Hoàng Việt | Mục tiêu: Chứng minh phân quyền nghiệp vụ RBAC, Least Privilege, Separation of Duties và Medical Records Assignment.*

#### Kịch bản 4.1: Luồng BF-01 — Lễ tân Tiếp nhận Bệnh nhân & Tạo Lượt khám
> **Lời dẫn thuyết trình:**  
> *"Bây giờ, em đăng nhập với vai trò Lễ tân `receptionist01`. Theo ma trận phân quyền Least Privilege, Lễ tân chỉ được thao tác trên thông tin hành chính và tạo lượt khám, tuyệt đối không được tiếp cận dữ liệu chuyên môn."*

- **Thao tác 4.1.1 (Allow):**
  - Đăng nhập `receptionist01` (qua mTLS + Keycloak + OTP).
  - Vào menu `Patient/Client` -> `New/Search`.
  - Tạo mới bệnh nhân: Họ tên `Nguyễn Văn A`, Giới tính Nam, Ngày sinh `15/08/1985`. Nhấn **Save**.
  - Vào mục `Visits` -> Tạo lượt khám mới (**Create Encounter**) cho Bệnh nhân A tại Khoa Tim mạch.
  - **Kết quả:** Thao tác tạo bệnh nhân và lượt khám thành công. **[ALLOW]**
- **Thao tác 4.1.2 (Deny - Least Privilege):**
  - Tại hồ sơ bệnh nhân A, Lễ tân cố tình bấm vào mục **Medical Issues / Diagnosis (Chẩn đoán)** hoặc **Lab Results (Xét nghiệm)**.
  - **Kết quả:** Hệ thống báo lỗi `Access Denied` hoặc các trường này bị ẩn/khóa chỉnh sửa hoàn toàn. Lễ tân không thể nhập hay xem bệnh lý. **[DENY THÀNH CÔNG]**

#### Kịch bản 4.2: Luồng BF-02 — Bác sĩ Khám bệnh & Ngữ cảnh Phạm vi Phụ trách (Context-Aware)
> **Lời dẫn thuyết trình:**  
> *"Tiếp theo, em đăng nhập tài khoản Bác sĩ `doctor01` (Khoa Tim mạch). Bác sĩ sẽ tiến hành khám bệnh cho Bệnh nhân A được phân công, và em sẽ chứng minh cơ chế Context-Aware chặn bác sĩ sửa bệnh án ngoài phạm vi."*

- **Thao tác 4.2.1 (Allow - Bệnh nhân thuộc phạm vi):**
  - Đăng xuất Lễ tân, đăng nhập tài khoản `doctor01` (mTLS + Keycloak + OTP).
  - Mở hồ sơ `Nguyễn Văn A` -> Mở lượt khám Tim mạch vừa tạo.
  - Nhập thông tin khám lâm sàng:
    + **SOAP Note:** S (Tức ngực, khó thở), O (Huyết áp 140/90 mmHg), A (Theo dõi Cơn đau thắt ngực), P (Chỉ định điện tâm đồ và xét nghiệm máu).
    + **Diagnosis:** Chọn mã ICD-10 `I20.9 - Angina pectoris, unspecified`.
    + **Lab Order:** Tạo chỉ định xét nghiệm `Tổng phân tích tế bào máu ngoại vi`.
  - Nhấn **Save Encounter**. Dữ liệu được ghi nhận thành công vào CSDL. **[ALLOW]**
- **Thao tác 4.2.2 (Deny - Bệnh nhân NGOÀI phạm vi phụ trách):**
  - Bác sĩ `doctor01` tìm kiếm và mở hồ sơ của Bệnh nhân B (`Trần Thị B`, thuộc Khoa Nội do `doctor02` phụ trách).
  - `doctor01` cố gắng chỉnh sửa chẩn đoán hoặc tạo ghi chú lâm sàng trên hồ sơ này.
  - **Kết quả:** Hệ thống từ chối quyền cập nhật: *"You do not have permission to modify clinical records of patients outside your assignment"* hoặc nút Save bị vô hiệu hóa. **[DENY THÀNH CÔNG]**

#### Kịch bản 4.3: Luồng BF-03 — Kỹ thuật viên Xét nghiệm & Tính Bất biến Dữ liệu (WORM)
> **Lời dẫn thuyết trình:**  
> *"Luồng BF-03 thể hiện nguyên tắc Separation of Duties giữa Bác sĩ và Kỹ thuật viên xét nghiệm, đồng thời áp dụng nguyên tắc WORM (Write Once, Read Many) bảo đảm tính toàn vẹn hồ sơ y tế."*

- **Thao tác 4.3.1 (Allow - Nhập kết quả xét nghiệm):**
  - Đăng xuất, đăng nhập tài khoản `lab_tech01` (vai trò Kỹ thuật viên xét nghiệm).
  - Vào menu `Procedures` -> `Electronic Reports / Orders`.
  - Mở chỉ định xét nghiệm máu của Bệnh nhân A.
  - Nhập các chỉ số xét nghiệm: `RBC = 4.8 T/L`, `WBC = 8.5 G/L`, `Hemoglobin = 145 g/L`.
  - Nhấn nút **Confirm / Finalize Results** (Ký xác nhận kết quả).
  - **Kết quả:** Kết quả xét nghiệm chuyển sang trạng thái `FINAL / CONFIRMED`. **[ALLOW]**
- **Thao tác 4.3.2 (Deny - Chặn chỉnh sửa sau khi đã xác nhận):**
  - KTV cố tình click đúp vào các ô kết quả vừa nhập để thay đổi số liệu.
  - **Kết quả:** Toàn bộ trường dữ liệu chuyển sang chế độ `Read-Only`. Hệ thống từ chối mọi yêu cầu chỉnh sửa hồi tố nhằm chống gian lận kết quả y khoa. **[DENY]**
- **Thao tác 4.3.3 (Deny - Chặn KTV sửa chẩn đoán của Bác sĩ):**
  - `lab_tech01` thử mở mục Chẩn đoán ICD-10 của Bác sĩ -> Bị từ chối quyền truy cập (Access Denied). **[DENY]**

#### Kịch bản 4.4: Luồng BF-04 & BF-05 — Phân công Hồ sơ & Thu hồi Quyền Truy cập Động (Dynamic Access Revocation)
> **Lời dẫn thuyết trình:**  
> *"Đây là điểm nhấn đặc biệt trong đồ án của chúng em: Cơ chế Medical Records Assignment. Nhân viên quản lý hồ sơ chỉ được đọc bệnh án khi được Giám sát viên (Supervisor) phân công. Khi Supervisor chuyển giao hồ sơ sang nhân viên khác, quyền truy cập của nhân viên cũ bị thu hồi NGAY LẬP TỨC (Dynamic Revocation) theo chuẩn Just-In-Time Access."*

- **Thao tác 4.4.1 (Supervisor phân công - BF-05):**
  - Đăng nhập tài khoản Giám sát viên `supervisor01`.
  - Vào giao diện quản lý `Medical Records Assignment`.
  - Phân công hồ sơ Bệnh nhân A cho nhân viên `records_staff01`. Nhấn **Assign**. **[ALLOW]**
- **Thao tác 4.4.2 (Nhân viên được phân công xem hồ sơ - BF-04 Allow):**
  - Đăng nhập tài khoản `records_staff01`.
  - Mở hồ sơ Bệnh nhân A -> Mở xem bệnh án, phiếu xét nghiệm thành công. **[ALLOW]**
- **Thao tác 4.4.3 (Nhân viên thử xem hồ sơ CHƯA phân công - BF-04 Deny):**
  - `records_staff01` cố gắng mở hồ sơ Bệnh nhân C (`Lê Văn C` - chưa được phân công).
  - **Kết quả:** Màn hình trả về lỗi `HTTP 403 Forbidden` hoặc thông báo *"Record unassigned or not permitted"*. **[DENY THÀNH CÔNG]**
- **Thao tác 4.4.4 [ĐIỂM NHẤN] Chuyển giao hồ sơ & Thu hồi quyền tức thì (Dynamic Revocation):**
  - Giám sát viên `supervisor01` thực hiện **Reassign** hồ sơ Bệnh nhân A từ `records_staff01` sang `records_staff02`.
  - Quay lại phiên làm việc của `records_staff01`: Nhấn F5 làm mới trang Bệnh nhân A.
  - **Kết quả trực tiếp:** Ngay lập tức màn hình chuyển thành `403 Access Denied`! Nhân viên cũ bị tước quyền ngay lập tức trong thời gian thực mà không cần đăng xuất! **[DYNAMIC REVOCATION THÀNH CÔNG]**
  - Đăng nhập `records_staff02`: Mở hồ sơ Bệnh nhân A thành công! **[ALLOW]**

#### Kịch bản 4.5: Nguyên tắc Segregation of Duties — IT Admin Quản trị nhưng KHÔNG Xem Bệnh án
> **Lời dẫn thuyết trình:**  
> *"Trong môi trường Zero Trust, người quản trị hạ tầng (IT Admin) có toàn quyền kỹ thuật nhưng không được phép xâm phạm tính riêng tư của dữ liệu y tế (Privacy of Patient Data)."*

- **Thao tác 4.5.1:** Đăng nhập tài khoản Quản trị viên `itadmin01`.
- **Thao tác 4.5.2 (Allow chức năng IT):** Quản trị viên vào được menu `Administration` -> `Users`, `Globals`, `System Logs`. **[ALLOW]**
- **Thao tác 4.5.3 (Deny xem dữ liệu bệnh nhân):** IT Admin cố tình bấm vào menu `Patient/Client` -> Danh sách bệnh án hoặc tìm kiếm hồ sơ bệnh nhân.
- **Kết quả:** Hệ thống báo lỗi phân quyền hoặc không hiển thị nội dung chuyên môn bệnh án. IT Admin bị tước quyền đọc thông tin sức khỏe cá nhân theo chuẩn HIPAA. **[DENY THÀNH CÔNG]**

---

### PHẦN 5: TRỤ CỘT DỮ LIỆU (DATA) — BẢO VỆ ĐA TẦNG (TRANSIT & AT-REST)
*Thời lượng: 3 phút | Người trình bày: Hoàng Việt | Mục tiêu: Chứng minh chống nghe lén đường truyền và mã hóa ổ đĩa vật lý MariaDB TDE.*

#### Kịch bản 5.1: Chống Nghe lén Mạng Nội bộ (Anti-Sniffing & Data in Transit)
> **Lời dẫn thuyết trình:**  
> *"Theo nguyên tắc Assume Breach, Zero Trust coi mạng LAN nội bộ cũng nguy hiểm như Internet. Nếu một máy trạm trong bệnh viện bị nhiễm mã độc nghe lén (Sniffing/ARP Spoofing), liệu dữ liệu y tế có bị lộ?"*

- **Thao tác 5.1.1:** Trên Proxmox Host hoặc VM trong mạng, bật lệnh bắt gói tin `tcpdump` trên bridge `vmbr1`:
  ```bash
  tcpdump -i vmbr1 -nn -s 0 -X "tcp port 443" -c 10
  ```
- **Thao tác 5.1.2:** Trên trình duyệt client, thực hiện gửi một yêu cầu khám bệnh chứa thông tin nhạy cảm.
- **Thao tác 5.1.3 (Phân tích gói tin):**
  - Toàn bộ nội dung gói tin bắt được đều là chuỗi mã hóa TLS nhị phân lộn xộn (Binary TLS Application Data).
  - Không tìm thấy bất kỳ chuỗi plain-text nào chứa tên bệnh nhân, số CMND hay chẩn đoán bệnh.
  - Chứng minh 100% đường truyền nội bộ được bảo vệ bởi TLS end-to-end. **[DATA IN TRANSIT PROTECTED]**

#### Kịch bản 5.2: Mã hóa Dữ liệu Lưu trữ MariaDB Transparent Data Encryption (Data at Rest)
> **Lời dẫn thuyết trình:**  
> *"Bây giờ, em xin chứng minh kịch bản tồi tệ nhất: Tin tặc đã chiếm được quyền root trên máy chủ CSDL hoặc tháo trộm ổ cứng vật lý mang về nhà. Liệu tin tặc có đọc được hồ sơ bệnh án?"*

- **Thao tác 5.2.1:** SSH vào máy chủ Database `emr-db01` (`10.10.50.10`).
- **Thao tác 5.2.2 (Kiểm tra Plugin TDE):** Đăng nhập MySQL Console kiểm tra tham số:
  ```sql
  SHOW PLUGINS;
  -- Kết quả: Plugin 'file_key_management' trạng thái ACTIVE.

  SHOW VARIABLES LIKE 'innodb_encrypt%';
  -- Kết quả: innodb_encrypt_tables = ON, innodb_encrypt_log = ON.
  ```
- **Thao tác 5.2.3 (Thử trích xuất dữ liệu trực tiếp từ file ổ đĩa):**
  - Thoát ra shell Linux, chạy lệnh `strings` để quét tìm dữ liệu thô trong file bảng CSDL `/var/lib/mysql/openemr/patient_data.ibd`:
  ```bash
  strings /var/lib/mysql/openemr/patient_data.ibd | grep -i "Nguyen Van A"
  ```
- **Kết quả hiển thị trên màn hình:**
  - Lệnh không trả về bất kỳ kết quả nào! File `.ibd` hoàn toàn là các khối dữ liệu nhị phân đã được mã hóa bằng thuật toán AES-256.
  - Dữ liệu hoàn toàn được bảo vệ ngay cả khi phần cứng lưu trữ bị xâm phạm vật lý! **[DATA AT REST PROTECTED]**

---

### PHẦN 6: TRỤ CỘT GIÁM SÁT AN NINH (VISIBILITY & ANALYTICS) — WAZUH SIEM/XDR
*Thời lượng: 4 phút | Người trình bày: Quốc Việt | Mục tiêu: Giám sát toàn diện, phát hiện Brute Force và cảnh báo FIM thay đổi cấu hình.*

#### Kịch bản 6.1: Tổng quan Năng lực Giám sát Trung tâm trên Wazuh Dashboard
> **Lời dẫn thuyết trình:**  
> *"Trụ cột thứ 5 của Zero Trust là Visibility and Analytics. Hệ thống sử dụng Wazuh SIEM/XDR v4.14.7 để thu thập toàn bộ log và sự kiện an ninh từ tất cả 5 máy chủ về một đầu mối duy nhất."*

- **Thao tác 6.1.1:** Mở trình duyệt truy cập Wazuh Dashboard: `https://10.10.30.20` (Đăng nhập tài khoản IT Admin).
- **Thao tác 6.1.2:** Vào mục `Agents`:
  - Hiển thị đầy đủ **5 Agents Active**: `emr-app01`, `zt-pomerium01`, `zt-keycloak01`, `zt-wazuh01`, `emr-db01`.
  - Không có bất kỳ node nào bị mù thông tin giám sát (Zero Blind Spot).

#### Kịch bản 6.2: Phát hiện Tấn công Dò quét Mật khẩu (SSH Brute Force Attack Detection)
> **Lời dẫn thuyết trình:**  
> *"Bây giờ, em mô phỏng một cuộc tấn công Brute Force SSH vào máy chủ OpenEMR để kiểm tra khả năng phát hiện chủ động của SIEM."*

- **Thao tác 6.2.1:** Từ máy Client, chạy script giả lập tấn công thử mật khẩu SSH sai liên tiếp 6 lần vào `10.10.40.10`:
  ```bash
  for i in {1..6}; do sshpass -p 'WrongPass' ssh -o StrictHostKeyChecking=no test@10.10.40.10; done
  ```
- **Thao tác 6.2.2:** Chuyển ngay sang màn hình Wazuh Dashboard -> Mục `Security Events`.
- **Kết quả quan sát trên màn hình:**
  - Ngay lập tức xuất hiện cảnh báo an ninh màu đỏ:
    - **Rule ID:** `5712` / `5710` (SSHD brute force trying to get access).
    - **Alert Level:** Level 10 (High Severity).
    - **Chi tiết:** Chỉ rõ IP nguồn tấn công, tài khoản bị nhắm tới, số lần thất bại và timestamp chính xác. **[THREAT DETECTED]**

#### Kịch bản 6.3: Giám sát Toàn vẹn Tệp tin (File Integrity Monitoring - FIM)
> **Lời dẫn thuyết trình:**  
> *"Trong kiến trúc Zero Trust, file cấu hình chính sách của Gateway (config.yaml) là tài sản tối mật. Nếu kẻ tấn công đột nhập và sửa file này để tự cấp quyền, Wazuh FIM sẽ phản ứng thế nào?"*

- **Thao tác 6.3.1:** Trên máy chủ `zt-pomerium01`, thực hiện sửa một dòng trong tệp cấu hình chính sách:
  ```bash
  echo "# Attacker modified policy at $(date)" >> /etc/pomerium/config.yaml
  ```
- **Thao tác 6.3.2:** Trên Wazuh Dashboard, mở tab `Integrity Monitoring (FIM)`:
  - Sự kiện cảnh báo xuất hiện tức thời (Rule ID `550` - Integrity checksum changed).
  - Bảng so sánh hiển thị rõ: File `/etc/pomerium/config.yaml`, thời gian thay đổi, mã băm SHA1/MD5 trước và sau khi bị can thiệp.
  - Chứng minh hệ thống kiểm soát toàn vẹn cấu hình (Configuration Integrity) tự động. **[FIM ALERT GENERATED]**

---

## 5. MA TRẬN ĐỐI CHIẾU TIÊU CHUẨN (TRACEABILITY MATRIX)

Bảng dưới đây tổng hợp mối liên kết chặt chẽ giữa Kịch bản Demo thực tế với **5 Trụ cột CISA Zero Trust**, **22 Test Cases trong Báo cáo** và **5 Luồng nghiệp vụ**:

| Phân đoạn Demo | Trụ cột CISA đại diện | Mã Test Case Báo cáo | Luồng Nghiệp vụ (BF) | Nguyên tắc Zero Trust cốt lõi được chứng minh |
|:---|:---|:---:|:---:|:---|
| **Phần 1: Hạ tầng & Firewall** | Networks | TC-06, TC-18 | - | Micro-segmentation, Default Deny, Chặn Bypass |
| **Phần 2: mTLS Chứng chỉ** | Devices | TC-04 | - | Device Trust, Mutual TLS, Chặn thiết bị lạ |
| **Phần 3: Keycloak IAM & MFA** | Identity | TC-01, TC-02, TC-03, TC-05 | - | Explicit Verification, Multi-Factor Auth, Continuous Validation |
| **Phần 4.1: Lễ tân tiếp nhận** | Applications | TC-07, TC-08 | **BF-01** | Role-Based Access Control, Least Privilege |
| **Phần 4.2: Bác sĩ khám bệnh**| Applications | TC-09, TC-10 | **BF-02** | Context-Aware Access, Giới hạn phạm vi phụ trách |
| **Phần 4.3: Xét nghiệm KTV** | Applications | TC-11, TC-12, TC-13 | **BF-03** | Separation of Duties, Data Immutability (WORM) |
| **Phần 4.4: Phân công hồ sơ**| Applications & Data | TC-14, TC-15, TC-21, TC-22 | **BF-04, BF-05** | Medical Records Assignment, Dynamic Access Revocation |
| **Phần 4.5: IT Admin Segregation**| Applications | TC-17 | - | Tách biệt trách nhiệm, Bảo vệ bí mật y tế |
| **Phần 5.1: Chống nghe lén** | Data | TC-20 | - | Encryption in Transit, Anti-Sniffing |
| **Phần 5.2: MariaDB TDE** | Data | TC-20 | - | Encryption at Rest, Bảo vệ dữ liệu vật lý |
| **Phần 6: Giám sát SIEM** | Visibility & Analytics| TC-19 | - | Continuous Monitoring, Threat Detection, File Integrity |

---

## 6. BẢNG XỬ LÝ SỰ CỐ NHANH TRONG BUỔI DEMO (TROUBLESHOOTING CHEAT SHEET)

Nếu xảy ra tình huống bất khả kháng trong buổi trình diễn thực tế (ví dụ: mất kết nối, cache trình duyệt, dịch vụ khởi động chậm), sinh viên bình tĩnh áp dụng các thao tác cứu hộ nhanh sau:

| Sự cố phát sinh | Nguyên nhân khả dĩ | Lệnh xử lý nhanh tại chỗ (Trong 30 giây) |
|:---|:---|:---|
| **1. Trình duyệt không hiện popup chọn Client Certificate** | Cache TLS session của trình duyệt cũ | Mở cửa sổ ẩn danh mới (Incognito) hoặc vào Chrome Settings -> Search "Certificates" -> Xóa cache SSL; hoặc dùng lệnh PowerShell: `Restart-Service -Name "pomerium"` |
| **2. Keycloak báo lỗi OIDC khi redirect từ Pomerium** | Sai lệch thời gian (NTP time drift) giữa các VM | Trên cả VM101 và VM102 chạy lệnh đồng bộ giờ: `sudo timedatectl set-ntp true; sudo chronyc makestep` |
| **3. OpenEMR không kết nối được CSDL MariaDB** | Container MariaDB trên VM104 bị dừng | SSH vào VM104 chạy: `docker restart emr-db01` (hoặc `systemctl restart mariadb`), kiểm tra port: `netstat -tlpn \| grep 3306` |
| **4. Wazuh Dashboard chưa hiển thị sự kiện FIM** | Chu kỳ quét FIM mặc định chưa kích hoạt | Kích hoạt quét tức thì trên VM mục tiêu: `sudo /var/ossec/bin/agent_control -r -u <agent_id>` |
| **5. Quên mã OTP Google Authenticator của tài khoản** | Chưa lưu seed hoặc lệch giờ điện thoại | Truy cập Keycloak Admin Console (`https://10.10.30.10:8443`) bằng tài khoản `admin` -> Vào `Users` -> Chọn user cần sửa -> Tab `Credentials` -> Tắt tạm `OTP` hoặc Reset OTP secret trong 10 giây! |

---

## LỜI KẾT & THÔNG ĐIỆP BẢO VỆ ĐỒ ÁN

> *"Kính thưa Hội đồng và Quý Thầy Cô, qua 6 phân đoạn trình diễn trực tiếp trên hệ sinh thái thực tế, nhóm chúng em đã chứng minh một cách toàn diện rằng: Mô hình Zero Trust không phải là một khẩu hiệu lý thuyết, mà là một giải pháp kiến trúc khả thi, mạnh mẽ và cần thiết để bảo vệ hệ thống y tế hiện đại. Mọi yêu cầu truy cập từ thiết bị, danh tính cho đến từng bản ghi bệnh án đều được kiểm soát nghiêm ngặt theo các nguyên tắc 'Không bao giờ tin tưởng ngầm định', 'Quyền tối thiểu' và 'Luôn giả định bị xâm nhập'. Nhóm chúng em xin chân thành cảm ơn Thầy Bùi Quy Anh đã tận tình hướng dẫn và xin kính mời Hội đồng đặt câu hỏi đóng góp cho dự án."*

---
