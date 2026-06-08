import flet as ft
import time

def main(page: ft.Page):
    page.title = "YKS Net & Tercih Sihirbazı"
    page.window_width = 440
    page.window_height = 760
    page.window_resizable = False
    
    page.bgcolor = "#0F172A" 
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 15

    # --- ANINDA KONTROL FONKSİYONU ---
    def sinir_kontrol(e):
        txt_field = e.control
        max_soru = txt_field.data
        if not txt_field.value: return
        val_str = txt_field.value.replace(",", ".")
        if "-" in val_str:
            txt_field.value = "0"
            page.update()
            return
        try:
            val_num = float(val_str)
            if val_num > max_soru: txt_field.value = str(max_soru)
            elif val_num < 0: txt_field.value = "0"
        except ValueError:
            txt_field.value = "0"
        page.update()

    # --- ESNEK INPUT OLUŞTURUCU ---
    def create_input(label, max_val):
        return ft.TextField(
            label=label,
            value="0",
            expand=True,
            height=45,
            text_align=ft.TextAlign.CENTER,
            text_size=13,
            color="#FFFFFF",
            cursor_color="#F59E0B",
            focused_border_color="#F59E0B",
            border_color="#334155",
            bgcolor="#1E293B",
            border_radius=10,
            keyboard_type=ft.KeyboardType.NUMBER,
            data=max_val,
            on_change=sinir_kontrol
        )

    # Giriş Alanları
    tyt_turkce = create_input("TR (40)", 40)
    tyt_sosyal = create_input("SOS (20)", 20)
    tyt_mat = create_input("MAT (40)", 40)
    tyt_fen = create_input("FEN (20)", 20)

    ayt_mat = create_input("MAT (40)", 40)
    ayt_edebiyat = create_input("EDB (24)", 24)
    ayt_tarih = create_input("TAR (10)", 10)
    ayt_cografya = create_input("COĞ (6)", 6)

    # Sonuç Elemanları
    txt_tyt_net = ft.Text(size=14, color="#94A3B8", weight=ft.FontWeight.W_500)
    txt_ayt_net = ft.Text(size=14, color="#94A3B8", weight=ft.FontWeight.W_500)
    txt_toplam_net = ft.Text(value="0.0\nNET", size=22, color="#F59E0B", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    txt_yuzde = ft.Text(size=14, color="#E2E8F0", weight=ft.FontWeight.W_600)
    txt_motivasyon = ft.Text(size=13, color="#38BDF8", italic=True, text_align=ft.TextAlign.CENTER)
    
    progress_circle = ft.ProgressRing(width=140, height=140, stroke_width=10, value=0, color="#F59E0B", bgcolor="#334155")
    
    # Kazanılan Üniversiteler Listesi İçin Kapsayıcı
    uni_list_container = ft.Column(spacing=5, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)

    def hesapla_ve_gec(e):
        input_screen.visible = False
        loading_screen.visible = True
        page.update()
        time.sleep(1.0)

        n_tyt_tr = float(tyt_turkce.value.replace(",", ".")) if tyt_turkce.value else 0.0
        n_tyt_sos = float(tyt_sosyal.value.replace(",", ".")) if tyt_sosyal.value else 0.0
        n_tyt_mat = float(tyt_mat.value.replace(",", ".")) if tyt_mat.value else 0.0
        n_tyt_fen = float(tyt_fen.value.replace(",", ".")) if tyt_fen.value else 0.0

        n_ayt_mat = float(ayt_mat.value.replace(",", ".")) if ayt_mat.value else 0.0
        n_ayt_edb = float(ayt_edebiyat.value.replace(",", ".")) if ayt_edebiyat.value else 0.0
        n_ayt_tar = float(ayt_tarih.value.replace(",", ".")) if ayt_tarih.value else 0.0
        n_ayt_cog = float(ayt_cografya.value.replace(",", ".")) if ayt_cografya.value else 0.0

        tyt_toplam = n_tyt_tr + n_tyt_sos + n_tyt_mat + n_tyt_fen
        ayt_toplam = n_ayt_mat + n_ayt_edb + n_ayt_tar + n_ayt_cog
        genel_toplam = tyt_toplam + ayt_toplam
        
        yuzde = (genel_toplam / 160)
        if yuzde > 1.0: yuzde = 1.0
        if yuzde < 0: yuzde = 0

        txt_tyt_net.value = f"🔹 TYT Toplam: {tyt_toplam:.2f} Net"
        txt_ayt_net.value = f"🔹 AYT Toplam: {ayt_toplam:.2f} Net"
        txt_toplam_net.value = f"{genel_toplam:.1f}\nNET"
        txt_yuzde.value = f"🎯 Sınav Başarı Oranı: %{yuzde*100:.1f}"
        progress_circle.value = yuzde

        # --- DİNAMİK ÜNİVERSİTE ÖNERİ MOTORU ---
        uni_list_container.controls.clear()
        
        if genel_toplam >= 130:
            txt_motivasyon.value = "🎯 Derece Kadrosu! Türkiye'nin Zirvesindesin."
            uniler = [
                ("Koç Üniversitesi", "Bilgisayar Mühendisliği (Burslu) / Tıp"),
                ("Boğaziçi Üniversitesi", "Yapay Zeka / Bilgisayar / EE Müh."),
                ("Bilkent Üniversitesi", "Endüstri / Bilgisayar Müh. (Burslu)"),
                ("ODTÜ", "Havacılık ve Uzay / Bilgisayar Müh."),
                ("Hacettepe Üniversitesi", "Tıp Fakültesi (İngilizce)")
            ]
        elif genel_toplam >= 100:
            txt_motivasyon.value = "🚀 Elit Kadro! Çok ciddi bir başarı."
            uniler = [
                ("İTÜ", "Yapay Zeka / Elektronik Haberleşme"),
                ("Yıldız Teknik Üni.", "Bilgisayar Mühendisliği / Yazılım"),
                ("Ankara Üniversitesi", "Tıp Fakültesi / Hukuk"),
                ("Marmara Üniversitesi", "Endüstri Mühendisliği (İngilizce)"),
                ("Ege Üniversitesi", "Bilgisayar Müh. / Diş Hekimliği")
            ]
        elif genel_toplam >= 60:
            txt_motivasyon.value = "📈 Harika Temel! Eksikleri kapatıp uçuşa geç."
            uniler = [
                ("Gazi Üniversitesi", "Makine / İnşaat Mühendisliği"),
                ("Dokuz Eylül Üni.", "Hukuk / Mimarlık / İşletme"),
                ("Akdeniz Üniversitesi", "Yazılım Müh. / Psikoloji"),
                ("Anadolu Üniversitesi", "Eczacılık / İletişim Fakültesi"),
                ("Kocaeli Üniversitesi", "Mekatronik Müh. / Yönetim Bilişim")
            ]
        else:
            txt_motivasyon.value = "📚 Çalışmaya Devam! Her büyük başarı sabırla başlar."
            uniler = [
                ("Yerel Devlet Üni.", "Mühendislik ve Mimarlık Alanları"),
                ("Köklü Vakıf Üni.", "Çeşitli Lisans Bölümleri (%50 İndirimli)"),
                ("Bölgesel Başarı", "Eğitim Fakülteleri / İİBF Bölümleri")
            ]

        # Üniversiteleri Şık Listeler Halinde Ekrana Basıyoruz
        for uni, bolum in uniler:
            uni_list_container.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.icons.SCHOOL, color="#F59E0B", size=18),
                        ft.Column([
                            ft.Text(uni, size=13, color="#FFFFFF", weight=ft.FontWeight.BOLD),
                            ft.Text(bolum, size=11, color="#94A3B8")
                        ], spacing=2, expand=True)
                    ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor="#1E293B",
                    padding=10,
                    border_radius=8,
                    border=ft.border.all(1, "#334155")
                )
            )

        loading_screen.visible = False
        result_screen.visible = True
        page.update()

    def _back(e):
        result_screen.visible = False
        input_screen.visible = True
        page.update()

    # --- 1. EKRAN: GİRİŞ PANELİ ---
    input_screen = ft.Container(
        content=ft.Column([
            ft.Text("YKS ANALİZ MERKEZİ", size=22, weight=ft.FontWeight.BOLD, color="#F59E0B"),
            ft.Text("Performans & Tercih Robotu", size=12, color="#64748B"),
            ft.Container(height=10),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("TYT OTURUMU (120 SORU)", size=12, color="#F59E0B", weight=ft.FontWeight.BOLD),
                    ft.Row([tyt_turkce, tyt_sosyal, tyt_mat, tyt_fen], alignment=ft.MainAxisAlignment.CENTER, spacing=6),
                ], spacing=8),
                bgcolor="#1E293B", padding=12, border_radius=12, border=ft.border.all(1, "#334155")
            ),
            
            ft.Container(height=5),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("AYT OTURUMU (80 SORU)", size=12, color="#38BDF8", weight=ft.FontWeight.BOLD),
                    ft.Row([ayt_mat, ayt_edebiyat, ayt_tarih, ayt_cografya], alignment=ft.MainAxisAlignment.CENTER, spacing=6),
                ], spacing=8),
                bgcolor="#1E293B", padding=12, border_radius=12, border=ft.border.all(1, "#334155")
            ),
            
            ft.Container(height=15),
            
            ft.ElevatedButton(
                "ANALİZ ET & TERCİH YAP ✨", 
                on_click=hesapla_ve_gec, 
                style=ft.ButtonStyle(color="#0F172A", bgcolor="#F59E0B", padding=18, shape=ft.RoundedRectangleBorder(radius=10)),
                width=220
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor="#111827", padding=20, border_radius=20, width=400, shadow=ft.BoxShadow(blur_radius=15, color="#000000")
    )

    # --- 2. EKRAN: YÜKLENİYOR ---
    loading_screen = ft.Container(
        content=ft.Column([
            ft.ProgressRing(width=50, height=50, color="#F59E0B", stroke_width=4),
            ft.Container(height=10),
            ft.Text("YÖK Atlas verileri analiz ediliyor...", color="#94A3B8", size=13, italic=True)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER),
        visible=False
    )

    # --- 3. EKRAN: PREMİUM SONUÇ VE ÜNİVERSİTE LİSTESİ ---
    result_screen = ft.Container(
        content=ft.Column([
            ft.Text("PERFORMANS VE TERCİH RAPORU", size=18, weight=ft.FontWeight.BOLD, color="#F59E0B"),
            ft.Divider(color="#334155", height=15),
            
            # Üst Kısım: Skor Çemberi ve Kısa Bilgiler
            ft.Row([
                ft.Container(
                    content=ft.Stack([
                        progress_circle,
                        ft.Container(content=txt_toplam_net, alignment=ft.alignment.center, width=140, height=140)
                    ], alignment=ft.alignment.center),
                    width=140, height=140
                ),
                ft.Column([
                    txt_tyt_net,
                    txt_ayt_net,
                    txt_yuzde,
                ], spacing=5, alignment=ft.MainAxisAlignment.CENTER)
            ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            
            ft.Container(height=5),
            txt_motivasyon,
            ft.Divider(color="#334155", height=15),
            
            # Alt Kısım: Olası Hedef Üniversiteler Başlığı ve Listesi
            ft.Text("🎯 HEDEFLEYEBİLECEĞİN POTANSİYEL ÜNİVERSİTELER", size=11, color="#64748B", weight=ft.FontWeight.BOLD),
            
            # Üniversite Kartlarının Dizildiği Alan
            uni_list_container,
            
            ft.Container(height=5),
            ft.TextButton("← Paneli Temizle", on_click=_back, style=ft.ButtonStyle(color="#F59E0B"))
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor="#111827", padding=20, border_radius=20, visible=False, width=400, shadow=ft.BoxShadow(blur_radius=15, color="#000000")
    )

    page.add(input_screen, loading_screen, result_screen)

ft.app(target=main)