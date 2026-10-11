/***********************************************************************/
/** 	ConsumableAlchemy - shared helpers
/***********************************************************************/

// Potions, decoctions and bombs use the consumable system. Oils, quest items
// and infinite-ammo items keep the vanilla singleton behaviour.
// Dose limits are vanilla (item 'ammo' attribute + vanilla bonuses).
function CA_IsConsumableItemName(itemName : name) : bool
{
	var dm : CDefinitionsManagerAccessor;

	if(!IsNameValid(itemName))
		return false;

	dm = theGame.GetDefinitionsManager();

	if(!dm.IsItemSingletonItem(itemName))
		return false;

	// Quest / tutorial items without the Quest tag: vanilla expects them to be refilled
	// or handed out by the quest (Pops Antidote, q303; ReinaldsPhiltre).
	if(itemName == 'Snow Ball' || itemName == 'Tutorial Bomb' || itemName == 'Village drink' || itemName == 'Pops Antidote' || itemName == 'ReinaldsPhiltre')
		return false;

	if(dm.ItemHasTag(itemName, 'Quest') || dm.ItemHasTag(itemName, 'NoAdditionalAmmo') || dm.ItemHasTag(itemName, theGame.params.TAG_INFINITE_AMMO))
		return false;

	return dm.IsItemBomb(itemName) || dm.IsItemPotion(itemName);
}

// Shown instead of the vanilla "already cooked" text when a consumable has all its doses.
// No .w3strings can be built, so the language is picked here (PL, anything else EN).
function CA_FullStockText() : string
{
	if(GetCurrentTextLocCode() == "PL")
		return "Masz już wszystkie dawki";

	return "Already fully stocked";
}

// True when the player owns this consumable with doses at or above the limit.
function CA_IsFullStock(itemName : name) : bool
{
	var inv : CInventoryComponent;
	var items : array<SItemUniqueId>;
	var i : int;

	if(!CA_IsConsumableItemName(itemName))
		return false;

	inv = thePlayer.inv;
	items = inv.GetItemsByName(itemName);
	for(i=0; i<items.Size(); i+=1)
	{
		if(inv.SingletonItemGetAmmo(items[i]) >= inv.SingletonItemGetMaxAmmo(items[i]))
			return true;
	}

	return false;
}

@addMethod(CInventoryComponent)
function CA_IsConsumableItem(itemID : SItemUniqueId) : bool
{
	if(GetEntity() != thePlayer)
		return false;

	return CA_IsConsumableItemName(GetItemName(itemID));
}
