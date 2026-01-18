# models.py
import math
import random
import os
from settings import *

# Lop dai dien cho mot nut (dinh) trong do thi


class Nut:
    def __init__(self, ma_so, toa_do_x, toa_do_y):
        self.ma_so = ma_so              # ID cua nut
        self.x = int(toa_do_x)          # Vi tri x
        self.y = int(toa_do_y)          # Vi tri y
        self.mau_sac = MAU_XAM          # Mau mac dinh
        # Danh sach hang xom: [(nut, trong_so)...]
        self.danh_sach_ke = []
        self.khoang_cach = float('inf')  # Khoang cach tu nguon
        self.nut_cha = None             # Nut cha de truy vet
        self.da_tham = False            # Da tham hay chua

    # Ham them canh noi sang nut khac
    def them_canh(self, nut_khac, trong_so=1, hai_chieu=True):
        # Kiem tra neu co canh roi thi thoi
        for ke, w in self.danh_sach_ke:
            if ke == nut_khac:
                return

        self.danh_sach_ke.append((nut_khac, trong_so))

        # Neu la vo huong (2 chieu) thi them nguoc lai
        if hai_chieu:
            tim_thay = False
            for ke, w in nut_khac.danh_sach_ke:
                if ke == self:
                    tim_thay = True
            if not tim_thay:
                nut_khac.danh_sach_ke.append((self, trong_so))

    # Reset trang thai de chay thuat toan moi
    def dat_lai_trang_thai(self):
        self.mau_sac = MAU_XAM
        self.khoang_cach = float('inf')
        self.nut_cha = None
        self.da_tham = False

    def __lt__(self, other):
        return self.khoang_cach < other.khoang_cach

# --- Cac ham phu tro ---


def tinh_khoang_cach(nut_1, nut_2):
    return math.hypot(nut_1.x - nut_2.x, nut_1.y - nut_2.y)

# Sap xep nut len luoi cho de nhin


def sap_xep_vi_tri_tren_luoi(danh_sach_nut, so_luong):
    rong = CHIEU_RONG_CUA_SO - 420
    cao = CHIEU_CAO_CUA_SO - 100

    so_cot = math.ceil(math.sqrt(so_luong * 2.5))
    if so_cot > 8:
        so_cot = 8
    so_dong = math.ceil(so_luong / so_cot)

    khoang_cach_x = rong // (so_cot + 1)
    khoang_cach_y = cao // (so_dong + 0.5)

    lech_x, lech_y = 50, 50
    vi_tri = []

    for r in range(so_dong):
        for c in range(so_cot):
            x = lech_x + (c + 1) * khoang_cach_x + random.randint(-2, 2)
            y = lech_y + (r + 1) * khoang_cach_y + random.randint(-2, 2)
            vi_tri.append((x, y))

    random.shuffle(vi_tri)
    for i in range(so_luong):
        if i < len(vi_tri):
            danh_sach_nut[i].x = int(vi_tri[i][0])
            danh_sach_nut[i].y = int(vi_tri[i][1])

# Tao do thi ngau nhien


def tao_do_thi_ngau_nhien(co_huong=False):
    danh_sach_nut = []
    so_luong = random.randint(10, 100)
    for i in range(so_luong):
        danh_sach_nut.append(Nut(i, 0, 0))

    sap_xep_vi_tri_tren_luoi(danh_sach_nut, so_luong)

    # Dam bao lien thong
    da_ket_noi = {danh_sach_nut[0]}
    chua_ket_noi = set(danh_sach_nut[1:])

    while chua_ket_noi:
        u, v = None, None
        min_dist = float('inf')

        ung_vien = list(da_ket_noi)
        if len(ung_vien) > 8:
            ung_vien = random.sample(ung_vien, 8)

        for hien_tai in ung_vien:
            for muc_tieu in chua_ket_noi:
                if (hien_tai.ma_so == 0 and muc_tieu.ma_so == so_luong-1) or (hien_tai.ma_so == so_luong-1 and muc_tieu.ma_so == 0):
                    continue
                if len(hien_tai.danh_sach_ke) >= 3:
                    continue

                d = tinh_khoang_cach(hien_tai, muc_tieu)
                if d < min_dist:
                    min_dist = d
                    u = hien_tai
                    v = muc_tieu

        if u is None:
            u = random.choice(list(da_ket_noi))
            v = random.choice(list(chua_ket_noi))

        u.them_canh(v, random.randint(1, 20), hai_chieu=False)
        da_ket_noi.add(v)
        chua_ket_noi.remove(v)

    # Them canh ngau nhien cho day
    for u in danh_sach_nut:
        cac_nut_khac = sorted(
            danh_sach_nut, key=lambda x: tinh_khoang_cach(u, x))
        gan_nhat = cac_nut_khac[1:6]
        random.shuffle(gan_nhat)

        for v in gan_nhat:
            if u == v or (u.ma_so == 0 and v.ma_so == so_luong-1) or (u.ma_so == so_luong-1 and v.ma_so == 0):
                continue

            dem_vao = 0
            for nut in danh_sach_nut:
                if nut == v:
                    continue
                for k, w in nut.danh_sach_ke:
                    if k == v:
                        dem_vao += 1

            if len(u.danh_sach_ke) < 2 and dem_vao < 2:
                da_co = False
                for k, w in u.danh_sach_ke:
                    if k == v:
                        da_co = True
                for k, w in v.danh_sach_ke:
                    if k == u:
                        da_co = True

                if not da_co:
                    u.them_canh(v, random.randint(1, 20), hai_chieu=False)
                    if len(u.danh_sach_ke) >= 2:
                        break

    if not co_huong:
        chuyen_thanh_vo_huong(danh_sach_nut)

    return danh_sach_nut

