/***********************************************************************/
/** 	ConsumableAlchemy - alchemy menu (crafting)
/***********************************************************************/

// Vanilla, but an owned consumable returns its copy recipe (see ConsumableAlchemy_recipes.ws).
// CanCookRecipe, CookItem and GetRequiredIngredients all read recipes through here.
@replaceMethod(W3AlchemyManager)
function GetRecipe(recipeName : name, out ret : SAlchemyRecipe) : bool
{
	var i : int;

	for(i=0; i<recipes.Size(); i+=1)
	{
		if(recipes[i].recipeName == recipeName)
		{
			ret = recipes[i];
			ret.requiredIngredients = CA_GetRecipeIngredients(ret);
			return true;
		}
	}

	return false;
}

// The recipe list shown in the alchemy menu.
@wrapMethod(W3AlchemyManager)
function GetRecipes(forceAll : bool) : array<SAlchemyRecipe>
{
	var ret : array<SAlchemyRecipe>;
	var i : int;

	ret = wrappedMethod(forceAll);

	for(i=0; i<ret.Size(); i+=1)
		ret[i].requiredIngredients = CA_GetRecipeIngredients(ret[i]);

	return ret;
}

// Vanilla reloads the menu's cached recipe list only after brewing level 2+,
// but every first brew switches the recipe to its copy, so always reload it.
@wrapMethod(CR4AlchemyMenu)
function CreateItem( recipeIndex : int )
{
	// A brew attempt at a full stock gets its own notification instead of the vanilla
	// "already cooked" one (which in vanilla means "brewed for good").
	if(recipeIndex >= 0 && recipeIndex < m_recipeList.Size() && bCouldCraft
		&& CA_IsFullStock(m_recipeList[recipeIndex].cookedItemName)
		&& m_alchemyManager.CanCookRecipe(m_recipeList[recipeIndex].recipeName) == EAE_CannotCookMore)
	{
		showNotification(CA_FullStockText());
		OnPlaySoundEvent("gui_global_denied");
		return;
	}

	wrappedMethod(recipeIndex);

	m_recipeList = m_alchemyManager.GetRecipes(false);

	if(recipeIndex >= 0 && recipeIndex < m_recipeList.Size())
		UpdateItemsById(recipeIndex);
}

