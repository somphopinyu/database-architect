import json
import random
import time
from browser import document, html, window, svg

# ==================== GAME DATA CONFIGURATION ====================

MISSIONS = [
    {
        "id": "intro",
        "title": "ความหมายและคำศัพท์พื้นฐานระบบฐานข้อมูล",
        "company": "ห้องฝึกอบรม DevBuilder SA",
        "difficulty": "Intro",
        "difficulty_class": "diff-easy",
        "avatar": "📚",
        "brief": "ยินดีต้อนรับสู่คอร์สปูพื้นฐานก่อนปฏิบัติงานจริงครับ! ก่อนที่เราจะเริ่มออกแบบฐานข้อมูลให้ลูกค้าจริง เราต้องมาทำความเข้าใจแนวคิดพื้นฐานเหล่านี้ก่อนนะครับ:<br>"
                 "1. <strong>ระบบฐานข้อมูล (Database)</strong>: แหล่งเก็บรวบรวมข้อมูลที่มีความสัมพันธ์กันเพื่อนำไปใช้ประโยชน์ เช่น ระบบสารสนเทศโรงเรียน<br>"
                 "2. <strong>ระบบจัดการฐานข้อมูล (DBMS)</strong>: ซอฟต์แวร์ตัวกลางที่คอยควบคุมและจัดการข้อมูลให้มีระเบียบและปลอดภัย เช่น MySQL, Oracle, SQL Server<br>"
                 "3. <strong>ตาราง (Table / Relation)</strong>: โครงสร้างจัดเก็บข้อมูลเป็นแถวและคอลัมน์<br>"
                 "4. <strong>ส่วนประกอบและบทบาทหน้าที่</strong>: เช่น แถวข้อมูล (Record), คอลัมน์ (Field), และบทบาทอย่าง DBA, Designer, End User<br>"
                 "มาทำความเข้าใจคำศัพท์พื้นฐานเหล่านี้ให้ถูกต้องกันก่อนลุยงานจริงนะครับ!",
        "tables": {
            "database": {
                "title": "Database (ฐานข้อมูล)",
                "attributes": {
                    "ระบบเก็บข้อมูลธนาคาร": {"type": "Field / Attribute", "is_pk": False},
                    "ระบบสารสนเทศโรงเรียน": {"type": "Field / Attribute", "is_pk": False}
                }
            },
            "dbms": {
                "title": "DBMS (ระบบจัดการฐานข้อมูล)",
                "attributes": {
                    "ซอฟต์แวร์ MySQL / Oracle": {"type": "Field / Attribute", "is_pk": False},
                    "ซอฟต์แวร์ SQL Server / Access": {"type": "Field / Attribute", "is_pk": False}
                }
            },
            "table": {
                "title": "Table (ตาราง / ความสัมพันธ์)",
                "attributes": {
                    "Rows & Columns (มิติตาราง)": {"type": "Field / Attribute", "is_pk": False},
                    "ตารางข้อมูล Students": {"type": "Field / Attribute", "is_pk": False}
                }
            }
        },
        "l2_custom_tables": {
            "student_table": {
                "title": "ตารางตัวอย่าง (Students Table)",
                "attributes": {
                    "student_id": {"type": "Primary Key (คีย์หลัก)", "is_pk": True},
                    "first_name": {"type": "Field / Attribute", "is_pk": False},
                    "ข้อมูลนักเรียน 1 แถว (Row)": {"type": "Record / Tuple", "is_pk": False},
                    "ตัวเลข หรือ ข้อความตัวอักษร": {"type": "Data Type (ชนิดข้อมูล)", "is_pk": False}
                }
            }
        },
        "relationships": [
            {"from_table": "dba", "from_col": "ผู้ดูแลระบบ (DBA)", "to_table": "duties", "to_col": "ติดตั้งซอฟต์แวร์และกำหนดสิทธิ์ผู้ใช้งาน"},
            {"from_table": "dba", "from_col": "ผู้ดูแลระบบ (DBA)", "to_table": "duties", "to_col": "สำรองและกู้คืนข้อมูลยามระบบเสียหาย"},
            {"from_table": "designer", "from_col": "ผู้ออกแบบ (Designer)", "to_table": "duties", "to_col": "วิเคราะห์ข้อมูลความต้องการและวาด ERD"},
            {"from_table": "designer", "from_col": "ผู้ออกแบบ (Designer)", "to_table": "duties", "to_col": "กำหนดโครงสร้างและคีย์หลักของตาราง"},
            {"from_table": "user", "from_col": "ผู้ใช้งาน (End User)", "to_table": "duties", "to_col": "ป้อนข้อมูลและทำรายการหน้าร้านประจำวัน"},
            {"from_table": "user", "from_col": "ผู้ใช้งาน (End User)", "to_table": "duties", "to_col": "กดเรียกดูรายงานสรุปยอดขายผ่านโปรแกรม"}
        ],
        "l3_custom_tables": {
            "dba": {
                "title": "บทบาท: DBA",
                "attributes": {
                    "ผู้ดูแลระบบ (DBA)": {"type": "สิทธิ์การจัดการระบบ", "is_pk": True}
                }
            },
            "designer": {
                "title": "บทบาท: Database Designer",
                "attributes": {
                    "ผู้ออกแบบ (Designer)": {"type": "โครงสร้างตาราง", "is_pk": True}
                }
            },
            "user": {
                "title": "บทบาท: End User",
                "attributes": {
                    "ผู้ใช้งาน (End User)": {"type": "การป้อนและค้นข้อมูล", "is_pk": True}
                }
            },
            "duties": {
                "title": "ภาระหน้าที่ความรับผิดชอบ",
                "attributes": {
                    "ติดตั้งซอฟต์แวร์และกำหนดสิทธิ์ผู้ใช้งาน": {"type": "ผู้ดูแลระบบ", "is_pk": False, "is_fk": True},
                    "สำรองและกู้คืนข้อมูลยามระบบเสียหาย": {"type": "ผู้ดูแลระบบ", "is_pk": False, "is_fk": True},
                    "วิเคราะห์ข้อมูลความต้องการและวาด ERD": {"type": "ผู้ออกแบบ", "is_pk": False, "is_fk": True},
                    "กำหนดโครงสร้างและคีย์หลักของตาราง": {"type": "ผู้ออกแบบ", "is_pk": False, "is_fk": True},
                    "ป้อนข้อมูลและทำรายการหน้าร้านประจำวัน": {"type": "ผู้ใช้งานทั่วไป", "is_pk": False, "is_fk": True},
                    "กดเรียกดูรายงานสรุปยอดขายผ่านโปรแกรม": {"type": "ผู้ใช้งานทั่วไป", "is_pk": False, "is_fk": True}
                }
            }
        }
    },
    {
        "id": "cafe",
        "title": "ระบบร้านกาแฟ Caffeine Hub",
        "company": "Caffeine Hub Ltd.",
        "difficulty": "Easy",
        "difficulty_class": "diff-easy",
        "avatar": "☕",
        "brief": "สวัสดีจ้าพี่เจี๊ยบเอง! พี่กำลังจะเปิดร้านกาแฟใหม่ อยากได้ระบบช่วยเก็บข้อมูลลูกค้าที่มาซื้อและรายการขายจ้ะ โดยรายละเอียดของข้อมูลมีดังนี้นะ:<br>"
                 "1. <strong>ตาราง Customers (ลูกค้า)</strong>: พี่ต้องการเก็บรหัสลูกค้า (customer_id) ซึ่งจะกำหนดให้รหัสสะสมแต้มเป็นโค้ดสั้น (ใช้ข้อความ 10 ตัวอักษร เช่น C000000001) ชื่อเล่นของลูกค้าเก็บเป็นข้อความไม่เกิน 50 ตัวอักษร และเบอร์โทรศัพท์ยาว 15 ตัวอักษรจ้า<br>"
                 "2. <strong>ตาราง Products (สินค้า)</strong>: ร้านพี่มีรายการขาย ซึ่งต้องจัดเก็บรหัสสินค้า (product_id) เป็นรหัสข้อความ 10 ตัวอักษร (เช่น PRD-000001) ชื่อรายการสินค้าเก็บเป็นข้อความไม่เกิน 100 ตัวอักษร และราคาขายต่อชิ้นเก็บเป็นตัวเลขทศนิยม (Decimal ขนาด 5, 2 เพื่อเก็บราคามีทศนิยม เช่น 55.50) จ้ะ<br>"
                 "3. <strong>ตาราง Orders (การสั่งซื้อ)</strong>: ตัวประวัติใบเสร็จการขาย พี่อยากบันทึกรหัสใบเสร็จ (order_id) เป็นรหัสข้อความ 15 ตัวอักษร (เช่น ORD-2026-00001) เก็บวันที่และเวลาที่สั่งซื้อ (Datetime) และจำนวนชิ้นที่สั่งเก็บเป็นจำนวนเต็ม (Integer) โดยต้องเชื่อมด้วยว่าใบเสร็จนี้ออกให้ลูกค้าคนไหน และซื้อสินค้าชิ้นไหนไปจ้า ซึ่งประเภทข้อมูลของไอดีเหล่านั้นจะต้องตรงกับตารางหลักด้วยนะจ๊ะ!<br>"
                 "ฝากคุณ SA ช่วยออกแบบตารางข้อมูลและเชื่อมโยงให้ถูกต้องทีนะจ๊ะ!",
        "tables": {
            "customers": {
                "title": "Customers (ลูกค้า)",
                "attributes": {
                    "customer_id": {"type": "VARCHAR(10)", "is_pk": True},
                    "first_name": {"type": "VARCHAR(50)", "is_pk": False},
                    "phone_number": {"type": "VARCHAR(15)", "is_pk": False}
                }
            },
            "products": {
                "title": "Products (สินค้า)",
                "attributes": {
                    "product_id": {"type": "VARCHAR(10)", "is_pk": True},
                    "product_name": {"type": "VARCHAR(100)", "is_pk": False},
                    "price": {"type": "DECIMAL(5,2)", "is_pk": False}
                }
            },
            "orders": {
                "title": "Orders (การสั่งซื้อ)",
                "attributes": {
                    "order_id": {"type": "VARCHAR(15)", "is_pk": True},
                    "customer_id": {"type": "VARCHAR(10)", "is_pk": False, "is_fk": True, "ref_table": "customers", "ref_col": "customer_id"},
                    "product_id": {"type": "VARCHAR(10)", "is_pk": False, "is_fk": True, "ref_table": "products", "ref_col": "product_id"},
                    "order_date": {"type": "DATETIME", "is_pk": False},
                    "quantity": {"type": "INT", "is_pk": False}
                }
            }
        },
        "relationships": [
            {"from_table": "customers", "from_col": "customer_id", "to_table": "orders", "to_col": "customer_id"},
            {"from_table": "products", "from_col": "product_id", "to_table": "orders", "to_col": "product_id"}
        ]
    },
    {
        "id": "warehouse",
        "title": "ระบบจัดการคลังสินค้า SafeKeep",
        "company": "SafeKeep Logistics Co.",
        "difficulty": "Medium",
        "difficulty_class": "diff-medium",
        "avatar": "📦",
        "brief": "สวัสดีครับ ผมนพ ผู้จัดการฝ่ายคลังสินค้า ตอนนี้ระบบสต็อกของเราเจอปัญหาสิ่งของปนเปกันหมด อยากรบกวนช่วยออกแบบดังนี้ครับ:<br>"
                 "1. <strong>ตาราง Products (สินค้า)</strong>: เก็บข้อมูลตัวสินค้า มีรหัสสินค้า (product_id) เป็นรหัสโค้ดตัวอักษร 10 ตัวอักษร (เช่น P000000001) ชื่อสินค้าไม่เกิน 100 ตัวอักษร และหมวดหมู่ไม่เกิน 50 ตัวอักษร พร้อมรหัสของซัพพลายเออร์ที่ส่งสินค้านี้เข้ามา<br>"
                 "2. <strong>ตาราง Suppliers (ผู้ส่งสินค้า)</strong>: รายละเอียดซัพพลายเออร์ มีรหัสผู้ส่งสินค้า (supplier_id) เป็นตัวอักษร 10 ตัวอักษร ชื่อบริษัทผู้ส่งสินค้าไม่เกิน 100 ตัวอักษร และเบอร์โทรติดต่อยาว 15 ตัวอักษรครับ<br>"
                 "3. <strong>ตาราง Staff (พนักงานคลัง)</strong>: ข้อมูลพนักงาน มีรหัสพนักงาน (staff_id) เป็นรหัสตัวอักษร 10 ตัวอักษร ชื่อพนักงานไม่เกิน 100 ตัวอักษร และแผนกที่สังกัดไม่เกิน 50 ตัวอักษรครับ<br>"
                 "4. <strong>ตาราง StockIn (รายการนำเข้าสินค้า)</strong>: ประวัติการรับสินค้า มีรหัสรายการนำเข้า (transaction_id) ซึ่งออกรหัสเป็นโค้ดข้อความ 15 ตัวอักษร (เช่น TXN000000000001) จำนวนสินค้าที่นำเข้าเก็บเป็นจำนวนเต็ม (Integer) และวันที่นำเข้าคลังเก็บเป็นวันและเวลา (Datetime) โดยในบันทึกนี้จะต้องระบุรหัสสินค้าที่นำเข้า และรหัสพนักงานที่เป็นคนเซ็นรับสินค้า ซึ่งไอดีเชื่อมโยงเหล่านี้ต้องตรงกับตารางหลักด้วยนะครับ!<br>"
                 "ช่วยเชื่อมตารางข้อมูลให้ครบถ้วนด้วยนะครับผม!",
        "tables": {
            "products": {
                "title": "Products (สินค้า)",
                "attributes": {
                    "product_id": {"type": "VARCHAR(10)", "is_pk": True},
                    "product_name": {"type": "VARCHAR(100)", "is_pk": False},
                    "category": {"type": "VARCHAR(50)", "is_pk": False},
                    "supplier_id": {"type": "VARCHAR(10)", "is_pk": False, "is_fk": True, "ref_table": "suppliers", "ref_col": "supplier_id"}
                }
            },
            "suppliers": {
                "title": "Suppliers (ผู้ส่งสินค้า)",
                "attributes": {
                    "supplier_id": {"type": "VARCHAR(10)", "is_pk": True},
                    "company_name": {"type": "VARCHAR(100)", "is_pk": False},
                    "phone_number": {"type": "VARCHAR(15)", "is_pk": False}
                }
            },
            "staff": {
                "title": "Staff (พนักงานคลัง)",
                "attributes": {
                    "staff_id": {"type": "VARCHAR(10)", "is_pk": True},
                    "name": {"type": "VARCHAR(100)", "is_pk": False},
                    "department": {"type": "VARCHAR(50)", "is_pk": False}
                }
            },
            "stock_in": {
                "title": "StockIn (การนำเข้า)",
                "attributes": {
                    "transaction_id": {"type": "VARCHAR(15)", "is_pk": True},
                    "product_id": {"type": "VARCHAR(10)", "is_pk": False, "is_fk": True, "ref_table": "products", "ref_col": "product_id"},
                    "staff_id": {"type": "VARCHAR(10)", "is_pk": False, "is_fk": True, "ref_table": "staff", "ref_col": "staff_id"},
                    "quantity": {"type": "INT", "is_pk": False},
                    "received_date": {"type": "DATETIME", "is_pk": False}
                }
            }
        },
        "relationships": [
            {"from_table": "suppliers", "from_col": "supplier_id", "to_table": "products", "to_col": "supplier_id"},
            {"from_table": "products", "from_col": "product_id", "to_table": "stock_in", "to_col": "product_id"},
            {"from_table": "staff", "from_col": "staff_id", "to_table": "stock_in", "to_col": "staff_id"}
        ]
    },
    {
        "id": "school",
        "title": "ระบบงานทะเบียนโรงเรียนศึกษาดี",
        "company": "SuksaDee School",
        "difficulty": "Hard",
        "difficulty_class": "diff-hard",
        "avatar": "🏫",
        "brief": "สวัสดีค่ะคุณ SA ครูวิภาเองค่ะ ตอนนี้ฝ่ายทะเบียนต้องการจัดเก็บข้อมูลแบบความสัมพันธ์ให้ถูกต้องและเป็นระบบค่ะ โดยมีข้อกำหนดของขนาดข้อมูลดังนี้นะคะ:<br>"
                 "1. <strong>ตาราง Students (นักเรียน)</strong>: เก็บข้อมูลนักเรียน มีรหัสนักเรียน (student_id) เป็นรหัสโค้ดตัวอักษร 10 ตัวอักษร (เช่น S000000001) ชื่อและนามสกุลเก็บเป็นข้อความไม่เกินอย่างละ 50 ตัวอักษร และวันเกิดของนักเรียนเก็บเป็นวันที่ (Date) ค่ะ<br>"
                 "2. <strong>ตาราง Teachers (คุณครู)</strong>: ข้อมูลครูผู้สอน มีรหัสครู (teacher_id) เป็นข้อความ 10 ตัวอักษร ชื่ออาจารย์ไม่เกิน 100 ตัวอักษร และอีเมลไม่เกิน 100 ตัวอักษรค่ะ<br>"
                 "3. <strong>ตาราง Classrooms (ห้องเรียน)</strong>: ข้อมูลสถานที่เรียน มีรหัสห้องเรียน (room_id) เป็นรหัสตัวอักษร 10 ตัวอักษร (เช่น ROOM-00001) ตึกเรียนไม่เกิน 50 ตัวอักษร และความจุที่นั่งเก็บเป็นจำนวนเต็ม (Integer) ค่ะ<br>"
                 "4. <strong>ตาราง Courses (รายวิชา)</strong>: ข้อมูลรายวิชา มีรหัสวิชา (course_code) เป็นโค้ดข้อความ 10 ตัวอักษร (เช่น DB-301) ชื่อวิชาไม่เกิน 100 ตัวอักษร จำนวนหน่วยกิตเก็บเป็นจำนวนเต็ม (Integer) และต้องการเชื่อมโยงด้วยว่าวิชานี้มีครูผู้สอนท่านใด และใช้ห้องเรียนไหนประจำเป็นหลัก ซึ่งต้องใช้ชนิดข้อมูลที่ตรงกับตารางหลักนะคะ<br>"
                 "5. <strong>ตาราง Enrollments (การลงทะเบียนเรียน)</strong>: ประวัติการลงเรียน มีรหัสการลงทะเบียน (enrollment_id) เป็นรหัสข้อความ 15 ตัวอักษร (เช่น ENR-2026-00001) วันที่ลงทะเบียนเก็บเป็นวันที่ (Date) เกรดที่ได้เก็บเป็นข้อความไม่เกิน 5 ตัวอักษร (เช่น A, B+, F) และต้องอ้างอิงให้ถูกว่านักเรียนคนใดลงเรียนในรายวิชาใดด้วยค่ะ<br>"
                 "มีรายละเอียดเยอะหน่อยนะคะ รบกวนคุณ SA ด้วยค่ะ!",
        "tables": {
            "students": {
                "title": "Students (นักเรียน)",
                "attributes": {
                    "student_id": {"type": "VARCHAR(10)", "is_pk": True},
                    "first_name": {"type": "VARCHAR(50)", "is_pk": False},
                    "last_name": {"type": "VARCHAR(50)", "is_pk": False},
                    "birth_date": {"type": "DATE", "is_pk": False}
                }
            },
            "teachers": {
                "title": "Teachers (คุณครู)",
                "attributes": {
                    "teacher_id": {"type": "VARCHAR(10)", "is_pk": True},
                    "teacher_name": {"type": "VARCHAR(100)", "is_pk": False},
                    "email": {"type": "VARCHAR(100)", "is_pk": False}
                }
            },
            "classrooms": {
                "title": "Classrooms (ห้องเรียน)",
                "attributes": {
                    "room_id": {"type": "VARCHAR(10)", "is_pk": True},
                    "building": {"type": "VARCHAR(50)", "is_pk": False},
                    "capacity": {"type": "INT", "is_pk": False}
                }
            },
            "courses": {
                "title": "Courses (รายวิชา)",
                "attributes": {
                    "course_code": {"type": "VARCHAR(10)", "is_pk": True},
                    "course_name": {"type": "VARCHAR(100)", "is_pk": False},
                    "credits": {"type": "INT", "is_pk": False},
                    "teacher_id": {"type": "VARCHAR(10)", "is_pk": False, "is_fk": True, "ref_table": "teachers", "ref_col": "teacher_id"},
                    "room_id": {"type": "VARCHAR(10)", "is_pk": False, "is_fk": True, "ref_table": "classrooms", "ref_col": "room_id"}
                }
            },
            "enrollments": {
                "title": "Enrollments (การลงทะเบียน)",
                "attributes": {
                    "enrollment_id": {"type": "VARCHAR(15)", "is_pk": True},
                    "student_id": {"type": "VARCHAR(10)", "is_pk": False, "is_fk": True, "ref_table": "students", "ref_col": "student_id"},
                    "course_code": {"type": "VARCHAR(10)", "is_pk": False, "is_fk": True, "ref_table": "courses", "ref_col": "course_code"},
                    "enroll_date": {"type": "DATE", "is_pk": False},
                    "grade": {"type": "VARCHAR(5)", "is_pk": False}
                }
            }
        },
        "relationships": [
            {"from_table": "teachers", "from_col": "teacher_id", "to_table": "courses", "to_col": "teacher_id"},
            {"from_table": "classrooms", "from_col": "room_id", "to_table": "courses", "to_col": "room_id"},
            {"from_table": "students", "from_col": "student_id", "to_table": "enrollments", "to_col": "student_id"},
            {"from_table": "courses", "from_col": "course_code", "to_table": "enrollments", "to_col": "course_code"}
        ]
    }
]

