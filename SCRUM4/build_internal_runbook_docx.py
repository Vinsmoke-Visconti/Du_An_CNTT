# -*- coding: utf-8 -*-
"""
Script tạo file Word: HUONG_DAN_DEMO_NOI_BO.docx
Định dạng Runbook kỹ thuật nội bộ nhóm (Không văn nói, tập trung thao tác, mục đích, ý nghĩa và đầu ra chuẩn)
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_runbook_docx(output_path):
    doc = docx.Document()
    for s in doc.sections:
        s.top_margin = Inches(0.7)
        s.bottom_margin = Inches(0.7)
        s.left_margin = Inches(0.75)
        s.right_margin = Inches(0.75)

    # Tiêu đề
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p_title.add_run("SỔ TAY THỰC THI DEMO NỘI BỘ (RUNBOOK)\n")
    r1.font.bold = True
    r1.font.size = Pt(16)
    r1.font.color.rgb = RGBColor(13, 27, 42)

    r2 = p_title.add_run("HỆ THỐNG ZERO TRUST HOSPITAL · HƯỚNG DẪN THAO TÁC & TIÊU CHUẨN ĐẦU RA\n")
    r2.font.bold = True
    r2.font.size = Pt(12)
    r2.font.color.rgb = RGBColor(21, 101, 192)

    r3 = p_title.add_run("Lưu hành nội bộ: Huỳnh Nguyễn Quốc Việt (52300267) – Nguyễn Hoàng Việt (52300268)\n"
                        "Dự Án CNTT (2026 – 2027) | Không dùng văn nói | Chạy thực hành đối soát chéo 2 người")
    r3.font.italic = True
    r3.font.size = Pt(9.5)
    r3.font.color.rgb = RGBColor(90, 90, 90)

    def add_h1(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(4)
        r = h.add_run(text)
        r.font.bold = True
        r.font.size = Pt(13)
        r.font.color.rgb = RGBColor(13, 71, 161)
        return h

    def add_h2(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(10)
        h.paragraph_format.space_after = Pt(3)
        r = h.add_run(text)
        r.font.bold = True
        r.font.size = Pt(11.5)
        r.font.color.rgb = RGBColor(0, 105, 92)
        return h

    def add_step_card(stt_str, title_str, goal_str, meaning_str, actions_list, expected_str, tag_res):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, "FAFAFA")
        set_cell_margins(cell, top=100, bottom=100, left=140, right=140)

        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r_head = p.add_run(f"[{stt_str}] {title_str}\n")
        r_head.font.bold = True
        r_head.font.size = Pt(10.5)
        r_head.font.color.rgb = RGBColor(21, 101, 192)

        r_g_label = p.add_run("• Mục đích kỹ thuật: ")
        r_g_label.font.bold = True
        r_g_label.font.size = Pt(9)
        r_g = p.add_run(f"{goal_str}\n")
        r_g.font.size = Pt(9)

        r_m_label = p.add_run("• Ý nghĩa đối với Zero Trust: ")
        r_m_label.font.bold = True
        r_m_label.font.size = Pt(9)
        r_m_label.font.color.rgb = RGBColor(198, 40, 40)
        r_m = p.add_run(f"{meaning_str}\n")
        r_m.font.size = Pt(9)

        r_a_label = p.add_run("• Thao tác thực hiện chi tiết:\n")
        r_a_label.font.bold = True
        r_a_label.font.size = Pt(9)
        for act in actions_list:
            r_act = p.add_run(f"   - {act}\n")
            r_act.font.size = Pt(8.5)

        r_exp_label = p.add_run(f"• Tiêu chuẩn đầu ra chuẩn [{tag_res}]: ")
        r_exp_label.font.bold = True
        r_exp_label.font.size = Pt(9)
        if "ALLOW" in tag_res or "PASS" in tag_res:
            r_exp_label.font.color.rgb = RGBColor(46, 125, 50)
        elif "DENY" in tag_res:
            r_exp_label.font.color.rgb = RGBColor(198, 40, 40)
        else:
            r_exp_label.font.color.rgb = RGBColor(230, 81, 0)
        
        r_exp = p.add_run(f"{expected_str}")
        r_exp.font.size = Pt(9)
        r_exp.font.bold = True

        doc.add_paragraph().paragraph_format.space_after = Pt(3)

    # 1. BẢNG TÀI KHOẢN VÀ THÔNG SỐ
    add_h1("1. BẢNG THÔNG SỐ VÀ TÀI KHOẢN ĐỐI SOÁT NHANH")
    
    headers_u = ["Username", "Password", "Role Keycloak", "Role OpenEMR", "Ngữ cảnh kiểm thử"]
    data_u = [
        ["receptionist01", "Receptionist@2026", "receptionist", "Receptionist", "Tiếp nhận BN A, tạo lượt khám (BF-01)"],
        ["doctor01", "Doctor@2026", "doctor", "Physician", "Khám BN A (Tim mạch), chẩn đoán, chỉ định CLS (BF-02)"],
        ["doctor02", "Doctor@2026", "doctor", "Physician", "Phụ trách BN B (Nội tổng quát) - Đối chứng ngoài phạm vi"],
        ["lab_tech01", "Labtech@2026", "lab", "Clinician / Lab", "Nhập KQ xét nghiệm BN A, xác nhận Final (BF-03)"],
        ["supervisor01", "Supervisor@2026", "supervisor", "Medical Records Supervisor", "Phân công BN A, chuyển giao sang Staff 2 (BF-05)"],
        ["records_staff01", "Records@2026", "records", "Medical Records", "Xem BN A khi được gán; mất quyền khi reassign (BF-04/05)"],
        ["records_staff02", "Records@2026", "records", "Medical Records", "Nhận BN A sau khi chuyển giao (BF-05)"],
        ["itadmin01", "ITAdmin@2026", "itadmin", "Administrator (System)", "Cấu hình kỹ thuật; bị chặn xem dữ liệu bệnh án"]
    ]
    tbl_u = doc.add_table(rows=len(data_u)+1, cols=len(headers_u))
    tbl_u.alignment = WD_TABLE_ALIGNMENT.CENTER
    for c_i, h in enumerate(headers_u):
        cell = tbl_u.cell(0, c_i)
        set_cell_background(cell, "1565C0")
        set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_i, row_val in enumerate(data_u):
        for c_i, val in enumerate(row_val):
            cell = tbl_u.cell(r_i+1, c_i)
            if r_i % 2 == 1:
                set_cell_background(cell, "F5F5F5")
            set_cell_margins(cell, top=50, bottom=50, left=60, right=60)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8)
            if c_i == 0:
                r.font.bold = True

    # 2. PRE-DEMO CHECKLIST
    add_h1("2. PRE-DEMO CHECKLIST (RÀ SOÁT TRƯỚC KHI TEST)")
    checks = [
        "P1: Kiểm tra Proxmox 9.2-1 (https://10.10.60.10:8006): 5 VM 100-104 đang ở trạng thái Running màu xanh.",
        "P2: File hosts client: 10.10.20.10 emr.hospital.local authenticate.hospital.local; 10.10.30.10 keycloak.hospital.local; 10.10.30.20 wazuh.hospital.local.",
        "P3: Trình duyệt A đã import chứng chỉ doctor01.pfx; Trình duyệt B để trắng cert để test kịch bản Deny.",
        "P4: Google Authenticator điện thoại đã scan mã QR OTP cho các user demo.",
        "P5: Mở 2 terminal SSH: (1) Host Proxmox 10.10.60.10 để tcpdump; (2) CSDL VM104 10.10.50.10 để kiểm tra file .ibd."
    ]
    for c in checks:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(c)
        r.font.size = Pt(8.5)

    # MODULE 1
    add_h1("3. MODULE 1: HẠ TẦNG MẠNG & TƯỜNG LỬA PHÂN ĐOẠN (NETWORKS)")
    add_step_card(
        "1.1", "Kiểm tra 6 VLAN & 5 VM Skeleton trên Proxmox",
        "Xác thực cấu hình mạng ảo hóa đúng Config Contract.",
        "Loại bỏ mạng phẳng (Flat Network). Cô lập các vùng dịch vụ, ngăn chặn quét ngang L2 giữa các máy chủ.",
        ["Đăng nhập https://10.10.60.10:8006 -> Node pve01 -> System -> Network.",
         "Kiểm tra vmbr1: bridge-vlan-aware = yes; có đủ 6 VLAN (10, 20, 30, 40, 50, 60).",
         "Kiểm tra danh sách VM: 100 (tag 40), 101 (tag 20), 102 (tag 30), 103 (tag 30), 104 (tag 50)."],
        "vmbr1 cấu hình VLAN aware thành công, 5 VM gán đúng VLAN tương ứng theo hợp đồng.", "PASS"
    )
    add_step_card(
        "1.2", "Kiểm tra luồng mạng hợp lệ (ALLOW Traffic)",
        "Xác minh các kết nối nội bộ thiết yếu thông tuyến theo chính sách tường lửa.",
        "Zero Trust mở luồng kết nối có kiểm soát theo Policy giữa PEP, IdP, App và Database.",
        ["Từ VM101 (Pomerium), chạy: curl -I -k https://10.10.30.10:8443/.../openid-configuration",
         "Từ VM101, chạy: curl -I http://10.10.40.10:80",
         "Từ VM100 (OpenEMR), chạy: nc -zv 10.10.50.10 3306"],
        "HTTP/2 200 OK với Keycloak; HTTP 200/302 với OpenEMR; Cổng 3306 mở thành công.", "ALLOW"
    )
    add_step_card(
        "1.3", "[CHỐNG BYPASS] Chặn Client truy cập trực tiếp OpenEMR & MariaDB (DENY Traffic)",
        "Chứng minh tường lửa drop kết nối cố tình đi tắt bỏ qua Pomerium Gateway.",
        "Triệt tiêu hoàn toàn nguy cơ Bypass Gateway và ngăn chặn di chuyển ngang (Lateral Movement).",
        ["Từ máy Client (VLAN 10), chạy: curl -k https://10.10.40.10 --connect-timeout 5",
         "Từ máy Client, chạy: Test-NetConnection -ComputerName 10.10.50.10 -Port 3306"],
        "curl báo Connection timed out; Test-NetConnection trả về TcpTestSucceeded = False. FW drop toàn bộ.", "DENY"
    )

    # MODULE 2
    add_h1("4. MODULE 2: XÁC THỰC THIẾT BỊ mTLS (DEVICES TRUST)")
    add_step_card(
        "2.1", "Thiết bị chưa tin cậy (Thiếu Client Cert) bị chặn tại TLS Handshake",
        "Kiểm chứng Pomerium downstream_client_ca từ chối thiết bị lạ.",
        "Trụ cột Devices CISA: Thiết bị phải được chứng thực trước khi được phép gửi request đến hệ thống y tế.",
        ["Mở Trình duyệt B (không có chứng chỉ máy trạm).",
         "Truy cập: https://emr.hospital.local"],
        "Lỗi SSL 400 Bad Request: No required SSL certificate was sent (ERR_BAD_SSL_CLIENT_AUTH_CERT).", "DENY"
    )
    add_step_card(
        "2.2", "Thiết bị được cấp phép hoàn tất mTLS Handshake",
        "Xác minh máy trạm cài cert nội bộ được thông qua bắt tay 2 chiều.",
        "Thiết bị tin cậy được chuyển tiếp sang bước xác thực danh tính người dùng.",
        ["Mở Trình duyệt A (đã cài doctor01.pfx).",
         "Truy cập https://emr.hospital.local -> Hộp thoại chọn chứng chỉ xuất hiện -> Nhấn OK."],
        "Bắt tay TLS thành công, trình duyệt tự động redirect sang Keycloak Login.", "ALLOW"
    )

    # MODULE 3
    add_h1("5. MODULE 3: QUẢN LÝ DANH TÍNH KEYCLOAK & MFA TOTP (IDENTITY)")
    add_step_card(
        "3.1", "Xác thực thất bại khi sai credentials",
        "Kiểm chứng cơ chế Explicit Verification và ghi log an ninh.",
        "Không chấp nhận danh tính chưa được kiểm tra nghiêm ngặt; ghi nhận sự kiện để SIEM giám sát.",
        ["Tại Keycloak, nhập: doctor01 / SaiPassword123 -> Nhấn Sign In."],
        "Báo lỗi đỏ Invalid username or password; không tạo session; ghi event log LOGIN_ERROR.", "DENY"
    )
    add_step_card(
        "3.2", "Bắt buộc Xác thực Đa yếu tố (MFA / TOTP)",
        "Chứng minh mật khẩu đúng vẫn không đủ nếu thiếu yếu tố xác thực thứ 2.",
        "Chống lộ mật khẩu qua phishing/credential stuffing. Bắt buộc có thiết bị sinh mã OTP.",
        ["Nhập đúng doctor01 / Doctor@2026 -> Màn hình OTP xuất hiện.",
         "Thử nhập sai mã OTP: 999888 -> Báo lỗi Invalid code (DENY).",
         "Mở Google Authenticator trên điện thoại, nhập đúng mã TOTP hiện tại -> Bấm Submit (ALLOW)."],
        "Keycloak cấp phiên đăng nhập thành công, phát hành JWT Access Token về Pomerium.", "ALLOW / DENY"
    )
    add_step_card(
        "3.3", "Kiểm tra Role claim và Pomerium Policy Route",
        "Đối soát token chứa claim đúng vai trò và gateway cho phép vào OpenEMR.",
        "Policy-Based Access Control (PBAC): Chỉ user sở hữu role được định nghĩa trong route mới được forward.",
        ["F12 -> Application/Cookies -> Kiểm tra cookie _pomerium.",
         "Token payload chứa realm_access.roles: ['doctor']. Khớp route policy của Pomerium."],
        "Trình duyệt tải thành công trang chủ làm việc của OpenEMR.", "ALLOW"
    )
    add_step_card(
        "3.4", "Kiểm tra thu hồi phiên làm việc tức thì (Session Invalidation)",
        "Đảm bảo mất cookie/hết hạn phiên thì quyền truy cập bị ngắt tức thì.",
        "Continuous Validation: Xác thực liên tục, ngăn ngừa chiếm đoạt phiên (Session Hijacking).",
        ["F12 -> Cookies -> Xóa cookie _pomerium -> Nhấn F5 trang OpenEMR."],
        "Pomerium chặn ngay lập tức, redirect về Keycloak yêu cầu đăng nhập lại.", "DENY"
    )

    # MODULE 4
    add_h1("6. MODULE 4: PHÂN QUYỀN OPENEMR RBAC & 5 LUỒNG NGHIỆP VỤ (APPLICATIONS)")
    add_step_card(
        "4.1", "BF-01: Lễ tân Tiếp nhận & Giới hạn Quyền hành chính (Least Privilege)",
        "Lễ tân chỉ làm thủ tục tiếp nhận, bị cấm xem/sửa dữ liệu chuyên môn.",
        "Least Privilege: Nhân viên tiếp đón không được tiếp cận bệnh lý hay kết quả xét nghiệm.",
        ["Đăng nhập receptionist01 -> Tạo BN 'Nguyễn Văn A' (Save thành công).",
         "Tạo lượt khám mới tại Khoa Tim mạch thành công (ALLOW).",
         "Lễ tân cố bấm vào menu Chẩn đoán (Diagnosis) hoặc Xét nghiệm (Lab Results)."],
        "Tạo BN & Encounter thành công; Menu chẩn đoán/xét nghiệm bị Access Denied / Ẩn hoàn toàn.", "ALLOW / DENY"
    )
    add_step_card(
        "4.2", "BF-02: Bác sĩ Khám bệnh & Kiểm soát Phạm vi Phụ trách (Context-Aware)",
        "Bác sĩ khám BN được phân công; bị chặn sửa đổi BN của bác sĩ khác.",
        "Context-Aware Access: Quyền thao tác dựa trên phân công phụ trách, không phải role chung chung.",
        ["Đăng nhập doctor01 -> Mở BN A -> Nhập SOAP Note, chẩn đoán ICD-10 (I20.9), chỉ định XN máu -> Save OK (ALLOW).",
         "doctor01 tìm và mở BN B (Trần Thị B do doctor02 phụ trách) -> Cố gắng sửa chẩn đoán/xóa ghi chú."],
        "BN A lưu khám thành công; BN B bị từ chối quyền chỉnh sửa ngoài phạm vi phụ trách.", "ALLOW / DENY"
    )
    add_step_card(
        "4.3", "BF-03: KTV Xét nghiệm & Tính Bất biến Dữ liệu WORM (Separation of Duties)",
        "KTV nhập kết quả; khi xác nhận Final thì dữ liệu bị đóng băng; KTV không được sửa chẩn đoán bác sĩ.",
        "Tách biệt nhiệm vụ và tính toàn vẹn dữ liệu (WORM). Chống sửa đổi gian lận kết quả xét nghiệm hồi tố.",
        ["Đăng nhập lab_tech01 -> Vào Procedures -> Nhập KQ máu: RBC 4.8, WBC 8.5, Hb 145 -> Bấm Confirm Results.",
         "Thử click sửa lại số liệu sau khi đã Final -> Bị khóa (DENY).",
         "Thử bấm vào mục Chẩn đoán của Bác sĩ -> Bị từ chối quyền (DENY)."],
        "Kết quả chuyển trạng thái FINAL, các trường chuyển Read-Only; Chặn can thiệp chẩn đoán bác sĩ.", "ALLOW / DENY"
    )
    add_step_card(
        "4.4", "BF-04 & BF-05: Medical Records Assignment & Thu hồi Quyền Động (Dynamic Revocation)",
        "Nhân viên hồ sơ chỉ xem BN khi được Supervisor gán; khi bị chuyển giao thì mất quyền tức thì.",
        "Just-In-Time Access & Dynamic Access Revocation: Quyền hạn gắn liền với phân công hiện hành và bị tước tức thời.",
        ["Đăng nhập supervisor01 -> Phân công BN A cho records_staff01.",
         "records_staff01 mở BN A thành công (ALLOW); mở BN C chưa phân công -> Bị chặn 403 (DENY).",
         "[ĐIỂM NHẤN]: supervisor01 chuyển giao BN A sang cho records_staff02.",
         "records_staff01 nhấn F5 -> LẬP TỨC BỊ CHẶN 403 ACCESS DENIED theo thời gian thực!",
         "records_staff02 đăng nhập -> Mở xem BN A thành công."],
        "Staff 1 xem được khi được gán, mất quyền ngay khi Reassign; Staff 2 nhận quyền chuẩn.", "ALLOW / DENY"
    )
    add_step_card(
        "4.5", "Segregation of Duties: IT Admin Quản trị nhưng KHÔNG Xem Bệnh án",
        "Quản trị viên CNTT quản lý hạ tầng kỹ thuật nhưng bị tước quyền đọc bệnh án.",
        "Loại bỏ 'Superuser toàn năng'. Tách biệt kỹ thuật khỏi dữ liệu y tế nhạy cảm (tuân thủ Privacy/HIPAA).",
        ["Đăng nhập itadmin01 -> Vào Administration -> Quản lý Users, Globals, Logs (ALLOW).",
         "itadmin01 thử truy cập danh sách bệnh nhân và nội dung hồ sơ bệnh án."],
        "Quản trị kỹ thuật hoạt động bình thường; Danh mục bệnh án bị từ chối truy cập / rỗng.", "ALLOW / DENY"
    )

    # MODULE 5
    add_h1("7. MODULE 5: BẢO VỆ DỮ LIỆU ĐA TẦNG (DATA PROTECTION: TRANSIT & AT-REST)")
    add_step_card(
        "5.1", "Bắt gói tin chứng minh Chống Nghe Lén (Anti-Sniffing / Data in Transit)",
        "Chứng minh dữ liệu trên đường truyền giữa các vùng mạng đều mã hóa TLS.",
        "Assume Breach: Mạng LAN nội bộ coi như không an toàn. Chống nghe lén Man-in-the-Middle trong bệnh viện.",
        ["SSH vào Proxmox host 10.10.60.10 -> Chạy: tcpdump -i vmbr1 -nn -s 0 -X 'tcp port 443' -c 10",
         "Thực hiện click thao tác trên trình duyệt để phát sinh lưu lượng.",
         "Quan sát gói tin hiển thị trên terminal."],
        "100% payload là nhị phân mã hóa TLS Application Data, không tìm thấy plain-text tên bệnh nhân.", "DATA PROTECTED"
    )
    add_step_card(
        "5.2", "Quét thô ổ đĩa chứng minh Mã hóa CSDL MariaDB TDE (Data at Rest)",
        "Kiểm tra tệp tin CSDL .ibd vật lý được mã hóa AES-256 mức tablespace.",
        "Bảo vệ dữ liệu vật lý. Dù kẻ trộm tháo trộm ổ cứng vật lý cũng không đọc được hồ sơ bệnh án thô.",
        ["SSH vào emr-db01 (10.10.50.10) -> MySQL: SHOW PLUGINS; -> file_key_management ACTIVE.",
         "Kiểm tra SHOW VARIABLES: innodb_encrypt_tables = ON, innodb_encrypt_log = ON.",
         "Chạy lệnh Linux: strings /var/lib/mysql/openemr/patient_data.ibd | grep -i 'Nguyen Van A'"],
        "strings không tìm thấy bất kỳ chuỗi plain-text nào (exit code 1). Dữ liệu được mã hóa toàn vẹn.", "DATA ENCRYPTED"
    )

    # MODULE 6
    add_h1("8. MODULE 6: GIÁM SÁT AN NINH TẬP TRUNG WAZUH SIEM/XDR (VISIBILITY)")
    add_step_card(
        "6.1", "Kiểm tra trạng thái kết nối 5 Agents tập trung",
        "Xác nhận 5 VM đẩy telemetry an ninh liên tục về máy chủ giám sát.",
        "Visibility & Analytics CISA: Loại bỏ hoàn toàn điểm mù thông tin (Zero Blind Spot).",
        ["Truy cập https://10.10.30.20 -> Đăng nhập admin Wazuh -> Vào mục Agents."],
        "Hiển thị đủ 5 Agents (001-005) tương ứng 5 VM với trạng thái Active màu xanh.", "PASS"
    )
    add_step_card(
        "6.2", "Mô phỏng tấn công SSH Brute Force và xem cảnh báo thời gian thực",
        "Thử nghiệm khả năng phát hiện hành vi dò quét mật khẩu vào máy chủ ứng dụng.",
        "Assume Breach: Chủ động phát hiện đe dọa điểm cuối theo thời gian thực để phản ứng kịp thời.",
        ["Từ máy Client, chạy thử sai SSH 6 lần: for i in {1..6}; do sshpass -p 'Sai123' ssh -o StrictHostKeyChecking=no admin@10.10.40.10; done",
         "Trên Wazuh Dashboard, mở tab Security Events."],
        "Cảnh báo đỏ Level 10 (Rule ID 5712: SSHD brute force) xuất hiện tức thì kèm IP nguồn và timestamp.", "ALERT TRIGGERED"
    )
    add_step_card(
        "6.3", "Giám sát Toàn vẹn Tệp tin (File Integrity Monitoring - FIM)",
        "Phát hiện hành vi can thiệp trái phép vào file cấu hình chính sách của Gateway.",
        "Bảo vệ tính toàn vẹn của Policy Engine. Cảnh báo ngay khi file config.yaml bị sửa đổi.",
        ["SSH vào VM101 (Pomerium) -> Chạy: sudo echo '# Tamper test' >> /etc/pomerium/config.yaml",
         "Trên Wazuh Dashboard, kiểm tra mục Integrity Monitoring (FIM)."],
        "Wazuh ghi nhận sự kiện Rule ID 550, hiển thị file bị sửa và so sánh mã băm SHA1/MD5 trước/sau.", "FIM ALERT"
    )

    # 9. BẢNG TỔNG HỢP TRẠNG THÁI KIỂM THỬ (TEST LOG SHEET)
    add_h1("9. BẢNG TỔNG HỢP TRẠNG THÁI KIỂM THỬ (TEST LOG SHEET)")
    
    headers_log = ["Module", "STT", "Nội dung kiểm thử", "Kết quả mong đợi", "Đánh giá", "Người test"]
    data_log = [
        ["M1", "1.1", "Trạng thái 6 VLAN & 5 VM trên PVE", "VLAN-aware OK, 5 VM gán đúng tag", "[PASS]", "Hoàng Việt"],
        ["M1", "1.2", "Luồng mạng hợp lệ (Pomerium/IdP/DB)", "Port 8443, 80, 3306 thông tuyến", "[PASS]", "Hoàng Việt"],
        ["M1", "1.3", "Chặn Client kết nối thẳng OpenEMR/DB", "Connection timeout, FW drop hoàn toàn", "[PASS]", "Quốc Việt"],
        ["M2", "2.1", "Trình duyệt thiếu Cert truy cập Gateway", "SSL 400 Bad Request / Handshake drop", "[PASS]", "Quốc Việt"],
        ["M2", "2.2", "Trình duyệt có Cert hợp lệ", "mTLS OK, redirect mượt sang Keycloak", "[PASS]", "Quốc Việt"],
        ["M3", "3.1", "Đăng nhập sai password Keycloak", "Invalid credentials, ghi audit log", "[PASS]", "Quốc Việt"],
        ["M3", "3.2", "Bắt buộc mã MFA OTP", "Sai OTP chặn, Đúng cấp token OIDC", "[PASS]", "Quốc Việt"],
        ["M3", "3.3", "Pomerium Policy Route role claim", "Role doctor được forward vào OpenEMR", "[PASS]", "Quốc Việt"],
        ["M3", "3.4", "Xóa cookie phiên (Session Invalidation)", "Mất phiên tức thì, chuyển về login", "[PASS]", "Quốc Việt"],
        ["M4", "4.1", "BF-01 Lễ tân: tạo BN/khám; chặn bệnh lý", "Tạo BN/khám OK, chặn chẩn đoán/XN", "[PASS]", "Hoàng Việt"],
        ["M4", "4.2", "BF-02 Bác sĩ: khám BN gán; chặn BN khác", "Lưu BN A OK, chặn sửa BN B", "[PASS]", "Hoàng Việt"],
        ["M4", "4.3", "BF-03 KTV xét nghiệm: nhập KQ, khóa WORM", "Finalized chuyển Read-Only, chặn sửa", "[PASS]", "Hoàng Việt"],
        ["M4", "4.4", "BF-04/05 Medical Records Assignment & Reassign", "Gán xem OK; Reassign mất quyền tức thì", "[PASS]", "Hoàng Việt"],
        ["M4", "4.5", "IT Admin quản trị; chặn xem bệnh án", "Cấu hình IT OK, chặn xem hồ sơ y tế", "[PASS]", "Hoàng Việt"],
        ["M5", "5.1", "Anti-sniffing: tcpdump bắt gói tin vmbr1", "100% TLS nhị phân, 0 plain-text", "[PASS]", "Hoàng Việt"],
        ["M5", "5.2", "MariaDB TDE: quét strings file .ibd", "strings không tìm thấy dữ liệu thô", "[PASS]", "Hoàng Việt"],
        ["M6", "6.1", "Kiểm tra 5 Wazuh Agents kết nối Active", "5/5 Agents trạng thái Active màu xanh", "[PASS]", "Quốc Việt"],
        ["M6", "6.2", "Tấn công SSH brute force tạo cảnh báo", "Rule 5712 (Level 10) xuất hiện tức thì", "[PASS]", "Quốc Việt"],
        ["M6", "6.3", "Sửa config.yaml tạo cảnh báo FIM", "Rule 550 phát hiện thay đổi mã băm", "[PASS]", "Quốc Việt"]
    ]

    tbl_log = doc.add_table(rows=len(data_log)+1, cols=len(headers_log))
    tbl_log.alignment = WD_TABLE_ALIGNMENT.CENTER
    for c_i, h in enumerate(headers_log):
        cell = tbl_log.cell(0, c_i)
        set_cell_background(cell, "37474F")
        set_cell_margins(cell, top=60, bottom=60, left=60, right=60)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_i, row_val in enumerate(data_log):
        for c_i, val in enumerate(row_val):
            cell = tbl_log.cell(r_i+1, c_i)
            if r_i % 2 == 1:
                set_cell_background(cell, "ECEFF1")
            set_cell_margins(cell, top=50, bottom=50, left=60, right=60)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8)
            if c_i == 4:
                r.font.bold = True
                r.font.color.rgb = RGBColor(46, 125, 50)
            elif c_i in [0, 1]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r.font.bold = True

    doc.save(output_path)
    print(f"[OK] Da tao thanh cong file Word Runbook: {output_path}")

if __name__ == "__main__":
    out_file = r"d:\NAM_IV (2026-27)\DU_AN_CNTT\SCRUM4\HUONG_DAN_DEMO_NOI_BO.docx"
    create_runbook_docx(out_file)
