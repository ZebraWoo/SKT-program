-- Version: Lua 5.4.4
-- 此线程为主线程，可调用任何指令。
-- P2 主要功能
-- P3 观测驻点
Safe = P1
MovJ(Safe)
DO(9,OFF)
DO(10,OFF)
local ip="192.168.5.1"
local port=6601
local err=0
local socket=0
local queue = Queue_p:new()
STC_points_robot = get_nine_points(P2)

data = {}
Buf = {}
data['user'] = P1['user']
data['name'] = 'Q1'
data['tool'] = P1['tool']
data['joint'] = P1['joint']

while true do
	::create_server::
	err, socket = TCPCreate(true, ip, port)
	if err ~= 0 then
		print("socket failed!")
		Wait(1000)
		goto create_server
	end
	err = TCPStart(socket, 0)
	if err ~= 0 then
		print("failed to connect!")
		TCPDestroy(socket)
		Wait(1000)
		goto create_server
	end
  n = 1
  
  
  color = 0
	while true do
		message = TableToStr(STC_points_robot)
      TCPWrite(socket, 'message')
      print(n)
		err, data['pose'] = TCPRead(socket, 5000, "string")
      print('message received!')
      data['pose'] = string_to_table(data['pose'])
      for i = 1,6
      do
      Buf[i] = data['pose'][i]
      end
      data['pose'] = Buf
      Q = data --receive data and create point
      queue:push(Q)
      
      if n == 11 then
      Wait(2000)
      end
      
      point = queue:pop()
      if n > 11 then
      color = 1
      end
      Mov(point, color)
      n = n + 1

		if err ~= 0 then
			print("receiving failed. Reconnecting...")
			TCPDestroy(socket)
			Wait(1000)
			break
		end
		if  data == "START" then
		print("receiving:",tonumber(data))

		TCPWrite(socket,"stop")		
		end
	end
end