// Vanilla, except the cantCookReason of a consumable at full stock is CA_FullStockText().
// Replaced because the entry array goes to Flash inside the method and cantCookReason is
// set there; canCookStatus stays untouched (the menu filters read it).
@replaceMethod(CR4AlchemyMenu)
function PopulateData()
{
	var l_DataFlashArray		: CScriptedFlashArray;
	var l_DataFlashObject 		: CScriptedFlashObject;

	var recipe					: SAlchemyRecipe;

	var i, length				: int;

	var l_Title					: string;
	var l_Tag					: name;
	var l_IconPath				: string;
	var l_GroupTitle			: string;
	var l_GroupTag				: name;
	var l_IsNew					: bool;
	var canCraftResult			: EAlchemyExceptions;
	var canCraftResultFilters	: EAlchemyExceptions;


	var cookableType			: EAlchemyCookedItemType;
	var cookable				: SCookable;
	var cookables				: array<SCookable>;
	var exists					: bool;
	var j, cookableCount		: int;
	var minQuality, maxQuality  : int;

	var expandedAlchemyCategories : array< name >;

	expandedAlchemyCategories = GetWitcherPlayer().GetExpandedAlchemyCategories();

	l_DataFlashArray = m_flashValueStorage.CreateTempFlashArray();
	length = m_recipeList.Size();


	for(i=0; i<length; i+=1)
	{
		if(m_alchemyManager.CanCookRecipe(m_recipeList[i].recipeName) == EAE_NoException)
		{
			exists = false;
			cookableType = m_recipeList[i].cookedItemType;

			for(j=0; j<cookables.Size(); j+=1)
			{
				if(cookables[j].type == cookableType)
				{
					cookables[j].cnt += 1;
					exists = true;
					break;
				}
			}

			if(!exists)
			{
				cookable.type = cookableType;
				cookable.cnt = 1;
				cookables.PushBack(cookable);
			}
		}
	}

	for( i = 0; i < length; i+= 1 )
	{
		recipe = m_recipeList[ i ];
		l_GroupTag = AlchemyCookedItemTypeEnumToName( recipe.cookedItemType );

		l_GroupTitle = GetLocStringByKeyExt( AlchemyCookedItemTypeToLocKey(recipe.cookedItemType) );

		l_Title = GetLocStringByKeyExt( m_definitionsManager.GetItemLocalisationKeyName( recipe.cookedItemName ) ) ;
		l_IconPath = m_definitionsManager.GetItemIconPath(recipe.cookedItemName);
		l_IsNew	= false;
		l_Tag = recipe.recipeName;

		canCraftResult = m_alchemyManager.CanCookRecipe(recipe.recipeName);
		canCraftResultFilters = m_alchemyManager.CanCookRecipe(recipe.recipeName, true);


		cookableCount = 0;
		for(j=0; j<cookables.Size(); j+=1)
		{
			if(cookables[j].type == recipe.cookedItemType)
			{
				cookableCount = cookables[j].cnt;
				break;
			}
		}


		l_DataFlashObject = m_flashValueStorage.CreateTempFlashObject();

		if(cookableCount > 0)
		{
			l_DataFlashObject.SetMemberFlashString(  "categoryPostfix", " | " + cookableCount + " |");
		}
		else
		{
			l_DataFlashObject.SetMemberFlashString(  "categoryPostfix", "" );
		}

		thePlayer.inv.GetItemQualityFromName( recipe.cookedItemName, minQuality, maxQuality );

		l_DataFlashObject.SetMemberFlashUInt(  "tag", NameToFlashUInt(l_Tag) );
		l_DataFlashObject.SetMemberFlashString(  "dropDownLabel", l_GroupTitle );
		l_DataFlashObject.SetMemberFlashUInt(  "dropDownTag",  NameToFlashUInt(l_GroupTag) );
		l_DataFlashObject.SetMemberFlashBool(  "dropDownOpened", expandedAlchemyCategories.Contains( l_GroupTag ) );
		l_DataFlashObject.SetMemberFlashString(  "dropDownIcon", "icons/monsters/ICO_MonsterDefault.png" );

		l_DataFlashObject.SetMemberFlashBool( "isNew", l_IsNew );

		if ( m_guiManager.GetShowItemNames() )
		{
			l_Title = l_Title + "<br><font color=\"#FFDB00\">'" + recipe.recipeName + "'</font>";
		}

		l_DataFlashObject.SetMemberFlashString(  "label", l_Title );
		l_DataFlashObject.SetMemberFlashString(  "iconPath", l_IconPath );
		l_DataFlashObject.SetMemberFlashInt( "rarity", minQuality );

		if (canCraftResult != EAE_NoException)
		{
			if (canCraftResult == EAE_CannotCookMore && CA_IsFullStock(recipe.cookedItemName))
				l_DataFlashObject.SetMemberFlashString( "cantCookReason", CA_FullStockText());
			else
				l_DataFlashObject.SetMemberFlashString( "cantCookReason", GetLocStringByKeyExt(AlchemyExceptionToString(canCraftResult)));
		}
		else
		{
			l_DataFlashObject.SetMemberFlashString( "cantCookReason", "" );
		}

		l_DataFlashObject.SetMemberFlashBool( "isSchematic", false );
		l_DataFlashObject.SetMemberFlashInt( "canCookStatus", canCraftResult);
		l_DataFlashObject.SetMemberFlashInt( "canCookStatusForFilter", canCraftResultFilters);

		l_DataFlashArray.PushBackFlashObject(l_DataFlashObject);
	}

	if( l_DataFlashArray.GetLength() > 0 )
	{
		m_flashValueStorage.SetFlashArray( DATA_BINDING_NAME, l_DataFlashArray );
		m_fxShowSecondaryModulesSFF.InvokeSelfOneArg(FlashArgBool(true));
	}
	else
	{
		m_fxShowSecondaryModulesSFF.InvokeSelfOneArg(FlashArgBool(false));
	}
}

