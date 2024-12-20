local function enumerate(iterator)
	local idx = 0
	return function()
		idx = idx + 1
		local v = iterator()
		if v ~= nil then
			return idx, v
		end
		return nil
	end
end
local j = 150

--- @class complex
--- @field x integer
--- @field y integer
local complex = {}

function complex:new(x, y)
	local obj = { x = x, y = y }
	self.__index = self
	return setmetatable(obj, self)
end

local function c(x, y)
	return complex:new(x, y)
end

function complex:add(z)
	return c(self.x + z.x, self.y + z.y)
end

--- @param z complex
local function h(z)
	return z.x + j * z.y
end

local function hinv(n)
	return c(n % j, math.floor(n / j))
end

local function parse(filename)
	local file = io.open(filename, 'r')
	if file == nil then
		return nil
	end
	--- @type boolean[]
	local grid = {}
	local start = nil
	for x, line in enumerate(file:lines('*l')) do
		for y = 1, #line do
			local char = line:sub(y, y)
			local z = c(x - 1, y - 1)
			grid[h(z)] = char == '#'
			if char == 'S' then
				start = z
			end
		end
	end
	return grid, start
end

--- @param z1 complex
--- @param z2 complex
local function manhattan(z1, z2)
    return math.abs(z1.x - z2.x) + math.abs(z1.y - z2.y)
end

---@param path complex[]
---@param target complex
---@param idx integer
local function close_enumerate(path, target, start)
    local pl = #path
    local idx = start
    return function()
        while idx <= pl do
            local v = path[idx]
            local dist = manhattan(v, target)
            if dist > 20 then
                idx = idx + dist - 20
            else
                idx = idx + 1
                return idx - 1, dist
            end
        end
    end
end

local deltas = { c(-1, 0), c(0, 1), c(1, 0), c(0, -1) }
local two_deltas = { c(2, 0), c(1, -1), c(0, -2), c(-1, -1) }

local function solve_p1(costs)
    local res = 0
    for hz, cost in pairs(costs) do
        local z = hinv(hz)
        for _, d in ipairs(two_deltas) do
            local new_cost = costs[h(z:add(d))] or cost
            if math.abs(new_cost - cost) >= 102 then
                res = res + 1
            end
        end
    end
    return res
end

local function solve_p2(path)
    local res = 0
    for c1, z1 in ipairs(path) do
        for c2, dist in close_enumerate(path, z1, c1 + 102) do
            if c2 - c1 - dist >= 100 then
                res = res + 1
            end
        end
    end
    return res
end

local function solve(grid, start)
	local bfs = {}
	bfs[1] = start
	local costs = {}
    for cost, z in ipairs(bfs) do
		costs[h(z)] = cost - 1
		local facing = nil
		for _, d in ipairs(deltas) do
			local loc = z:add(d)
			if not grid[h(loc)] and costs[h(loc)] == nil then
				facing = d
				break
			end
		end
		if facing ~= nil then
			bfs[cost + 1] = z:add(facing)
		end
	end

	return solve_p1(costs), solve_p2(bfs)
end

local function main()
	print(solve(parse('input.txt')))
end
main()