DATA_TYPE_CHOICES = ["VARCHAR(10)", "VARCHAR(15)", "VARCHAR(50)", "VARCHAR(100)", "INT", "DECIMAL(5,2)", "DATE", "DATETIME", "VARCHAR(5)", "Primary Key (คีย์หลัก)", "Field / Attribute", "Record / Tuple", "Data Type (ชนิดข้อมูล)"]

# ==================== ENCRYPTION HASH SYSTEM ====================

SECRET_KEY = 42

def encode_score(name, mission_id, score, satisfaction):
    """
    เข้ารหัสข้อมูลผู้เล่น คะแนน และวันที่เล่น ออกมาเป็นรหัส Hash ป้องกันการแก้ไข
    ใช้ระบบ UTF-8 Bytes + Hex-XOR ทำให้รองรับภาษาไทย และไม่ขึ้นกับตัวพิมพ์เล็ก-ใหญ่
    """
    timestamp = int(time.time())
    raw_str = f"{name}|{mission_id}|{score}|{satisfaction}|{timestamp}"
    
    # แปลงอักษรภาษาไทย/อังกฤษเป็น UTF-8 bytes ก่อนเพื่อไม่ให้จำนวนไบต์คลาดเคลื่อน
    raw_bytes = raw_str.encode('utf-8')
    hex_parts = []
    
    for b in raw_bytes:
        xor_val = b ^ SECRET_KEY
        hex_parts.append(f"{xor_val:02x}")
    
    hex_str = "".join(hex_parts).upper()
    # แบ่งกลุ่มตัวอักษรทีละ 4 ตัวให้อ่านง่าย เช่น DB-ARCH-A1B2-C3D4...
    chunks = [hex_str[i:i+4] for i in range(0, len(hex_str), 4)]
    return "DB-ARCH-" + "-".join(chunks)

