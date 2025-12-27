# main.py
import pygame
import sys
import math
import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
from settings import *
from models import *
from ui import NutBam, ve_toan_bo_do_thi, ve_bang_ket_qua, hien_cua_so_so_sanh, HopNhapLieu
from algorithms import chay_bfs, chay_dijkstra, chay_dfs, lay_ket_qua_duong_di

# --- Logic tao bao cao ---

def chay_thong_ke(danh_sach_nut):
    # BFS
    for n in danh_sach_nut: n.dat_lai_trang_thai()
    bo_sinh = chay_bfs(danh_sach_nut[0])
    buoc1 = 0
    try:
        while True: next(bo_sinh); buoc1 += 1
    except StopIteration: pass
    cp1, duong1 = lay_ket_qua_duong_di(danh_sach_nut)
    
    # DFS
    for n in danh_sach_nut: n.dat_lai_trang_thai()
    bo_sinh = chay_dfs(danh_sach_nut[0])
    buoc2 = 0
    try:
        while True: next(bo_sinh); buoc2 += 1
    except StopIteration: pass
    cp2, duong2 = lay_ket_qua_duong_di(danh_sach_nut)
    
    # Dijkstra
    for n in danh_sach_nut: n.dat_lai_trang_thai()
    bo_sinh = chay_dijkstra(danh_sach_nut[0])
    buoc3 = 0
    try:
        while True: next(bo_sinh); buoc3 += 1
    except StopIteration: pass
    cp3, duong3 = lay_ket_qua_duong_di(danh_sach_nut)
    
    return buoc1, cp1, duong1, buoc2, cp2, duong2, buoc3, cp3, duong3

def tao_noi_dung_bao_cao(danh_sach_nut):
    du_lieu = [str(len(danh_sach_nut))]
    for u in danh_sach_nut:
        for v, w in u.danh_sach_ke: du_lieu.append(f"{u.ma_so} {v.ma_so} {w}")
    du_lieu_tho = "\n".join(du_lieu)
    
    txt = "BAO CAO KET QUA\n"
    txt += f"Thoi gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    txt += "-"*50 + "\n\n"
    
    def dinh_dang(ten, s, c, p):
        return f"[{ten}]\n  - So buoc: {s} | Chi phi: {c} | Duong di: {p}\n"

    txt += "--- 1. CO HUONG ---\n"
    g1 = phan_tich_van_ban(du_lieu_tho)
    if g1:
        s1, c1, p1, s2, c2, p2, s3, c3, p3 = chay_thong_ke(g1)
        txt += dinh_dang("BFS", s1, c1, p1) + dinh_dang("DFS", s2, c2, p2) + dinh_dang("Dijkstra", s3, c3, p3)
        
    txt += "\n--- 2. VO HUONG ---\n"
    g2 = phan_tich_van_ban(du_lieu_tho)
    if g2:
        chuyen_thanh_vo_huong(g2)
        s1, c1, p1, s2, c2, p2, s3, c3, p3 = chay_thong_ke(g2)
        txt += dinh_dang("BFS", s1, c1, p1) + dinh_dang("DFS", s2, c2, p2) + dinh_dang("Dijkstra", s3, c3, p3)

    return txt

def so_sanh_thuat_toan(danh_sach_nut):
    # BFS
    for n in danh_sach_nut: n.dat_lai_trang_thai()
    bo_sinh = chay_bfs(danh_sach_nut[0])
    buoc1 = 0
    try: 
        while True: next(bo_sinh); buoc1 += 1
    except StopIteration: pass
    cp1, duong1 = lay_ket_qua_duong_di(danh_sach_nut)
    
    # DFS
    for n in danh_sach_nut: n.dat_lai_trang_thai()
    bo_sinh = chay_dfs(danh_sach_nut[0])
    buoc2 = 0
    try: 
        while True: next(bo_sinh); buoc2 += 1
    except StopIteration: pass
    cp2, duong2 = lay_ket_qua_duong_di(danh_sach_nut)
    
    # Dijkstra
    for n in danh_sach_nut: n.dat_lai_trang_thai()
    bo_sinh = chay_dijkstra(danh_sach_nut[0])
    buoc3 = 0
    try: 
        while True: next(bo_sinh); buoc3 += 1
    except StopIteration: pass
    cp3, duong3 = lay_ket_qua_duong_di(danh_sach_nut)
    
    return {'buoc': buoc1, 'chi_phi': cp1, 'duong_di': duong1}, \
           {'buoc': buoc2, 'chi_phi': cp2, 'duong_di': duong2}, \
           {'buoc': buoc3, 'chi_phi': cp3, 'duong_di': duong3}

