# -*- coding: utf-8 -*-
"""
=============================================================
  ZERO TRUST HOSPITAL - BO TEST CASE TOAN DIEN (v2)
  Du an: Bao mat Ho so Y te Dien tu bang Kien truc Zero Trust (Du An CNTT)
  Nhom: 52300267 - Huynh Nguyen Quoc Viet
        52300268 - Nguyen Hoang Viet
  GVHD: TS. Bui Quy Anh
=============================================================
  Chay: python generate_testcases.py
  Output: ZeroTrust_TestCases_Toan_Dien.xlsx
=============================================================

 GIAI THICH COT "MUC DO UU TIEN KIEM THU":
   Cot nay the hien muc do uu tien thuc hien test case,
   duoc danh gia dua tren 3 tieu chi ket hop:
     1. Rui ro bao mat: Neu test nay fail, he thong co bi lo hong bao mat nghiem trong khong?
     2. Tang huong toi core Zero Trust: Test co truc tiep chung minh nguyen tac ZT khong?
     3. Anh huong den toan bo luong he thong: Fail test nay co lam sup do ca quy trinh khong?
   Bieu: Rat cao > Cao > Trung binh
=============================================================
"""

import subprocess
import sys

# Fix Windows console encoding for Unicode / emoji
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                                      errors="replace")

# ── Tự động cài openpyxl nếu chưa có ──────────────────────────
def install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

try:
    import openpyxl
except ImportError:
    print("Dang cai dat openpyxl...")
    install("openpyxl")
    import openpyxl

from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime

# ══════════════════════════════════════════════════════════════
#  DỮ LIỆU TEST CASE
#  Tuple: (giai_doan, stt, ten_test, mo_ta, buoc_thuc_hien,
#          yeu_cau_dau_ra, tieu_chi_zt, muc_do, loai_test,
#          giai_thich_zero_trust)
#
#  GIAI_THICH_ZERO_TRUST (>=20 tu):
#    Giai thich cu the test case nay chung minh / kiem chung
#    nguyen tac nao cua Zero Trust Architecture (NIST SP 800-207,
#    CISA 5 tru cot), va tai sao viec pass test nay la bang chung
#    truc tiep cho nguyen tac do.
# ══════════════════════════════════════════════════════════════