def decode_score(hash_str):
    """
    ถอดรหัสรหัสลับ Hex-XOR กลับมาเป็นข้อมูลรายละเอียดคะแนนดิบภาษาไทยที่ถูกต้อง
    """
    if not hash_str.startswith("DB-ARCH-"):
        return None
    
    # เอาส่วนนำออก และลบขีดกลางออก
    clean_str = hash_str[8:].replace("-", "").lower()
    
    try:
        decoded_bytes = bytearray()
        for i in range(0, len(clean_str), 2):
            hex_pair = clean_str[i:i+2]
            xor_val = int(hex_pair, 16)
            original_byte = xor_val ^ SECRET_KEY
            decoded_bytes.append(original_byte)
            
        # ถอดรหัส UTF-8 ไบต์กลับเป็นสตริงข้อความภาษาไทย
        original_str = decoded_bytes.decode('utf-8')
        data_parts = original_str.split("|")
        
        if len(data_parts) == 5:
            # แปลง Timestamp เป็นรูปแบบวันที่ที่อ่านง่าย
            formatted_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(data_parts[4])))
            return {
                "name": data_parts[0],
                "mission_id": data_parts[1],
                "score": int(data_parts[2]),
                "satisfaction": int(data_parts[3]),
                "date": formatted_date,
                "verified": True
            }
    except Exception as e:
        window.console.log(f"Decoding error: {e}")
        return None
    return None

# ==================== GAME STATE MANAGER ====================

class GameState:
    def __init__(self):
        self.student_name = ""
        self.current_view = "view-home"
        self.active_mission_idx = 0
        self.active_stage = 1
        
        # Scoring variables
        self.score = 1000
        self.satisfaction = 100 # Starts at 100%
        
        # Level 1 data: dict table_name -> list of attributes dropped
        self.l1_assignments = {}
        
        # Level 2 data: dict table_name -> dict attr_name -> {"type": selected_type, "is_pk": bool}
        self.l2_configurations = {}
        
        # Level 3 data: list of connections: {"from_table": t1, "from_col": c1, "to_table": t2, "to_col": c2}
        self.l3_connections = []
        self.l3_active_origin = None # Stores {"table": t, "col": c, "node_el": el} when clicked PK
        self.l3_temp_line = None # บันทึกอิลิเมนต์เส้นจำลองชั่วคราว
        
        # Drag and Drop temporary storage
        self.dragged_attr_id = None
        
    def get_active_mission(self):
        return MISSIONS[self.active_mission_idx]
        
    def reset_for_mission(self, mission_idx):
        self.active_mission_idx = mission_idx
        self.active_stage = 1
        self.score = 1000
        self.satisfaction = 100
        self.l1_assignments = {t_name: [] for t_name in self.get_active_mission()["tables"]}
        self.l2_configurations = {}
        self.l3_connections = []
        self.l3_active_origin = None
        self.l3_temp_line = None
        self.dragged_attr_id = None

# Instantiate global state
state = GameState()

# ==================== HELPER FUNCTIONS ====================

def show_view(view_id):
    """
    สลับการแสดงผลหน้าจอหลัก
    """
    for view in document.select(".view"):
        view.classList.add("hidden")
    document[view_id].classList.remove("hidden")
    state.current_view = view_id
    
    # Scroll back to top
    window.scrollTo(0, 0)
    
    # Redraw lines if entering level 3
    if view_id == "view-game" and state.active_stage == 3:
        # Give a small delay to make sure elements are rendered and positions can be read
        window.setTimeout(redraw_connections, 100)

