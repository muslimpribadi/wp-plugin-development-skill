# Keterampilan Pengembangan Plugin WordPress

Keterampilan AI agent ahli untuk membuat plugin WordPress yang aman dan terstruktur dengan baik, mengikuti standar WP.org.

## Ikhtisar

> 🔗 **Baru mengenal AI Agent Skills?** Jika Anda belum familiar dengan cara kerja file `SKILL.md`, bagaimana agent menemukan dan memuatnya, atau ingin mempelajari lebih lanjut tentang membangun skill Anda sendiri — mulailah dari **[agentskills.io/home](https://agentskills.io/home)**. Ini adalah pusat informasi untuk memahami ekosistem skill, mulai dari instalasi hingga kustomisasi lanjutan.

Paket keterampilan ini menyediakan semua yang diperlukan untuk mengembangkan plugin WordPress siap produksi — mulai dari scaffolding dan daftar pemeriksaan keamanan hingga pola lanjutan seperti REST API, custom post types, dan penjadwalan cron. Dirancang untuk AI agent tetapi juga dapat digunakan sebagai panduan referensi bagi pengembang.

> **Sumber:** Keterampilan ini diturunkan dan dioptimalkan dari [Panduan Plugin Resmi WordPress.org](https://developer.wordpress.org/plugins/) (Terakhir diperbarui 14 Desember 2023). Konten telah disusun ulang untuk konsumsi AI agent dengan discovery bertahap, daftar pemeriksaan yang dapat ditindaklanjuti, dan pola validasi otomatis.

## Memulai Cepat

1. **Tinjau `SKILL.md`** — Ini adalah file instruksi utama yang memandu pembuatan plugin langkah demi langkah.
2. **Mulai dari skeleton** — Salin `assets/plugin-skeleton/` dan ganti nama sesuai slug plugin Anda.
3. **Jalankan validator keamanan** — Gunakan `scripts/verify_wp_plugin.py` untuk memindai kode yang dihasilkan terhadap kerentanan umum.

## Struktur

```
wp-plugin-development-skill/
├── SKILL.md                          # Definisi & instruksi skill utama
├── assets/
│   └── plugin-skeleton/              # Template plugin kerja
│       ├── my-plugin.php             # File utama dengan scaffolding lengkap
│       ├── uninstall.php             # Pembersihan saat penghapusan
│       └── README.md                 # Panduan penggunaan skeleton
├── references/                       # Panduan topik lanjutan (19 subdirektori)
│   ├── custom-post-types/            # Pola registrasi CPT
│   ├── taxonomies/                   # Taksonomi kustom
│   ├── rest-api/                     # Pembuatan endpoint REST
│   ├── cron/                         # Pola penjadwalan tugas
│   ├── internationalization/         # Terjemahan & i18n
│   ├── http-api/                     # Eksternal HTTP requests
│   ├── database/                     # $wpdb, $dbDelta, kueri
│   ├── users/                        # Peran, kapabilitas
│   ├── javascript/                   # Pemuatan aset
│   ├── privacy/                      # Hook privasi/ekspor
│   ├── metadata/                     # readme.txt & persiapan WP.org
│   ├── plugin-security/              # Sanitasi, nonce, pelarian
│   ├── admin-menus/                  # Pembuatan halaman admin
│   ├── block-editor/                 # Blok kustom & editor
│   ├── hooks/                        # Pola action/filter
│   ├── settings/                     # Pola Settings API
│   └── ...                           # (dan lainnya)
├── scripts/
│   └── verify_wp_plugin.py           # Pemindai keamanan otomatis
└── .gitignore
```

## Apa yang Dicakup

### Aspek Dasar (Setiap Plugin)
- Struktur plugin & konvensi penamaan
- Header & metadata plugin WP
- Pola hook (aktivasi, deaktivasi, init)
- Daftar pemeriksaan keamanan dengan loop validasi
- Pembuatan menu admin
- Implementasi Settings API
- Pengembangan shortcode

### Pola Modern PHP 8.2+ (Diterapkan)
- **Sintaks array pendek** — `[]` bukan `array()`
- **Parameter bertipe** — Petunjuk tipe pada semua parameter fungsi
- **Deklarasi tipe pengembalian** — `: void`, `: string`, `: array`, dll.
- **Mode tipe ketat** — `declare(strict_types=1)` disarankan
- **Ekspresi match** — Di mana sesuai untuk kondisional yang lebih bersih
- **Argumen bernama** — Untuk keterbacaan yang lebih baik dalam panggilan fungsi kompleks

### Topik Lanjutan (Sesuai Kebutuhan)
- Custom post types & taksonomi
- Endpoint REST API
- Penjadwalan cron
- Internasionalisasi (i18n)
- Integrasi HTTP API
- Tabel database kustom
- Peran & kapabilitas pengguna
- Pemuatan JavaScript/CSS
- Kepatuhan privasi
- Persiapan submit WP.org

## Fitur Keamanan

Keterampilan ini menerapkan pendekatan keamanan-first:

- **Daftar pemeriksaan non-negosiable** — Sanitasi, pelarian (escaping), nonce, cek kapabilitas
- **Loop validasi** — Prosedur self-check sebelum pengiriman kode
- **Bagian Gotchas** — Jebakan umum WordPress yang perlu dihindari
- **Pemindai otomatis** — `verify_wp_plugin.py` mendeteksi input tak tersanitasi, output tak terescape, nonce hilang, dan risiko injeksi SQL

## Persyaratan

- **PHP 8.2+** — Semua contoh kode menggunakan sintaks PHP modern (array pendek, parameter bertipe, tipe ketat)
- WordPress 6.0+
- Python 3.8+ (untuk skrip pemindai keamanan)

## Lisensi

GPL-2.0+ — Lisensi yang sama dengan WordPress itu sendiri.

## Pengakuan

Keterampilan ini dibangun dengan bantuan [Qwen3.6-35B-A3B](https://qwen.ai/blog?id=qwen3.6-35b-a3b):

```bibtex
@misc{qwen36_35b_a3b,
    title = {{Qwen3.6-35B-A3B}: Agentic Coding Power, Now Open to All},
    url = {https://qwen.ai/blog?id=qwen3.6-35b-a3b},
    author = {{Qwen Team}},
    month = {April},
    year = {2026}
}
```

## Penulis

- [M.Pribadi](https://github.com/muslimpribadi)
- [LUNA bot](https://github.com/luna-bot-agent)

---

*Untuk penggunaan AI agent, file `SKILL.md` adalah titik masuknya. Subdirektori referensi dimuat sesuai permintaan berdasarkan kebutuhan plugin.*