TEST_CASES = [

    # ──────────────────────────────────────────────────────────
    # GIAI ĐOẠN 1 – HẠ TẦNG PROXMOX VE & PHÂN ĐOẠN MẠNG
    # ──────────────────────────────────────────────────────────
    ("GĐ1 – Hạ tầng Proxmox & VLAN", 1,
     "Proxmox VE khởi động thành công",
     "Xác nhận Proxmox VE 9.2-1 đã cài đặt và chạy ổn định trên máy chủ pve01",
     "Truy cập https://10.10.60.10:8006 → đăng nhập admin",
     "Giao diện Web UI Proxmox VE hiển thị trang đăng nhập; version 9.2-1; đăng nhập admin thành công",
     "Networks – Infrastructure", "Cao", "Chức năng",
     "Proxmox VE là nền tảng hypervisor duy nhất lưu trú toàn bộ hạ tầng Zero Trust. "
     "Nếu Proxmox không khởi động được, toàn bộ 5 VM (Pomerium, Keycloak, Wazuh, OpenEMR, MariaDB) "
     "sẽ không hoạt động, khiến mô hình ZTA không thể triển khai. Test này xác nhận nền tảng vật lý "
     "đủ điều kiện để các lớp bảo mật Zero Trust bên trên hoạt động đúng."),

    ("GĐ1 – Hạ tầng Proxmox & VLAN", 2,
     "VLAN-aware bridge vmbr1 cấu hình đúng",
     "Kiểm tra vmbr1 có bridge-vlan-aware=yes, VLAN IDs 10–60 đầy đủ",
     "SSH pve01 → cat /etc/network/interfaces",
     "Output chứa 'bridge-vlan-aware yes' và 'bridge-vids 10 20 30 40 50 60'; vmbr1.60=10.10.60.10/24",
     "Networks – Segmentation", "Cao", "Chức năng",
     "Trụ cột Networks của CISA Zero Trust yêu cầu phân đoạn mạng logic loại bỏ hoàn toàn niềm tin ngầm "
     "định theo vị trí kết nối vật lý. Cầu nối vmbr1 VLAN-aware là nền tảng kỹ thuật duy nhất tạo ra "
     "6 phân vùng cô lập (Client, DMZ, Security, App, DB, Management). Không có VLAN-aware bridge, mọi "
     "VM sẽ nằm chung một mặt phẳng mạng phẳng, phá vỡ toàn bộ kiến trúc ZTA."),

    ("GĐ1 – Hạ tầng Proxmox & VLAN", 3,
     "5 VM skeleton khởi tạo đúng theo Config Contract",
     "Kiểm tra VMID 100–104 đúng VLAN, vCPU, RAM, Disk",
     "Proxmox Web UI → Datacenter → pve01 → xem VM list",
     "5 VM: emr-app01(100/VLAN40), zt-pomerium01(101/VLAN20), zt-keycloak01(102/VLAN30), "
     "zt-wazuh01(103/VLAN30), emr-db01(104/VLAN50); mỗi VM 2vCPU/2048MB/32GB",
     "Networks – Segmentation", "Cao", "Chức năng",
     "Mỗi VM được đặt vào đúng VLAN thể hiện nguyên tắc Microsegmentation của Zero Trust: "
     "mỗi dịch vụ nằm trong một vùng mạng riêng biệt, không có implicit trust giữa các zone. "
     "VM Pomerium ở VLAN20-DMZ đóng vai trò Policy Enforcement Point duy nhất; Keycloak/Wazuh ở "
     "VLAN30-Security; OpenEMR ở VLAN40-App; MariaDB ở VLAN50-DB – cô lập theo chiều sâu."),

    ("GĐ1 – Hạ tầng Proxmox & VLAN", 4,
     "Ping nội bộ cùng VLAN thành công",
     "Xác nhận các VM trong cùng VLAN giao tiếp được với nhau (Keycloak ↔ Wazuh cùng VLAN30)",
     "Từ zt-keycloak01 (10.10.30.10): ping 10.10.30.20 -c 4",
     "Ping thành công, 0% packet loss, RTT < 5ms",
     "Networks – Intra-zone Connectivity", "Trung bình", "Kết nối",
     "Zero Trust không cấm giao tiếp hợp lệ trong cùng security zone – Keycloak và Wazuh đều thuộc "
     "Security Zone (VLAN30) và cần giao tiếp để Wazuh agent trên Keycloak gửi log về Manager. "
     "Test này xác nhận routing nội bộ đúng, là điều kiện tiên quyết để các dịch vụ "
     "telemetry giám sát an ninh hoạt động liên tục theo yêu cầu của trụ cột Visibility & Analytics."),

    ("GĐ1 – Hạ tầng Proxmox & VLAN", 5,
     "Firewall chặn Client bypass Pomerium → OpenEMR trực tiếp",
     "Client VLAN10 KHÔNG thể kết nối TCP/443 thẳng đến OpenEMR 10.10.40.10 (FW-03)",
     "Từ client (10.10.10.x): curl -k https://10.10.40.10 --connect-timeout 5",
     "Kết nối timeout hoặc 'Connection refused'; curl trả lỗi; không có HTTP response từ OpenEMR",
     "Networks – Segmentation / Gateway Enforcement", "Rất cao", "Bảo mật",
     "Đây là test case cốt lõi nhất của Zero Trust Networks. Nguyên tắc 'Never Trust, Always Verify' "
     "yêu cầu KHÔNG có luồng truy cập trực tiếp nào từ người dùng tới tài nguyên ứng dụng mà bỏ qua "
     "Policy Enforcement Point (Pomerium). Nếu test này FAIL, kẻ tấn công có thể bypass toàn bộ lớp "
     "xác thực danh tính, MFA và kiểm soát truy cập chỉ bằng cách biết địa chỉ IP của OpenEMR."),

    ("GĐ1 – Hạ tầng Proxmox & VLAN", 6,
     "Firewall chặn Client kết nối trực tiếp MariaDB",
     "Client KHÔNG thể kết nối TCP/3306 đến MariaDB 10.10.50.10 (FW-07)",
     "Từ client: nc -zv 10.10.50.10 3306 --wait 5",
     "Netcat báo 'Connection refused' hoặc timeout; port 3306 không reachable từ VLAN10",
     "Networks – Segmentation / DB Protection", "Rất cao", "Bảo mật",
     "Cơ sở dữ liệu MariaDB chứa toàn bộ dữ liệu y tế nhạy cảm của bệnh nhân. Trụ cột Data của "
     "Zero Trust CISA yêu cầu dữ liệu phải được bảo vệ theo nguyên tắc Defense-in-Depth. "
     "Việc chặn Client trực tiếp kết nối DB tạo ra lớp bảo vệ thứ hai: dù kẻ tấn công có thể "
     "đoán được địa chỉ IP của MariaDB, firewall rule mức VLAN vẫn ngăn chặn hoàn toàn."),

    ("GĐ1 – Hạ tầng Proxmox & VLAN", 7,
     "Pomerium giao tiếp được với Keycloak (FW-04)",
     "Xác nhận VLAN20 → VLAN30 TCP/8443 ALLOW",
     "Từ zt-pomerium01: curl -v https://10.10.30.10:8443/ --connect-timeout 5",
     "Kết nối thành công đến Keycloak; HTTP response nhận được; không bị firewall drop",
     "Networks – Policy-Defined Connectivity", "Cao", "Kết nối",
     "Zero Trust thay thế mô hình 'deny all' toàn diện bằng mô hình 'cho phép có kiểm soát theo policy'. "
     "Luồng Pomerium → Keycloak là luồng OIDC xác thực danh tính bắt buộc, phải được mở có chủ đích "
     "(FW-04). Test này xác nhận chính sách mạng đã được định nghĩa đúng theo policy-based access: "
     "chỉ đúng nguồn, đúng đích, đúng port mới được phép, không phải mở rộng toàn bộ."),

    ("GĐ1 – Hạ tầng Proxmox & VLAN", 8,
     "Pomerium forward được traffic đến OpenEMR (FW-05)",
     "Xác nhận VLAN20 → VLAN40 TCP/443 ALLOW",
     "Từ zt-pomerium01: curl -k https://10.10.40.10 --connect-timeout 5",
     "Kết nối thành công; HTTP response từ OpenEMR; không bị firewall drop",
     "Networks – Authorized Traffic Path", "Cao", "Kết nối",
     "Sau khi Pomerium xác thực danh tính người dùng và thiết bị, nó phải forward traffic đã được "
     "ủy quyền đến OpenEMR. Luồng này thể hiện nguyên tắc 'Assume Breach' và 'Verify Explicitly' "
     "của ZTA: chỉ luồng đã được Policy Decision Point (Pomerium/Keycloak) xác minh và chấp thuận "
     "mới có thể tiếp cận tài nguyên ứng dụng thông qua Policy Enforcement Point."),

    ("GĐ1 – Hạ tầng Proxmox & VLAN", 9,
     "OpenEMR kết nối MariaDB qua TCP/3306 (FW-06)",
     "Xác nhận VLAN40 → VLAN50 TCP/3306 ALLOW; OpenEMR query được dữ liệu",
     "Đăng nhập OpenEMR Web UI admin → xem danh sách bệnh nhân hoặc Administration → Database",
     "OpenEMR kết nối MariaDB thành công; dữ liệu hiển thị; không có lỗi DB connection",
     "Networks – Application-to-Data Connectivity", "Cao", "Chức năng",
     "Zero Trust Micro-segmentation cho phép giao tiếp giữa Application Zone và DB Zone theo "
     "luồng duy nhất đã được định nghĩa rõ: chỉ OpenEMR (10.10.40.10) được kết nối MariaDB "
     "(10.10.50.10) qua TCP/3306. Test này xác nhận rằng ứng dụng có thể hoạt động bình thường "
     "trong mô hình ZTA – bảo mật không gây ra gián đoạn nghiệp vụ hợp lệ theo nguyên tắc usability."),

    ("GĐ1 – Hạ tầng Proxmox & VLAN", 10,
     "Management Zone cô lập với App và DB Zone",
     "Xác nhận VLAN60 Proxmox không reachable từ VLAN40 App hoặc VLAN10 Client",
     "Từ OpenEMR (10.10.40.10): ping 10.10.60.10; curl https://10.10.60.10:8006",
     "Kết nối bị từ chối; VLAN40 không giao tiếp được với VLAN60",
     "Networks – Management Plane Isolation", "Cao", "Bảo mật",
     "NIST SP 800-207 quy định mặt phẳng quản trị (Management Plane) của hệ thống Zero Trust phải được "
     "bảo vệ và cô lập nghiêm ngặt. Nếu kẻ tấn công đã vào được App Zone (ví dụ compromise OpenEMR) "
     "nhưng không thể tiếp cận Proxmox Management, họ không thể leo thang quyền để thao túng toàn bộ "
     "hypervisor hoặc tắt các VM bảo mật. Test này kiểm chứng lớp phòng thủ chiều sâu cuối cùng."),

    # ──────────────────────────────────────────────────────────
    # GIAI ĐOẠN 2 – KEYCLOAK IAM: REALM, ROLE, MFA
    # ──────────────────────────────────────────────────────────
    ("GĐ2 – Keycloak IAM & Identity", 11,
     "Keycloak khởi động và Hospital-Realm tồn tại",
     "Xác nhận Keycloak v26.7.2 chạy; Realm 'medical-realm' import thành công",
     "Truy cập https://10.10.30.10:8443/realms/medical-realm/.well-known/openid-configuration",
     "HTTP 200; JSON chứa 'issuer': 'medical-realm'; các endpoint xác thực đầy đủ",
     "Identity – IAM Setup", "Cao", "Chức năng",
     "Trụ cột Identity của CISA Zero Trust Maturity Model yêu cầu tập trung quản lý danh tính "
     "tại một Identity Provider (IdP) duy nhất thay vì phân tán ở từng ứng dụng. Keycloak "
     "đóng vai trò IdP trung tâm toàn bộ hệ thống y tế. Không có Realm hoạt động, không một "
     "người dùng nào có thể được xác thực, toàn bộ luồng ZTA sẽ sụp đổ ngay từ bước đầu tiên."),

    ("GĐ2 – Keycloak IAM & Identity", 12,
     "5 vai trò nghiệp vụ được tạo đúng trong Realm",
     "Kiểm tra Realm có đủ các roles: doctor, lab, receptionist, records_staff, supervisor, it_admin",
     "Keycloak Admin Console → Realm Roles → xem danh sách",
     "Hiển thị đủ roles; không duplicate; tên đúng convention",
     "Identity – RBAC Role Definition", "Cao", "Chức năng",
     "Zero Trust áp dụng nguyên tắc Least Privilege thông qua Role-Based Access Control (RBAC). "
     "Mỗi vai trò đại diện cho tập quyền tối thiểu cần thiết để thực hiện công việc: Lễ tân chỉ "
     "có quyền hành chính, Bác sĩ chỉ có quyền lâm sàng trong phạm vi phụ trách, IT Admin chỉ có "
     "quyền quản trị kỹ thuật mà không mặc định đọc được hồ sơ bệnh án. Roles phải tồn tại và "
     "đúng tên để Pomerium Policy Route và OpenEMR ACL hoạt động chính xác."),

    ("GĐ2 – Keycloak IAM & Identity", 13,
     "Đăng nhập thành công với credentials hợp lệ",
     "Tài khoản doctor01 đăng nhập được bằng username/password đúng",
     "Keycloak Login Page → username=doctor01, password=Doctor@2026",
     "Đăng nhập thành công; redirect đến trang MFA setup hoặc OTP input",
     "Identity – Authentication", "Cao", "Chức năng",
     "Zero Trust không loại bỏ xác thực bằng mật khẩu mà sử dụng nó như bước đầu trong quy trình "
     "xác thực đa tầng. Test này xác nhận rằng layer 1 (Something You Know – mật khẩu) hoạt động đúng, "
     "là tiền đề để yêu cầu layer 2 (Something You Have – OTP). Một hệ thống ZTA không thể yêu cầu MFA "
     "nếu bước xác thực mật khẩu cơ bản bị lỗi; cả chuỗi Explicit Verification sẽ thất bại."),

    ("GĐ2 – Keycloak IAM & Identity", 14,
     "Đăng nhập thất bại với mật khẩu sai – từ chối và ghi log",
     "Hệ thống từ chối khi sai credentials; ghi sự kiện vào Event Log",
     "Keycloak Login → username=doctor01, password=SaiMatKhau123",
     "Thông báo 'Invalid username or password'; không tạo session; lỗi được ghi Keycloak Event Log",
     "Identity – Explicit Verification / Audit", "Rất cao", "Bảo mật",
     "Nguyên tắc 'Verify Explicitly' của Zero Trust yêu cầu mọi yêu cầu xác thực đều phải được "
     "kiểm tra chặt chẽ và không thể đoán mò. Việc Keycloak từ chối rõ ràng và ghi log sự kiện thất "
     "bại là bằng chứng trực tiếp của cơ chế Explicit Verification. Nếu hệ thống chấp nhận mật khẩu "
     "sai hoặc không ghi log, khả năng phát hiện tấn công brute force và Audit Trailing sẽ bị mất."),

    ("GĐ2 – Keycloak IAM & Identity", 15,
     "MFA bắt buộc: Thiếu OTP không hoàn thành xác thực",
     "Dù nhập đúng password, thiếu OTP vẫn không nhận được access token",
     "Nhập đúng username/password → khi màn hình yêu cầu OTP: bỏ qua hoặc nhập sai",
     "Xác thực không hoàn tất; không có access token; không truy cập được OpenEMR",
     "Identity – MFA / Explicit Verification", "Rất cao", "Bảo mật",
     "Đây là test case chứng minh Multi-Factor Authentication (MFA) – yếu tố cốt lõi nhất của "
     "trụ cột Identity trong CISA Zero Trust Maturity. MFA đảm bảo rằng dù mật khẩu của Bác sĩ "
     "bị lộ qua phishing hay credential stuffing, kẻ tấn công vẫn không thể vào hệ thống vì "
     "thiếu yếu tố thứ hai (OTP từ Google Authenticator). Test FAIL đồng nghĩa hệ thống có thể "
     "bị xâm phạm bởi bất kỳ kẻ nào có được mật khẩu – vi phạm nghiêm trọng ZTA."),

    ("GĐ2 – Keycloak IAM & Identity", 16,
     "MFA thành công: OTP hợp lệ → nhận Access Token có role đúng",
     "Luồng password + OTP hoàn chỉnh → Keycloak cấp JWT token chứa role đúng",
     "Nhập username=doctor01, password đúng → nhập mã OTP 6 chữ số từ Google Authenticator",
     "Keycloak cấp Access Token và ID Token; payload chứa realm_access.roles=['doctor']",
     "Identity – MFA / SSO / Token Issuance", "Rất cao", "Chức năng",
     "Test này xác nhận toàn bộ chuỗi xác thực đa yếu tố Zero Trust hoạt động end-to-end: "
     "người dùng chứng minh danh tính qua hai yếu tố (mật khẩu + TOTP), nhận JWT token mang "
     "thông tin vai trò (claims). Token này sau đó được Pomerium sử dụng để ra quyết định "
     "Allow/Deny theo Policy Route. Nếu token không chứa role đúng, toàn bộ RBAC tầng trên "
     "sẽ hoạt động sai, dẫn đến leo thang quyền hoặc từ chối nhầm người dùng hợp lệ."),

    ("GĐ2 – Keycloak IAM & Identity", 17,
     "JWT Token chứa đúng role claim theo từng người dùng",
     "Token doctor01 chứa role 'doctor'; token lab_tech01 chứa 'lab'; không có role chéo",
     "Giải mã JWT Access Token sau đăng nhập thành công (dùng jwt.io hoặc python-jwt)",
     "Payload: 'realm_access': {'roles': ['doctor']} cho doctor01; không có role 'lab' hay 'it_admin'",
     "Identity – RBAC / Token Integrity", "Cao", "Chức năng",
     "Zero Trust sử dụng token claims làm cơ sở ra quyết định ủy quyền tại Pomerium (PEP). "
     "Nếu token bị lỗi chứa sai role (ví dụ receptionist nhận được claims 'doctor'), hệ thống "
     "sẽ cấp quyền sai theo nguyên tắc RBAC, vi phạm Least Privilege. Test này xác nhận tính "
     "toàn vẹn của token issuance – yếu tố quyết định độ chính xác của toàn bộ chuỗi ủy quyền."),

    ("GĐ2 – Keycloak IAM & Identity", 18,
     "IT Admin quản lý tài khoản: tạo và vô hiệu hóa (không xóa)",
     "IT Admin tạo user mới và disable tài khoản; tài khoản bị disable không đăng nhập được",
     "Keycloak Admin Console → tạo 'test_user' → disable → test_user cố đăng nhập",
     "User tạo thành công; disable thành công (Enabled=false); test_user không đăng nhập được",
     "Identity – Account Lifecycle / Least Privilege", "Trung bình", "Chức năng",
     "Quản lý vòng đời tài khoản (Account Lifecycle Management) là thành phần bắt buộc trong "
     "trụ cột Identity của Zero Trust. Nguyên tắc Least Privilege yêu cầu khi nhân viên nghỉ "
     "việc hoặc đổi vai trò, quyền truy cập phải bị thu hồi ngay lập tức. Vô hiệu hóa thay vì "
     "xóa đảm bảo audit trail được bảo toàn theo yêu cầu của hệ thống y tế và pháp lý."),

    # ──────────────────────────────────────────────────────────
    # GIAI ĐOẠN 3 – POMERIUM GATEWAY & OIDC / mTLS
    # ──────────────────────────────────────────────────────────
    ("GĐ3 – Pomerium Gateway & mTLS", 19,
     "Pomerium khởi động và kết nối OIDC Keycloak thành công",
     "Xác nhận Pomerium kết nối được với Keycloak OIDC discovery endpoint",
     "journalctl -u pomerium -n 50 | grep -i 'oidc\\|connected\\|error'",
     "Log không có lỗi OIDC; hiển thị 'connected to identity provider'; Pomerium lắng nghe TCP/443",
     "Identity – Gateway / OIDC Integration", "Cao", "Chức năng",
     "Pomerium đóng vai trò Policy Enforcement Point (PEP) – thành phần thiết yếu nhất trong kiến "
     "trúc ZTA theo NIST SP 800-207. Để Pomerium ra được quyết định Allow/Deny, nó phải kết nối "
     "được với Policy Decision Point thông qua OIDC để nhận và xác thực JWT token từ Keycloak. "
     "Nếu OIDC bị lỗi, Pomerium không thể xác thực bất kỳ người dùng nào, toàn bộ cổng vào "
     "Zero Trust bị tê liệt, buộc admin phải tắt gateway hoặc mở bypass – vi phạm ZTA."),

    ("GĐ3 – Pomerium Gateway & mTLS", 20,
     "Luồng Zero Trust đầy đủ: Certificate + Password + OTP → truy cập OpenEMR (TC-01)",
     "Người dùng hợp lệ với đầy đủ 3 yếu tố xác thực đi qua toàn bộ chuỗi ZTA",
     "Client có Certificate hợp lệ → https://emr.hospital.local → đăng nhập Keycloak → OTP",
     "Pomerium allow; trình duyệt load giao diện OpenEMR; HTTP 200; không có lỗi SSL hay 403",
     "Identity / MFA / Device Trust / Gateway Enforcement", "Rất cao", "End-to-End",
     "Test này là bài kiểm chứng tổng thể nhất: xác nhận đồng thời 3 trụ cột Zero Trust CISA "
     "hoạt động tích hợp. Trụ cột Devices: mTLS client certificate được Pomerium xác thực. "
     "Trụ cột Identity: Keycloak xác thực username/password + MFA OTP. Trụ cột Networks + "
     "Applications: Pomerium enforce policy route, chỉ forward traffic được ủy quyền đến OpenEMR. "
     "Pass test này là bằng chứng mạnh nhất rằng kiến trúc ZTA đã hoạt động end-to-end đúng thiết kế."),

    ("GĐ3 – Pomerium Gateway & mTLS", 21,
     "Thiết bị không có Client Certificate bị chặn tại TLS (TC-04)",
     "Máy không có certificate do CA nội bộ cấp bị từ chối ngay tại tầng TLS",
     "Từ máy KHÔNG có Client Certificate: truy cập https://emr.hospital.local",
     "Trình duyệt báo lỗi SSL handshake (ERR_BAD_SSL_CLIENT_AUTH_CERT); từ chối trước trang Keycloak",
     "Devices – mTLS / Device Trust", "Rất cao", "Bảo mật",
     "Trụ cột Devices của CISA Zero Trust yêu cầu mọi thiết bị phải được nhận diện và kiểm tra "
     "trước khi được phép truy cập tài nguyên. mTLS (Mutual TLS) với Client Certificate là cơ "
     "chế kỹ thuật để Pomerium xác định 'Thiết bị này có phải do bệnh viện cấp phép không?'. "
     "Nếu test FAIL (thiết bị không có cert mà vẫn vào được), kẻ tấn công từ thiết bị cá nhân "
     "bên ngoài có thể truy cập hệ thống chỉ với username/password – vi phạm Device Trust."),

    ("GĐ3 – Pomerium Gateway & mTLS", 22,
     "Client Certificate hết hạn bị từ chối",
     "Pomerium từ chối chứng chỉ hết hạn dù từng hợp lệ",
     "Cài certificate đã hết hạn lên trình duyệt → truy cập https://emr.hospital.local",
     "Lỗi certificate expired; kết nối từ chối; không load được trang đăng nhập",
     "Devices – Certificate Validity / Device Posture", "Cao", "Bảo mật",
     "Zero Trust Device Trust không phải kiểm tra một lần duy nhất mà yêu cầu liên tục (Continuous "
     "Verification). Chứng chỉ hết hạn đồng nghĩa trạng thái tin cậy của thiết bị không còn được "
     "bảo đảm – thiết bị có thể đã bị mất, bị đánh cắp, hoặc không còn được quản lý bởi bệnh viện. "
     "Test này xác nhận Pomerium thực thi thời hạn certificate, buộc thiết bị phải gia hạn "
     "định kỳ và không thể dùng cert cũ vô thời hạn."),

    ("GĐ3 – Pomerium Gateway & mTLS", 23,
     "Phiên xác thực hết hạn bị từ chối tự động (TC-05)",
     "Pomerium từ chối request khi session token hết hạn hoặc cookie bị xóa",
     "Xóa cookie session hoặc dùng token hết hạn → gửi request đến https://emr.hospital.local",
     "Pomerium redirect về trang đăng nhập Keycloak; HTTP 302 hoặc 401; không forward đến OpenEMR",
     "Identity – Session Verification / Continuous Auth", "Cao", "Bảo mật",
     "Zero Trust áp dụng 'Continuous Validation' – không phải kiểm tra một lần rồi tin tưởng mãi. "
     "Khi session hết hạn, người dùng phải xác thực lại từ đầu kể cả khi đang trong mạng nội bộ. "
     "Điều này ngăn chặn tình huống 'session hijacking': kẻ tấn công đánh cắp cookie cũ vẫn "
     "không thể duy trì truy cập nếu session đã hết hạn. Đây là biểu hiện của 'Never Trust, "
     "Always Verify' ở cấp độ session management."),

    ("GĐ3 – Pomerium Gateway & mTLS", 24,
     "Client bypass Pomerium bị Proxmox Firewall chặn (TC-06)",
     "Kết nối thẳng đến IP OpenEMR 10.10.40.10:443 từ VLAN10 bị drop",
     "Từ client: curl -k https://10.10.40.10 --connect-timeout 5 (trực tiếp IP)",
     "curl timeout; OpenEMR không nhận request; Proxmox Firewall drop gói tin",
     "Networks – Gateway Enforcement / Anti-Bypass", "Rất cao", "Bảo mật",
     "Defense in Depth là nguyên tắc ZTA: nếu cơ chế phần mềm bị vượt qua, tầng mạng vẫn phải "
     "chặn. Test này kiểm chứng rằng ngay cả khi kẻ tấn công biết địa chỉ IP nội bộ của OpenEMR "
     "và cố kết nối thẳng (bypass Pomerium), Proxmox Firewall rule tầng VLAN vẫn drop gói tin "
     "trước khi đến ứng dụng. Hai lớp phòng thủ (Pomerium logic + Firewall rule) hoạt động "
     "song song đảm bảo không có single point of failure trong gateway enforcement."),

    ("GĐ3 – Pomerium Gateway & mTLS", 25,
     "Pomerium Policy Route đúng role: Doctor được Allow vào OpenEMR",
     "doctor01 với role 'doctor' trong JWT được Pomerium định tuyến đến OpenEMR",
     "Đăng nhập doctor01 → truy cập https://emr.hospital.local",
     "HTTP 200; Pomerium allow và forward đến OpenEMR; giao diện load thành công",
     "Applications – Gateway Policy / RBAC Enforcement", "Cao", "Chức năng",
     "Pomerium đóng vai trò Policy Enforcement Point (PEP) thực thi quyết định của Policy Decision "
     "Point (JWT từ Keycloak). Khi Pomerium đọc claim 'realm_access.roles' trong JWT và tìm thấy "
     "'doctor', nó cho phép định tuyến theo policy route đã cấu hình. Test này xác nhận "
     "chuỗi Policy-Based Access Control (PBAC) hoạt động: Identity Provider cấp token → "
     "PEP kiểm tra → ứng dụng được phép truy cập. Đây là hiện thực hóa 'Assume Breach' – "
     "mọi request đều phải qua kiểm tra policy dù đến từ mạng nội bộ."),

    ("GĐ3 – Pomerium Gateway & mTLS", 26,
     "Đường truyền HTTPS end-to-end được mã hóa TLS",
     "Toàn bộ kết nối nội bộ (Client→Pomerium→Keycloak→OpenEMR) đều dùng TLS",
     "Wireshark capture traffic trên VLAN20; phân tích packets Pomerium↔OpenEMR",
     "100% packets là TLS encrypted; không có plain-text HTTP; certificate hợp lệ trên tất cả kết nối",
     "Data – Encryption in Transit / TLS End-to-End", "Cao", "Bảo mật",
     "Trụ cột Data của Zero Trust yêu cầu mã hóa dữ liệu trên đường truyền (Data in Transit) "
     "không chỉ từ người dùng đến Pomerium mà còn toàn bộ đường nội bộ. Điều này ngăn chặn "
     "tấn công 'Insider Threat' hoặc 'ARP Spoofing' trong VLAN nội bộ: dù kẻ tấn công cắm "
     "máy sniffing trong mạng LAN bệnh viện cũng chỉ thấy chuỗi dữ liệu đã mã hóa, không "
     "thể đọc được thông tin bệnh nhân hay token xác thực đang lưu chuyển."),

    # ──────────────────────────────────────────────────────────
    # GIAI ĐOẠN 4 – OPENEMR RBAC: PHÂN QUYỀN NGHIỆP VỤ
    # ──────────────────────────────────────────────────────────
    ("GĐ4 – OpenEMR RBAC & Nghiệp vụ", 27,
     "Lễ tân: thao tác hành chính và tạo lượt khám thành công (TC-07 / BF-01)",
     "Receptionist đọc/tạo/sửa thông tin hành chính; tạo encounter mới",
     "receptionist01 đăng nhập → tìm bệnh nhân → cập nhật thông tin hành chính → tạo encounter",
     "Tất cả thao tác thành công; encounter được tạo; không có lỗi 403",
     "Applications – RBAC / Least Privilege", "Cao", "Chức năng",
     "Test này xác nhận role Receptionist được gán đúng quyền theo Least Privilege: chỉ đủ quyền "
     "thực hiện công việc nghiệp vụ hành chính (BF-01), không hơn không kém. Trong ZTA, mỗi vai "
     "trò nhận đúng quyền tối thiểu cần thiết. Việc Lễ tân tạo được encounter (nhưng không thể "
     "nhập chẩn đoán – test TC-08) thể hiện Separation of Duties và RBAC hoạt động đúng theo "
     "ma trận phân quyền đã định nghĩa trong thiết kế kiến trúc."),

    ("GĐ4 – OpenEMR RBAC & Nghiệp vụ", 28,
     "Lễ tân KHÔNG thể truy cập Chẩn đoán và Kết quả xét nghiệm (TC-08)",
     "Receptionist bị từ chối khi cố truy cập dữ liệu chuyên môn",
     "receptionist01 đăng nhập → cố mở mục Diagnosis → cố xem Lab Results",
     "Hệ thống hiển thị 'Access Denied' hoặc HTTP 403; menu bị ẩn hoặc locked",
     "Applications – RBAC / Least Privilege", "Rất cao", "Bảo mật",
     "Nguyên tắc Least Privilege của Zero Trust không chỉ áp dụng ở tầng mạng (Pomerium) mà "
     "còn phải được thực thi ở tầng ứng dụng (OpenEMR ACL). Test này xác nhận Defense in Depth "
     "ở tầng ứng dụng: dù Lễ tân đã vượt qua Pomerium Gateway (vì có quyền truy cập OpenEMR "
     "nói chung), OpenEMR vẫn kiểm tra ACL và từ chối quyền đọc dữ liệu chuyên môn. "
     "Nếu FAIL, Lễ tân có thể đọc toàn bộ chẩn đoán và kết quả xét nghiệm – vi phạm "
     "Data Privacy và HIPAA-equivalent trong hệ thống y tế."),

    ("GĐ4 – OpenEMR RBAC & Nghiệp vụ", 29,
     "Bác sĩ đọc hồ sơ và tạo ghi chú lâm sàng trong phạm vi (TC-09 / BF-02)",
     "Doctor được đọc hồ sơ và tạo/sửa ghi chú lâm sàng với bệnh nhân thuộc phạm vi",
     "doctor01 đăng nhập → mở hồ sơ bệnh nhân được phân công → tạo ghi chú → tạo chẩn đoán",
     "Ghi chú lâm sàng tạo thành công; chẩn đoán lưu được; HTTP 200",
     "Applications – RBAC / Context-Aware Access", "Cao", "Chức năng",
     "Test xác nhận Context-Aware Access Control: Bác sĩ không chỉ cần có role 'doctor' mà còn "
     "phải đang xử lý bệnh nhân thuộc phạm vi phụ trách. Đây là biểu hiện của nguyên tắc "
     "'Verify Explicitly with Context' trong Zero Trust – quyền truy cập được đánh giá dựa "
     "trên ngữ cảnh (context) bao gồm danh tính, vai trò VÀ phạm vi bệnh nhân được giao, "
     "không chỉ đơn thuần là vai trò. Test PASS xác nhận OpenEMR RBAC hoạt động đúng "
     "theo ma trận Granular Role-Permission Matrix đã thiết kế ở Chương 2."),

    ("GĐ4 – OpenEMR RBAC & Nghiệp vụ", 30,
     "Bác sĩ KHÔNG thể sửa hồ sơ ngoài phạm vi phụ trách (TC-10)",
     "Doctor có role hợp lệ nhưng bị từ chối khi cố sửa bệnh nhân không được phân công",
     "doctor01 đăng nhập → truy cập hồ sơ bệnh nhân KHÔNG thuộc phạm vi → cố cập nhật ghi chú",
     "Hệ thống từ chối; HTTP 403 hoặc thông báo lỗi; dữ liệu không bị thay đổi",
     "Applications – Context / Least Privilege", "Rất cao", "Bảo mật",
     "Test này kiểm chứng Attribute-Based Access Control (ABAC) ở tầng sâu nhất: dù doctor01 "
     "có role 'doctor' hợp lệ trong JWT, OpenEMR vẫn từ chối vì attribute 'bệnh nhân này không "
     "trong phạm vi phụ trách của doctor01'. Điều này thể hiện Zero Trust không tin tưởng "
     "tuyệt đối vào role – mà còn kiểm tra thêm context cụ thể của từng resource request. "
     "Nếu FAIL, Bác sĩ A có thể đọc và sửa hồ sơ của bệnh nhân Bác sĩ B – vi phạm "
     "Separation of Duties và Data Privacy nghiêm trọng."),

    ("GĐ4 – OpenEMR RBAC & Nghiệp vụ", 31,
     "Bác sĩ không thể sửa chỉ định sau khi KTV đã có kết quả (TC-11 / BF-03)",
     "Doctor tạo lab order → KTV nhập kết quả → Doctor cố sửa nội dung chỉ định",
     "doctor01 tạo lab order → lab_tech01 nhập kết quả → doctor01 cố sửa order",
     "Tạo order thành công; sau khi kết quả confirmed, sửa order bị từ chối; dữ liệu nhất quán",
     "Applications – RBAC / Separation of Duties / Data Integrity", "Cao", "Chức năng",
     "Separation of Duties là nguyên tắc quan trọng trong cả Zero Trust và quản lý bệnh viện: "
     "không một cá nhân nào được kiểm soát toàn bộ vòng đời của một giao dịch nhạy cảm. "
     "Bác sĩ tạo chỉ định nhưng không được sửa sau khi KTV đã xử lý và xác nhận kết quả "
     "– điều này đảm bảo Data Integrity và tính truy vết (Auditability). Trong ZTA, "
     "Data Protection không chỉ là mã hóa mà còn bao gồm kiểm soát tính toàn vẹn dữ liệu "
     "theo ngữ cảnh và trạng thái xử lý."),

    ("GĐ4 – OpenEMR RBAC & Nghiệp vụ", 32,
     "KTV xét nghiệm xử lý kết quả; không sửa được sau khi xác nhận (TC-12 / BF-03)",
     "lab_tech01 nhập kết quả → confirm → cố sửa lại kết quả đã confirmed",
     "lab_tech01 nhập và confirm kết quả → cố chỉnh sửa lần hai",
     "Nhập/confirm thành công; sửa sau confirm bị từ chối; kết quả readonly",
     "Applications – RBAC / Data Integrity / Audit Trail", "Cao", "Chức năng",
     "Nguyên tắc Data Immutability sau khi xác nhận (Confirmed) là một dạng Data Protection "
     "trong Zero Trust: dữ liệu y tế đã được ký xác nhận không thể thay đổi hồi tố để "
     "bảo đảm tính toàn vẹn của hồ sơ sức khỏe. Điều này tương đương với Write-Once Read-Many "
     "(WORM) cho kết quả xét nghiệm. Test PASS đảm bảo Audit Trail không bị giả mạo hồi tố, "
     "đây là yêu cầu bắt buộc trong hệ thống y tế điện tử (EMR) theo chuẩn HL7/HIPAA-equivalent."),

    ("GĐ4 – OpenEMR RBAC & Nghiệp vụ", 33,
     "KTV xét nghiệm KHÔNG thể sửa Chẩn đoán hoặc Ghi chú lâm sàng (TC-13)",
     "lab_tech01 bị từ chối khi cố thao tác dữ liệu chuyên môn ngoài phạm vi xét nghiệm",
     "lab_tech01 đăng nhập → cố mở Diagnosis → cố sửa Clinical Notes của Bác sĩ",
     "Các thao tác bị từ chối; không có menu hoặc HTTP 403; dữ liệu của Bác sĩ không thay đổi",
     "Applications – Least Privilege / Separation of Duties", "Rất cao", "Bảo mật",
     "Test này xác nhận ranh giới nghiệp vụ giữa các vai trò được Zero Trust RBAC thực thi "
     "nghiêm ngặt ở tầng ứng dụng. KTV Xét nghiệm chỉ có quyền xử lý kết quả xét nghiệm "
     "(BF-03), tuyệt đối không có quyền ghi vào dữ liệu chuyên môn của Bác sĩ (Chẩn đoán, "
     "Ghi chú lâm sàng). Nếu FAIL, KTV có thể giả mạo hoặc thay đổi chẩn đoán – một sự vi "
     "phạm Separation of Duties nghiêm trọng có thể gây nguy hiểm cho tính mạng bệnh nhân."),

    ("GĐ4 – OpenEMR RBAC & Nghiệp vụ", 34,
     "Nhân viên quản lý hồ sơ truy cập bệnh nhân đã được assign (TC-14 / BF-04)",
     "records_staff01 chỉ truy cập được hồ sơ đã được Supervisor phân công",
     "Supervisor assign bệnh nhân A cho records_staff01 → records_staff01 truy cập hồ sơ A",
     "records_staff01 truy cập thành công hồ sơ A; chỉ đọc theo quyền Records; HTTP 200",
     "Applications – RBAC / Medical Records Assignment", "Cao", "Chức năng",
     "Medical Records Assignment là cơ chế bổ sung phản ánh nguyên tắc 'Need to Know' trong "
     "Zero Trust Data Protection: nhân viên chỉ được tiếp cận dữ liệu khi thực sự cần và "
     "đã được phân công cụ thể. Không phải mọi Records Staff đều thấy mọi hồ sơ – chỉ những "
     "hồ sơ được Supervisor giao mới được phép truy cập. Test này xác nhận cơ chế "
     "Context-Aware Authorization kết hợp Assignment-based Access Control hoạt động đúng."),

    ("GĐ4 – OpenEMR RBAC & Nghiệp vụ", 35,
     "Nhân viên quản lý hồ sơ KHÔNG truy cập bệnh nhân chưa được assign (TC-21)",
     "records_staff01 bị từ chối khi cố truy cập hồ sơ bệnh nhân chưa được phân công",
     "records_staff01 cố truy cập hồ sơ bệnh nhân B (chưa assign cho records_staff01)",
     "Từ chối truy cập; HTTP 403 hoặc thông báo lỗi; hồ sơ B không hiển thị",
     "Applications – Context / Medical Records Assignment", "Rất cao", "Bảo mật",
     "Đây là mặt phòng thủ của TC-14: xác nhận rằng cơ chế Medical Records Assignment thực "
     "sự ngăn chặn truy cập trái phép, không chỉ cho phép truy cập hợp lệ. Zero Trust "
     "yêu cầu kiểm tra theo cả chiều Allow (TC-14) và chiều Deny (TC-21) – một hệ thống "
     "mạnh phải pass cả hai. Nếu TC-21 FAIL, nhân viên hồ sơ có thể xem toàn bộ database "
     "bệnh nhân mà không cần được phân công, phá vỡ Data Privacy toàn diện."),

    ("GĐ4 – OpenEMR RBAC & Nghiệp vụ", 36,
     "Nhân viên hồ sơ KHÔNG thể sửa Chẩn đoán, Ghi chú lâm sàng, Kết quả xét nghiệm (TC-15)",
     "records_staff chỉ có quyền đọc dữ liệu chuyên môn, không được ghi",
     "records_staff01 mở hồ sơ được assign → cố sửa Diagnosis → cố sửa Lab Results",
     "Tất cả thao tác update bị từ chối; các trường hiển thị readonly; không HTTP 200 save",
     "Applications – Least Privilege / Separation of Duties", "Rất cao", "Bảo mật",
     "Least Privilege ở tầng dữ liệu y tế: Nhân viên quản lý hồ sơ có nhiệm vụ quản lý "
     "administrative documents, không phải chuyên môn y tế. Dù họ được phép đọc hồ sơ "
     "(để phục vụ công việc), họ không được phép ghi vào dữ liệu lâm sàng do Bác sĩ hoặc "
     "KTV tạo ra. Test này xác nhận tầng thứ ba của Defense in Depth: Pomerium (gateway) → "
     "OpenEMR RBAC role (chức năng) → OpenEMR ACL resource (trường dữ liệu cụ thể)."),

    ("GĐ4 – OpenEMR RBAC & Nghiệp vụ", 37,
     "Medical Records Supervisor phân công và reassign hồ sơ (TC-22 / BF-05)",
     "Supervisor assign bệnh nhân C cho staff01 → reassign sang staff02; staff01 mất quyền",
     "Supervisor assign C cho staff01 → staff01 access OK → Supervisor reassign sang staff02 → staff01 bị từ chối",
     "4 bước đều đúng; quyền thay đổi ngay sau reassign; staff01 HTTP 403; staff02 access thành công",
     "Applications – RBAC / Context / Dynamic Access Revocation", "Cao", "Chức năng",
     "Reassignment là minh họa hoàn hảo của 'Dynamic Access Control' trong Zero Trust: quyền "
     "truy cập thay đổi ngay lập tức theo context thực tế (ai đang phụ trách hồ sơ) chứ không "
     "phải cố định. Khi staff01 không còn phụ trách bệnh nhân C, hệ thống phải thu hồi quyền "
     "ngay lập tức mà không cần chờ session hết hạn. Test này xác nhận ZTA cung cấp "
     "Just-in-Time Access: quyền chỉ tồn tại trong thời gian thực sự cần, bị thu hồi khi không còn lý do."),

    ("GĐ4 – OpenEMR RBAC & Nghiệp vụ", 38,
     "IT Admin quản trị hệ thống nhưng KHÔNG đọc được hồ sơ bệnh án (TC-17)",
     "Quyền quản trị kỹ thuật không mặc định kèm quyền đọc nội dung bệnh án",
     "it_admin đăng nhập → thực hiện admin tasks → cố truy cập bệnh nhân và hồ sơ bệnh án",
     "Admin tasks thành công; truy cập hồ sơ bệnh án bị từ chối HTTP 403; không hiển thị menu bệnh án",
     "Applications – RBAC / Least Privilege / Segregation", "Rất cao", "Bảo mật",
     "Đây là một trong những nguyên tắc quan trọng nhất của Zero Trust trong môi trường y tế: "
     "Superuser hoặc Admin không mặc định có quyền đọc dữ liệu nghiệp vụ nhạy cảm. "
     "IT Admin có thể cấu hình hệ thống, xem security log, quản lý tài khoản – nhưng không "
     "được phép đọc thông tin bệnh án bệnh nhân. Test FAIL nghĩa là người quản trị CNTT có "
     "thể xem toàn bộ dữ liệu y tế bệnh nhân – vi phạm Separation of Duties và HIPAA-equivalent."),

    ("GĐ4 – OpenEMR RBAC & Nghiệp vụ", 39,
     "Giám sát hồ sơ KHÔNG đọc được dữ liệu chuyên môn bệnh án",
     "medicalrecordssupervisor có quyền assign nhưng không có quyền đọc chuyên môn",
     "medicalrecordssupervisor đăng nhập → thực hiện assign → cố mở nội dung Chẩn đoán",
     "Assign thành công; truy cập nội dung chuyên môn bị từ chối; không có dữ liệu bệnh án",
     "Applications – Least Privilege / Separation of Duties", "Cao", "Bảo mật",
     "Ma trận phân quyền Zero Trust phân biệt rõ ràng: quyền quản lý metadata (ai được giao "
     "hồ sơ nào – Assignment) và quyền đọc nội dung chuyên môn (Diagnosis, Clinical Notes). "
     "Supervisor quản lý assignment nhưng không được xem nội dung chuyên môn y tế – tránh "
     "tập trung quá nhiều quyền vào một người (Privilege Concentration). Test này xác nhận "
     "hệ thống thực thi đúng ranh giới giữa quản lý phân công và truy cập nội dung dữ liệu."),

    # ──────────────────────────────────────────────────────────
    # GIAI ĐOẠN 5 – MARIADB TDE: MÃ HÓA DỮ LIỆU LƯU TRỮ
    # ──────────────────────────────────────────────────────────
    ("GĐ5 – MariaDB TDE & Mã hóa Dữ liệu", 40,
     "MariaDB TDE plugin file_key_management đã được kích hoạt",
     "Kiểm tra MariaDB đã load plugin mã hóa và encryption at rest đang ON",
     "SSH emr-db01 → mysql → SHOW PLUGINS; SHOW VARIABLES LIKE 'innodb_encrypt%';",
     "Plugin 'file_key_management' trạng thái ACTIVE; innodb_encrypt_tables=ON; innodb_encrypt_log=ON",
     "Data – Encryption at Rest / TDE", "Rất cao", "Bảo mật",
     "Trụ cột Data của CISA Zero Trust yêu cầu bảo vệ dữ liệu 'At Rest' (khi lưu trữ) ngoài "
     "việc bảo vệ 'In Transit' (khi truyền). Transparent Data Encryption (TDE) mã hóa toàn "
     "bộ tablespace của MariaDB bằng encryption key do file_key_management plugin quản lý. "
     "Dù kẻ tấn công lấy cắp được ổ cứng vật lý của máy chủ emr-db01, họ vẫn không thể "
     "đọc được dữ liệu bệnh nhân vì toàn bộ file .ibd đều được mã hóa AES-256."),

    ("GĐ5 – MariaDB TDE & Mã hóa Dữ liệu", 41,
     "File .ibd lưu trữ trên ổ đĩa không chứa plain-text dữ liệu bệnh nhân",
     "Xác nhận strings command không tìm thấy dữ liệu nhạy cảm trong file .ibd",
     "SSH emr-db01 → strings /var/lib/mysql/openemr/patient_data.ibd | grep -i 'patient\\|diagnosis'",
     "Không có plain-text tên bệnh nhân, chẩn đoán trong file .ibd; chỉ binary/encrypted data",
     "Data – File Encryption / Physical Security", "Rất cao", "Bảo mật",
     "Test này thực hiện mô phỏng kịch bản tấn công vật lý: kẻ tấn công đã có quyền root trên "
     "máy chủ hoặc đánh cắp ổ cứng và trực tiếp đọc file dữ liệu. Nếu TDE hoạt động đúng, "
     "file .ibd chỉ chứa chuỗi byte ngẫu nhiên không có nghĩa. Đây là lớp bảo vệ cuối cùng "
     "của Zero Trust Data Protection: kể cả khi tất cả các lớp kiểm soát truy cập logic bị "
     "vượt qua, dữ liệu vật lý vẫn không thể đọc được nếu không có encryption master key."),

    ("GĐ5 – MariaDB TDE & Mã hóa Dữ liệu", 42,
     "MariaDB từ chối khởi động khi thiếu encryption key file",
     "Xác nhận DB không thể start nếu key file bị xóa hoặc mất",
     "Rename/xóa key file → systemctl restart mariadb → kiểm tra service status",
     "MariaDB khởi động thất bại; error log: 'Cannot find encryption key'; service không start",
     "Data – Key Management / Availability-Security Balance", "Cao", "Bảo mật",
     "Test này xác nhận tính chặt chẽ của Key Management: MariaDB TDE chỉ hoạt động khi có "
     "đúng encryption key, không có cơ chế fallback về plain-text. Điều này đảm bảo rằng "
     "không thể 'tắt' mã hóa bằng cách xóa key (hệ thống sẽ dừng toàn bộ thay vì tiếp tục "
     "hoạt động không mã hóa). Zero Trust Data Protection ưu tiên bảo mật hơn availability "
     "khi có xung đột – đây là quyết định kiến trúc đúng đắn cho dữ liệu y tế nhạy cảm."),

    ("GĐ5 – MariaDB TDE & Mã hóa Dữ liệu", 43,
     "OpenEMR hoạt động bình thường với MariaDB TDE (Transparent với ứng dụng)",
     "Xác nhận TDE không ảnh hưởng đến hoạt động nghiệp vụ của OpenEMR",
     "Tạo bệnh nhân mới trong OpenEMR sau khi bật TDE → query lại → kết quả hiển thị đúng",
     "Bệnh nhân mới tạo thành công; query trả về đúng; OpenEMR hoạt động bình thường; không lỗi DB",
     "Data – TDE Transparency / Application Compatibility", "Cao", "Chức năng",
     "'Transparent' trong TDE có nghĩa là ứng dụng bên trên (OpenEMR) không cần biết hay thay "
     "đổi code để hỗ trợ mã hóa – MariaDB tự động mã hóa khi ghi và giải mã khi đọc ở tầng "
     "storage engine. Test này xác nhận nguyên tắc ZTA rằng bảo mật phải được tích hợp vào "
     "hệ thống một cách trong suốt, không gây ra friction cho người dùng hoặc ứng dụng hợp lệ "
     "– 'Security without usability is no security at all'."),

    ("GĐ5 – MariaDB TDE & Mã hóa Dữ liệu", 44,
     "Client không thể kết nối trực tiếp MariaDB; OpenEMR kết nối bình thường (TC-18)",
     "FW-07 DENY và FW-06 ALLOW hoạt động đồng thời: Client→DB DENY, OpenEMR→DB ALLOW",
     "Client: mysql -h 10.10.50.10 timeout [DENY]\nOpenEMR tạo bệnh nhân mới thành công [ALLOW]",
     "Client kết nối bị từ chối; OpenEMR kết nối DB thành công; hai kết quả trái chiều xác nhận FW đúng",
     "Networks – DB Segmentation / Data Protection", "Rất cao", "Bảo mật",
     "Test kép này kiểm tra đồng thời cả hai chiều của firewall policy tại DB Zone: chiều DENY "
     "(ngăn Client trực tiếp vào DB) và chiều ALLOW (cho phép OpenEMR query DB để nghiệp vụ "
     "hoạt động). Đây là kiểm chứng trực tiếp cho nguyên tắc 'Network Micro-segmentation' của "
     "Zero Trust: mỗi zone chỉ nhận traffic từ đúng nguồn được ủy quyền, không có luồng "
     "ngang không kiểm soát (Lateral Movement) từ vùng người dùng đến vùng dữ liệu nhạy cảm."),

    # ──────────────────────────────────────────────────────────
    # GIAI ĐOẠN 6 – WAZUH SIEM/XDR: GIÁM SÁT AN NINH
    # ──────────────────────────────────────────────────────────
    ("GĐ6 – Wazuh SIEM & Giám sát An ninh", 45,
     "Wazuh Manager nhận kết nối từ tất cả 5 Agent",
     "Wazuh Manager v4.14.7 chạy; 5 Agent từ 5 VM đều Active",
     "Wazuh Dashboard → Agents; hoặc: /var/ossec/bin/agent_control -l",
     "5 Agent (emr-app01, zt-pomerium01, zt-keycloak01, zt-wazuh01, emr-db01) đều Active; TCP 1514/1515 ổn định",
     "Visibility – Monitoring / Agent Connectivity", "Cao", "Chức năng",
     "Trụ cột Visibility & Analytics của Zero Trust yêu cầu thu thập telemetry liên tục từ "
     "tất cả thành phần hệ thống. Wazuh Agent trên mỗi VM là đầu mối thu thập security events, "
     "log xác thực, cảnh báo thay đổi cấu hình và gửi về Wazuh Manager tập trung. Không có "
     "agent hoạt động trên một VM nào, VM đó trở thành 'blind spot' trong hệ thống giám sát, "
     "kẻ tấn công có thể hoạt động tự do mà không bị phát hiện."),

    ("GĐ6 – Wazuh SIEM & Giám sát An ninh", 46,
     "Wazuh phát cảnh báo Brute Force khi nhiều lần SSH thất bại (TC-19)",
     "Wazuh tạo alert khi phát hiện ≥5 lần SSH thất bại trong thời gian ngắn",
     "Thực hiện 5+ lần SSH sai password vào emr-app01 → kiểm tra Wazuh Dashboard",
     "Alert xuất hiện với Rule ID 5551+; level ≥ 5; chứa IP nguồn, số lần thất bại, timestamp",
     "Visibility – Threat Detection / Brute Force", "Rất cao", "Bảo mật",
     "Continuous Monitoring và Threat Detection là thành phần không thể thiếu trong ZTA theo "
     "nguyên tắc 'Assume Breach': dù kiến trúc đã ngăn chặn nhiều vector tấn công, hệ thống "
     "vẫn phải có khả năng phát hiện các hành vi bất thường xảy ra. Brute force SSH là kỹ "
     "thuật tấn công phổ biến nhất vào hạ tầng Linux. Wazuh phát cảnh báo kịp thời cho IT Admin "
     "để ngăn chặn trước khi kẻ tấn công thành công – đây là reactive defense layer của ZTA."),

    ("GĐ6 – Wazuh SIEM & Giám sát An ninh", 47,
     "Wazuh FIM phát hiện thay đổi file cấu hình Pomerium",
     "FIM theo dõi /etc/pomerium/config.yaml; cảnh báo khi file bị sửa",
     "Sửa nội dung /etc/pomerium/config.yaml trên zt-pomerium01 → kiểm tra Wazuh trong 5 phút",
     "FIM alert trong 5 phút; chứa file path, hash trước/sau, thời gian; Rule ID 550/553",
     "Visibility – FIM / Configuration Integrity", "Rất cao", "Bảo mật",
     "File Integrity Monitoring (FIM) là cơ chế phát hiện thay đổi cấu hình trái phép – một "
     "mối đe dọa nghiêm trọng khi kẻ tấn công đã vào được máy chủ và cố gắng thay đổi policy "
     "của Pomerium để tự cấp quyền truy cập. Nếu config.yaml bị sửa mà không bị phát hiện, "
     "toàn bộ cơ chế Policy Enforcement Point có thể bị vô hiệu hóa âm thầm. Wazuh FIM là "
     "lớp giám sát ZTA cuối cùng đảm bảo 'Configuration Integrity' của trụ cột Applications."),

    ("GĐ6 – Wazuh SIEM & Giám sát An ninh", 48,
     "Wazuh FIM phát hiện thay đổi file cấu hình MariaDB",
     "FIM theo dõi /etc/mysql/mariadb.conf.d/ trên emr-db01; cảnh báo khi sửa",
     "Sửa /etc/mysql/mariadb.conf.d/50-server.cnf → kiểm tra Wazuh alert",
     "FIM alert trong vòng 5 phút; thông tin file thay đổi; không bỏ sót sự kiện",
     "Visibility – FIM / DB Config Protection", "Cao", "Bảo mật",
     "Cấu hình MariaDB bao gồm đường dẫn key file TDE, cài đặt encryption, bind-address và "
     "các tham số bảo mật quan trọng. Nếu kẻ tấn công sửa file cấu hình DB để tắt TDE hoặc "
     "mở bind-address ra ngoài, toàn bộ lớp bảo vệ dữ liệu sẽ sụp đổ. Wazuh FIM phát hiện "
     "thay đổi này ngay lập tức và cảnh báo IT Admin để điều tra – thể hiện 'Continuous "
     "Monitoring' của trụ cột Visibility & Analytics trong ZTA."),

    ("GĐ6 – Wazuh SIEM & Giám sát An ninh", 49,
     "Log sự kiện đăng nhập thất bại Keycloak được thu thập vào Wazuh",
     "Events đăng nhập sai từ Keycloak được tập trung về Wazuh Manager",
     "Thực hiện 3 lần sai password trên Keycloak → kiểm tra Wazuh Dashboard filter Keycloak",
     "Wazuh hiển thị events Keycloak với: user, IP nguồn, timestamp, realm; alert tương ứng được tạo",
     "Visibility – Log Collection / Identity Events", "Cao", "Bảo mật",
     "Audit Logging tập trung là thành phần bắt buộc trong ZTA để đảm bảo khả năng forensics "
     "và incident response. Khi có sự cố xâm phạm danh tính, IT Admin phải có thể truy vết "
     "toàn bộ lịch sử đăng nhập thất bại từ Identity Provider (Keycloak) thông qua SIEM "
     "(Wazuh). Nếu log không được thu thập, hệ thống mù quáng trong việc phát hiện tấn công "
     "credential stuffing hoặc account takeover xảy ra qua nhiều ngày."),

    ("GĐ6 – Wazuh SIEM & Giám sát An ninh", 50,
     "Wazuh Dashboard hiển thị Security Overview đầy đủ cho IT Admin",
     "IT Admin xem được tổng quan an ninh hệ thống trên Wazuh Dashboard",
     "IT Admin truy cập https://10.10.30.20 → xem Security Events, Active Agents, Top Alerts",
     "Dashboard load thành công; 5 Active Agents hiển thị; biểu đồ alerts; không lỗi kết nối",
     "Visibility – Analytics / Security Dashboard", "Trung bình", "Chức năng",
     "Visibility & Analytics là trụ cột kích hoạt (enabling pillar) của Zero Trust: không có "
     "khả năng quan sát toàn diện, các quyết định bảo mật trở nên mù quáng và phản ứng chậm. "
     "Wazuh Dashboard cung cấp Security Operations Center (SOC) view cho IT Admin: xem real-time "
     "alerts, phân tích xu hướng tấn công, drill-down vào sự kiện cụ thể. Đây là công cụ "
     "để thực thi nguyên tắc 'Assume Breach' – luôn giả định đã bị tấn công và chủ động tìm kiếm."),

    # ──────────────────────────────────────────────────────────
    # GIAI ĐOẠN 7 – END-TO-END & KIỂM THỬ TÍCH HỢP
    # ──────────────────────────────────────────────────────────
    ("GĐ7 – End-to-End & Tích hợp", 51,
     "Luồng BF-01: Lễ tân tiếp nhận bệnh nhân mới end-to-end",
     "Luồng hoàn chỉnh: Lễ tân đăng nhập qua ZTA → tạo bệnh nhân → tạo encounter",
     "receptionist01 đăng nhập (Certificate + MFA) → tạo patient 'Nguyen Van A' → tạo encounter mới",
     "Không có lỗi 403 hay SSL; bệnh nhân tạo thành công; encounter được ghi nhận; traffic qua HTTPS",
     "End-to-End / BF-01 / Full ZTA Flow", "Cao", "End-to-End",
     "Test end-to-end xác nhận rằng kiến trúc Zero Trust không phá vỡ quy trình nghiệp vụ y tế "
     "thực tế. Một hệ thống bảo mật tốt phải cho phép người dùng hợp lệ hoàn thành công việc "
     "của mình mà không gặp rào cản không đáng có. BF-01 là nghiệp vụ đầu tiên trong vòng đời "
     "bệnh nhân – nếu Lễ tân không thể tiếp nhận bệnh nhân, toàn bộ chuỗi y tế (khám → xét "
     "nghiệm → hồ sơ) không thể bắt đầu. Test này xác nhận ZTA và usability cùng tồn tại."),

    ("GĐ7 – End-to-End & Tích hợp", 52,
     "Luồng BF-02: Bác sĩ khám bệnh và ghi chẩn đoán end-to-end",
     "Bác sĩ đăng nhập qua ZTA → mở hồ sơ → SOAP note → chẩn đoán → chỉ định XN",
     "doctor01 đăng nhập → mở bệnh nhân trong phạm vi → thêm SOAP note → diagnosis → lab order",
     "Tất cả bước hoàn thành; dữ liệu lưu vào DB; token OIDC hợp lệ trong suốt phiên",
     "End-to-End / BF-02 / Clinical Workflow", "Cao", "End-to-End",
     "Luồng khám bệnh (BF-02) là core nghiệp vụ của hệ thống EMR. Test này xác nhận Bác sĩ "
     "có thể thực hiện toàn bộ công việc lâm sàng thông qua kiến trúc Zero Trust mà không bị "
     "gián đoạn. Đặc biệt, nó kiểm tra token OIDC còn hợp lệ trong suốt phiên làm việc dài "
     "(Bác sĩ có thể khám nhiều bệnh nhân liên tiếp) – xác nhận Session Management của "
     "Pomerium và Keycloak không gây ra lỗi mid-session cho người dùng hợp lệ."),

    ("GĐ7 – End-to-End & Tích hợp", 53,
     "Luồng BF-03: Vòng đời xét nghiệm đầy đủ (Bác sĩ → KTV → Kết quả → Bác sĩ)",
     "Kiểm tra toàn bộ vòng đời: tạo chỉ định → xử lý → kết quả → đọc kết quả",
     "doctor01 tạo lab order → lab_tech01 nhập kết quả → confirm → doctor01 đọc kết quả",
     "Mỗi bước thực hiện bởi đúng vai trò; kết quả sau confirm không sửa được; dữ liệu nhất quán",
     "End-to-End / BF-03 / Multi-role Workflow", "Cao", "End-to-End",
     "BF-03 là test đa vai trò phức tạp nhất, yêu cầu 2 người dùng khác nhau (Bác sĩ và KTV) "
     "tương tác tuần tự với cùng một tài nguyên (chỉ định xét nghiệm). Trong ZTA, mỗi "
     "lần tương tác phải được xác thực và ủy quyền độc lập. Test này xác nhận rằng "
     "Separation of Duties hoạt động trong môi trường đa người dùng thực tế, không chỉ "
     "trên lý thuyết – và Pomerium/Keycloak xử lý đúng multiple concurrent sessions."),

    ("GĐ7 – End-to-End & Tích hợp", 54,
     "Luồng BF-04 + BF-05: Phân công hồ sơ và thu hồi quyền sau reassign",
     "Supervisor assign → Staff truy cập → Supervisor reassign → Staff cũ mất quyền ngay",
     "Supervisor assign C cho staff01 → staff01 access OK → reassign sang staff02 → staff01 HTTP 403",
     "4 bước đúng kết quả; quyền thay đổi ngay; staff01 mất quyền; staff02 nhận quyền",
     "End-to-End / BF-04+05 / Dynamic Access", "Cao", "End-to-End",
     "Dynamic Access Revocation là minh chứng mạnh nhất cho ZTA trong thực tế: quyền truy cập "
     "không phải 'được cấp một lần, dùng mãi' mà thay đổi theo context thực tế. Khi Supervisor "
     "reassign, staff01 mất quyền ngay lập tức mà không cần đăng xuất hay hết session. Điều "
     "này thể hiện Just-in-Time và Just-Enough-Access (JIT/JEA) – hai nguyên tắc quan trọng "
     "trong Zero Trust Privileged Access Management (PAM)."),

    ("GĐ7 – End-to-End & Tích hợp", 55,
     "Anti-Sniffing: Kẻ tấn công sniffing trong LAN chỉ thấy dữ liệu mã hóa",
     "Wireshark capture toàn bộ traffic nội bộ không tiết lộ dữ liệu y tế plain-text",
     "Wireshark capture trên vmbr1 khi Bác sĩ đang sử dụng hệ thống → phân tích packets",
     "100% packets là TLS encrypted; không tìm thấy plain-text dữ liệu bệnh nhân; không có HTTP không mã hóa",
     "Data – Encryption in Transit / Anti-Sniffing / Insider Threat", "Rất cao", "Bảo mật",
     "Test này mô phỏng kịch bản Insider Threat: một nhân viên IT hoặc kẻ tấn công đã xâm nhập "
     "được vào mạng LAN nội bộ và gắn máy sniffing (ARP poisoning, switch port mirror) để nghe "
     "lén traffic. ZTA yêu cầu mã hóa end-to-end ngay cả trong mạng nội bộ vì 'mạng nội bộ "
     "không đáng tin tưởng hơn Internet'. Nếu test FAIL (traffic plain-text), toàn bộ dữ liệu "
     "y tế bệnh nhân có thể bị thu thập bởi bất kỳ ai trong cùng VLAN."),

    ("GĐ7 – End-to-End & Tích hợp", 56,
     "Ngăn chặn Lateral Movement: Compromise VLAN10 không tấn công được VLAN40/50",
     "Từ VLAN10 Client compromise không thể scan hay kết nối đến App/DB Zone",
     "Từ client compromise: nmap -sV 10.10.40.0/24; nmap -sV 10.10.50.0/24; nc -zv 10.10.40.10 443",
     "nmap không phát hiện open ports từ VLAN10; kết nối TCP bị drop; Proxmox Firewall ghi log deny",
     "Networks – Lateral Movement Prevention / Micro-segmentation", "Rất cao", "Bảo mật",
     "Lateral Movement là kỹ thuật tấn công nguy hiểm nhất trong môi trường mạng phẳng: sau khi "
     "xâm nhập một máy, kẻ tấn công di chuyển ngang để đến các hệ thống giá trị cao hơn. "
     "Zero Trust Network Micro-segmentation (6 VLANs + Proxmox Firewall) thiết kế để chặn "
     "hoàn toàn lateral movement: mỗi zone là một 'trust boundary' độc lập. Test này là "
     "kiểm chứng hiệu quả nhất rằng nguyên tắc 'Assume Breach' được thực thi vật lý: "
     "dù bị compromise tại VLAN10, kẻ tấn công vẫn không thể tiếp cận VLAN40 hay VLAN50."),

    ("GĐ7 – End-to-End & Tích hợp", 57,
     "Certificate Revocation: Thu hồi cert → thiết bị mất quyền ngay lập tức",
     "Revoke client certificate → thiết bị đó không thể kết nối; thiết bị khác của cùng user vẫn được",
     "Revoke cert của doctor01-device trong CA → doctor01 cố đăng nhập từ thiết bị đó",
     "Pomerium từ chối mTLS; thiết bị không kết nối; thiết bị khác của doctor01 vẫn truy cập được",
     "Devices – Certificate Revocation / Device Trust", "Cao", "Bảo mật",
     "Certificate Revocation là cơ chế thu hồi Device Trust ngay lập tức khi thiết bị bị mất, "
     "đánh cắp hoặc không còn được quản lý. Khác với việc xóa tài khoản (thu hồi Identity), "
     "revoke certificate thu hồi quyền của thiết bị cụ thể mà không ảnh hưởng đến tài khoản "
     "người dùng trên các thiết bị khác. Test này xác nhận ZTA thực thi Device Trust ở mức "
     "độ hạt nhân (granular): một thiết bị, một certificate, một mức độ tin cậy riêng biệt."),

    ("GĐ7 – End-to-End & Tích hợp", 58,
     "Multi-user: 5 người dùng đồng thời, phiên độc lập, không session leak",
     "5 user đăng nhập đồng thời; mỗi phiên độc lập; không có dữ liệu chéo giữa các phiên",
     "5 users (doctor01, supervisor01, receptionist01, lab_tech01, records_staff01) đăng nhập đồng thời → kiểm tra dữ liệu từng phiên",
     "Mỗi phiên độc lập; không session collision; mỗi user chỉ thấy dữ liệu của mình; 5 events trong Wazuh",
     "Identity – Session Isolation / Multi-user Concurrency", "Cao", "End-to-End",
     "Session Isolation là yêu cầu bảo mật quan trọng trong môi trường multi-tenant: phiên làm "
     "việc của Bác sĩ A không được lẫn vào phiên của Bác sĩ B, đặc biệt khi cả hai cùng xem "
     "hồ sơ bệnh nhân khác nhau. Test này xác nhận Pomerium và Keycloak xử lý đúng session "
     "isolation trong môi trường đồng thời thực tế – một yêu cầu production-readiness quan "
     "trọng trước khi triển khai trong bệnh viện thực tế."),

    # ──────────────────────────────────────────────────────────
    # GIAI ĐOẠN 8 – KIỂM THỬ HIỆU NĂNG & ĐỘ BỀN
    # ──────────────────────────────────────────────────────────
    ("GĐ8 – Hiệu năng & Độ bền", 59,
     "Overhead độ trễ của Zero Trust Gateway ≤ 500ms",
     "Đo thêm độ trễ khi request đi qua Pomerium + Keycloak OIDC so với truy cập trực tiếp",
     "curl --write-out time_total: qua Pomerium vs nội bộ trực tiếp (10 lần, lấy trung bình)",
     "Overhead ZTA Gateway ≤ 500ms; page load total < 3s; trải nghiệm sử dụng được trong thực tế",
     "Performance – Latency / Usability / ZTA Overhead", "Trung bình", "Hiệu năng",
     "Zero Trust đôi khi bị phê phán vì thêm độ trễ do multiple authentication hops "
     "(Client → Pomerium → Keycloak → OpenEMR). Test này đo lường overhead thực tế để "
     "xác nhận rằng bảo mật ZTA không gây ra trải nghiệm người dùng không chấp nhận được. "
     "Ngưỡng 500ms là tiêu chuẩn UX thực tế trong y tế: Bác sĩ cần phản hồi nhanh khi tra "
     "cứu hồ sơ bệnh nhân khẩn cấp. Usability là điều kiện để ZTA được chấp nhận và triển khai."),

    ("GĐ8 – Hiệu năng & Độ bền", 60,
     "Hệ thống ổn định sau 1 giờ hoạt động liên tục",
     "Không có service crash, memory leak hoặc lỗi tích lũy sau 1 giờ tải liên tục",
     "Script tự động gửi request mỗi 30 giây trong 1 giờ → kiểm tra log Pomerium, Keycloak, OpenEMR",
     "Không có crash; không có OOM; response time ổn định; không lỗi tích lũy trong log; 5 Wazuh Agent vẫn kết nối",
     "Performance – Stability / Reliability / Production Readiness", "Trung bình", "Hiệu năng",
     "Stability testing xác nhận hệ thống ZTA đủ ổn định để triển khai môi trường production "
     "bệnh viện. Các dịch vụ như Keycloak (xử lý token), Pomerium (proxy hàng nghìn request) "
     "và Wazuh (thu thập log liên tục) phải hoạt động bền vững không bị memory leak hay "
     "connection exhaustion. Một hệ thống ZTA mạnh về bảo mật nhưng không ổn định sẽ "
     "gây ra downtime cho dịch vụ y tế – điều không thể chấp nhận trong môi trường bệnh viện."),

    ("GĐ8 – Hiệu năng & Độ bền", 61,
     "Hệ thống tự phục hồi sau khi restart service Pomerium",
     "Sau khi Pomerium restart, OIDC connection tự tái thiết lập; người dùng đăng nhập lại bình thường",
     "Restart Pomerium service → chờ 60 giây → truy cập https://emr.hospital.local → đăng nhập",
     "Pomerium khởi động lại trong < 30 giây; OIDC reconnect tự động; người dùng đăng nhập thành công sau 60 giây",
     "Performance – Auto-recovery / Resilience / OIDC Reconnection", "Trung bình", "Hiệu năng",
     "Resilience là thuộc tính quan trọng của ZTA trong production: Policy Enforcement Point "
     "(Pomerium) có thể cần restart để áp dụng cập nhật cấu hình hoặc sau khi có lỗi. "
     "Hệ thống phải tự phục hồi mà không cần can thiệp thủ công. Test này xác nhận "
     "auto-reconnect OIDC với Keycloak sau restart – đảm bảo không có thời gian downtime "
     "kéo dài gây gián đoạn truy cập y tế, đặc biệt quan trọng với hệ thống bệnh viện "
     "hoạt động 24/7."),
]