def main():
    cua_so_an = tk.Tk(); cua_so_an.withdraw()
    pygame.init()
    man_hinh = pygame.display.set_mode((CHIEU_RONG_CUA_SO, CHIEU_CAO_CUA_SO), pygame.RESIZABLE)
    pygame.display.set_caption("Do an: Mo phong BFS - DFS - Dijkstra")
    dong_ho = pygame.time.Clock()
    
    font = pygame.font.SysFont('Arial', 16, bold=True)
    font_nhap = pygame.font.SysFont('Consolas', 14)

    trang_thai = CHE_DO_CHINH
    co_huong = True 
    danh_sach_nut = tao_do_thi_ngau_nhien(co_huong=co_huong)
    # --- BIEN LUU TRU DE KHOI PHUC ---
    # Khi chuyen sang Vo Huong, ta se luu lai ban Co Huong vao day
    # De khi chuyen lai Co Huong, ta lay ra dung, khong bi doi chieu
    du_lieu_du_phong = None 
    
    # Tao cac nut bam KHONG DAU
    # Index: 0=BFS, 1=DFS, 2=Dijkstra, 3=SoSanh, 4=Kieu, 5=LamMoi, 6=NhapTay, 7=XuatBC, 8=ChonFile
    ds_nut_bam = [
        NutBam(30, 580, 70, 40, "BFS", MAU_XANH_DUONG),
        NutBam(110, 580, 70, 40, "DFS", MAU_TIM),
        NutBam(190, 580, 100, 40, "Dijkstra", MAU_XANH_LA),
        NutBam(300, 580, 90, 40, "So Sanh", (100, 100, 100)),
        NutBam(400, 580, 130, 40, "Kieu: Co Huong", MAU_DEN),
        NutBam(540, 580, 90, 40, "Lam Moi", MAU_DO),
        NutBam(30, 630, 100, 40, "Nhap Tay", MAU_VANG),
        NutBam(140, 630, 120, 40, "Xuat Bao Cao", (0, 128, 128)),
        NutBam(270, 630, 120, 40, "Chon File BC", (128, 0, 128))
    ]

    bo_sinh_du_lieu = None; lich_su_chay = []; cuon_bang = 0; duong_di_ket_qua = []
    ti_le_zoom = 1.0; lech_x = 0; lech_y = 0; nut_dang_keo = None; dang_di_chuyen_man_hinh = False; chuot_cu = (0, 0)
    hien_bang_so_sanh = False
    kq_bfs = kq_dfs = kq_dijk = None

    hop_nhap = HopNhapLieu(50, 80, 400, 500, font_nhap)
    hop_nhap.dat_noi_dung("5\n0 1 5\n1 2 3\n2 3 1\n3 4 7\n4 0 2")
    
    # KHONG DAU
    nut_nap = NutBam(50, 600, 120, 40, "NAP DO THI", MAU_XANH_LA)
    nut_random = NutBam(185, 600, 130, 40, "NGAU NHIEN", MAU_TIM)
    nut_quay_lai = NutBam(330, 600, 120, 40, "QUAY LAI", MAU_DO)
    
    ds_nut_lich_su = []; cuon_lich_su = 0
    
    def cap_nhat_giao_dien_lich_su():
        nonlocal ds_nut_lich_su
        du_lieu_tho = lay_lich_su_nhap()
        ds_nut_lich_su = []
        y = 80
        for i, t in enumerate(du_lieu_tho):
            nhan = f"Input {i+1}: " + (t.split('\n')[0] if t else "Rong")
            b = NutBam(500, y + i * 50, 300, 40, nhan, MAU_XAM)
            b.gia_tri_an = t 
            ds_nut_lich_su.append(b)
    cap_nhat_giao_dien_lich_su()
    
    def ve_man_hinh_chinh(nut_hover=None):
        man_hinh.set_clip(None); man_hinh.fill(MAU_TRANG); W, H = man_hinh.get_size()
        
        for i, b in enumerate(ds_nut_bam): 
            if i < 6: b.hinh_chu_nhat.y = H - 110 
            else: b.hinh_chu_nhat.y = H - 60      
        
        ve_toan_bo_do_thi(man_hinh, danh_sach_nut, font, co_huong, duong_di_ket_qua, nut_hover, ti_le_zoom, (lech_x, lech_y))
        
        pygame.draw.rect(man_hinh, (240,240,240), (0, H-120, 650, 120), border_top_right_radius=20) 
        for b in ds_nut_bam: b.ve(man_hinh)
        
        lbl = f"Do thi {'CO HUONG' if co_huong else 'VO HUONG'} ({len(danh_sach_nut)} dinh)"
        man_hinh.blit(font.render(lbl, True, MAU_DEN), (30, H - 140))
        
        chieu_cao_bang = ve_bang_ket_qua(man_hinh, lich_su_chay, cuon_bang)
        if hien_bang_so_sanh and kq_bfs: hien_cua_so_so_sanh(man_hinh, kq_bfs, kq_dfs, kq_dijk)
        
        pygame.display.flip()
        return chieu_cao_bang

    def ve_man_hinh_nhap():
        man_hinh.fill(MAU_NEN_NHAP)
        man_hinh.blit(font.render("NHAP DU LIEU (So Dinh [enter] U V W [enter]...)", True, MAU_DEN), (50, 40))
        hop_nhap.ve(man_hinh)
        nut_nap.ve(man_hinh); nut_random.ve(man_hinh); nut_quay_lai.ve(man_hinh)
        man_hinh.blit(font.render("LICH SU (Click chon)", True, MAU_XANH_DUONG), (500, 40))
        W, H = man_hinh.get_size()
        man_hinh.set_clip(pygame.Rect(490, 70, 350, H - 100))
        for b in ds_nut_lich_su:
            oy = b.hinh_chu_nhat.y; b.hinh_chu_nhat.y += cuon_lich_su
            b.ve(man_hinh); b.hinh_chu_nhat.y = oy
        man_hinh.set_clip(None)
        pygame.draw.line(man_hinh, MAU_VIEN_BANG, (480, 50), (480, H-50), 2)
        pygame.display.flip()

    dang_chay = True
    while dang_chay:
        cac_su_kien = pygame.event.get()
        for e in cac_su_kien:
            if e.type == pygame.QUIT: dang_chay = False
            
            if trang_thai == CHE_DO_NHAP_LIEU:
                hop_nhap.xu_ly_su_kien(e)
                if e.type == pygame.MOUSEWHEEL and pygame.mouse.get_pos()[0] > 480:
                    cuon_lich_su = min(0, cuon_lich_su + e.y * 20)
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if nut_quay_lai.duoc_nhan(e.pos): trang_thai = CHE_DO_CHINH
                    elif nut_nap.duoc_nhan(e.pos):
                        txt = hop_nhap.lay_noi_dung()
                        g = phan_tich_van_ban(txt)
                        if g:
                            danh_sach_nut = g; luu_lich_su_nhap(txt); cap_nhat_giao_dien_lich_su()
                            bo_sinh_du_lieu = None; lich_su_chay = []; duong_di_ket_qua = []
                            ti_le_zoom = 1.0; lech_x = 0; lech_y = 0; trang_thai = CHE_DO_CHINH
                            du_lieu_du_phong = None # Reset backup
                        else: print("Loi dinh dang!")
                    elif nut_random.duoc_nhan(e.pos): hop_nhap.dat_noi_dung(tao_du_lieu_ngau_nhien_dang_chu())
                    else:
                        for b in ds_nut_lich_su:
                            kiem_tra = b.hinh_chu_nhat.copy(); kiem_tra.y += cuon_lich_su
                            if kiem_tra.collidepoint(e.pos): hop_nhap.dat_noi_dung(b.gia_tri_an); break

            elif trang_thai == CHE_DO_CHINH:
                mx, my = pygame.mouse.get_pos()
                wx = (mx - lech_x) / ti_le_zoom
                wy = (my - lech_y) / ti_le_zoom
                
                nut_hover = None
                if nut_dang_keo: nut_hover = nut_dang_keo
                else:
                    for n in danh_sach_nut:
                        if math.hypot(wx - n.x, wy - n.y) <= BAN_KINH_NUT: nut_hover = n; break

                if hien_bang_so_sanh:
                    if e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.KEYDOWN:
                        hien_bang_so_sanh = False; 
                        for n in danh_sach_nut: n.dat_lai_trang_thai() 
                        duong_di_ket_qua = []
                    continue 

                if e.type == pygame.VIDEORESIZE: man_hinh = pygame.display.set_mode((e.w, e.h), pygame.RESIZABLE)
                
                if e.type == pygame.MOUSEWHEEL:
                    if mx < man_hinh.get_size()[0] - 450:
                        s = 1.1 if e.y > 0 else 0.9
                        ti_le_zoom = max(0.2, min(5.0, ti_le_zoom * s))
                        lech_x = mx - wx * ti_le_zoom; lech_y = my - wy * ti_le_zoom
                    else: cuon_bang += e.y * 20

                if e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 1: 
                        da_click_nut = False
                        # FIX: DUNG INDEX DE CHECK NUT CHO CHAC CHAN
                        for i, b in enumerate(ds_nut_bam):
                            if b.duoc_nhan(e.pos):
                                da_click_nut = True
                                
                                # 5: Lam Moi
                                if i == 5: 
                                    danh_sach_nut = tao_do_thi_ngau_nhien(co_huong=co_huong)
                                    bo_sinh_du_lieu = None; lich_su_chay = []; cuon_bang = 0; duong_di_ket_qua = []
                                    ti_le_zoom = 1.0; lech_x = 0; lech_y = 0; du_lieu_du_phong = None
                                
                                # 4: Kieu (Co Huong <-> Vo Huong) - FIX LOI DOI CHIEU MUI TEN
                                elif i == 4:
                                    co_huong = not co_huong
                                    if not co_huong: # Chuyen sang Vo Huong
                                        # Luu lai trang thai Co Huong hien tai
                                        du_lieu_du_phong = sao_chep_do_thi(danh_sach_nut)
                                        danh_sach_nut = chuyen_thanh_vo_huong(danh_sach_nut)
                                        ds_nut_bam[4].noi_dung = "Kieu: Vo Huong"
                                    else: # Chuyen sang Co Huong
                                        # Khoi phuc lai trang thai cu (neu co)
                                        if du_lieu_du_phong:
                                            danh_sach_nut = khoi_phuc_do_thi(du_lieu_du_phong, danh_sach_nut)
                                        else:
                                            danh_sach_nut = chuyen_thanh_co_huong(danh_sach_nut)
                                        ds_nut_bam[4].noi_dung = "Kieu: Co Huong"
                                    
                                    for n in danh_sach_nut: n.dat_lai_trang_thai()
                                    bo_sinh_du_lieu = None; lich_su_chay = []; duong_di_ket_qua = []
                                
                                # 6: Nhap Tay
                                elif i == 6:
                                    trang_thai = CHE_DO_NHAP_LIEU; cap_nhat_giao_dien_lich_su()
                                
                                # 3: So Sanh
                                elif i == 3:
                                    kq_bfs, kq_dfs, kq_dijk = so_sanh_thuat_toan(danh_sach_nut)
                                    hien_bang_so_sanh = True; bo_sinh_du_lieu = None; duong_di_ket_qua = []
                                
                                # 7: Xuat Bao Cao
                                elif i == 7:
                                    thu_muc = "bao_cao"
                                    if not os.path.exists(thu_muc): os.makedirs(thu_muc)
                                    t = datetime.now().strftime("%Y%m%d_%H%M%S")
                                    ten_file = f"{thu_muc}/BaoCao_{t}.txt"
                                    noi_dung = tao_noi_dung_bao_cao(danh_sach_nut)
                                    if luu_file_day_du(ten_file, danh_sach_nut, co_huong, noi_dung):
                                        lich_su_chay.append(f">> DA LUU: {ten_file}")
                                        try: os.startfile(thu_muc)
                                        except: pass
                                    else: lich_su_chay.append(">> LOI LUU FILE!")
                                    cuon_bang = -99999

                                # 8: Chon File BC
                                elif i == 8:
                                    fd = "bao_cao"
                                    if not os.path.exists(fd): os.makedirs(fd)
                                    duong_dan = filedialog.askopenfilename(initialdir=fd, filetypes=(("Text", "*.txt"), ("All", "*.*")))
                                    if duong_dan:
                                        gn, mode = doc_file_day_du(duong_dan)
                                        if gn:
                                            danh_sach_nut = gn; co_huong = mode
                                            ds_nut_bam[4].noi_dung = "Kieu: Co Huong" if co_huong else "Kieu: Vo Huong"
                                            bo_sinh_du_lieu = None; lich_su_chay = []; duong_di_ket_qua = []
                                            du_lieu_du_phong = None # Reset backup
                                            lich_su_chay.append(f">> DA NAP: {os.path.basename(duong_dan)}")
                                        else: lich_su_chay.append(">> FILE LOI!")
                                    else: lich_su_chay.append(">> DA HUY")
                                    cuon_bang = -99999

                                # 0, 1, 2: Cac Thuat Toan
                                elif bo_sinh_du_lieu is None:
                                    for n in danh_sach_nut: n.dat_lai_trang_thai() 
                                    duong_di_ket_qua = []
                                    if i == 0: bo_sinh_du_lieu = chay_bfs(danh_sach_nut[0])
                                    elif i == 1: bo_sinh_du_lieu = chay_dfs(danh_sach_nut[0])
                                    elif i == 2: bo_sinh_du_lieu = chay_dijkstra(danh_sach_nut[0])
                                break
                        if not da_click_nut and nut_hover: nut_dang_keo = nut_hover
                    elif e.button == 3: dang_di_chuyen_man_hinh = True; chuot_cu = e.pos

                if e.type == pygame.MOUSEBUTTONUP:
                    if e.button == 1: nut_dang_keo = None
                    if e.button == 3: dang_di_chuyen_man_hinh = False

                if e.type == pygame.MOUSEMOTION:
                    if nut_dang_keo:
                        nut_dang_keo.x = (e.pos[0] - lech_x) / ti_le_zoom
                        nut_dang_keo.y = (e.pos[1] - lech_y) / ti_le_zoom
                    if dang_di_chuyen_man_hinh:
                        dx = e.pos[0] - chuot_cu[0]; dy = e.pos[1] - chuot_cu[1]
                        lech_x += dx; lech_y += dy; chuot_cu = e.pos

                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE and bo_sinh_du_lieu:
                    try:
                        hang = next(bo_sinh_du_lieu); lich_su_chay.append(hang); cuon_bang = -99999
                    except StopIteration:
                        bo_sinh_du_lieu = None; dich = danh_sach_nut[-1]
                        c, p = lay_ket_qua_duong_di(danh_sach_nut)
                        duong_di_ket_qua = []
                        tam = dich
                        while tam: duong_di_ket_qua.append(tam); tam = tam.nut_cha
                        lich_su_chay.append(f"KET QUA: {p} (Chi phi: {c})"); cuon_bang = -99999

        if trang_thai == CHE_DO_CHINH:
            cao_bang = ve_man_hinh_chinh(nut_hover if trang_thai == CHE_DO_CHINH else None)
            _, ch = man_hinh.get_size()
            if cao_bang < (ch - 40): cuon_bang = 0
            elif cuon_bang < -(cao_bang - (ch-40) + 20): cuon_bang = -(cao_bang - (ch-40) + 20)
        elif trang_thai == CHE_DO_NHAP_LIEU:
            ve_man_hinh_nhap()

        dong_ho.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()