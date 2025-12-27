# algorithms.py
import heapq
from collections import deque
from settings import *

# Ham in ra danh sach ID rut gon (Co dau cach de xuong dong)
def in_danh_sach(danh_sach_nut):
    return "[" + ", ".join([str(n.ma_so) for n in danh_sach_nut]) + "]"

# Truy vet duong di tu dich ve nguon
def lay_ket_qua_duong_di(danh_sach_nut):
    dich = danh_sach_nut[-1]
    chi_phi = "Khong co"
    if dich.khoang_cach != float('inf'): chi_phi = dich.khoang_cach
    
    chuoi_duong_di = ""
    if dich.nut_cha is None and dich.ma_so != 0:
        chuoi_duong_di = "Ko tim thay duong"
    else:
        duong_di = []
        hien_tai = dich
        while hien_tai:
            duong_di.append(str(hien_tai.ma_so))
            hien_tai = hien_tai.nut_cha
        chuoi_duong_di = " -> ".join(duong_di[::-1])
        
    return chi_phi, chuoi_duong_di

# 1. BFS
def chay_bfs(nut_bat_dau):
    hang_doi = deque([nut_bat_dau])
    # Dung set de check nhanh O(1)
    tap_mo = {nut_bat_dau.ma_so} 
    tap_dong = set()
    thu_tu_duyet = [] 
    nut_bat_dau.mau_sac = MAU_VANG
    nut_bat_dau.khoang_cach = 0 
    buoc = 0
    yield (buoc, "-", "-", f"Q: [{nut_bat_dau.ma_so}]", "{}", "Khoi tao BFS")
    while hang_doi:
        buoc += 1
        nut_hien_tai = hang_doi.popleft() 
        # Roi Tap Mo -> Vao Tap Dong
        if nut_hien_tai.ma_so in tap_mo: tap_mo.remove(nut_hien_tai.ma_so)
        tap_dong.add(nut_hien_tai.ma_so)
        if nut_hien_tai not in thu_tu_duyet:
            thu_tu_duyet.append(nut_hien_tai)
        nut_hien_tai.mau_sac = MAU_XANH_DUONG
        danh_sach_them_moi = []
        for ke, trong_so in nut_hien_tai.danh_sach_ke:
            # Check: Chua co trong Open va chua co trong Close
            if ke.ma_so not in tap_mo and ke.ma_so not in tap_dong:
                ke.da_tham = True
                ke.nut_cha = nut_hien_tai
                ke.mau_sac = MAU_VANG
                ke.khoang_cach = nut_hien_tai.khoang_cach + trong_so 
                hang_doi.append(ke)
                tap_mo.add(ke.ma_so) 
                danh_sach_them_moi.append(ke)
        # Format ky co dau cach de UI tu cat dong
        chuoi_hang_doi = "Q: [" + ", ".join([str(x.ma_so) for x in hang_doi]) + "]"
        chuoi_tap_dong = in_danh_sach(thu_tu_duyet)
        thong_tin = f"Lay {nut_hien_tai.ma_so}, them {in_danh_sach(danh_sach_them_moi)}"
        yield (buoc, str(nut_hien_tai.ma_so), in_danh_sach(danh_sach_them_moi), chuoi_hang_doi, chuoi_tap_dong, thong_tin)
        nut_hien_tai.mau_sac = MAU_DEN

# 2. DFS
def chay_dfs(nut_bat_dau):
    ngan_xep = [nut_bat_dau] 

    tap_mo = {nut_bat_dau.ma_so}
    tap_dong = set()             
    
    thu_tu_duyet = []
    
    nut_bat_dau.khoang_cach = 0
    nut_bat_dau.nut_cha = None
    
    buoc = 0
    yield (buoc, "-", "-", f"Stack: [{nut_bat_dau.ma_so}]", "{}", "Khoi tao DFS")
    
    while ngan_xep:
        buoc += 1
        
        nut_hien_tai = ngan_xep.pop()
        
        if nut_hien_tai.ma_so in tap_dong:
            continue
            
        if nut_hien_tai.ma_so in tap_mo: tap_mo.remove(nut_hien_tai.ma_so)
        tap_dong.add(nut_hien_tai.ma_so)
        
        thu_tu_duyet.append(nut_hien_tai)
        nut_hien_tai.mau_sac = MAU_XANH_DUONG 
        
        danh_sach_them_moi = []
        # Dao nguoc de khi vao Stack, cai dau tien duoc lay ra truoc
        danh_sach_ke_dao_nguoc = list(nut_hien_tai.danh_sach_ke)
        danh_sach_ke_dao_nguoc.reverse()
        
        for ke, trong_so in danh_sach_ke_dao_nguoc:
            if ke.ma_so not in tap_mo and ke.ma_so not in tap_dong:
                ke.nut_cha = nut_hien_tai
                ke.khoang_cach = nut_hien_tai.khoang_cach + trong_so
                ke.mau_sac = MAU_VANG
                
                ngan_xep.append(ke)
                tap_mo.add(ke.ma_so) 
                danh_sach_them_moi.append(ke)
        
        # Them dau cach sau dau phay de UI cat dong
        chuoi_stack = "Stack: [" + ", ".join([str(x.ma_so) for x in ngan_xep]) + "]"
        chuoi_tap_dong = in_danh_sach(thu_tu_duyet)
        thong_tin = f"Pop {nut_hien_tai.ma_so}, Push {len(danh_sach_them_moi)} ke"
        
        yield (buoc, str(nut_hien_tai.ma_so), in_danh_sach(danh_sach_them_moi), chuoi_stack, chuoi_tap_dong, thong_tin)
        nut_hien_tai.mau_sac = MAU_DEN

