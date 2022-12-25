
local self = require('openmw.self')
local types = require('openmw.types')
local I = require('openmw.interfaces')

local dynamicStats = types.Actor.stats.dynamic
local Player = types.Player

local Helmet = Player.EQUIPMENT_SLOT.Helmet
local Cuirass = Player.EQUIPMENT_SLOT.Cuirass
local Shirt = Player.EQUIPMENT_SLOT.Shirt
local Robe = Player.EQUIPMENT_SLOT.Robe
local LeftGauntlet = Player.EQUIPMENT_SLOT.LeftGauntlet
local RightGauntlet = Player.EQUIPMENT_SLOT.RightGauntlet
local Ammunition =  Player.EQUIPMENT_SLOT.Ammunition

local Potion = types.Potion
local Ingredient = types.Ingredient

I.Settings.registerPage {
    key = 'bHaptics',
    l10n = 'bHaptics',
    name = "bHaptics",
    description = "Confirmation that the Lua script loaded. See config.json for settings."
}

local function onInit()
    -- get current player state
    currentHealth = dynamicStats['health'](self).current
    currentMagicka = dynamicStats['magicka'](self).current
    currentHelmet = Player.equipment(self)[Helmet]
    currentCuirass = Player.equipment(self)[Cuirass]
    currentShirt = Player.equipment(self)[Shirt]
    currentRobe = Player.equipment(self)[Robe]
    currentLeftGauntlet = Player.equipment(self)[LeftGauntlet]
    currentRightGauntlet = Player.equipment(self)[RightGauntlet]
    currentAmmunition = Player.equipment(self)[Ammunition]
    -- starting a new game actually sets the player off the ground?
    -- not a huge deal, just a haptic trigger on a new game
    currentPlayerGround = Player.isOnGround(self)
end

local function onLoad(data)
    currentHealth = data.currentHealth
    currentMagicka = data.currentMagicka
    currentHelment = data.currentHelment
    currentCuirass = data.currentCuirass
    currentShirt = data.currentShirt
    currentRobe = data.currentRobe
    currentLeftGauntlet = data.currentLeftGauntlet
    currentRightGauntlet = data.currentRightGauntlet
    currentAmmunition = data.currentAmmunition
    currentPlayerGround = data.currentPlayerGround
end

local function onSave()
    -- save player state so we can compare to new values once the script is loaded
    data = {}
    data["currentHealth"] = currentHealth
    data["currentMagicka"] = currentMagicka
    data["currentHelmet"] = currentHelmet
    data["currentCuirass"] = currentCuirass
    data["currentShirt"] = currentShirt
    data["currentRobe"] = currentRobe
    data["currentLeftGauntlet"] = currentLeftGauntlet
    data["currentRightGauntlet"] = currentRightGauntlet
    data["currentAmmunition"] = currentAmmunition
    data["currentPlayerGround"] = currentPlayerGround
    return data
end

