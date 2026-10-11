/***********************************************************************/
/** 	ConsumableAlchemy - standalone starts (HoS / B&W)
/***********************************************************************/

// The standalone starts wipe the recipes but hand out about twenty consumables. Without a recipe
// they would be one-shot, because the mod never refills them. Every owned consumable without
// a known recipe gets its recipe (silently, idempotent; nothing is stored by the mod).
function CA_LearnRecipesOfOwnedConsumables()
{
	var dm : CDefinitionsManagerAccessor;
	var main : SCustomNode;
	var items : array<SItemUniqueId>;
	var owned, recipeNames, cookedNames : array<name>;
	var known : array<name>;
	var recipeName, cookedName : name;
	var i : int;

	if(!thePlayer || !thePlayer.inv)
		return;

	thePlayer.inv.GetAllItems(items);
	for(i=0; i<items.Size(); i+=1)
	{
		cookedName = thePlayer.inv.GetItemName(items[i]);
		if(CA_IsConsumableItemName(cookedName) && !owned.Contains(cookedName))
			owned.PushBack(cookedName);
	}

	if(owned.Size() == 0)
		return;

	// Pair every recipe with the item it cooks (as W3AlchemyManager.LoadRecipesCustomXMLData does).
	dm = theGame.GetDefinitionsManager();
	main = dm.GetCustomDefinition('alchemy_recipes');
	for(i=0; i<main.subNodes.Size(); i+=1)
	{
		if(dm.GetCustomNodeAttributeValueName(main.subNodes[i], 'name_name', recipeName) && IsNameValid(recipeName)
			&& dm.GetCustomNodeAttributeValueName(main.subNodes[i], 'cookedItem_name', cookedName))
		{
			recipeNames.PushBack(recipeName);
			cookedNames.PushBack(cookedName);
		}
	}

	// An item whose recipe is already known is left alone.
	known = GetWitcherPlayer().GetAlchemyRecipes();
	for(i=0; i<recipeNames.Size(); i+=1)
	{
		if(known.Contains(recipeNames[i]))
			owned.Remove(cookedNames[i]);
	}

	for(i=0; i<recipeNames.Size(); i+=1)
	{
		if(owned.Contains(cookedNames[i]))
		{
			GetWitcherPlayer().AddAlchemyRecipe(recipeNames[i], true, true);
			owned.Remove(cookedNames[i]);
		}
	}
}

@wrapMethod(W3PlayerWitcher)
function StandaloneEp1_1()
{
	wrappedMethod();
	CA_LearnRecipesOfOwnedConsumables();
}

@wrapMethod(W3PlayerWitcher)
function StandaloneEp2_1()
{
	wrappedMethod();
	CA_LearnRecipesOfOwnedConsumables();
}

// Saves made after a standalone start before the mod was installed.
@wrapMethod(W3PlayerWitcher)
function ApplyPatchFixes()
{
	wrappedMethod();

	if(FactsQuerySum("standalone_ep1") > 0 || FactsQuerySum("standalone_ep2") > 0)
		CA_LearnRecipesOfOwnedConsumables();
}