# ══════════════════════════════════════════════════════════════
#  MÀU SẮC THEO GIAI ĐOẠN
# ══════════════════════════════════════════════════════════════
PHASE_COLORS = {
    "GĐ1 – Hạ tầng Proxmox & VLAN":       ("1A237E", "E3F2FD"),
    "GĐ2 – Keycloak IAM & Identity":        ("1B5E20", "E8F5E9"),
    "GĐ3 – Pomerium Gateway & mTLS":        ("4A148C", "F3E5F5"),
    "GĐ4 – OpenEMR RBAC & Nghiệp vụ":      ("E65100", "FFF3E0"),
    "GĐ5 – MariaDB TDE & Mã hóa Dữ liệu":  ("B71C1C", "FFEBEE"),
    "GĐ6 – Wazuh SIEM & Giám sát An ninh":  ("37474F", "ECEFF1"),
    "GĐ7 – End-to-End & Tích hợp":          ("004D40", "E0F2F1"),
    "GĐ8 – Hiệu năng & Độ bền":             ("F57F17", "FFFDE7"),
}

SEVERITY_COLORS = {
    "Rất cao":   "C62828",
    "Cao":       "E65100",
    "Trung bình":"F9A825",
}

# ══════════════════════════════════════════════════════════════
#  HÀM HELPER
# ══════════════════════════════════════════════════════════════
def hex_fill(hex_color):
    return PatternFill("solid", fgColor=hex_color)

