# pwnable.tw - orw

Read the flag from `/home/orw/flag`.

Only `open` `read` `write` syscall are allowed to use.

`nc chall.pwnable.tw 10001`

# 1) Analysis and find Bug

Đầu tiên ta kiếm tra các secure flag và xem thông tin cơ bản của file.

![checksec.png](images/checksec.png)

Chương trình khá đơn giản, nó yêu cầu một chuỗi đầu vào và cuối hàm main thì gọi tới con trỏ có giá trị là địa chỉ của chuỗi mà ta nhập vào. 



# 2) Idea

Thường những bài mà khi check secure flag `NX: NX disabled` và không có hàm giúp lấy shell hay đọc flag thì ý tưởng đầu tiên mình nghĩ tới là ghi shellcode vào chương trình sau đó điều khiển return address trỏ về shellcode. Ta sẽ giải quyết bài này theo ý tưởng đó nhưng có 2 vấn đề cần giải quyết:

      1) Shellcode: Cái này thì ta có thể dễ dàng tìm thấy trên mạng hoặc tự viết cũng được miễn nó không quá dài vì input cho nhập tối đa 60 kí tự.
      
      2) Ta cần xác định được chính xác địa chỉ shellcode mà ta đã overwrite vào stack, để điều khiển return address trỏ về đúng vị trí shellcode.

# 3) Exploit

Để giải quyết vấn đề thứ hai, ta để ý đầu hàm `_start` là `push esp` đẩy giá trị esp vào stack rồi mới đến đẩy địa chỉ của hàm `_exit` lên stack. Khi đó bố cục của stack trước khi nhận input sẽ như sau. 

![layoutStack1.png](images/layoutStack1.png)

Nếu ta tạo payload điều khiển chương trình return về `0x08048087` - địa chỉ của câu lệnh `mov ecx,esp`, đưa địa chỉ của chuỗi cần in vào ecx để thực hiện `syscall write()` và sau khi return về chương trình sẽ thực hiện `syscall write()` lần thứ hai, in ra 20 bytes trên stack. Vì 4 bytes đầu tiên trên stack lúc này chính là esp nên ta sẽ leak được địa chỉ esp. Chương trình sẽ tiếp tục với một lệnh `syscall read()` thứ hai, ta sẽ gửi payload thứ hai bao gồm "A"*0x14 + (giá trị leak được chính là nơi ta ghi shellcode = esp+20) + shellcode, lúc này chương trình sẽ return về đúng shellcode mà ta cần.

![layoutStack2.png](images/layoutStack2.png)

Layout stack sau khi ta ghi đè return address bằng địa chỉ câu lệnh `mov ecx,esp` và chương trình return về địa chỉ đó. Khi thực hiện lệnh `ret` - địa chỉ hàm `_exit` bị đẩy ra khỏi stack và esp tăng lên 4 chỉ vào nơi mà ở đó lưu giá trị của esp (Ô nhớ lưu giá trị là địa chỉ của chính ô nhớ đó). Vì vậy ta sẽ in ra được giá trị chính là địa chỉ của ô nhớ trên stack - là nơi ta lưu shellcode vì dễ dàng return về đúng shellcode do biết được chính xác địa chỉ.

![layoutStack2.png](images/layoutStack2.png)

Lần nhập thứ hai ta ghi đè địa chỉ trả về là địa chỉ leak được sau đó chính là shellcode, gửi payload thứ hai: payload = "A"*0x14 + (esp+20) + shellcode, lúc này chương trình sẽ return về đúng shellcode mà ta cần.

# 4) Source code and get Flag

Tiến hành viết file [exploit.py](exploit.py) và khai thác:

![flag.png](images/flag.png)

------------------------------------------------------