def show_notification(message, type="info"):
    """
    แสดง Toast แจ้งเตือนมุมล่างขวา
    """
    notif = document["notification"]
    notif.innerHTML = f"<i class='fa-solid fa-circle-info'></i> {message}"
    notif.className = "notification-toast"
    
    if type == "error":
        notif.classList.add("error")
        notif.innerHTML = f"<i class='fa-solid fa-circle-exclamation'></i> {message}"
    elif type == "success":
        notif.classList.add("success")
        notif.innerHTML = f"<i class='fa-solid fa-circle-check'></i> {message}"
        
    notif.classList.remove("hidden")
    
    # Auto hide after 4 seconds
    def hide_notif():
        notif.classList.add("hidden")
    window.setTimeout(hide_notif, 4000)

def deduct_points(points=50, sat_loss=10):
    """
    หักคะแนนผู้เล่นและหักความพึงพอใจของลูกค้าหากตอบผิด
    """
    state.score = max(0, state.score - points)
    state.satisfaction = max(0, state.satisfaction - sat_loss)
    
    # Update UI displays
    document["game-score"].text = str(state.score)
    document["game-satisfaction"].text = str(state.satisfaction)
    
    if state.satisfaction <= 0:
        # Game Over: Client satisfaction hit zero!
        show_notification("ลูกค้าไม่พอใจการทำงานของคุณอย่างมาก! งานออกแบบล้มเหลว", "error")
        # Let them retry the mission
        def go_to_selection():
            show_view("view-select-mission")
        window.setTimeout(go_to_selection, 2500)

# ==================== CONTROLLER & VIEW RENDERING ====================

def start_game_clicked(ev):
    name = document["student-name"].value.strip()
    if not name:
        show_notification("กรุณากรอกชื่อ-นามสกุล ก่อนเริ่มต้นเกมครับ/ค่ะ", "error")
        return
    state.student_name = name
    document["game-user-name"].text = name
    render_missions_list()
    show_view("view-select-mission")

def render_missions_list():
    container = document["missions-container"]
    container.innerHTML = ""
    
    for idx, mission in enumerate(MISSIONS):
        card = html.DIV(Class="glass-card mission-card")
        card.bind("click", lambda ev, i=idx: select_mission(i))
        
        header = html.DIV(Class="mission-card-header")
        avatar = html.SPAN(mission["avatar"], Class="client-avatar")
        diff = html.SPAN(mission["difficulty"], Class=f"difficulty-badge {mission['difficulty_class']}")
        header <= avatar
        header <= diff
        
        title = html.H3(mission["title"], Class="mission-title")
        desc = html.P(mission["brief"][:110] + "...", Class="mission-desc")
        
        footer = html.DIV(Class="mission-card-footer")
        table_count = len(mission["tables"])
        rel_count = len(mission["relationships"])
        footer <= html.SPAN(f"<i class='fa-solid fa-table'></i> {table_count} ตาราง")
        footer <= html.SPAN(f"<i class='fa-solid fa-diagram-project'></i> {rel_count} ความสัมพันธ์")
        
        card <= header
        card <= title
        card <= desc
        card <= footer
        container <= card

def select_mission(mission_idx):
    state.reset_for_mission(mission_idx)
    mission = state.get_active_mission()
    
    # Clear DOM elements from previous mission plays to prevent carry-over/leaks
    if "l1-tables-board" in document:
        document["l1-tables-board"].innerHTML = ""
    if "l1-attributes-source" in document:
        document["l1-attributes-source"].innerHTML = ""
    if "l2-tables-board" in document:
        document["l2-tables-board"].innerHTML = ""
    if "l3-tables-board" in document:
        document["l3-tables-board"].innerHTML = ""
    if "svg-connections" in document:
        svg_layer = document["svg-connections"]
        defs = svg_layer.select_one("defs")
        svg_layer.innerHTML = ""
        if defs:
            svg_layer <= defs

    # Populate Brief View
    document["brief-client-avatar"].text = mission["avatar"]
    document["brief-client-name"].text = mission["company"]
    document["brief-client-company"].text = mission["title"]
    document["brief-text"].innerHTML = mission["brief"]
    
    # Set difficulty tag in brief
    diff_el = document["brief-difficulty"]
    diff_el.innerHTML = f"<span class='difficulty-badge {mission['difficulty_class']}'>{mission['difficulty']}</span>"
    
    show_view("view-brief")

def start_mission_clicked(ev):
    # Set status bar
    document["game-mission-title"].text = state.get_active_mission()["title"]
    document["game-score"].text = str(state.score)
    document["game-satisfaction"].text = str(state.satisfaction)
    
    # Initialize Stage 1
    init_stage_1()
    show_view("view-game")

# ==================== LEVEL 1: DRAG & DROP ====================

def init_stage_1():
    state.active_stage = 1
    update_stage_indicator()
    
    # Hide other level containers, show Level 1
    document["level-1-container"].classList.remove("hidden")
    document["level-2-container"].classList.add("hidden")
    document["level-3-container"].classList.add("hidden")
    
    mission = state.get_active_mission()
    
    # Dynamic header/text adjustments for intro mission
    l1_title = document.select_one("#level-1-container .level-intro h3")
    l1_desc = document.select_one("#level-1-container .level-intro p")
    l1_conveyor_title = document.select_one("#level-1-container .conveyor-belt-container h4")
    
    if mission["id"] == "intro":
        if l1_title: l1_title.text = "ด่านที่ 1: จับคู่คำศัพท์และคำนิยาม"
        if l1_desc: l1_desc.text = "ลากตัวอย่างและคำอธิบายด้านล่างไปใส่ในประเภทคำศัพท์หลัก (กล่องนีออน) ให้ถูกต้องตามหลักการ"
        if l1_conveyor_title: l1_conveyor_title.text = "คลังข้อมูลตัวอย่าง/คำนิยาม (ลากไปจับคู่)"
    else:
        if l1_title: l1_title.text = "ด่านที่ 1: แยกแยะ Entities & Attributes"
        if l1_desc: l1_desc.text = "ลาก Attributes ด้านล่างไปหย่อนใส่ Entity (ตาราง) ที่ถูกต้องให้เหมาะสมตามโจทย์"
        if l1_conveyor_title: l1_conveyor_title.text = "คลัง Attribute ข้อมูลลูกค้า (ลากไปใส่ตาราง)"
        
    # Render Tables Dropzones
    tables_board = document["l1-tables-board"]
    tables_board.innerHTML = ""
    
    for t_name, t_info in mission["tables"].items():
        table_card = html.DIV(id=f"l1-table-{t_name}", Class="table-card")
        
        header = html.DIV(Class="table-header")
        header <= html.SPAN(f"<i class='fa-solid fa-table'></i> {t_info['title']}")
        header <= html.SPAN("0", id=f"l1-count-{t_name}", Class="badge")
        
        body = html.DIV(id=f"l1-body-{t_name}", Class="table-body")
        # Bind Drag events to table body
        body.bind("dragover", on_dragover)
        body.bind("dragleave", on_dragleave)
        body.bind("drop", lambda ev, name=t_name: on_drop(ev, name))
        
        table_card <= header
        table_card <= body
        tables_board <= table_card
        
    # Render conveyor belt attributes
    conveyor = document["l1-attributes-source"]
    conveyor.innerHTML = ""
    # Bind conveyor drag events for returning items
    conveyor.bind("dragover", on_dragover)
    conveyor.bind("dragleave", on_dragleave)
    conveyor.bind("drop", lambda ev, name="source": on_drop(ev, name))
    
    # Gather all attributes from all tables in this mission
    all_attrs = []
    for t_name, t_info in mission["tables"].items():
        for attr_name in t_info["attributes"]:
            all_attrs.append((attr_name, t_name))
            
    # Shuffle attributes
    random.shuffle(all_attrs)
    
    for attr_name, origin_table in all_attrs:
        # Generate a unique DOM ID to prevent collision of duplicate attribute names (e.g. customer_id)
        attr_id = f"l1-attr-{origin_table}-{attr_name}"
        attr_el = html.DIV(
            attr_name, 
            id=attr_id, 
            Class="attr-item", 
            draggable="true"
        )
        # Store metadata as custom elements attributes
        attr_el.setAttribute("data-attr-name", attr_name)
        attr_el.setAttribute("data-correct-table", origin_table)
        
        # Bind Drag events to attribute card
        attr_el.bind("dragstart", on_dragstart)
        attr_el.bind("dragend", on_dragend)
        
        conveyor <= attr_el
        
    document["btn-check-l1"].setAttribute("disabled", "true")
    check_l1_button_status()

# Drag & Drop Events
def on_dragstart(ev):
    ev.dataTransfer.setData("text", ev.target.id)
    state.dragged_attr_id = ev.target.id
    ev.target.classList.add("dragging")

