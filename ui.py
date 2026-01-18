# ui.py
import pygame
import math
import tkinter as tk
from settings import *

# --- Cac ham ve ---


def cat_dong_van_ban(van_ban, font, chieu_rong_toi_da):
    cac_tu = van_ban.split(' ')
    cac_dong = []
    dong_hien_tai = ""
    for tu in cac_tu:
        thu = dong_hien_tai + tu + " "
        if font.size(thu)[0] < chieu_rong_toi_da:
            dong_hien_tai = thu
        else:
            if dong_hien_tai:
                cac_dong.append(dong_hien_tai)
            dong_hien_tai = tu + " "
    if dong_hien_tai:
        cac_dong.append(dong_hien_tai)
    return cac_dong


def chuyen_toa_do_man_hinh(x, y, ti_le, do_lech):
    return (x * ti_le + do_lech[0], y * ti_le + do_lech[1])


def lay_trung_diem(p1, p2):
    return ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)


def duong_cong_bezier(p0, p1, p2, t):
    x = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
    y = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
    return (x, y)


def ve_duong_noi(man_hinh, diem_dau, diem_cuoi, mau=MAU_DEN, do_day=2, ti_le=1.0):
    dx = diem_cuoi[0] - diem_dau[0]
    dy = diem_cuoi[1] - diem_dau[1]
    d = math.hypot(dx, dy)
    if d == 0:
        return diem_dau

    if d < 180 * ti_le:
        rut_ngan = 6 * ti_le
        px, py = -dy/d, dx/d
        sx = diem_dau[0] + px*rut_ngan
        sy = diem_dau[1] + py*rut_ngan
        ex = diem_cuoi[0] + px*rut_ngan
        ey = diem_cuoi[1] + py*rut_ngan

        r = int(BAN_KINH_NUT * ti_le)
        goc = math.atan2(ey - sy, ex - sx)
        dich_thuc = ex - r * math.cos(goc)
        dich_thuc_y = ey - r * math.sin(goc)

        pygame.draw.line(man_hinh, mau, (sx, sy),
                         (dich_thuc, dich_thuc_y), do_day)

        do_lon_mui_ten = 10 * ti_le
        x1 = dich_thuc - do_lon_mui_ten * math.cos(goc - math.pi/6)
        y1 = dich_thuc_y - do_lon_mui_ten * math.sin(goc - math.pi/6)
        x2 = dich_thuc - do_lon_mui_ten * math.cos(goc + math.pi/6)
        y2 = dich_thuc_y - do_lon_mui_ten * math.sin(goc + math.pi/6)
        pygame.draw.polygon(
            man_hinh, mau, [(dich_thuc, dich_thuc_y), (x1, y1), (x2, y2)])
        return lay_trung_diem((sx, sy), (dich_thuc, dich_thuc_y))
    else:
        mx, my = (diem_dau[0]+diem_cuoi[0])/2, (diem_dau[1]+diem_cuoi[1])/2
        do_cong = d * 0.2
        nx, ny = -dy/d, dx/d
        cx, cy = mx + nx*do_cong, my + ny*do_cong

        cac_diem = [duong_cong_bezier(
            diem_dau, (cx, cy), diem_cuoi, t/20) for t in range(21)]
        if len(cac_diem) > 1:
            pygame.draw.lines(man_hinh, mau, False, cac_diem, do_day)

        cuoi, gan_cuoi = cac_diem[-1], cac_diem[-2]
        goc = math.atan2(cuoi[1]-gan_cuoi[1], cuoi[0]-gan_cuoi[0])
        r = int(BAN_KINH_NUT * ti_le)
        dich_thuc = diem_cuoi[0] - r * math.cos(goc)
        dich_thuc_y = diem_cuoi[1] - r * math.sin(goc)

        do_lon_mui_ten = 10 * ti_le
        x1 = dich_thuc - do_lon_mui_ten * math.cos(goc - math.pi/6)
        y1 = dich_thuc_y - do_lon_mui_ten * math.sin(goc - math.pi/6)
        x2 = dich_thuc - do_lon_mui_ten * math.cos(goc + math.pi/6)
        y2 = dich_thuc_y - do_lon_mui_ten * math.sin(goc + math.pi/6)
        pygame.draw.polygon(
            man_hinh, mau, [(dich_thuc, dich_thuc_y), (x1, y1), (x2, y2)])
        return duong_cong_bezier(diem_dau, (cx, cy), diem_cuoi, 0.5)


