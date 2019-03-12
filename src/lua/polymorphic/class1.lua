local class1 = {x = 0,y = 0}

function class1:new(x,y)

-- body

local self = {}

setmetatable(self,class5)
    class1.__index = class1
    self.x = x
    self.y = y
    return self
end

function class1:test()
    print(self.x,self.y)
end


function class1:gto()
    return 100
end


function class1:gio()
    return self:gto()*2
end

return class1