def on_dragend(ev):
    ev.target.classList.remove("dragging")
    state.dragged_attr_id = None
    # Clean all drag over classes
    for el in document.select(".table-body, .conveyor-belt"):
        el.classList.remove("drag-over")

def on_dragover(ev):
    ev.preventDefault()
    ev.currentTarget.classList.add("drag-over")

def on_dragleave(ev):
    ev.currentTarget.classList.remove("drag-over")

def on_drop(ev, target_name):
    ev.preventDefault()
    ev.currentTarget.classList.remove("drag-over")
    
    attr_id = ev.dataTransfer.getData("text") or state.dragged_attr_id
    if not attr_id:
        return
        
    attr_el = document[attr_id]
    
    # Remove from previous assignment lists using unique DOM ID
    for t_name in state.l1_assignments:
        if attr_id in state.l1_assignments[t_name]:
            state.l1_assignments[t_name].remove(attr_id)
            
    # Append element in DOM
    ev.currentTarget <= attr_el
    
    # Update local assignments state & table count badge
    if target_name != "source":
        state.l1_assignments[target_name].append(attr_id)
        
    # Update all badges count
    for t_name in state.l1_assignments:
        document[f"l1-count-{t_name}"].text = str(len(state.l1_assignments[t_name]))
        
    check_l1_button_status()

def check_l1_button_status():
    # Enable check button if all attributes have been assigned to tables (conveyor belt is empty)
    conveyor = document["l1-attributes-source"]
    btn = document["btn-check-l1"]
    
    if len(conveyor.children) == 0:
        btn.removeAttribute("disabled")
    else:
        btn.setAttribute("disabled", "true")

def check_l1_clicked(ev):
    mission = state.get_active_mission()
    all_correct = True
    errors_found = 0
    
    for t_name, t_info in mission["tables"].items():
        assigned_ids = state.l1_assignments[t_name]
        correct_attrs = t_info["attributes"]
        
        # รายการคุณลักษณะทั้งหมดที่ตารางนี้ต้องการ (ใช้เปรียบเทียบตามชื่อคอลัมน์)
        needed_attrs = list(correct_attrs.keys())
        
        # ตรวจเช็คทีละไอเทมที่นักเรียนลากมาวางในตารางนี้
        for attr_id in list(assigned_ids):
            attr_el = document[attr_id]
            attr_name = attr_el.getAttribute("data-attr-name")
            
            if attr_name in needed_attrs:
                # ถูกต้อง! ชื่อคอลัมน์นี้เป็นหนึ่งในสิ่งที่ตารางนี้ต้องการ
                needed_attrs.remove(attr_name)
                attr_el.className = "attr-item correct"
                attr_el.setAttribute("draggable", "false")
            else:
                # ผิดพลาด! คอลัมน์นี้ไม่ได้อยู่ในข้อกำหนดของตารางนี้ (หรือใส่มาซ้ำซ้อน)
                all_correct = False
                errors_found += 1
                attr_el.className = "attr-item incorrect"
                
                # หักคะแนนผู้เรียน
                deduct_points(30, 8)
                
                # ย้ายการ์ดที่ใส่ผิดกลับไปที่สายพานคลังข้อมูลหลังจากดีเลย์ 1.5 วินาที
                def send_back(el=attr_el, aid=attr_id, name=attr_name, origin=t_name):
                    el.className = "attr-item"
                    el.setAttribute("draggable", "true")
                    document["l1-attributes-source"] <= el
                    if aid in state.l1_assignments[origin]:
                        state.l1_assignments[origin].remove(aid)
                    document[f"l1-count-{origin}"].text = str(len(state.l1_assignments[origin]))
                    check_l1_button_status()
                    
                window.setTimeout(send_back, 1500)
                
        # หากจำนวน Attributes ที่ตารางนี้ต้องการยังใส่ไม่ครบ
        if len(needed_attrs) > 0:
            all_correct = False
                
    if all_correct:
        show_notification("วิเคราะห์ Entities & Attributes สำเร็จ! ลูกค้าชื่นชมการจัดหมวดหมู่ข้อมูลของคุณ", "success")
        
        # ทำเครื่องหมายว่าผ่านด่านที่ 1 แล้ว
        document["dot-stage-1"].className = "stage-dot completed"
        
        # ไปยังด่านที่ 2 ต่อไป
        window.setTimeout(init_stage_2, 1500)
    else:
        show_notification(f"พบการจัดหมวดหมู่ข้อมูลผิดพลาด หรือยังกรอกตารางไม่สมบูรณ์! กรุณาตรวจสอบตามบรีฟลูกค้าอีกครั้ง", "error")

# ==================== LEVEL 2: DATA TYPES & PK ====================

def init_stage_2():
    state.active_stage = 2
    update_stage_indicator()
    
    # Hide level 1, show Level 2
    document["level-1-container"].classList.add("hidden")
    document["level-2-container"].classList.remove("hidden")
    
    mission = state.get_active_mission()
    board = document["l2-tables-board"]
    board.innerHTML = ""
    
    state.l2_configurations = {}
    
    # Dynamic header/text adjustments for intro mission
    l2_title = document.select_one("#level-2-container .level-intro h3")
    l2_desc = document.select_one("#level-2-container .level-intro p")
    btn_check_l2 = document["btn-check-l2"]
    
    if mission["id"] == "intro":
        if l2_title: l2_title.text = "ด่านที่ 2: องค์ประกอบของตารางข้อมูล"
        if l2_desc: l2_desc.text = "วิเคราะห์และจับคู่ส่วนประกอบของตารางข้อมูลให้ถูกต้อง และเปิดใช้งาน PK สำหรับคีย์หลักของตาราง"
        if btn_check_l2: btn_check_l2.innerHTML = 'ตรวจสอบองค์ประกอบ & Keys <i class="fa-solid fa-circle-check"></i>'
    else:
        if l2_title: l2_title.text = "ด่านที่ 2: เลือกชนิดข้อมูล (Data Types) & Primary Key (PK)"
        if l2_desc: l2_desc.text = "เลือกชนิดข้อมูลที่ถูกต้องให้กับแต่ละ Attributes และเลือกอย่างน้อย 1 คอลัมน์เป็น Primary Key ของตาราง"
        if btn_check_l2: btn_check_l2.innerHTML = 'ตรวจสอบชนิดข้อมูล & Keys <i class="fa-solid fa-circle-check"></i>'
        
    target_tables = mission.get("l2_custom_tables", mission["tables"])
    
    for t_name, t_info in target_tables.items():
        state.l2_configurations[t_name] = {}
        
        table_card = html.DIV(Class="table-card-l2")
        
        header = html.DIV(Class="table-header")
        header <= html.SPAN(f"<i class='fa-solid fa-table'></i> {t_info['title']}")
        table_card <= header
        
        grid = html.DIV(Class="table-grid-l2")
        
        # Grid Header
        grid_head = html.DIV(Class="grid-row-header")
        grid_head <= html.DIV("ส่วนประกอบตาราง" if mission["id"] == "intro" else "ชื่อ Attribute")
        grid_head <= html.DIV("ระบุคำศัพท์" if mission["id"] == "intro" else "ชนิดข้อมูล (Data Type)")
        grid_head <= html.DIV("PK")
        grid <= grid_head
        
        # Grid Rows for each attribute
        for attr_name in t_info["attributes"]:
            # State initializer for choices
            choices_list = ["Primary Key (คีย์หลัก)", "Field / Attribute", "Record / Tuple", "Data Type (ชนิดข้อมูล)"] if mission["id"] == "intro" else DATA_TYPE_CHOICES[:9]
            state.l2_configurations[t_name][attr_name] = {"type": choices_list[0], "is_pk": False}
            
            row = html.DIV(Class="grid-row-data", id=f"l2-row-{t_name}-{attr_name}")
            
            name_col = html.DIV(attr_name, Class="grid-attr-name")
            
            # Select element
            select_type = html.SELECT()
            for choice in choices_list:
                select_type <= html.OPTION(choice, value=choice)
            # Bind choice update
            select_type.bind("change", lambda ev, t=t_name, a=attr_name: on_datatype_change(ev, t, a))
            
            # PK Key toggle button
            pk_btn = html.BUTTON(html.I(Class="fa-solid fa-key"), Class="pk-toggle", id=f"l2-pk-{t_name}-{attr_name}")
            pk_btn.bind("click", lambda ev, t=t_name, a=attr_name: toggle_pk(ev, t, a))
            
            row <= name_col
            row <= select_type
            row <= pk_btn
            grid <= row
            
        table_card <= grid
        board <= table_card

def on_datatype_change(ev, table_name, attr_name):
    selected_val = ev.target.value
    state.l2_configurations[table_name][attr_name]["type"] = selected_val

def toggle_pk(ev, table_name, attr_name):
    # Prevent default form action
    ev.preventDefault()
    
    # Toggle PK state in client config
    current_val = state.l2_configurations[table_name][attr_name]["is_pk"]
    new_val = not current_val
    state.l2_configurations[table_name][attr_name]["is_pk"] = new_val
    
    # Update UI button state
    btn = document[f"l2-pk-{table_name}-{attr_name}"]
    if new_val:
        btn.classList.add("active")
    else:
        btn.classList.remove("active")