def lay_mau_nut(nut, nut_dang_chon, duong_di):
    mau_nen, mau_vien, mau_chu = nut.mau_sac, MAU_DEN, MAU_DEN
    if mau_nen in [MAU_DEN, MAU_XANH_DUONG]:
        mau_chu = MAU_TRANG
    mo_di = False

    if nut_dang_chon:
        if nut == nut_dang_chon:
            mau_nen, mau_vien, mau_chu = MAU_TRANG, MAU_DEN, MAU_DEN
        else:
            di_ra = any(k == nut_dang_chon for k, w in nut.danh_sach_ke)
            di_vao = any(k == nut for k, w in nut_dang_chon.danh_sach_ke)
            if di_ra:
                mau_nen, mau_vien, mau_chu = MAU_DO, MAU_DO, MAU_TRANG
            elif di_vao:
                mau_nen, mau_vien, mau_chu = MAU_XANH_LA, MAU_XANH_LA, MAU_TRANG
            else:
                mau_nen, mau_vien, mau_chu = (
                    240, 240, 240), (220, 220, 220), (200, 200, 200)
                mo_di = True

    if nut in duong_di and not nut_dang_chon:
        mau_vien = MAU_DO
        mau_chu = MAU_TRANG if mau_nen in [
            MAU_DEN, MAU_XANH_DUONG] else MAU_DEN
    return mau_nen, mau_vien, mau_chu, mo_di

# --- CLASS GIAO DIEN ---


class NutBam:
    def __init__(self, x, y, rong, cao, van_ban, mau=MAU_XANH_LA):
        self.hinh_chu_nhat = pygame.Rect(x, y, rong, cao)
        self.noi_dung = van_ban
        self.mau = mau
        self.font = pygame.font.SysFont('Arial', 18, bold=True)
        self.gia_tri_an = ""

    def ve(self, man_hinh):
        bong = self.hinh_chu_nhat.copy()
        bong.x += 2
        bong.y += 2
        pygame.draw.rect(man_hinh, (200, 200, 200), bong, border_radius=8)
        pygame.draw.rect(man_hinh, self.mau,
                         self.hinh_chu_nhat, border_radius=8)
        pygame.draw.rect(man_hinh, MAU_DEN,
                         self.hinh_chu_nhat, 2, border_radius=8)
        text_surf = self.font.render(self.noi_dung, True, MAU_TRANG)
        man_hinh.blit(text_surf, text_surf.get_rect(
            center=self.hinh_chu_nhat.center))

    def duoc_nhan(self, vi_tri_chuot): return self.hinh_chu_nhat.collidepoint(
        vi_tri_chuot)