# --- CAC HAM CHUYEN DOI VA SAO LUU ---

# Luu cau truc do thi hien tai (de backup)


def sao_chep_do_thi(ds_nut):
    data = []
    for n in ds_nut:
        edges = [(ke.ma_so, w) for ke, w in n.danh_sach_ke]
        # Luu ID, toa do (du toa do co the thay doi khi keo tha, ta se cap nhat sau)
        data.append({'id': n.ma_so, 'x': n.x, 'y': n.y, 'edges': edges})
    return data

# Khoi phuc do thi tu ban backup (nhung giu vi tri hien tai neu co)


def khoi_phuc_do_thi(data_luu, ds_hien_tai=None):
    # Lay vi tri hien tai cua cac nut (de khi switch khong bi nhay vi tri)
    pos_map = {}
    if ds_hien_tai:
        for n in ds_hien_tai:
            pos_map[n.ma_so] = (n.x, n.y)

    new_nodes = []
    # Tao nut moi
    for d in data_luu:
        x, y = d['x'], d['y']
        if d['id'] in pos_map:
            x, y = pos_map[d['id']]
        new_nodes.append(Nut(d['id'], x, y))

    # Tao canh
    for d in data_luu:
        u = next(n for n in new_nodes if n.ma_so == d['id'])
        for v_id, w in d['edges']:
            v = next(n for n in new_nodes if n.ma_so == v_id)
            u.danh_sach_ke.append((v, w))

    return new_nodes


def chuyen_thanh_vo_huong(danh_sach_nut):
    for u in danh_sach_nut:
        for v, w in u.danh_sach_ke:
            tim_thay = False
            for k, kw in v.danh_sach_ke:
                if k == u:
                    tim_thay = True
                    break
            if not tim_thay:
                v.danh_sach_ke.append((u, w))
    return danh_sach_nut


def chuyen_thanh_co_huong(danh_sach_nut):
    # Ham nay chi dung khi KHONG co ban backup
    da_xu_ly = set()
    for u in danh_sach_nut:
        danh_sach_copy = list(u.danh_sach_ke)
        for v, w in danh_sach_copy:
            cap_canh = tuple(sorted((u.ma_so, v.ma_so)))
            if cap_canh in da_xu_ly:
                continue

            v_noi_u = False
            for k, kw in v.danh_sach_ke:
                if k == u:
                    v_noi_u = True
                    break

            if v_noi_u:
                if (u.ma_so + v.ma_so) % 2 == 0:
                    danh_sach_moi = []
                    for k, kw in v.danh_sach_ke:
                        if k != u:
                            danh_sach_moi.append((k, kw))
                    v.danh_sach_ke = danh_sach_moi
                else:
                    if (v, w) in u.danh_sach_ke:
                        u.danh_sach_ke.remove((v, w))
            da_xu_ly.add(cap_canh)
    return danh_sach_nut

# --- Xu ly file lich su ---


FILE_LICH_SU = "lich_su_nhap.txt"
DAU_CACH = "---HET---"


def phan_tich_van_ban(van_ban):
    danh_sach_nut = []
    cac_dong = [l.strip() for l in van_ban.strip().split('\n') if l.strip()]
    if not cac_dong:
        return None

    try:
        so_luong = int(cac_dong[0])
        for i in range(so_luong):
            danh_sach_nut.append(Nut(i, 0, 0))
        sap_xep_vi_tri_tren_luoi(danh_sach_nut, so_luong)

        for l in cac_dong[1:]:
            mang_so = list(map(int, l.split()))
            if len(mang_so) >= 3:
                u, v, w = mang_so
                if 0 <= u < so_luong and 0 <= v < so_luong:
                    danh_sach_nut[u].them_canh(
                        danh_sach_nut[v], w, hai_chieu=False)
        return danh_sach_nut
    except:
        return None