def check_l2_clicked(ev):
    mission = state.get_active_mission()
    all_correct = True
    errors_found = 0
    
    target_tables = mission.get("l2_custom_tables", mission["tables"])
    for t_name, t_info in target_tables.items():
        correct_attrs = t_info["attributes"]
        user_config = state.l2_configurations[t_name]
        
        for attr_name, correct_cfg in correct_attrs.items():
            user_attr_cfg = user_config[attr_name]
            row_el = document[f"l2-row-{t_name}-{attr_name}"]
            
            # Reset borders
            row_el.style.border = "none"
            
            # Compare DataType and PK status
            is_type_correct = user_attr_cfg["type"] == correct_cfg["type"]
            is_pk_correct = user_attr_cfg["is_pk"] == correct_cfg["is_pk"]
            
            if not (is_type_correct and is_pk_correct):
                all_correct = False
                errors_found += 1
                row_el.style.border = "1px solid var(--color-error)"
                row_el.style.borderRadius = "5px"
                
                # Deduct points
                deduct_points(25, 6)
                
    if all_correct:
        if mission["id"] == "intro":
            show_notification("วิเคราะห์ส่วนประกอบของตารางข้อมูลและคีย์หลักถูกต้องทั้งหมด!", "success")
        else:
            show_notification("ตั้งค่าโครงสร้างตาราง ชนิดข้อมูล และ Primary Key ถูกต้องทั้งหมด!", "success")
        
        # Mark stage 2 dot completed
        document["dot-stage-2"].className = "stage-dot completed"
        
        # Delay then proceed to Level 3
        window.setTimeout(init_stage_3, 1500)
    else:
        show_notification(f"พบการกำหนดชนิดข้อมูลหรือ PK ผิดพลาดจำนวน {errors_found} แห่ง กรุณาตรวจทานตามบรีฟลูกค้าอีกครั้ง", "error")

# ==================== LEVEL 3: RELATIONSHIPS ====================

def init_stage_3():
    state.active_stage = 3
    update_stage_indicator()
    
    # Hide level 2, show Level 3
    document["level-2-container"].classList.add("hidden")
    document["level-3-container"].classList.remove("hidden")
    
    mission = state.get_active_mission()
    board = document["l3-tables-board"]
    board.innerHTML = ""
    
    # Clear SVG connections layer
    svg_container = document["svg-connections"]
    defs = svg_container.select_one("defs")
    svg_container.innerHTML = ""
    if defs:
        svg_container <= defs
        
    state.l3_connections = []
    state.l3_active_origin = None
    state.l3_temp_line = None
    
    # Dynamic header/text adjustments for intro mission
    l3_title = document.select_one("#level-3-container .level-intro h3")
    l3_desc = document.select_one("#level-3-container .level-intro p")
    
    if mission["id"] == "intro":
        if l3_title: l3_title.text = "ด่านที่ 3: บทบาทและสิทธิ์การเข้าใช้งาน"
        if l3_desc: l3_desc.text = "คลิกเลือกบทบาทของระบบฐานข้อมูล (วงกลมสีทอง 🔑) แล้วลากเส้นเชื่อมโยงไปยังภาระหน้าที่ความรับผิดชอบ (วงกลมสีเงิน 🔗) ที่ถูกต้อง"
    else:
        if l3_title: l3_title.text = "ด่านที่ 3: จับคู่ความสัมพันธ์ของตาราง (One-to-Many Relationships)"
        if l3_desc: l3_desc.text = "คลิกเลือกปุ่มวงกลมสีทอง 🔑 (Primary Key) จากตารางต้นทาง แล้วลากไปคลิกวงกลมสีเงิน 🔗 (Foreign Key) ของตารางปลายทางเพื่อสร้างเส้นเชื่อมความสัมพันธ์"
        
    target_tables = mission.get("l3_custom_tables", mission["tables"])
    
    # Render Tables with PK and FK indicator nodes
    for t_name, t_info in target_tables.items():
        table_card = html.DIV(Class="table-card-l3", id=f"l3-table-{t_name}")
        
        header = html.DIV(Class="table-header")
        header <= html.SPAN(f"<i class='fa-solid fa-table'></i> {t_info['title']}")
        table_card <= header
        
        body = html.DIV(Class="table-body-l3")
        
        for attr_name, attr_cfg in t_info["attributes"].items():
            row = html.DIV(Class="column-row-l3", id=f"l3-row-{t_name}-{attr_name}")
            
            # Left node: PK (Gold)
            if attr_cfg.get("is_pk"):
                node_pk = html.DIV(Class="connect-node node-pk", id=f"node-pk-{t_name}-{attr_name}")
                node_pk.bind("click", lambda ev, t=t_name, a=attr_name: on_node_clicked(ev, t, a, "pk"))
                row <= node_pk
            else:
                # Empty space for layout alignment
                row <= html.DIV(style="width: 14px")
                
            # Column label
            col_info = html.SPAN(Class="column-name-l3")
            col_info <= html.SPAN(attr_name)
            col_info <= html.SPAN(f" {attr_cfg['type']}", Class="column-type-l3")
            row <= col_info
            
            # Right node: FK (Silver/Gray)
            if attr_cfg.get("is_fk"):
                node_fk = html.DIV(Class="connect-node node-fk", id=f"node-fk-{t_name}-{attr_name}")
                node_fk.bind("click", lambda ev, t=t_name, a=attr_name: on_node_clicked(ev, t, a, "fk"))
                row <= node_fk
            else:
                row <= html.DIV(style="width: 14px")
                
            body <= row
            
        table_card <= body
        board <= table_card
        
    # Resize listener to redraw connections on window size change
    window.bind("resize", lambda ev: redraw_connections())
    
    # Initialize mousemove listeners to draw floating drag line if active
    document.bind("mousemove", draw_floating_line)

def on_node_clicked(ev, table_name, attr_name, node_type):
    ev.stopPropagation()
    
    if node_type == "pk":
        # Activating a Primary Key source node
        # Deactivate previous active node UI
        if state.l3_active_origin:
            state.l3_active_origin["node_el"].classList.remove("active-origin")
            
        # Clean up any existing temp line
        if state.l3_temp_line:
            try:
                state.l3_temp_line.parent.removeChild(state.l3_temp_line)
            except Exception:
                pass
            state.l3_temp_line = None
            
        node_el = document[f"node-pk-{table_name}-{attr_name}"]
        node_el.classList.add("active-origin")
        
        state.l3_active_origin = {
            "table": table_name,
            "col": attr_name,
            "node_el": node_el
        }
        
        # Create a new temp line in state with explicit attributes for stroke to prevent style delays
        svg_layer = document["svg-connections"]
        state.l3_temp_line = svg.path()
        state.l3_temp_line.setAttribute("class", "temp-line")
        state.l3_temp_line.setAttribute("stroke", "var(--accent-magenta)")
        state.l3_temp_line.setAttribute("stroke-dasharray", "5,5")
        state.l3_temp_line.setAttribute("stroke-width", "3")
        state.l3_temp_line.setAttribute("fill", "none")
        svg_layer <= state.l3_temp_line
        
        show_notification(f"เลือกตาราง {table_name}.{attr_name} (Primary Key) แล้ว. คลิกที่คีย์นอก (Foreign Key) ของอีกตารางเพื่อเชื่อมความสัมพันธ์", "info")
        
    elif node_type == "fk":
        # Target node Foreign Key clicked
        if not state.l3_active_origin:
            show_notification("กรุณาคลิกเลือก Primary Key (🔑) สีทองต้นทางก่อนจะเลือกคีย์นอกปลายทางค่ะ", "error")
            return
            
        origin_t = state.l3_active_origin["table"]
        origin_c = state.l3_active_origin["col"]
        
        # Check self referencing constraints / logical check
        if origin_t == table_name:
            show_notification("ไม่สามารถสร้างความสัมพันธ์ระหว่างคอลัมน์ในตารางเดียวกันในเกมนี้ได้ (Self-Reference จะเรียนในบทถัดไป)", "error")
            return
            
        # Add new connection if it doesn't already exist
        exists = False
        for conn in state.l3_connections:
            if (conn["from_table"] == origin_t and conn["from_col"] == origin_c and 
                conn["to_table"] == table_name and conn["to_col"] == attr_name):
                exists = True
                break
                
        if not exists:
            # Check if this FK is already connected to something
            for conn in list(state.l3_connections):
                if conn["to_table"] == table_name and conn["to_col"] == attr_name:
                    state.l3_connections.remove(conn) # Replace existing connection for this FK
            
            state.l3_connections.append({
                "from_table": origin_t,
                "from_col": origin_c,
                "to_table": table_name,
                "to_col": attr_name
            })
            
            show_notification(f"เชื่อมความสัมพันธ์สำเร็จ: {origin_t}.{origin_c} ➔ {table_name}.{attr_name}", "success")
        
        # Clear active status and remove temp line from DOM
        if state.l3_temp_line:
            try:
                state.l3_temp_line.parent.removeChild(state.l3_temp_line)
            except Exception:
                pass
            state.l3_temp_line = None
            
        state.l3_active_origin["node_el"].classList.remove("active-origin")
        state.l3_active_origin = None
        
        redraw_connections()

