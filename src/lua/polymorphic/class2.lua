local class2 ={}

local class2 = require("class1")

function class2:new(x,y)
    setmetatable(class2, class1)
    class1.__index = class2
    local self = {}
    setmetatable(self, class2)
    class2.__index = class2
    self.x = x
    self.y = y
    return self
end

function class2:gto()
    return 50
end

return class2