Learnings
=========
The csv from mssql is in "Little-endian UTF-16 Unicode text, with very long lines, with CRLF, CR line terminators" format. Convert it to ascii  
__iconv -f utf-16 -t utf-8 calls.csv > data.csv__