def get_node_center_coords(node_el):
    """
    คำนวณพิกัดกึ่งกลางของ Node สำหรับเชื่อม SVG โค้ง
    """
    svg_layer = document["svg-connections"]
    node_rect = node_el.getBoundingClientRect()
    svg_rect = svg_layer.getBoundingClientRect()
    
    x = node_rect.left - svg_rect.left + node_rect.width / 2
    y = node_rect.top - svg_rect.top + node_rect.height / 2
    return (x, y)

def draw_floating_line(ev):
    """
    วาดเส้นชั่วคราวเคลื่อนไหวตามเคอร์เซอร์เมาส์เมื่อคลิก PK ไว้แล้ว
    """
    if not state.l3_active_origin or not state.l3_temp_line:
        return
        
    svg_layer = document["svg-connections"]
    x1, y1 = get_node_center_coords(state.l3_active_origin["node_el"])
    
    # Get current mouse coords relative to SVG
    svg_rect = svg_layer.getBoundingClientRect()
    x2 = ev.clientX - svg_rect.left
    y2 = ev.clientY - svg_rect.top
    
    # Draw smooth S-curve line
    dx = abs(x2 - x1) * 0.5
    cx1 = x1 + dx
    cy1 = y1
    cx2 = x2 - dx
    cy2 = y2
    
    state.l3_temp_line.setAttribute("d", f"M {x1} {y1} C {cx1} {cy1}, {cx2} {cy2}, {x2} {y2}")

def redraw_connections():
    svg_layer = document["svg-connections"]
    
    # Clear SVG connections layer (keeping only defs marker)
    defs = svg_layer.select_one("defs")
    svg_layer.innerHTML = ""
    if defs:
        svg_layer <= defs
            
    # Draw each connection
    for idx, conn in enumerate(state.l3_connections):
        try:
            node_from = document[f"node-pk-{conn['from_table']}-{conn['from_col']}"]
            node_to = document[f"node-fk-{conn['to_table']}-{conn['to_col']}"]
        except KeyError:
            continue
            
        x1, y1 = get_node_center_coords(node_from)
        x2, y2 = get_node_center_coords(node_to)
        
        # Calculate smooth Bezier Control Points
        dx = abs(x2 - x1) * 0.5
        cx1 = x1 + dx
        cy1 = y1
        cx2 = x2 - dx
        cy2 = y2
        
        # Draw line path
        path_d = f"M {x1} {y1} C {cx1} {cy1}, {cx2} {cy2}, {x2} {y2}"
        
        # Creating path using Brython SVG library
        path_el = svg.path(
            d=path_d,
            stroke="var(--accent-cyan)",
            stroke_width="3",
            fill="none"
        )
        # Add custom hover/delete ability
        path_el.bind("click", lambda ev, i=idx: remove_connection(i))
        path_el.setAttribute("title", "คลิกเพื่อลบเส้นเชื่อมนี้")
        
        # Text or indicator marking: Draw '1' and 'N' labels next to lines
        txt_1 = svg.text("1", x=x1 + 10, y=y1 - 5, fill="#f1c40f", font_size="12", font_weight="bold")
        txt_n = svg.text("N", x=x2 - 20, y=y2 - 5, fill="#a4b0be", font_size="12", font_weight="bold")
        
        svg_layer <= path_el
        
        # Text or indicator marking: Draw '1' and 'N' labels next to lines (skipped for intro mission)
        mission = state.get_active_mission()
        if mission["id"] != "intro":
            txt_1 = svg.text("1", x=x1 + 10, y=y1 - 5, fill="#f1c40f", font_size="12", font_weight="bold")
            txt_n = svg.text("N", x=x2 - 20, y=y2 - 5, fill="#a4b0be", font_size="12", font_weight="bold")
            svg_layer <= txt_1
            svg_layer <= txt_n
        
    # Re-append temp line if it exists so it stays on top of other lines
    if state.l3_temp_line:
        svg_layer <= state.l3_temp_line

def remove_connection(conn_idx):
    if conn_idx < len(state.l3_connections):
        removed = state.l3_connections.pop(conn_idx)
        redraw_connections()
        show_notification(f"ลบเส้นเชื่อมต่อ {removed['from_table']} ➔ {removed['to_table']} แล้ว", "info")

def clear_connections_clicked(ev):
    state.l3_connections = []
    redraw_connections()
    show_notification("ล้างเส้นเชื่อมสัมพันธ์ทั้งหมดแล้ว", "info")

def check_l3_clicked(ev):
    if not state.l3_connections:
        show_notification("กรุณาลากเส้นเชื่อมโยงความสัมพันธ์ของตารางอย่างน้อย 1 เส้น ก่อนกดตรวจสอบค่ะ", "error")
        return

    # Remove temp line
    if state.l3_temp_line:
        try:
            state.l3_temp_line.parent.removeChild(state.l3_temp_line)
        except Exception:
            pass
        state.l3_temp_line = None
        
    mission = state.get_active_mission()
    correct_rels = mission["relationships"]
    
    # We must match correct relationship sets. Order does not matter,
    # but (from_table, from_col, to_table, to_col) must match.
    match_count = 0
    total_needed = len(correct_rels)
    
    # Trace user connections
    matched_conns = []
    
    for user_conn in state.l3_connections:
        is_matched = False
        for correct_conn in correct_rels:
            if (user_conn["from_table"] == correct_conn["from_table"] and
                user_conn["from_col"] == correct_conn["from_col"] and
                user_conn["to_table"] == correct_conn["to_table"] and
                user_conn["to_col"] == correct_conn["to_col"]):
                is_matched = True
                break
        if is_matched:
            match_count += 1
            matched_conns.append(user_conn)
            
    # Calculate errors
    incorrect_count = len(state.l3_connections) - match_count
    missing_count = total_needed - match_count
    
    if match_count == total_needed and incorrect_count == 0:
        # 100% Success!
        show_notification("ยอดเยี่ยมมาก! การออกแบบฐานข้อมูลเสร็จสมบูรณ์และถูกต้องตรงตามความต้องการลูกค้า", "success")
        
        # Mark stage 3 completed
        document["dot-stage-3"].className = "stage-dot completed"
        
        # Delay then proceed to Finish screen
        window.setTimeout(finish_mission, 1500)
    else:
        # Highlight errors & deduct points
        if incorrect_count > 0:
            deduct_points(40 * incorrect_count, 10 * incorrect_count)
            show_notification(f"มีเส้นเชื่อมต่อผิดพลาด {incorrect_count} จุด! ลองตรวจทาน Primary Key และ Foreign Key ปลายทางดีๆ นะ", "error")
        elif missing_count > 0:
            deduct_points(30, 8)
            show_notification(f"คุณยังลากเส้นเชื่อมต่อไม่ครบถ้วน ขาดอีก {missing_count} ความสัมพันธ์ครับ", "error")

# ==================== FINISH MISSION & CERTIFICATE ====================

def finish_mission():
    mission = state.get_active_mission()
    
    # Update values in finish view
    document["finish-student-name"].text = state.student_name
    document["finish-mission-title"].text = mission["title"]
    document["finish-score"].text = str(state.score)
    document["finish-satisfaction"].text = str(state.satisfaction)
    
    # Generate verification hash
    hash_val = encode_score(state.student_name, mission["id"], state.score, state.satisfaction)
    document["finish-hash"].text = hash_val
    
    # Save completion to localStorage
    try:
        saves = window.localStorage.getItem("db_architect_saves")
        saves_dict = json.loads(saves) if saves else {}
    except Exception:
        saves_dict = {}
        
    saves_dict[mission["id"]] = {"score": state.score, "satisfaction": state.satisfaction, "hash": hash_val}
    window.localStorage.setItem("db_architect_saves", json.dumps(saves_dict))
    
    show_view("view-finish")

def copy_hash_clicked(ev):
    hash_txt = document["finish-hash"].text
    
    # Use window.navigator.clipboard or write to temp input for copying
    try:
        window.navigator.clipboard.writeText(hash_txt)
        show_notification("คัดลอกรหัสลับเรียบร้อยแล้ว! สามารถนำไปส่งครูได้ทันที", "success")
    except Exception:
        # Fallback copy method
        temp_input = html.INPUT(value=hash_txt)
        document <= temp_input
        temp_input.select()
        document.execCommand("copy")
        temp_input.parent.removeChild(temp_input)
        show_notification("คัดลอกรหัสลับเรียบร้อยแล้ว! (Fallback)", "success")