def luu_lich_su_nhap(van_ban):
    if not van_ban.strip():
        return
    cu = lay_lich_su_nhap()
    if cu and cu[0].strip() == van_ban.strip():
        return

    try:
        with open(FILE_LICH_SU, "a", encoding="utf-8") as f:
            f.write(van_ban.strip() + "\n" + DAU_CACH + "\n")
    except:
        pass


def lay_lich_su_nhap():
    if not os.path.exists(FILE_LICH_SU):
        return []
    ket_qua = []
    try:
        with open(FILE_LICH_SU, "r", encoding="utf-8") as f:
            cac_doan = f.read().split(DAU_CACH)
            for doan in cac_doan:
                if doan.strip():
                    ket_qua.insert(0, doan.strip())
    except:
        pass
    return ket_qua


def tao_du_lieu_ngau_nhien_dang_chu():
    danh_sach_nut = tao_do_thi_ngau_nhien(co_huong=True)
    ket_qua = [str(len(danh_sach_nut))]
    for u in danh_sach_nut:
        for v, w in u.danh_sach_ke:
            ket_qua.append(f"{u.ma_so} {v.ma_so} {w}")
    return "\n".join(ket_qua)


def luu_file_day_du(ten_file, danh_sach_nut, co_huong, noi_dung_bao_cao):
    try:
        with open(ten_file, 'w', encoding='utf-8') as f:
            f.write("CHE_DO: " + ("CO_HUONG" if co_huong else "VO_HUONG") + "\n")
            f.write(f"SO_NUT: {len(danh_sach_nut)}\n")
            for n in danh_sach_nut:
                f.write(f"{n.ma_so} {n.x} {n.y}\n")
            f.write("CANH:\n")
            for u in danh_sach_nut:
                for v, w in u.danh_sach_ke:
                    f.write(f"{u.ma_so} {v.ma_so} {w}\n")
            f.write("KET_THUC_DU_LIEU\n")
            f.write("\n============================================\n")
            f.write("         BAO CAO SO SANH THUAT TOAN         \n")
            f.write("============================================\n")
            f.write(noi_dung_bao_cao)
        return True
    except Exception as e:
        print(f"Loi luu file: {e}")
        return False


def doc_file_day_du(ten_file):
    danh_sach_nut = []
    co_huong = True
    try:
        with open(ten_file, 'r', encoding='utf-8') as f:
            cac_dong = [l.strip() for l in f.readlines()]

        dong_che_do = -1
        dong_so_nut = -1
        dong_canh = -1
        dong_ket_thuc = -1

        for i, l in enumerate(cac_dong):
            if l.startswith("CHE_DO:"):
                dong_che_do = i
            elif l.startswith("SO_NUT:"):
                dong_so_nut = i
            elif l.startswith("CANH:"):
                dong_canh = i
            elif l.startswith("KET_THUC_DU_LIEU"):
                dong_ket_thuc = i

        if dong_che_do == -1 or dong_so_nut == -1:
            return None, True

        kieu = cac_dong[dong_che_do].split(":")[1].strip()
        co_huong = (kieu == "CO_HUONG")

        so_luong = int(cac_dong[dong_so_nut].split(":")[1].strip())
        for i in range(dong_so_nut + 1, dong_canh):
            phan = list(map(int, cac_dong[i].split()))
            if len(phan) >= 3:
                danh_sach_nut.append(Nut(phan[0], phan[1], phan[2]))

        diem_dung = dong_ket_thuc if dong_ket_thuc != -1 else len(cac_dong)
        for i in range(dong_canh + 1, diem_dung):
            if not cac_dong[i]:
                continue
            phan = list(map(int, cac_dong[i].split()))
            if len(phan) >= 3:
                u_id, v_id, w = phan[0], phan[1], phan[2]
                u_obj = next(
                    (n for n in danh_sach_nut if n.ma_so == u_id), None)
                v_obj = next(
                    (n for n in danh_sach_nut if n.ma_so == v_id), None)
                if u_obj and v_obj:
                    u_obj.them_canh(v_obj, w, hai_chieu=False)

        return danh_sach_nut, co_huong

    except Exception as e:
        print(f"Loi doc file: {e}")
        return None, True
