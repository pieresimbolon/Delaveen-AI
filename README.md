# Delaveen-AI
Asisten AI yang dibuat menggunakan GPT dan Eleven Labs

ini adalah sebuah program asisten AI sederhana yang dapat menerima perintah suara dari pengguna dan melakukan berbagai tugas. Dengan menggunakan pustaka SpeechRecognition, program dapat mendengarkan perintah yang diucapkan melalui mikrofon. Perintah tersebut kemudian dikenali menggunakan Google Speech Recognition API.
## How it works

•Setelah menjalankan program dan konsol menampilkan teks "listening...", ucapkan kata pengaktif yang telah Anda tentukan, diikuti dengan perintah user.

•Pustaka SpeechRecognition akan mengubah ucapan Anda menjadi teks, kemudian teks tersebut akan diberikan kepada model bahasa (LLM) yang akan menghasilkan teks respons. 

•teks respons akan diberikan kepada ElevenLabs, dan AI akan merespons dengan suara sintesis teks kecepatan tinggi (TTS)

•Proses ini membutuhkan beberapa waktu, terutama karena waktu yang dibutuhkan oleh SpeechRecognition. 

•Cobalah untuk menghindari penggunaan kalimat pendek atau menanggapi hanya dengan satu kata, karena hal ini dapat menyebabkan LLM menghasilkan saran pelengkapan otomatis untuk apa yang harus diberikan setelah tanggapan singkat Anda.

•perlu di ingat bahwa pengenalan ucapan bisa "terjebak" dalam mode pendengaran jika terdapat terlalu banyak kebisingan latar belakang. user dapat mengatur variabel "thresh" atau menambahkan parameter "phrase_time_limit" pada bagian "voice = listener.listen(source, timeout=10)" untuk mengatur batas waktu.

•Untuk membuat percakapan dengan AI terasa lebih lancar, saya mengatur agar user hanya perlu mengucapkan kata pengaktif pada iterasi pertama. Pada iterasi selanjutnya, kata pengaktif tidak perlu diucapkan lagi.Namun, jika pada iterasi kedua tidak ada yang dikatakan, maka pada iterasi ketiga Anda harus mengucapkan kata pengaktif kembali.

•File delaveenmem.txt digunakan untuk menyimpan percakapan sehingga Anda dapat mengajukan pertanyaan lanjutan kepada AI, karena secara default AI hanya memiliki ingatan yang pendek. Namun, penggunaan token akan meningkat seiring dengan bertambahnya percakapan. Ketika user memberitahukan AI untuk menghentikan program, file ini akan otomatis dihapus. Namun, jika user ingin menghentikan program tanpa menghapus ingatan, user perlu menghentikan program secara manual.

•Program ini membutuhkan biaya penggunaan dari ElevenLabs dan GPT.

## How to run

Pastikan program dan file delaveenmem.txt berada dalam folder yang sama. 
instal semua modul yang diperlukan. 