def generate_pdf(name, mission_title, score, satisfaction, hash_val, date_str):
    # 1. โหลดข้อมูลลงในเทมเพลต HTML
    document["cert-student-name"].text = name
    document["cert-mission-title"].text = f'"{mission_title}"'
    document["cert-score-value"].text = f"{score} / 1000"
    document["cert-satisfaction-value"].text = f"{satisfaction}%"
    document["cert-date-string"].text = f"วันที่ออกใบรับรอง: {date_str}"
    document["cert-hash-code"].text = f"Verification Code: {hash_val}"
    
    # แสดงข้อความแจ้งเตือนขณะทำงาน
    show_notification("กำลังประมวลผลไฟล์เกียรติบัตรภาษาไทย... กรุณารอสักครู่", "info")
    
    # ฟังก์ชัน Callback เมื่อ html2canvas ทำงานเสร็จ
    def save_pdf_from_canvas(canvas):
        try:
            img_data = canvas.toDataURL("image/png")
            # สร้าง PDF ขนาด A4 แนวนอน (297 x 210 มม.)
            pdf = window.jspdf.jsPDF.new("landscape", "mm", "a4")
            pdf.addImage(img_data, "PNG", 0, 0, 297, 210)
            
            clean_name = name.replace(" ", "_")
            pdf.save(f"Database-Architect-Certificate-{clean_name}.pdf")
            show_notification("ดาวน์โหลดเกียรติบัตรสำเร็จแล้วค่ะ!", "success")
        except Exception as e:
            window.console.log(f"PDF creation error: {e}")
            show_notification("ไม่สามารถส่งออก PDF ได้: " + str(e), "error")
            
    # เรียกใช้ html2canvas จากหน้าต่างเบราว์เซอร์ กำหนด scale: 2 เพื่อตัวอักษรที่คมชัด
    try:
        cert_el = document["cert-template"]
        window.html2canvas(cert_el, {"scale": 2}).then(save_pdf_from_canvas)
    except Exception as e:
        show_notification("ไม่สามารถสร้างเกียรติบัตรได้: " + str(e), "error")

def download_certificate_clicked(ev):
    """
    สร้างเกียรติบัตร PDF จากโครงสร้าง HTML ด้วย html2canvas เพื่อความถูกต้องในการแสดงผลภาษาไทย 100%
    """
    mission = state.get_active_mission()
    name = state.student_name
    score = state.score
    satisfaction = state.satisfaction
    hash_val = encode_score(name, mission["id"], score, satisfaction)
    date_str = time.strftime('%Y-%m-%d')
    
    generate_pdf(name, mission["title"], score, satisfaction, hash_val, date_str)

# ==================== TEACHER VERIFICATION ====================

def verify_hash_clicked(ev):
    hash_txt = document["hash-input"].value.strip()
    result_box = document["verify-result"]
    
    if not hash_txt:
        show_notification("กรุณากรอกรหัสลับยืนยันคะแนนเพื่อทำการตรวจสอบครับ", "error")
        return
        
    result_data = decode_score(hash_txt)
    
    result_box.classList.remove("hidden")
    if result_data:
        result_box.className = "verify-result-box"
        
        # Translate mission name
        m_title = "ไม่พบรหัสภารกิจ"
        for m in MISSIONS:
            if m["id"] == result_data["mission_id"]:
                m_title = m["title"]
                break
                
        html_content = f"""
            <h4 class='text-accent' style='margin-bottom: 12px;'><i class="fa-solid fa-square-check"></i> ผลการตรวจสอบ: รหัสถูกต้อง (Verified)</h4>
            <div style='display: grid; grid-template-columns: 1fr 2fr; gap: 8px; font-size: 0.9rem; margin-bottom: 15px;'>
                <span>ชื่อนักเรียน:</span><strong>{result_data['name']}</strong>
                <span>ด่านภารกิจ:</span><strong>{m_title}</strong>
                <span>คะแนนวิเคราะห์:</span><strong>{result_data['score']} / 1000</strong>
                <span>ความพึงพอใจ:</span><strong>{result_data['satisfaction']}%</strong>
                <span>วันที่ทำภารกิจ:</span><strong>{result_data['date']}</strong>
            </div>
            <button id="btn-teacher-download-cert" class="btn btn-primary w-full" style="font-size: 0.9rem; padding: 10px; border-radius: 6px;">
                <i class="fa-solid fa-file-pdf"></i> ดาวน์โหลดเกียรติบัตร (PDF) ของนักเรียน
            </button>
        """
        result_box.innerHTML = html_content
        
        # Bind teacher certificate download click
        def download_teacher_cert(e):
            date_only = result_data["date"].split(" ")[0]
            generate_pdf(result_data["name"], m_title, result_data["score"], result_data["satisfaction"], hash_txt, date_only)
            
        document["btn-teacher-download-cert"].bind("click", download_teacher_cert)
        
        show_notification("ตรวจสอบรหัสลับสำเร็จ! ข้อมูลตรงกับประวัติการทำภารกิจจริง", "success")
    else:
        result_box.className = "verify-result-box error"
        result_box.innerHTML = f"""
            <h4 class='text-danger'><i class="fa-solid fa-square-xmark"></i> ตรวจสอบผิดพลาด</h4>
            <p style='font-size: 0.85rem; color: var(--text-muted); margin-top: 5px;'>
                รหัสลับยืนยันคะแนนไม่ถูกต้อง หรือถูกดัดแปลงข้อมูลระบบทำให้ถอดรหัสไม่สำเร็จ กรุณาเช็คตัวสะกดอีกครั้งค่ะ
            </p>
        """
        show_notification("รหัสยืนยันไม่ถูกต้องกรุณาตรวจสอบ", "error")

# ==================== STATE INITIALIZER ====================

def update_stage_indicator():
    # Update top status bar dot colors based on current active stage
    for i in range(1, 4):
        dot = document[f"dot-stage-{i}"]
        if i == state.active_stage:
            dot.className = "stage-dot active"
        elif i < state.active_stage:
            dot.className = "stage-dot completed"
        else:
            dot.className = "stage-dot"

def reset_to_home(ev):
    show_view("view-home")

def exit_to_selection(ev):
    show_view("view-select-mission")

def open_brief_modal(ev):
    """
    ดึงข้อมูลภารกิจปัจจุบันมาแสดงผลบน Modal
    """
    mission = state.get_active_mission()
    document["modal-client-avatar"].text = mission["avatar"]
    document["modal-client-name"].text = mission["company"]
    document["modal-client-company"].text = mission["title"]
    document["modal-brief-text-content"].innerHTML = mission["brief"]
    document["modal-brief"].classList.remove("hidden")

def close_brief_modal(ev):
    """
    ปิดการแสดงผล Modal
    """
    document["modal-brief"].classList.add("hidden")

def on_backdrop_click(ev):
    """
    ปิด Modal เมื่อคลิกพื้นที่ด้านนอกกล่องการ์ด
    """
    if ev.target.id == "modal-brief":
        close_brief_modal(ev)
    elif ev.target.id == "modal-manual":
        close_manual_modal(ev)

def open_manual_modal(ev):
    document["modal-manual"].classList.remove("hidden")
    switch_manual_tab("student")

def close_manual_modal(ev):
    document["modal-manual"].classList.add("hidden")

def switch_manual_tab(tab_name):
    student_btn = document["tab-student"]
    teacher_btn = document["tab-teacher"]
    student_content = document["manual-student-content"]
    teacher_content = document["manual-teacher-content"]
    
    if tab_name == "student":
        student_btn.classList.add("active-tab")
        teacher_btn.classList.remove("active-tab")
        student_content.classList.remove("hidden")
        teacher_content.classList.add("hidden")
    else:
        student_btn.classList.remove("active-tab")
        teacher_btn.classList.add("active-tab")
        student_content.classList.add("hidden")
        teacher_content.classList.remove("hidden")

# ==================== INITIAL EVENT BINDINGS ====================

# Bind Buttons
document["btn-start-game"].bind("click", start_game_clicked)
document["btn-teacher-panel"].bind("click", lambda ev: show_view("view-teacher"))
document["btn-back-home"].bind("click", reset_to_home)
document["btn-verify-hash"].bind("click", verify_hash_clicked)
document["btn-start-mission"].bind("click", start_mission_clicked)

# Gameplay controls
document["btn-check-l1"].bind("click", check_l1_clicked)
document["btn-check-l2"].bind("click", check_l2_clicked)
document["btn-check-l3"].bind("click", check_l3_clicked)
document["btn-clear-connections"].bind("click", clear_connections_clicked)

# Finish screen controls
document["btn-copy-hash"].bind("click", copy_hash_clicked)
document["btn-download-cert"].bind("click", download_certificate_clicked)
document["btn-restart"].bind("click", exit_to_selection)

# Modal controls
document["btn-view-brief-modal"].bind("click", open_brief_modal)
document["btn-close-brief-modal"].bind("click", close_brief_modal)
document["modal-brief"].bind("click", on_backdrop_click)

# Manual controls
document["btn-how-to-play"].bind("click", open_manual_modal)
document["btn-close-manual-modal"].bind("click", close_manual_modal)
document["modal-manual"].bind("click", on_backdrop_click)
document["tab-student"].bind("click", lambda ev: switch_manual_tab("student"))
document["tab-teacher"].bind("click", lambda ev: switch_manual_tab("teacher"))