local function onUpdate()
    -- don't know if there's a way to tell what caused the health change
    -- sword, mace, arrow, spell, fall damage, bad music, etc.
    -- you can find which actors nearby have what weapon types but do you know
    -- which weapon type was used to land the hit?
    -- so for now, just check if health decreased
    local health = dynamicStats['health'](self)
    local newHealth = health.current
    -- get change in health
    local deltaHealth = newHealth - currentHealth
    -- update current health
    currentHealth = newHealth
    -- get base health
    -- health modifier still returns 0 when fortifying health, so disregard for now
    -- local modifierHealth = dynamicStats['health'](self).modifier
    local baseHealth = dynamicStats['health'](self).base
    if deltaHealth < 0 then
        -- percentage of health lost
        local percentageHealthLost = (-deltaHealth / baseHealth)
        print('bHap health lost ' .. percentageHealthLost)
    end

    -- don't know if there's a way to detect which school of magic was used
    local magicka = dynamicStats['magicka'](self)
    local newMagicka = magicka.current
    -- get change in magicka
    local deltaMagicka = newMagicka - currentMagicka
    -- update current magicka
    currentMagicka = newMagicka
    -- get base magicka
    -- magicka modifier still returns 0 when fortifying magicka, so disregard for now
    -- local modifierMagicka = dynamicStats['magicka'](self).modifier
    local baseMagicka = dynamicStats['magicka'](self).base
    -- check if the player cast a spell but doing this by see if magicka decreased
    -- when the player is in the magic casting stance (not ideal)
    if deltaMagicka < 0 then
        -- check player's stance
        if Player.stance(self) == 2 then
            -- percentage of magicka lost
            local percentageMagickaLost = (-deltaMagicka / baseMagicka)
            print('bHap magicka used ' .. percentageMagickaLost)
        end
    end

    -- check if player is wearing helmet
    local newHelmet = Player.equipment(self, Helmet)
    if newHelmet ~= currentHelmet then
        if newHelmet then
            print('bHap helmet equipped')
        else
            print('bHap helmet unequipped')
        end
        currentHelmet = newHelmet
    end

    -- check if player is wearing cuirass
    local newCuirass = Player.equipment(self, Cuirass)
    if newCuirass ~= currentCuirass then
        if newCuirass then
            print('bHap cuirass equipped')
        else
            print('bHap cuirass unequipped')
        end
        currentCuirass = newCuirass
    end

    -- check if player is wearing shirt
    local newShirt = Player.equipment(self, Shirt)
    if newShirt ~= currentShirt then
        if newShirt then
            print('bHap shirt equipped')
        else
            print('bHap shirt unequipped')
        end
        currentShirt = newShirt
    end

    -- check if player is wearing shirt
    local newShirt = Player.equipment(self, Shirt)
    if newShirt ~= currentShirt then
        if newShirt then
            print('bHap shirt equipped')
        else
            print('bHap shirt unequipped')
        end
        currentShirt = newShirt
    end

    -- check if player is wearing robe
    local newRobe = Player.equipment(self, Robe)
    if newRobe ~= currentRobe then
        if newRobe then
            print('bHap robe equipped')
        else
            print('bHap robe unequipped')
        end
        currentRobe = newRobe
    end

    -- check if player is wearing left gauntlets
    local newLeftGauntlet = Player.equipment(self, LeftGauntlet)
    if newLeftGauntlet ~= currentLeftGauntlet then
        if newLeftGauntlet then
            print('bHap left gauntlet equipped')
        else
            print('bHap left gauntlet unequipped')
        end
        currentLeftGauntlet = newLeftGauntlet
    end

    -- check if player is wearing right gauntlets
    local newRightGauntlet = Player.equipment(self, RightGauntlet)
    if newRightGauntlet ~= currentRightGauntlet then
        if newRightGauntlet then
            print('bHap right gauntlet equipped')
        else
            print('bHap right gauntlet unequipped')
        end
        currentRightGauntlet = newRightGauntlet
    end

    -- check if player is wearing ammo
    local newAmmunition = Player.equipment(self, Ammunition)
    if newAmmunition ~= currentAmmunition then
        if newAmmunition then
            print('bHap ammo equipped')
        else
            print('bHap ammo unequipped')
        end
        currentAmmunition = newAmmunition
    end

    -- Player.isOnGround(self) is true if the player is on the ground
    -- If the player was airborne and lands (False -> True), print
    -- don't need to do anything if the ground state doesn't change, but we're
    -- updating the state anyway (is another if statement worth it?)
    local newPlayerGround = Player.isOnGround(self)
    if newPlayerGround and not currentPlayerGround then
        print('bHap player landed')
    end
    currentPlayerGround = newPlayerGround

end

local function onConsume(recordId)
    if Potion.objectIsInstance(recordId) then
        print('bHap potion consumed')
    elseif Ingredient.objectIsInstance(recordId) then
        print('bHap ingredient consumed')
    end
end

return {
    engineHandlers = {
        onInit = onInit,
        onLoad = onLoad,
        onSave = onSave,
        onUpdate = onUpdate,
        onConsume = onConsume
    }
}