class HopNhapLieu:
    def __init__(self, x, y, rong, cao, font):
        self.hinh_chu_nhat = pygame.Rect(x, y, rong, cao)
        self.cac_dong = [""]
        self.font = font
        self.dang_kich_hoat = True
        self.cuon_doc = 0
        self.con_tro = [0, 0]
        self.diem_neo = [0, 0]
        self.dang_keo_chuot = False
        self.chieu_cao_dong = 20

    def lay_noi_dung(self): return "\n".join(self.cac_dong)

    def dat_noi_dung(self, van_ban_tho):
        self.cac_dong = van_ban_tho.split('\n')
        self.con_tro = [len(self.cac_dong)-1, len(self.cac_dong[-1])]
        self.diem_neo = list(self.con_tro)

    def xoa_vung_chon(self):
        if self.con_tro == self.diem_neo:
            return False
        dau, cuoi = sorted([self.con_tro, self.diem_neo])
        r1, c1 = dau
        r2, c2 = cuoi

        if r1 == r2:
            l = self.cac_dong[r1]
            self.cac_dong[r1] = l[:c1] + l[c2:]
        else:
            dau_dong = self.cac_dong[r1][:c1]
            cuoi_dong = self.cac_dong[r2][c2:]
            self.cac_dong[r1] = dau_dong + cuoi_dong
            for _ in range(r2-r1):
                self.cac_dong.pop(r1+1)

        self.con_tro = [r1, c1]
        self.diem_neo = [r1, c1]
        return True

    def chen_chu(self, chu):
        self.xoa_vung_chon()
        danh_sach = chu.split('\n')
        r, c = self.con_tro
        dau = self.cac_dong[r][:c]
        cuoi = self.cac_dong[r][c:]

        if len(danh_sach) == 1:
            self.cac_dong[r] = dau + danh_sach[0] + cuoi
            self.con_tro = [r, c + len(danh_sach[0])]
        else:
            self.cac_dong[r] = dau + danh_sach[0]
            for i in range(1, len(danh_sach)-1):
                self.cac_dong.insert(r+i, danh_sach[i])
            self.cac_dong.insert(r+len(danh_sach)-1, danh_sach[-1] + cuoi)
            self.con_tro = [r+len(danh_sach)-1, len(danh_sach[-1])]
        self.diem_neo = list(self.con_tro)

    def copy(self):
        if self.con_tro == self.diem_neo:
            return
        dau, cuoi = sorted([self.con_tro, self.diem_neo])
        r1, c1 = dau
        r2, c2 = cuoi
        t = ""
        if r1 == r2:
            t = self.cac_dong[r1][c1:c2]
        else:
            t = self.cac_dong[r1][c1:] + "\n"
            for i in range(r1+1, r2):
                t += self.cac_dong[i] + "\n"
            t += self.cac_dong[r2][:c2]

        try:
            r = tk.Tk()
            r.withdraw()
            r.clipboard_clear()
            r.clipboard_append(t)
            r.update()
            r.destroy()
        except:
            pass

    def paste(self):
        try:
            r = tk.Tk()
            r.withdraw()
            c = r.clipboard_get()
            r.destroy()

            if c:
                self.chen_chu(str(c))
        except:
            pass

    def lay_vi_tri_con_tro_tu_chuot(self, x, y):
        lech_y = y - self.hinh_chu_nhat.y - 5
        r = int(lech_y // self.chieu_cao_dong) + self.cuon_doc
        r = max(0, min(r, len(self.cac_dong) - 1))

        l = self.cac_dong[r]
        lech_x = x - self.hinh_chu_nhat.x - 5
        best = 0
        min_d = float('inf')

        for i in range(len(l) + 1):
            w, _ = self.font.size(l[:i])
            d = abs(w - lech_x)
            if d < min_d:
                min_d = d
                best = i
            else:
                break
        return [r, best]

    def xu_ly_su_kien(self, e):
        mods = pygame.key.get_mods()
        ctrl = (mods & pygame.KMOD_CTRL)
        shift = (mods & pygame.KMOD_SHIFT)

        if e.type == pygame.MOUSEBUTTONDOWN:
            if self.hinh_chu_nhat.collidepoint(e.pos):
                self.dang_kich_hoat = True
                if e.button == 1:
                    t = self.lay_vi_tri_con_tro_tu_chuot(*e.pos)
                    self.con_tro = t
                    if not shift:
                        self.diem_neo = list(t)
                    self.dang_keo_chuot = True
                elif e.button == 4:
                    self.cuon_doc = max(0, self.cuon_doc - 1)
                elif e.button == 5:
                    self.cuon_doc += 1
            else:
                self.dang_kich_hoat = False

        elif e.type == pygame.MOUSEBUTTONUP:
            if e.button == 1:
                self.dang_keo_chuot = False

        elif e.type == pygame.MOUSEMOTION:
            if self.dang_kich_hoat and self.dang_keo_chuot:
                self.con_tro = self.lay_vi_tri_con_tro_tu_chuot(*e.pos)
                so_dong_hien_thi = self.hinh_chu_nhat.height // self.chieu_cao_dong
                if self.con_tro[0] < self.cuon_doc:
                    self.cuon_doc = self.con_tro[0]
                if self.con_tro[0] > self.cuon_doc + so_dong_hien_thi - 2:
                    self.cuon_doc = self.con_tro[0] - so_dong_hien_thi + 2

        elif e.type == pygame.KEYDOWN and self.dang_kich_hoat:
            da_di_chuyen = False
            if e.key == pygame.K_UP:
                if self.con_tro[0] > 0:
                    self.con_tro[0] -= 1
                    self.con_tro[1] = min(self.con_tro[1], len(
                        self.cac_dong[self.con_tro[0]]))
                da_di_chuyen = True
            elif e.key == pygame.K_DOWN:
                if self.con_tro[0] < len(self.cac_dong)-1:
                    self.con_tro[0] += 1
                    self.con_tro[1] = min(self.con_tro[1], len(
                        self.cac_dong[self.con_tro[0]]))
                da_di_chuyen = True
            elif e.key == pygame.K_LEFT:
                if self.con_tro[1] > 0:
                    self.con_tro[1] -= 1
                elif self.con_tro[0] > 0:
                    self.con_tro[0] -= 1
                    self.con_tro[1] = len(self.cac_dong[self.con_tro[0]])
                da_di_chuyen = True
            elif e.key == pygame.K_RIGHT:
                if self.con_tro[1] < len(self.cac_dong[self.con_tro[0]]):
                    self.con_tro[1] += 1
                elif self.con_tro[0] < len(self.cac_dong)-1:
                    self.con_tro[0] += 1
                    self.con_tro[1] = 0
                da_di_chuyen = True

            if da_di_chuyen and not shift:
                self.diem_neo = list(self.con_tro)

            if ctrl and e.key == pygame.K_a:
                self.diem_neo = [0, 0]
                self.con_tro = [len(self.cac_dong)-1, len(self.cac_dong[-1])]
            elif ctrl and e.key == pygame.K_c:
                self.copy()
            elif ctrl and e.key == pygame.K_v:
                self.paste()
            elif ctrl and e.key == pygame.K_x:
                self.copy()
                self.xoa_vung_chon()

            elif e.key == pygame.K_RETURN:
                self.chen_chu("\n")
            elif e.key == pygame.K_BACKSPACE:
                if self.con_tro != self.diem_neo:
                    self.xoa_vung_chon()
                else:
                    r, c = self.con_tro
                    if c > 0:
                        self.cac_dong[r] = self.cac_dong[r][:c-1] + \
                            self.cac_dong[r][c:]
                        self.con_tro[1] -= 1
                    elif r > 0:
                        pr = self.cac_dong[r-1]
                        cr = self.cac_dong[r]
                        self.cac_dong[r-1] = pr+cr
                        self.cac_dong.pop(r)
                        self.con_tro = [r-1, len(pr)]
                    self.diem_neo = list(self.con_tro)
            elif e.key == pygame.K_DELETE:
                if self.con_tro != self.diem_neo:
                    self.xoa_vung_chon()
                else:
                    r, c = self.con_tro
                    if c < len(self.cac_dong[r]):
                        self.cac_dong[r] = self.cac_dong[r][:c] + \
                            self.cac_dong[r][c+1:]
                    elif r < len(self.cac_dong)-1:
                        self.cac_dong[r] += self.cac_dong[r+1]
                        self.cac_dong.pop(r+1)
            elif e.unicode and e.unicode.isprintable() and not ctrl:
                self.chen_chu(e.unicode)

    def ve(self, man_hinh):
        pygame.draw.rect(man_hinh, MAU_NEN_HOP, self.hinh_chu_nhat)
        mau_vien = MAU_VIEN_HOP if self.dang_kich_hoat else MAU_XAM
        pygame.draw.rect(man_hinh, mau_vien, self.hinh_chu_nhat, 2)

        so_dong_hien_thi = self.hinh_chu_nhat.height // self.chieu_cao_dong
        if self.cuon_doc > len(self.cac_dong) - so_dong_hien_thi:
            self.cuon_doc = max(0, len(self.cac_dong) - so_dong_hien_thi)

        man_hinh.set_clip(self.hinh_chu_nhat.inflate(-10, -10))
        sx = self.hinh_chu_nhat.x + 5
        sy = self.hinh_chu_nhat.y + 5

        dau, cuoi = sorted([self.con_tro, self.diem_neo])
        co_chon = (dau != cuoi)

        for i in range(self.cuon_doc, min(len(self.cac_dong), self.cuon_doc + so_dong_hien_thi + 1)):
            dong = self.cac_dong[i]
            y = sy + (i - self.cuon_doc) * self.chieu_cao_dong

            if co_chon:
                if dau[0] < i < cuoi[0]:
                    w, _ = self.font.size(dong if dong else " ")
                    pygame.draw.rect(man_hinh, (180, 210, 255),
                                     (sx, y, w+5, self.chieu_cao_dong))
                elif i == dau[0] and i == cuoi[0]:
                    x1, _ = self.font.size(dong[:dau[1]])
                    x2, _ = self.font.size(dong[:cuoi[1]])
                    pygame.draw.rect(man_hinh, (180, 210, 255),
                                     (sx+x1, y, x2-x1, self.chieu_cao_dong))
                elif i == dau[0]:
                    x1, _ = self.font.size(dong[:dau[1]])
                    wf, _ = self.font.size(dong)
                    pygame.draw.rect(man_hinh, (180, 210, 255),
                                     (sx+x1, y, wf-x1+5, self.chieu_cao_dong))
                elif i == cuoi[0]:
                    x2, _ = self.font.size(dong[:cuoi[1]])
                    pygame.draw.rect(man_hinh, (180, 210, 255),
                                     (sx, y, x2, self.chieu_cao_dong))

            if dong and len(dong) > 0:
                try:
                    t = self.font.render(dong, True, MAU_DEN)
                    man_hinh.blit(t, (sx, y))
                except pygame.error:
                    pass

            if self.dang_kich_hoat and i == self.con_tro[0]:
                if pygame.time.get_ticks() % 1000 < 500:
                    cx, _ = self.font.size(dong[:self.con_tro[1]])
                    pygame.draw.line(man_hinh, MAU_DEN, (sx+cx, y),
                                     (sx+cx, y+self.chieu_cao_dong), 2)
        man_hinh.set_clip(None)


def ve_toan_bo_do_thi(man_hinh, danh_sach_nut, font, co_huong=False, duong_di=[], nut_dang_chon=None, ti_le=1.0, do_lech=(0, 0)):
    for n in danh_sach_nut:
        nx, ny = chuyen_toa_do_man_hinh(n.x, n.y, ti_le, do_lech)
        for ke, w in n.danh_sach_ke:
            kx, ky = chuyen_toa_do_man_hinh(ke.x, ke.y, ti_le, do_lech)
            mau = MAU_DEN
            do_day = max(1, int(2*ti_le))

            if nut_dang_chon:
                mau = (230, 230, 230)
                do_day = max(1, int(1*ti_le))
                if n == nut_dang_chon:
                    mau = MAU_XANH_LA
                    do_day = max(2, int(4*ti_le))
                elif ke == nut_dang_chon:
                    mau = MAU_DO
                    do_day = max(2, int(4*ti_le))
            elif len(duong_di) > 1:
                for i in range(len(duong_di)-1):
                    if (duong_di[i] == n and duong_di[i+1] == ke):
                        mau = MAU_DO
                        do_day = max(2, int(5*ti_le))
                        break
                    if not co_huong and (duong_di[i] == ke and duong_di[i+1] == n):
                        mau = MAU_DO
                        do_day = max(2, int(5*ti_le))
                        break

            if co_huong:
                ve_duong_noi(man_hinh, (nx, ny), (kx, ky), mau, do_day, ti_le)
            else:
                if n.ma_so < ke.ma_so:
                    pygame.draw.line(man_hinh, mau, (nx, ny), (kx, ky), do_day)

    for n in danh_sach_nut:
        nx, ny = chuyen_toa_do_man_hinh(n.x, n.y, ti_le, do_lech)
        for ke, w in n.danh_sach_ke:
            if not co_huong and n.ma_so > ke.ma_so:
                continue
            kx, ky = chuyen_toa_do_man_hinh(ke.x, ke.y, ti_le, do_lech)
            hien = True
            mau = MAU_DEN
            if nut_dang_chon:
                hien = False
                if n == nut_dang_chon or ke == nut_dang_chon:
                    mau = MAU_XANH_LA if n == nut_dang_chon else MAU_DO
                    hien = True
            elif len(duong_di) > 1:
                for i in range(len(duong_di)-1):
                    if (duong_di[i] == n and duong_di[i+1] == ke):
                        mau = MAU_DO
                        hien = True
                        break
                    if not co_huong and (duong_di[i] == ke and duong_di[i+1] == n):
                        mau = MAU_DO
                        hien = True
                        break

            if hien:
                pos = ve_duong_noi(man_hinh, (nx, ny), (kx, ky), (0, 0, 0), 0,
                                   ti_le) if co_huong else lay_trung_diem((nx, ny), (kx, ky))
                if pos:
                    pygame.draw.circle(man_hinh, MAU_TRANG, (int(
                        pos[0]), int(pos[1])), int(10*ti_le))
                    if mau == MAU_DEN:
                        mau = MAU_XANH_LA
                    t = font.render(str(w), True, mau)
                    man_hinh.blit(t, t.get_rect(
                        center=(int(pos[0]), int(pos[1]))))

    W, H = man_hinh.get_size()
    r = max(5, int(BAN_KINH_NUT * ti_le))
    for n in danh_sach_nut:
        sx, sy = chuyen_toa_do_man_hinh(n.x, n.y, ti_le, do_lech)
        if not (-r < sx < W+r and -r < sy < H+r):
            continue

        mau_nen, mau_vien, mau_chu, mo_di = lay_mau_nut(
            n, nut_dang_chon, duong_di)
        pygame.draw.circle(man_hinh, mau_nen, (int(sx), int(sy)), r)
        pygame.draw.circle(man_hinh, mau_vien, (int(
            sx), int(sy)), r, max(1, int(2*ti_le)))

        tid = font.render(str(n.ma_so), True, mau_chu)
        man_hinh.blit(tid, tid.get_rect(center=(int(sx), int(sy))))

        if n.khoang_cach != float('inf') and not mo_di:
            td = font.render(str(n.khoang_cach), True, MAU_XANH_DUONG)
            br = td.get_rect(center=(int(sx), int(sy)-r-15))
            pygame.draw.rect(man_hinh, MAU_TRANG, br)
            man_hinh.blit(td, br)


def ve_bang_ket_qua(man_hinh, lich_su, cuon_doc):
    W, H = man_hinh.get_size()
    rong_bang = 450
    x = W - rong_bang
    pygame.draw.rect(man_hinh, MAU_NEN_BANG, (x, 0, rong_bang, H))

    font_kq = pygame.font.SysFont('Arial', 15, bold=True)
    font_dong = pygame.font.SysFont('Arial', 13)

    cac_cot = [("Buoc", 35), ("Dinh", 40), ("Mo", 145),
               ("Dong", 90), ("Thong Tin", 140)]

    man_hinh.set_clip(pygame.Rect(x, 35, rong_bang, H - 35))
    y = 35 + cuon_doc
    tong_chieu_cao = 0

    for hang in lich_su:
        h = 0
        if isinstance(hang, str) and (hang.startswith("KET QUA") or hang.startswith(">>")):
            ls = cat_dong_van_ban(hang, font_kq, rong_bang-10)
            h = len(ls)*20 + 10
            if y+h > 0 and y < H:
                pygame.draw.rect(man_hinh, MAU_NEN_KET_QUA,
                                 (x, y, rong_bang, h))
                pygame.draw.line(man_hinh, MAU_DO, (x, y), (x+rong_bang, y))
                for i, l in enumerate(ls):
                    man_hinh.blit(font_kq.render(
                        l, True, MAU_DO), (x+10, y+5+i*20))
        else:
            cac_o_con = []
            du_lieu_hien_thi = [hang[0], hang[1], hang[3], hang[4], hang[5]]

            for i, gia_tri in enumerate(du_lieu_hien_thi):
                if i < len(cac_cot):
                    rong_cot = cac_cot[i][1]
                    noi_dung_con = cat_dong_van_ban(
                        str(gia_tri), font_dong, rong_cot - 5)
                    cac_o_con.append(noi_dung_con)
                else:
                    cac_o_con.append([])

            h = max(1, max([len(c) for c in cac_o_con])) * 16 + 10

            if y+h > 0 and y < H:
                if int(hang[0]) % 2 == 0:
                    pygame.draw.rect(man_hinh, MAU_HANG_CHAN,
                                     (x, y, rong_bang, h))
                pygame.draw.line(man_hinh, (200, 200, 200),
                                 (x, y+h), (x+rong_bang, y+h))
                cx = x + 5
                for i, cac_dong in enumerate(cac_o_con):
                    mau_chu = MAU_DO if i == 1 else (
                        MAU_XANH_DUONG if i == 2 else MAU_DEN)
                    for j, l in enumerate(cac_dong):
                        man_hinh.blit(font_dong.render(
                            l, True, mau_chu), (cx, y+5+j*16))
                    cx += cac_cot[i][1]
        y += h
        tong_chieu_cao += h
    man_hinh.set_clip(None)

    pygame.draw.line(man_hinh, MAU_VIEN_BANG, (x, 0), (x, H), 3)
    pygame.draw.rect(man_hinh, MAU_TIEU_DE_BANG, (x, 0, rong_bang, 35))
    cx = x + 5
    for t, r in cac_cot:
        man_hinh.blit(pygame.font.SysFont(
            'Arial', 14, bold=True).render(t, True, MAU_TRANG), (cx, 8))
        cx += r
    return tong_chieu_cao


def hien_cua_so_so_sanh(man_hinh, kq_bfs, kq_dfs, kq_dijk):
    W, H = man_hinh.get_size()
    w = 900
    h = 600  # Tang chieu cao de chua duoc noi dung
    x = (W-w)//2
    y = (H-h)//2

    nen_mo = pygame.Surface((W, H))
    nen_mo.set_alpha(150)
    nen_mo.fill(0)
    man_hinh.blit(nen_mo, (0, 0))

    r = pygame.Rect(x, y, w, h)
    pygame.draw.rect(man_hinh, MAU_TRANG, r, border_radius=12)
    pygame.draw.rect(man_hinh, MAU_VIEN_BANG, r, 3, border_radius=12)

    fL = pygame.font.SysFont('Arial', 24, bold=True)
    fS = pygame.font.SysFont('Arial', 16)
    fBold = pygame.font.SysFont('Arial', 17, bold=True)

    t = fL.render("SO SANH: BFS vs DFS vs DIJKSTRA", True, MAU_DO)
    man_hinh.blit(t, t.get_rect(center=(W//2, y+40)))

    cot_x = [x+30, x+220, x+440, x+660]
    tieu_de = ["Tieu Chi", "BFS", "DFS (Stack)", "Dijkstra"]
    mau_sac = [MAU_DEN, MAU_XANH_DUONG, MAU_TIM, MAU_XANH_LA]

    for i, txt in enumerate(tieu_de):
        man_hinh.blit(fBold.render(txt, True, mau_sac[i]), (cot_x[i], y+90))

    pygame.draw.line(man_hinh, MAU_XAM, (x+20, y+120), (x+w-20, y+120), 2)

    cac_dong = [
        ("Nguyen ly", "Queue (FIFO)", "Stack (LIFO)", "Min-Heap"),
        ("Do phuc tap", "O(V + E)", "O(V + E)", "O((V+E)logV)"),
        ("So buoc chay", str(kq_bfs['buoc']), str(
            kq_dfs['buoc']), str(kq_dijk['buoc'])),
        ("Tong Chi phi", str(kq_bfs['chi_phi']), str(
            kq_dfs['chi_phi']), str(kq_dijk['chi_phi'])),
        ("So dinh di qua", str(len(kq_bfs['duong_di'].split('->')) if '->' in kq_bfs['duong_di'] else 0),
         str(len(kq_dfs['duong_di'].split('->'))
             if '->' in kq_dfs['duong_di'] else 0),
         str(len(kq_dijk['duong_di'].split('->')) if '->' in kq_dijk['duong_di'] else 0))
    ]

    cy = y+140
    for dong in cac_dong:
        for i, gia_tri in enumerate(dong):
            man_hinh.blit(fS.render(gia_tri, True, MAU_DEN), (cot_x[i], cy))
        cy += 40

    pygame.draw.line(man_hinh, MAU_XAM, (x+20, cy+10), (x+w-20, cy+10), 1)
    cy += 20

    # --- PHAN HIEN THI DUONG DI (TU DONG XUONG DONG) ---
    chieu_rong_chu = w - 60

    txt_bfs = f"BFS: {kq_bfs['duong_di']}"
    cac_dong_bfs = cat_dong_van_ban(txt_bfs, fS, chieu_rong_chu)
    for line in cac_dong_bfs:
        man_hinh.blit(fS.render(line, True, MAU_XANH_DUONG), (x+30, cy))
        cy += 22
    cy += 10

    txt_dfs = f"DFS: {kq_dfs['duong_di']}"
    cac_dong_dfs = cat_dong_van_ban(txt_dfs, fS, chieu_rong_chu)
    for line in cac_dong_dfs:
        man_hinh.blit(fS.render(line, True, MAU_TIM), (x+30, cy))
        cy += 22
    cy += 10

    txt_dijk = f"Dijkstra: {kq_dijk['duong_di']}"
    cac_dong_dijk = cat_dong_van_ban(txt_dijk, fS, chieu_rong_chu)
    for line in cac_dong_dijk:
        man_hinh.blit(fS.render(line, True, MAU_XANH_LA), (x+30, cy))
        cy += 22

    nut_dong = pygame.Rect(x+(w-100)//2, y+h-60, 100, 40)
    pygame.draw.rect(man_hinh, MAU_DO, nut_dong, border_radius=8)
    pygame.draw.rect(man_hinh, MAU_DEN, nut_dong, 2, border_radius=8)
    txt = pygame.font.SysFont('Arial', 18, bold=True).render(
        "Dong", True, MAU_TRANG)
    man_hinh.blit(txt, txt.get_rect(center=nut_dong.center))

    return nut_dong
