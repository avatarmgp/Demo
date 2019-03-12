local class2 = {}

local class1 = require("class1")

function class2:func2()
    print("class2 : func2")
end

function class2:new()
    setmetatable(class2 , {__index = class1})  --设置class1为class2的元表的__index字段来实
    local self = {}
    setmetatable(self , {__index = class2})
    return self
end

return class2

