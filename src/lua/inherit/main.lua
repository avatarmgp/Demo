--[[Shape = {area = 0}

function Shape:new(o, side)
    o = o or {}
    setmetatable(o, self)
    self.__index = self
    side = side or 0
    self.area = side*side

    return o
end

function Shape:printArea()
    print("面积为",self.area)
end

myshape = Shape:new(nil, 10)
myshape:printArea()]]--


--[[local class = require("class")
s1 = class:new()   --实例化对象s1--
s1:func()   --self通过index找到class，然后调用class的func]]--


local class2 = require("class2")
local s1 = class2:new()
s1:func1()
s1:func2()