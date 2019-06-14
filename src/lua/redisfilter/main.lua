local cur = 0
local rep = {}
local tmp


repeat
  tmp = redis.call("SCAN", cur, "MATCH", "*", "COUNT", 2000)
  cur = tonumber(tmp[1])
  if tmp[2] then
    for k, v in pairs(tmp[2]) do
        local exist = false
        for _, v2 in pairs(ARGV) do
            if string.find(v,v2)
                exist = true
            end
        end
      if exist then
        rep[#rep+1] = v
      end
    end
  end
until cur == 0
return rep