// Vanilla, except an owned consumable can be brewed again until it reaches the cap.
// At the cap the vanilla "already brewed" exception is returned, so the menu
// shows the original localized message.
@replaceMethod(W3AlchemyManager)
function CanCookRecipe(recipeName : name, optional ignorePlayerState:bool) : EAlchemyExceptions
{
	var i, cnt, itemLevel : int;
	var recipe : SAlchemyRecipe;
	var items  : array<SItemUniqueId>;
	var itemType : string;
	var itemName : name;
	var dm : CDefinitionsManagerAccessor;
	var isConsumable : bool;

	if(!GetRecipe(recipeName, recipe))
		return EAE_NoRecipe;

	if (!ignorePlayerState)
	{
		if (isPlayerMounted) return EAE_Mounted;
		if (isPlayerInCombat) return EAE_InCombat;
	}

	itemType = GetItemNameWithoutLevelAsString(recipe.cookedItemName);
	isConsumable = CA_IsConsumableItemName(recipe.cookedItemName);

	if( theGame.GetDefinitionsManager().IsItemSingletonItem(recipe.cookedItemName) )
	{
		thePlayer.inv.GetAllItems(items);
		for(i=0; i<items.Size(); i+=1)
		{
			itemName = thePlayer.inv.GetItemName(items[i]);

			if(itemName == recipe.cookedItemName)
			{
				if(!isConsumable || thePlayer.inv.SingletonItemGetAmmo(items[i]) >= thePlayer.inv.SingletonItemGetMaxAmmo(items[i]))
					return EAE_CannotCookMore;

				continue;
			}

			if(StrStartsWith(NameToString(itemName), itemType))
			{
				itemLevel = (int)CalculateAttributeValue(thePlayer.inv.GetItemAttributeValue(items[i], 'level'));
				if(itemLevel >= recipe.level)
					return EAE_CannotCookMore;
			}
		}
	}

	dm = theGame.GetDefinitionsManager();

	for(i=0; i<recipe.requiredIngredients.Size(); i+=1)
	{
		itemName = recipe.requiredIngredients[i].itemName;

		if (dm.ItemHasTag( itemName, 'MutagenIngredient' ))
		{
			cnt = thePlayer.inv.GetUnusedMutagensCount(itemName);
		}
		else
		{
			cnt = thePlayer.inv.GetItemQuantityByName(itemName);
		}

		if(cnt < recipe.requiredIngredients[i].quantity)
		{
			return EAE_NotEnoughIngredients;
		}
	}
	return EAE_NoException;
}

// One brew fills the item up to its limit, as meditation did in vanilla.
// Vanilla already does it for a new item, but leaves an owned one untouched.
@wrapMethod(W3AlchemyManager)
function CookItem(recipeName : name)
{
	var recipe : SAlchemyRecipe;
	var inv : CInventoryComponent;
	var items : array<SItemUniqueId>;
	var i, maxAmmo : int;

	wrappedMethod(recipeName);

	if(!GetRecipe(recipeName, recipe) || !CA_IsConsumableItemName(recipe.cookedItemName))
		return;

	inv = thePlayer.inv;
	items = inv.GetItemsByName(recipe.cookedItemName);
	for(i=0; i<items.Size(); i+=1)
	{
		maxAmmo = inv.SingletonItemGetMaxAmmo(items[i]);
		if(inv.SingletonItemGetAmmo(items[i]) < maxAmmo)
			inv.SingletonItemSetAmmo(items[i], maxAmmo);
	}
}
