local class = {}

function class:func()
    print("class : func")
end

--新建一个类，添加index
function  class:new()
    local self = {}     --创建新的表作为实例的对象
    setmetatable(self, {__index = class})  --设置class为对象元表的__index
    return self         --返回该新表
end

return class