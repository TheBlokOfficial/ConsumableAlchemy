/***********************************************************************/
/** 	ConsumableAlchemy - inventory (doses, refills)
/***********************************************************************/

// Every regular refill (meditation, bed, alchemy table, NG+) goes through here; quest rewards
// and the Water Hag decoction set doses directly and stay vanilla.
// Vanilla also calls it from OnItemAdded to initialize a newly acquired item;
// that first call stays vanilla (full doses), every later call is ignored for consumables.
@wrapMethod(CInventoryComponent)
function SingletonItemRefillAmmo(id : SItemUniqueId, optional alchemyTableUsed : bool)
{
	if(CA_IsConsumableItem(id) && GetItemModifierInt(id, 'is_initialized', 0) != 0)
		return;

	wrappedMethod(id, alchemyTableUsed);
}

// Consumables never need a refill, so they must not trigger alcohol use
// or the "items refilled" / "cannot refill" notifications.
@replaceMethod(CInventoryComponent)
function HasNotFilledSingletonItem( optional alchemyTableUsed : bool ) : bool
{
	var i : int;
	var singletonItems : array<SItemUniqueId>;
	var hasLab : bool;
	var l_bed : W3WitcherBed;

	hasLab = false;
	if( FactsQuerySum( "PlayerInsideOuterWitcherHouse" ) >= 1 && FactsQuerySum( "AlchemyTableExists" ) >= 1 )
	{
		l_bed = (W3WitcherBed)theGame.GetEntityByTag( 'witcherBed' );
		if( l_bed.GetWasUsed() || alchemyTableUsed )
		{
			hasLab = true;
		}
	}

	singletonItems = GetSingletonItems();
	for(i=0; i<singletonItems.Size(); i+=1)
	{
		if( CA_IsConsumableItem( singletonItems[i] ) )
			continue;

		if( hasLab && !IsItemMutagenPotion( singletonItems[i] ) )
		{
			if(SingletonItemGetAmmo(singletonItems[i]) <= SingletonItemGetMaxAmmo(singletonItems[i]))
			{
				return true;
			}
		}
		else if(SingletonItemGetAmmo(singletonItems[i]) < SingletonItemGetMaxAmmo(singletonItems[i]))
		{
			return true;
		}
	}

	return false;
}

// Same as vanilla, but an empty consumable doesn't trigger the "refill with alcohol" tutorial.
@replaceMethod(CInventoryComponent)
function SingletonItemRemoveAmmo(itemID : SItemUniqueId, optional quantity : int)
{
	var ammo : int;

	if(!IsItemSingletonItem(itemID) || ItemHasTag(itemID, theGame.params.TAG_INFINITE_AMMO))
		return;

	if(quantity <= 0)
		quantity = 1;

	ammo = GetItemModifierInt(itemID, 'ammo_current');
	ammo = Max(0, ammo - quantity);
	SetItemModifierInt(itemID, 'ammo_current', ammo);

	if(ammo == 0 && !CA_IsConsumableItem(itemID) && ShouldProcessTutorial('TutorialAlchemyRefill') && FactsQuerySum("q001_nightmare_ended") > 0)
	{
		FactsAdd('tut_alch_refill', 1);
	}
	theGame.GetGlobalEventsManager().OnScriptedEvent( SEC_OnAmmoChanged );
}

// Corvo Bianco alchemy table: the +1 bonus stays vanilla for non-consumable potions and bombs
// (quest items); consumables are skipped, because they are never refilled.
// Same as vanilla otherwise, including its notifications.
@replaceMethod(CInventoryComponent)
function ManageSingletonItemsBonus()
{
	var l_items			: array<SItemUniqueId>;
	var l_i				: int;
	var l_haveBombOrPot	: bool;

	l_items = GetSingletonItems();

	for( l_i = 0 ; l_i < l_items.Size() ; l_i += 1 )
	{
		if( CA_IsConsumableItem( l_items[ l_i ] ) )
			continue;

		if( IsItemPotion( l_items[ l_i ] ) || IsItemBomb( l_items[ l_i ] ) )
		{
			l_haveBombOrPot = true;
			if( SingletonItemGetMaxAmmo( l_items[ l_i ] ) >= SingletonItemGetAmmo( l_items[ l_i ] ) )
			{
				if( SingletonItemsRefillAmmo( true ) )
				{
					theGame.GetGuiManager().ShowNotification( GetLocStringByKeyExt( "message_common_alchemy_table_buff_applied" ),, true );
				}

				return;
			}
		}
	}

	if( !l_haveBombOrPot )
	{
		theGame.GetGuiManager().ShowNotification( GetLocStringByKeyExt( "message_common_alchemy_table_buff_no_items" ),, true );
		return;
	}

	theGame.GetGuiManager().ShowNotification( GetLocStringByKeyExt( "message_common_alchemy_table_buff_already_on" ),, true );
}