def thin_border():
    s = Side(style="thin", color="BDBDBD")
    return Border(left=s, right=s, top=s, bottom=s)

def header_font(size=11, bold=True, color="FFFFFF"):
    return Font(name="Calibri", size=size, bold=bold, color=color)

def cell_font(size=10, bold=False, color="212121"):
    return Font(name="Calibri", size=size, bold=bold, color=color)

def wrap_align(h="left", v="top"):
    return Alignment(horizontal=h, vertical=v, wrap_text=True)

# ══════════════════════════════════════════════════════════════
#  SHEET 1: TỔNG HỢP TEST CASES (đủ 11 cột)
# ══════════════════════════════════════════════════════════════
def build_main_sheet(ws):
    ws.title = "Toan bo Test Cases"

    # ── Row 1: Tiêu đề dự án ─────────────────────────────────
    ws.merge_cells("A1:K1")
    c = ws["A1"]
    c.value = "ZERO TRUST HOSPITAL - BO TEST CASE TOAN DIEN"
    c.font = Font(name="Calibri", size=15, bold=True, color="FFFFFF")
    c.fill = hex_fill("0D1B2A")
    c.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 34

    # ── Row 2: Thông tin dự án ───────────────────────────────
    ws.merge_cells("A2:K2")
    c = ws["A2"]
    c.value = (f"Du an: Bao mat Ho so Y te bang Zero Trust (ZTNA + IAM) - Du An CNTT  |  "
               f"Nhom: 52300267 - 52300268  |  GVHD: TS. Bui Quy Anh  |  "
               f"Ngay tao: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    c.font = Font(name="Calibri", size=10, italic=True, color="ECEFF1")
    c.fill = hex_fill("263238")
    c.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 18

    # ── Row 3: Giải thích cột Mức độ ─────────────────────────
    ws.merge_cells("A3:K3")
    c = ws["A3"]
    c.value = (
        "  [*] COT 'MUC DO UU TIEN' = Muc do uu tien thuc hien test case, "
        "danh gia ket hop 3 tieu chi: (1) Rui ro bao mat neu FAIL, "
        "(2) Muc do the hien nguyen tac Zero Trust, "
        "(3) Anh huong den toan bo luong he thong. "
        "Rat cao = Fail gay lo hong bao mat ngay lap tuc hoac pha vo nguyen tac core ZTA. "
        "Cao = Fail anh huong dang ke den chuc nang hoac bao mat. "
        "Trung binh = Fail chi anh huong den hieu nang hoac trai nghiem nguoi dung."
    )
    c.font = Font(name="Calibri", size=9, italic=True, color="212121")
    c.fill = hex_fill("FFF9C4")
    c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    c.border = Border(left=Side(style="medium", color="F9A825"),
                      right=Side(style="medium", color="F9A825"),
                      top=Side(style="medium", color="F9A825"),
                      bottom=Side(style="medium", color="F9A825"))
    ws.row_dimensions[3].height = 48

    # ── Row 4: Header cột ────────────────────────────────────
    HEADERS = [
        ("A",  9,  "Ma TC"),
        ("B",  28, "Giai doan"),
        ("C",  5,  "STT"),
        ("D",  36, "Ten Test"),
        ("E",  40, "Mo ta"),
        ("F",  42, "Buoc thuc hien / Du lieu dau vao"),
        ("G",  52, "Yeu cau Dau ra (Dieu kien PASS)"),
        ("H",  28, "Tieu chi Zero Trust (CISA / NIST)"),
        ("I",  13, "Muc do\nUu tien"),
        ("J",  14, "Loai Test"),
        ("K",  65, "Giai thich: Test nay chung minh nguyen tac Zero Trust nhu the nao"),
    ]

    for col_letter, col_width, col_header in HEADERS:
        ws.column_dimensions[col_letter].width = col_width
        cell = ws[f"{col_letter}4"]
        cell.value = col_header
        cell.font = header_font(10)
        cell.fill = hex_fill("1565C0")
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = thin_border()
    ws.row_dimensions[4].height = 30

    # ── Rows 5+: Dữ liệu ─────────────────────────────────────
    row = 5
    for tc in TEST_CASES:
        (phase, stt, name, desc, inputs, outputs,
         zt_criteria, severity, test_type, zt_explanation) = tc

        phase_key = phase.split("–")[0].strip().replace(" ", "").upper()
        tc_code = f"TC-{phase_key}-{stt:02d}"

        hdark, hlight = PHASE_COLORS.get(phase, ("424242", "F5F5F5"))
        row_fill = hex_fill(hlight)

        data_row = [tc_code, phase, stt, name, desc, inputs,
                    outputs, zt_criteria, severity, test_type, zt_explanation]
        cols = ["A","B","C","D","E","F","G","H","I","J","K"]

        for col_letter, value in zip(cols, data_row):
            cell = ws[f"{col_letter}{row}"]
            cell.value = value
            cell.fill = row_fill
            cell.border = thin_border()
            cell.font = cell_font()
            cell.alignment = wrap_align()

            if col_letter == "I":
                sev_color = SEVERITY_COLORS.get(severity, "757575")
                cell.font = Font(name="Calibri", size=10, bold=True, color=sev_color)
                cell.alignment = Alignment(horizontal="center", vertical="top", wrap_text=True)
            if col_letter in ("A", "C", "J"):
                cell.alignment = Alignment(horizontal="center", vertical="top", wrap_text=True)
            if col_letter == "B":
                cell.font = Font(name="Calibri", size=9, bold=True, color=hdark)
            if col_letter == "K":
                cell.fill = hex_fill("FAFAFA")
                cell.font = Font(name="Calibri", size=9, italic=False, color="37474F")

        ws.row_dimensions[row].height = 95
        row += 1

    ws.freeze_panes = "A5"
    ws.auto_filter.ref = f"A4:K{row-1}"

# ══════════════════════════════════════════════════════════════
#  SHEET 2: THỐNG KÊ TỔNG QUAN
# ══════════════════════════════════════════════════════════════
def build_summary_sheet(ws):
    ws.title = "Thong ke Tong quan"

    from collections import Counter
    phase_count = Counter(tc[0] for tc in TEST_CASES)
    severity_count = Counter(tc[7] for tc in TEST_CASES)
    type_count = Counter(tc[8] for tc in TEST_CASES)

    ws.merge_cells("A1:E1")
    c = ws["A1"]
    c.value = "THONG KE BO TEST CASE ZERO TRUST HOSPITAL"
    c.font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
    c.fill = hex_fill("0D1B2A")
    c.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 30

    # ── Chú thích Mức độ ưu tiên ─────────────────────────────
    ws.merge_cells("A2:E5")
    note_cell = ws["A2"]
    note_cell.value = (
        "GIAI THICH COT 'MUC DO UU TIEN KIEM THU'\n\n"
        "Rat cao  :  FAIL gay lo hong bao mat ngay lap tuc HOAC pha vo nguyen tac core cua Zero Trust Architecture. "
        "Day la nhung test case PHAI PASS truoc khi coi he thong la an toan. Vi du: bypass Pomerium, thieu MFA, "
        "client ket noi thang DB.\n\n"
        "Cao  :  FAIL anh huong dang ke den chuc nang va bao mat nhung chua phai catastrophic. "
        "Can pass de he thong hoat dong dung theo thiet ke. Vi du: Pomerium-Keycloak OIDC, RBAC role assignment.\n\n"
        "Trung binh  :  FAIL chu yeu anh huong den hieu nang, do on dinh hoac trai nghiem nguoi dung. "
        "Quan trong de production nhung khong phai security blocker. Vi du: latency, stability sau 1 gio."
    )
    note_cell.font = Font(name="Calibri", size=10, color="212121")
    note_cell.fill = hex_fill("FFFDE7")
    note_cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    note_cell.border = Border(
        left=Side(style="medium", color="F9A825"),
        right=Side(style="medium", color="F9A825"),
        top=Side(style="medium", color="F9A825"),
        bottom=Side(style="medium", color="F9A825"),
    )
    for r in range(2, 6):
        ws.row_dimensions[r].height = 36

    row = 7
    # ── Tổng ─────────────────────────────────────────────────
    ws[f"A{row}"].value = "Tong so Test Cases"
    ws[f"A{row}"].font = Font(name="Calibri", size=12, bold=True, color="1565C0")
    ws[f"B{row}"].value = len(TEST_CASES)
    ws[f"B{row}"].font = Font(name="Calibri", size=14, bold=True, color="C62828")
    ws[f"B{row}"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[row].height = 24
    row += 2

    # ── Theo Giai đoạn ────────────────────────────────────────
    for label, fill_hex, data in [
        ("Phan bo theo Giai doan", "1565C0",
         [(p, c) for p, c in sorted(phase_count.items())]),
        ("Phan bo theo Muc do Uu tien", "C62828",
         [("Rat cao", severity_count.get("Rat cao",0)),
          ("Cao", severity_count.get("Cao",0)),
          ("Trung binh", severity_count.get("Trung binh",0))]),
        ("Phan bo theo Loai Test", "004D40",
         sorted(type_count.items(), key=lambda x: -x[1])),
    ]:
        ws[f"A{row}"].value = label
        ws[f"B{row}"].value = "So luong"
        ws[f"C{row}"].value = "Ti le"
        for col in ["A","B","C"]:
            cell = ws[f"{col}{row}"]
            cell.font = header_font(10)
            cell.fill = hex_fill(fill_hex)
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = thin_border()
        ws.row_dimensions[row].height = 22
        row += 1

        for name_item, count_item in data:
            phase_color_dark = PHASE_COLORS.get(name_item, ("424242","F5F5F5"))[0]
            phase_color_light = PHASE_COLORS.get(name_item, ("424242","F5F5F5"))[1]
            sev_color = SEVERITY_COLORS.get(name_item, "212121")

            ws[f"A{row}"].value = name_item
            ws[f"B{row}"].value = count_item
            ws[f"C{row}"].value = f"{count_item/len(TEST_CASES)*100:.1f}%"
            for col in ["A","B","C"]:
                cell = ws[f"{col}{row}"]
                cell.border = thin_border()
                cell.font = cell_font()
                cell.alignment = Alignment(
                    horizontal="center" if col in ["B","C"] else "left",
                    vertical="center", wrap_text=True)
            ws.row_dimensions[row].height = 18
            row += 1
        row += 1

    ws.column_dimensions["A"].width = 42
    ws.column_dimensions["B"].width = 14
    ws.column_dimensions["C"].width = 12

# ══════════════════════════════════════════════════════════════
#  SHEET 3: CHECKLIST THỰC THI
# ══════════════════════════════════════════════════════════════
def build_checklist_sheet(ws):
    ws.title = "Checklist Thuc thi"

    ws.merge_cells("A1:I1")
    c = ws["A1"]
    c.value = "CHECKLIST THUC THI - KET QUA KIEM THU THUC TE"
    c.font = Font(name="Calibri", size=12, bold=True, color="FFFFFF")
    c.fill = hex_fill("0D1B2A")
    c.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 26

    HEADERS = [
        ("A", 10,  "Ma TC"),
        ("B", 34,  "Ten Test"),
        ("C", 16,  "Giai doan"),
        ("D", 13,  "Muc do\nUu tien"),
        ("E", 18,  "Ket qua\n(PASS/FAIL/SKIP)"),
        ("F", 32,  "Ghi chu thuc thi / Loi phat sinh"),
        ("G", 20,  "Nguoi thuc hien"),
        ("H", 16,  "Ngay kiem thu"),
        ("I", 42,  "Giai thich Zero Trust (tom tat)"),
    ]

    for col_letter, col_width, col_header in HEADERS:
        ws.column_dimensions[col_letter].width = col_width
        cell = ws[f"{col_letter}2"]
        cell.value = col_header
        cell.font = header_font(10)
        cell.fill = hex_fill("37474F")
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = thin_border()
    ws.row_dimensions[2].height = 30

    row = 3
    for tc in TEST_CASES:
        (phase, stt, name, desc, inputs, outputs,
         zt_criteria, severity, test_type, zt_explanation) = tc

        phase_key = phase.split("–")[0].strip().replace(" ", "").upper()
        tc_code = f"TC-{phase_key}-{stt:02d}"
        hdark, hlight = PHASE_COLORS.get(phase, ("424242", "F5F5F5"))

        # Tóm tắt giải thích ZT (lấy câu đầu)
        zt_summary = zt_explanation.split(".")[0].strip() + "."

        row_data = [tc_code, name, phase, severity, "", "", "", "", zt_summary]
        cols = ["A","B","C","D","E","F","G","H","I"]

        for col_letter, value in zip(cols, row_data):
            cell = ws[f"{col_letter}{row}"]
            cell.value = value
            cell.border = thin_border()
            cell.alignment = wrap_align(
                "center" if col_letter in ["A","D","E","G","H"] else "left")
            cell.font = cell_font()
            if col_letter == "C":
                cell.fill = hex_fill(hlight)
                cell.font = Font(name="Calibri", size=9, bold=True, color=hdark)
            elif col_letter == "D":
                sev_color = SEVERITY_COLORS.get(severity, "757575")
                cell.font = Font(name="Calibri", size=10, bold=True, color=sev_color)
            elif col_letter == "I":
                cell.fill = hex_fill("FAFAFA")
                cell.font = Font(name="Calibri", size=8, italic=True, color="455A64")

        ws.row_dimensions[row].height = 36
        row += 1

    ws.freeze_panes = "A3"
    ws.auto_filter.ref = f"A2:I{row-1}"

# ══════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════
def main():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, "ZeroTrust_TestCases_Toan_Dien.xlsx")
    print("Dang tao file Excel bo Test Case (v2 - co cot Giai thich Zero Trust)...")

    wb = Workbook()
    del wb[wb.sheetnames[0]]

    ws_main = wb.create_sheet()
    build_main_sheet(ws_main)
    print("  Sheet 1: Toan bo Test Cases (11 cot)")

    ws_summary = wb.create_sheet()
    build_summary_sheet(ws_summary)
    print("  Sheet 2: Thong ke & Tong quan")

    ws_checklist = wb.create_sheet()
    build_checklist_sheet(ws_checklist)
    print("  Sheet 3: Checklist Thuc thi")

    wb.save(output_file)
    print(f"\nHoan thanh! File da duoc luu: {output_file}")
    print(f"Tong so test cases: {len(TEST_CASES)}")

    from collections import Counter
    phase_count = Counter(tc[0] for tc in TEST_CASES)
    print("\nPhan bo theo giai doan:")
    for phase, count in sorted(phase_count.items()):
        print(f"   {phase}: {count} tests")

    severity_count = Counter(tc[7] for tc in TEST_CASES)
    print("\nPhan bo theo muc do uu tien:")
    for sev, count in [("Rat cao", severity_count.get("Rat cao",0)),
                        ("Cao", severity_count.get("Cao",0)),
                        ("Trung binh", severity_count.get("Trung binh",0))]:
        print(f"   {sev}: {count} tests")

if __name__ == "__main__":
    main()