# 3. Dijkstra
def chay_dijkstra(nut_bat_dau):
    nut_bat_dau.khoang_cach = 0
    nut_bat_dau.mau_sac = MAU_VANG
    nut_bat_dau.nut_cha = None
    buoc = 0
    hang_doi_uu_tien = [(0, nut_bat_dau.ma_so, nut_bat_dau)]
    tap_dong = set()
    chi_phi_tot_nhat_trong_mo = {nut_bat_dau.ma_so: 0} 
    yield (buoc, "-", "-", "Khoi tao Heap", "{}", f"d[{nut_bat_dau.ma_so}]=0")
    danh_sach_da_xu_ly = []
    while hang_doi_uu_tien:
        buoc += 1
        khoang_cach, _, nut_hien_tai = heapq.heappop(hang_doi_uu_tien)
        if nut_hien_tai.ma_so in tap_dong:
            continue
        if nut_hien_tai.ma_so in chi_phi_tot_nhat_trong_mo and khoang_cach > chi_phi_tot_nhat_trong_mo[nut_hien_tai.ma_so]:
            continue
        tap_dong.add(nut_hien_tai.ma_so)
        if nut_hien_tai.ma_so in chi_phi_tot_nhat_trong_mo: del chi_phi_tot_nhat_trong_mo[nut_hien_tai.ma_so]
        danh_sach_da_xu_ly.append(nut_hien_tai)
        nut_hien_tai.mau_sac = MAU_XANH_DUONG
        cac_cap_nhat = []
        for ke, trong_so in nut_hien_tai.danh_sach_ke:
            if ke.ma_so in tap_dong:
                continue
            khoang_cach_moi = nut_hien_tai.khoang_cach + trong_so
            can_them_vao = False
            if ke.ma_so not in chi_phi_tot_nhat_trong_mo:
                can_them_vao = True
            elif khoang_cach_moi < chi_phi_tot_nhat_trong_mo[ke.ma_so]:
                can_them_vao = True
            if can_them_vao:
                if khoang_cach_moi < ke.khoang_cach:
                    ke.khoang_cach = khoang_cach_moi
                    ke.nut_cha = nut_hien_tai
                    ke.mau_sac = MAU_VANG
                heapq.heappush(hang_doi_uu_tien, (ke.khoang_cach, ke.ma_so, ke))
                chi_phi_tot_nhat_trong_mo[ke.ma_so] = ke.khoang_cach 
                cac_cap_nhat.append(f"N{ke.ma_so}({ke.khoang_cach})")
        # Sort Heap de hien thi cho dep mat
        heap_de_hien_thi = sorted(hang_doi_uu_tien, key=lambda x: (x[0], x[1]))
        # HIEN THI TAT CA (khong cat nua)
        xem_truoc = [f"N{item[2].ma_so}:{item[0]}" for item in heap_de_hien_thi]        
        # Join co dau cach de UI cat dong
        chuoi_heap = f"Heap({len(hang_doi_uu_tien)}): [" + ", ".join(xem_truoc) + "]"
        chuoi_cap_nhat = "[" + ", ".join(cac_cap_nhat) + "]"
        chuoi_da_xu_ly = in_danh_sach(danh_sach_da_xu_ly)
        thong_tin_cha = f", p={nut_hien_tai.nut_cha.ma_so}" if nut_hien_tai.nut_cha else ""
        thong_tin = f"Chot d[{nut_hien_tai.ma_so}]={nut_hien_tai.khoang_cach}{thong_tin_cha}"
        yield (buoc, str(nut_hien_tai.ma_so), chuoi_cap_nhat, chuoi_heap, chuoi_da_xu_ly, thong_tin)
        nut_hien_tai.mau_sac = MAU_DEN