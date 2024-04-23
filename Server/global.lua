-- 此文件仅用于定义变量和子函数
data = {}
function ToStringEx(value)
    if type(value)=='table' then
       return TableToStr(value)
    elseif type(value)=='string' then
        return "\'"..value.."\'"
    else
       return tostring(value)
    end
end

function TableToStr(t)
    if t == nil then return "" end
    local retstr= "{"

    local i = 1
    for key,value in pairs(t) do
        local signal = ","
        if i==1 then
          signal = ""
        end

        if key == i then
            retstr = retstr..signal..ToStringEx(value)
        else
            if type(key)=='number' or type(key) == 'string' then
                retstr = retstr..signal..'['..ToStringEx(key).."]="..ToStringEx(value)
            else
                if type(key)=='userdata' then
                    retstr = retstr..signal.."*s"..TableToStr(getmetatable(key)).."*e".."="..ToStringEx(value)
                else
                    retstr = retstr..signal..key.."="..ToStringEx(value)
                end
            end
        end

        i = i+1
    end

     retstr = retstr.."}"
     return retstr
end

function string_to_table(str)
    local table_data = {}
    for num in str:gmatch("-?%d+%.?%d*") do
        table.insert(table_data, tonumber(num))
    end
    return table_data
end

function get_nine_points(p1)
    data = {p1, P3, P4, P5, P6, P7, P8, P9, P10}
    P3['pose'][2] = p1['pose'][2] + 54
    P4['pose'][2] = P3['pose'][2] + 54

    P5['pose'][1] = p1['pose'][1] + 54
    P6['pose'][1] = P5['pose'][1]
    P7['pose'][1] = P5['pose'][1]

    P5['pose'][2] = p1['pose'][2]
    P6['pose'][2] = P5['pose'][2] + 54
    P7['pose'][2] = P6['pose'][2] + 54

    P8['pose'][1] = P5['pose'][1] + 54
    P9['pose'][1] = P8['pose'][1]
    P10['pose'][1] = P8['pose'][1]
    
    P8['pose'][2] = p1['pose'][2]
    P9['pose'][2] = P8['pose'][2] + 54
    P10['pose'][2] = P9['pose'][2] + 54
    
    P3['pose'][4] = p1['pose'][4]
    P4['pose'][4] = p1['pose'][4]
    P5['pose'][4] = p1['pose'][4]
    P6['pose'][4] = p1['pose'][4]
    P7['pose'][4] = p1['pose'][4]
    P8['pose'][4] = p1['pose'][4]
    P9['pose'][4] = p1['pose'][4]
    P10['pose'][4] = p1['pose'][4]
    
    P3['pose'][5] = p1['pose'][5]
    P4['pose'][5] = p1['pose'][5]
    P5['pose'][5] = p1['pose'][5]
    P6['pose'][5] = p1['pose'][5]
    P7['pose'][5] = p1['pose'][5]
    P8['pose'][5] = p1['pose'][5]
    P9['pose'][5] = p1['pose'][5]
    P10['pose'][5] = p1['pose'][5]
    
    P3['pose'][6] = p1['pose'][6]
    P4['pose'][6] = p1['pose'][6]
    P5['pose'][6] = p1['pose'][6]
    P6['pose'][6] = p1['pose'][6]
    P7['pose'][6] = p1['pose'][6]
    P8['pose'][6] = p1['pose'][6]
    P9['pose'][6] = p1['pose'][6]
    P10['pose'][6] = p1['pose'][6]

return {p1, P3, P4, P5, P6, P7, P8, P9, P10}
end


function Mov(Q,color)
      MovL(P11)
      MovL(Q)
      print(Q['pose'])
      MovL(RelPointUser(Q, {0, 0, -30, 0, 0, 0}))
      DO(9, ON)
      Wait(100)
      MovL(Q)
      
      if color == 0 then
      MovL(P12)
      elseif color == 1 then
      MovL(P13)
      end
      DO(9, OFF)
      DO(10,ON)
      Wait(500)
      DO(10,OFF)
      Wait(500)
end

--local queue={}
--function enqueue_data(point):
--  table.insert(queue,data)
--end
--function dequeue_and_process_data():
 -- if #queue>0 then
 --   local data = queue[1]
  --  print('Processing data',data)
 --   table.remove(queue,1)
 -- else then
 --   print('Queue is empty.')
--  end
--end




-- 定义队列类
Queue_p = {}

-- 创建新的队列对象
function Queue_p:new()
    newObj = {first = 0, last = -1}
    setmetatable(newObj, self)
    self.__index = self
    return newObj
end

-- 向队列尾部添加元素
function Queue_p:push(value)
    local last = self.last + 1
    self.last = last
    self[last] = value
end

-- 从队列头部移除元素并返回
function Queue_p:pop()
    local first = self.first
    if first > self.last then error("队列为空") end
    local value = self[first]
    self[first] = nil        -- 防止内存泄漏
    self.first = first + 1
    return value
end

-- 检查队列是否为空
function Queue_p:isEmpty()
    return self.first > self.last
end

-- 获取队列的大小
function Queue_p:size()
    return self.last - self.first + 1
end

-- 测试
--local q = Queue:new()
--q:push(1)
--q:push(2)
--q:push(3)

--print("队列的大小:", q:size())
--print("队列是否为空:", q:isEmpty())

--print("出队列元素:", q:pop())
--print("出队列元素:", q:pop())
--print("出队列元素:", q:pop())

--print("队列是否为空:", q:isEmpty())
