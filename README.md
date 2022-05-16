## Awas Banjir

Awas Banjir adalah sebuah sistem informasi untuk memantau dan mendeteksi terjadinya banjir. Sistem ini terintegrasi dengan sebuah perangkat yang dapat mengukur ketinggian air. Perangkat tersebut dibangun menggunakan microcontroller (NodeMCU ESP8266) yang dipadukan dengan module ultrasonic. Perangkat tersebut akan membaca ketinggian air lalu mengirimkan data ke sistem melalui protokol MQTT dengan melakukan pengecekan apakah ketinggian air sudah masuk dalam status normal, waspada, awas, siaga.


### Tentang Aplikasi
Aplikasi berbasis web Awas Banjir dibangun menggunakan framework Django. Fitur yang diberikan
- Otentifikasi
  - masuk
  - daftar (belum)
  - lupa sandi (belum)
- Perangkat
  - Tambah perangkat, dengan property
     - nama
     - tipe
     - lokasi (map)
     - Batas status waspada, siaga, awas
     - Aktif/nonaktif beel alert
  - Perubahan batas status waspada, siaga, awas serta aktif/nonaktif beep alert akan dikirim ke perangkat
  - Melihat titik lokasi perangkat pada map
  - Graphic
    - Live graphic: Menampikan hasil pantuan data ketinggian air yang dikirim oleh perangkat secara real-time
    - History graphic: Menampilkan hasil riwayat pantuan kettinggian air berdasarkan rentang waktu yang dipilih
  - Notifikasi
    - Telegram: konfigurasi API bot dan channel. Notifikasi live report akan dikirim ke channel yang ada pada konfigurasi
    - Email: (belum)
    - WhatsApp: (belum)

### Tentang Perangkat
Perangkat yang digunakan
  - Spek
    - NodeMCU ESP8266
    - penambahan modul ultrasonic HCSR04
    - Packaging / Case (DIY)
  - Lokal server: Perangkat dapat menjadi lokal server untuk melakukan,
    - Registrasi device_id agar perangkat terkoneksi dengan aplikasi Awas Banjir
    - Registrasi perangkat dengan koneksi WiFi disekitar
  - Behavior
    - Mengirimkan data setiap 1 menit sekali apabila ketinggian air masuk dalam status normal
    - Mengirimkan data setiap 1 detik sekali apabila ketinggian air masuk dalam status waspada, siaga dan awas
    - Beep alert / buzzer akan berbunyi bila masuk pada status waspada, siaga, awas
  - Konfigurasi
    - Perangkat dapat menerima perubahan konfigurasi aktif/nonaktif beel alert atau batas ketinggian waspada
